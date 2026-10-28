#!/usr/bin/env python3
"""Local, revisioned Be Real project records. Uses only Python's standard library."""

import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import errno
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time
import uuid

if os.name == "nt":
    import msvcrt
else:
    import fcntl


class StoreError(Exception):
    pass


def validate_portfolio(record):
    if not isinstance(record, dict) or type(record.get("schema_version")) is not int or record["schema_version"] != 1:
        raise StoreError("Unsupported portfolio schema; preserve the file for inspection.")
    if type(record.get("revision")) is not int or record["revision"] < 0 or not isinstance(record.get("months"), dict):
        raise StoreError("Invalid portfolio revision or months.")
    for month, value in record["months"].items():
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", month):
            raise StoreError("Portfolio months must use YYYY-MM.")
        if not isinstance(value, dict):
            raise StoreError("Each month must be an object.")
        capacity, plan = value.get("capacity", {}), value.get("plan", {})
        if not isinstance(capacity, dict) or not isinstance(plan, dict):
            raise StoreError("Monthly capacity and plan must be objects.")
        allocations = plan.get("allocations", {})
        if not isinstance(allocations, dict):
            raise StoreError("Monthly allocations must be keyed by project ID.")
        if plan.get("status", "proposed") not in ("proposed", "user_confirmed"):
            raise StoreError("Plan status must distinguish proposals from user-confirmed decisions.")
        numbers = [capacity.get(k) for k in ("max_hours", "used_hours", "remaining_hours")]
        numbers.append(plan.get("buffer_hours"))
        for project_id, allocation in allocations.items():
            if not ID_PATTERN.fullmatch(project_id) or not isinstance(allocation, dict):
                raise StoreError("Invalid project allocation.")
            if allocation.get("mode") not in ("priority", "maintenance_only", "parked"):
                raise StoreError("Allocation mode must be priority, maintenance_only, or parked.")
            numbers.append(allocation.get("hours"))
        for number in numbers:
            if number is not None and (type(number) not in (int, float) or not math.isfinite(number) or number < 0):
                raise StoreError("Hours must be finite nonnegative numbers or null when unknown.")
    try:
        json.dumps(record, allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise StoreError(f"Portfolio is not valid finite JSON: {exc}") from exc


def check_portfolio(record):
    """Check each month's remaining plan independently; do not assume missing hours are zero."""
    validate_portfolio(record)
    results = {}
    for month, data in record["months"].items():
        capacity, plan = data.get("capacity", {}), data.get("plan", {})
        ceiling, used, available = (capacity.get(k) for k in ("max_hours", "used_hours", "remaining_hours"))
        derived = max(0, ceiling - used) if ceiling is not None and used is not None else None
        if available is None:
            available = derived
        allocations = plan.get("allocations", {})
        unknown = [key for key, item in allocations.items() if item.get("hours") is None]
        known_hours = math.fsum(item["hours"] for item in allocations.values() if item.get("hours") is not None)
        buffer = plan.get("buffer_hours")
        known_total = round(known_hours + (buffer if buffer is not None else 0), 6)
        priorities = [key for key, item in allocations.items() if item["mode"] == "priority"]
        warnings = []
        inconsistent_capacity = False
        if len(priorities) > 2:
            warnings.append("More than two priorities; recommend narrowing the focus.")
        if available is not None and ((derived is not None and available > derived) or (ceiling is not None and available > ceiling)):
            inconsistent_capacity = True
            warnings.append("Remaining hours exceed the stated monthly cap after known usage; reconcile capacity.")
        if ceiling is not None and used is not None and used > ceiling:
            inconsistent_capacity = True
            warnings.append("The monthly cap has already been exceeded.")
        over = round(max(0, known_total - available), 6) if available is not None else None
        if over:
            warnings.append("The known plan exceeds available hours; reduce, defer, or park work.")
        missing = available is None or buffer is None or bool(unknown)
        incomplete = missing or inconsistent_capacity
        if missing:
            warnings.append("Capacity, buffer, or allocation hours remain unknown; this is not a verified fit.")
        results[month] = {
            "available_hours": available, "known_allocated_hours": known_hours,
            "buffer_hours": buffer, "unknown_allocations": unknown,
            "priority_count": len(priorities), "overallocated_hours": over,
            "unallocated_hours": round(available - known_total, 6) if not incomplete else None,
            "budget_state": "exceeds" if over else "unknown" if incomplete else "fits",
            "warnings": warnings,
        }
    return results


EDITABLE = {
    "name", "workspace_paths", "status", "priority", "expectations",
    "commitments", "proficiency", "progress", "research", "decisions", "open_questions",
}
SECTIONS = {
    "expectations": dict, "commitments": dict, "proficiency": dict,
    "progress": list, "research": dict, "decisions": list, "open_questions": list,
}
ID_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*-[0-9a-f]{12}")


def default_root():
    override = os.environ.get("BE_REAL_HOME")
    if override:
        return Path(override).expanduser().resolve()
    if sys.platform == "darwin":
        root = Path.home() / "Library" / "Application Support" / "Be Real"
    elif sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
        if not base.is_absolute():
            base = Path.home() / "AppData" / "Local"
        root = base / "Be Real"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
        if not base.is_absolute():
            base = Path.home() / ".local" / "share"
        root = base / "be-real"
    return root.resolve()


def lock_file(handle, timeout=10):
    """OS-managed locks are released on process exit, including an interrupted writer."""
    deadline = time.monotonic() + timeout
    while True:
        try:
            if os.name == "nt":
                handle.seek(0)
                # Windows permits locking a byte beyond EOF; never truncate the lock file.
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except OSError as exc:
            if exc.errno not in (errno.EACCES, errno.EAGAIN, errno.EDEADLK):
                raise
            if time.monotonic() >= deadline:
                raise StoreError("Store is busy. Retry after the other writer finishes; do not delete the lock file.") from exc
            time.sleep(0.05)


def unlock_file(handle):
    if os.name == "nt":
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(handle, fcntl.LOCK_UN)


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise StoreError(f"Cannot read {path}: {exc}. Existing data was not reset.") from exc


def atomic_json(path, value):
    """Replace one document only after a complete, flushed write in the same folder."""
    body = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def merge(current, patch):
    """Objects merge; arrays replace; null is an unknown value, not a deletion."""
    if isinstance(current, dict) and isinstance(patch, dict):
        result = deepcopy(current)
        for key, value in patch.items():
            result[key] = merge(result.get(key), value)
        return result
    return deepcopy(patch)


def validate_record(record, project_id):
    if not isinstance(record, dict) or type(record.get("schema_version")) is not int or record["schema_version"] != 1:
        raise StoreError("Unsupported or malformed project schema; preserve the file for inspection.")
    if record.get("id") != project_id:
        raise StoreError("Project ID does not match its folder.")
    if type(record.get("revision")) is not int or record["revision"] < 1:
        raise StoreError("Invalid project revision.")
    if not isinstance(record.get("name"), str) or not record["name"].strip():
        raise StoreError("A nonempty project name is required.")
    if not isinstance(record.get("status"), str) or record["status"] not in {"active", "paused", "completed", "archived", "unknown"}:
        raise StoreError("Invalid project status.")
    if not isinstance(record.get("priority"), str) or record["priority"] not in {"main", "secondary", "experiment", "unknown"}:
        raise StoreError("Invalid project priority.")
    paths = record.get("workspace_paths")
    if not isinstance(paths, list) or any(not isinstance(p, str) or not Path(p).is_absolute() for p in paths):
        raise StoreError("workspace_paths must be a list of absolute paths.")
    for section, kind in SECTIONS.items():
        if not isinstance(record.get(section), kind):
            raise StoreError(f"{section} must be a {kind.__name__}.")
    for key in ("created_at", "updated_at", "change_note"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise StoreError(f"Missing {key}.")
    try:
        json.dumps(record, allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise StoreError(f"Record is not valid finite JSON: {exc}") from exc


class Store:
    def __init__(self, root=None):
        self.root = Path(root).expanduser().resolve() if root is not None else default_root()
        self.projects = self.root / "projects"

    def _check_root(self):
        if self.projects.is_symlink():
            raise StoreError("The projects directory must not be a symlink.")

    def initialize(self):
        self._check_root()
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.projects.mkdir(mode=0o700, exist_ok=True)
        return {"root": str(self.root), "projects": str(self.projects)}

    @contextmanager
    def _lock(self):
        self.initialize()
        lock = self.root / ".write.lock"
        if lock.is_symlink():
            raise StoreError("Lock file must not be a symlink.")
        fd = os.open(lock, os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "r+b") as handle:
            lock_file(handle)
            try:
                yield
            finally:
                unlock_file(handle)

    def _directory(self, project_id):
        self._check_root()
        if not isinstance(project_id, str) or not ID_PATTERN.fullmatch(project_id):
            raise StoreError("Invalid project ID. Use an ID returned by list, resolve, or create.")
        directory = self.projects / project_id
        if directory.is_symlink() or (directory / "project.json").is_symlink():
            raise StoreError("Project folders and records must not be symlinks.")
        return directory

    def show(self, project_id):
        record = read_json(self._directory(project_id) / "project.json")
        validate_record(record, project_id)
        return record

    def records(self):
        self._check_root()
        if not self.projects.exists():
            return []
        result = []
        for entry in sorted(self.projects.iterdir()):
            if entry.name.startswith("."):
                continue
            if not entry.is_dir():
                continue
            result.append(self.show(entry.name))
        return result

    def summaries(self):
        keys = ("id", "name", "status", "priority", "workspace_paths", "revision", "updated_at")
        return [{key: r[key] for key in keys} for r in self.records()]

    def portfolio_show(self):
        path = self.root / "portfolio.json"
        if path.is_symlink():
            raise StoreError("Portfolio record must not be a symlink.")
        if not path.exists():
            return {"schema_version": 1, "revision": 0, "created_at": None,
                    "updated_at": None, "change_note": "No portfolio saved yet", "months": {}}
        record = read_json(path)
        validate_portfolio(record)
        if record["revision"] < 1:
            raise StoreError("A stored portfolio must have a positive revision.")
        return record

    def portfolio_update(self, patch, expected_revision, note):
        if not isinstance(patch, dict) or set(patch) != {"months"} or not isinstance(patch["months"], dict):
            raise StoreError("Portfolio patches must contain a months object only.")
        if not isinstance(note, str) or not note.strip():
            raise StoreError("A short change note is required.")
        with self._lock():
            old = self.portfolio_show()
            if old["revision"] != expected_revision:
                raise StoreError(f"Revision conflict: expected {expected_revision}, found {old['revision']}. Reload and reconcile the shared plan.")
            new = merge(old, patch)
            validate_portfolio(new)
            for month in new["months"].values():
                for project_id in month.get("plan", {}).get("allocations", {}):
                    self.show(project_id)
            if new == old:
                return old
            now = timestamp()
            new.update(revision=old["revision"] + 1, created_at=old["created_at"] or now,
                       updated_at=now, change_note=note.strip())
            if old["revision"]:
                history = self.root / "portfolio-history"
                if history.is_symlink():
                    raise StoreError("Portfolio history must not be a symlink.")
                history.mkdir(mode=0o700, exist_ok=True)
                snapshot = history / f"{old['revision']:06d}.json"
                if snapshot.is_symlink():
                    raise StoreError("Portfolio snapshot must not be a symlink.")
                if snapshot.exists():
                    if read_json(snapshot) != old:
                        raise StoreError("Portfolio history conflicts with the current revision.")
                else:
                    atomic_json(snapshot, old)
            atomic_json(self.root / "portfolio.json", new)
        return new

    def resolve(self, workspace):
        location = Path(workspace).expanduser().resolve()
        matches = []
        for record in self.records():
            depths = []
            for alias in record["workspace_paths"]:
                path = Path(alias).resolve()
                try:
                    location.relative_to(path)
                    depths.append(len(path.parts))
                except ValueError:
                    pass
            if depths:
                matches.append((max(depths), record))
        if not matches:
            return {"match": None, "workspace": str(location)}
        depth = max(d for d, _ in matches)
        candidates = [r for d, r in matches if d == depth]
        if len(candidates) != 1:
            raise StoreError("Ambiguous workspace mapping; select a project ID explicitly.")
        return {"match": candidates[0]["id"], "name": candidates[0]["name"], "workspace": str(location)}

    def _prepare(self, record):
        validate_record(record, record["id"])
        record["workspace_paths"] = list(dict.fromkeys(str(Path(p).resolve()) for p in record["workspace_paths"]))
        for other in self.records():
            if other["id"] != record["id"] and set(other["workspace_paths"]) & set(record["workspace_paths"]):
                raise StoreError(f"Workspace already belongs to {other['id']}; reuse or explicitly reconcile that record.")

    def create(self, name, workspace=None, initial=None):
        patch = initial if initial is not None else {}
        if not isinstance(patch, dict) or set(patch) - EDITABLE:
            raise StoreError("Initial data contains unsupported or protected fields.")
        if not isinstance(name, str) or not name.strip():
            raise StoreError("A project name is required.")
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:48].rstrip("-") or "project"
        project_id = f"{slug}-{uuid.uuid4().hex[:12]}"
        now = timestamp()
        record = {
            "schema_version": 1, "id": project_id, "name": name.strip(), "revision": 1,
            "created_at": now, "updated_at": now, "change_note": "Project record created",
            "workspace_paths": [str(Path(workspace).expanduser().resolve())] if workspace else [],
            "status": "unknown", "priority": "unknown",
            **{key: kind() for key, kind in SECTIONS.items()},
        }
        record = merge(record, patch)
        with self._lock():
            self._prepare(record)
            destination = self._directory(project_id)
            if destination.exists():
                raise StoreError("Generated project ID already exists; retry create.")
            pending = Path(tempfile.mkdtemp(prefix=".new-", dir=self.projects))
            try:
                atomic_json(pending / "project.json", record)
                pending.rename(destination)
            finally:
                if pending.exists():
                    shutil.rmtree(pending)
        return record

    def update(self, project_id, patch, expected_revision, note):
        if not isinstance(patch, dict) or not patch or set(patch) - EDITABLE:
            raise StoreError("Patch must contain editable fields only and must not be empty.")
        if not isinstance(note, str) or not note.strip():
            raise StoreError("A short change note is required.")
        with self._lock():
            old = self.show(project_id)
            if old["revision"] != expected_revision:
                raise StoreError(f"Revision conflict: expected {expected_revision}, found {old['revision']}. Reload and reconcile; do not blindly retry.")
            new = merge(old, patch)
            self._prepare(new)
            if new == old:
                return old
            new.update(revision=old["revision"] + 1, updated_at=timestamp(), change_note=note.strip())
            directory = self._directory(project_id)
            history = directory / "history"
            if history.is_symlink():
                raise StoreError("History directory must not be a symlink.")
            history.mkdir(mode=0o700, exist_ok=True)
            snapshot = history / f"{old['revision']:06d}.json"
            if snapshot.is_symlink():
                raise StoreError("History snapshot must not be a symlink.")
            if snapshot.exists():
                if read_json(snapshot) != old:
                    raise StoreError("Existing history conflicts with the current revision; inspect before updating.")
            else:
                atomic_json(snapshot, old)
            atomic_json(directory / "project.json", new)
        return new


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Override BE_REAL_HOME and the platform data directory")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("info")
    commands.add_parser("init-store")
    commands.add_parser("list")
    commands.add_parser("portfolio-show")
    commands.add_parser("portfolio-check")
    portfolio_update = commands.add_parser("portfolio-update")
    portfolio_update.add_argument("--patch", required=True)
    portfolio_update.add_argument("--expected-revision", required=True, type=int)
    portfolio_update.add_argument("--note", required=True)
    resolve = commands.add_parser("resolve")
    resolve.add_argument("--workspace", required=True)
    show = commands.add_parser("show")
    show.add_argument("project_id")
    create = commands.add_parser("create")
    create.add_argument("--name", required=True)
    create.add_argument("--workspace")
    create.add_argument("--initial", help="JSON file with initial editable fields")
    update = commands.add_parser("update")
    update.add_argument("project_id")
    update.add_argument("--patch", required=True, help="JSON file containing only changed fields")
    update.add_argument("--expected-revision", required=True, type=int)
    update.add_argument("--note", required=True)
    args = parser.parse_args()
    store = Store(args.root)
    try:
        if args.command == "info":
            result = {"root": str(store.root), "platform": sys.platform,
                      "python": sys.version.split()[0], "schema_version": 1}
        elif args.command == "init-store":
            result = store.initialize()
        elif args.command == "list":
            result = store.summaries()
        elif args.command == "portfolio-show":
            result = store.portfolio_show()
        elif args.command == "portfolio-check":
            result = check_portfolio(store.portfolio_show())
        elif args.command == "portfolio-update":
            result = store.portfolio_update(read_json(args.patch), args.expected_revision, args.note)
        elif args.command == "resolve":
            result = store.resolve(args.workspace)
        elif args.command == "show":
            result = store.show(args.project_id)
        elif args.command == "create":
            result = store.create(args.name, args.workspace, read_json(args.initial) if args.initial else None)
        else:
            result = store.update(args.project_id, read_json(args.patch), args.expected_revision, args.note)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (StoreError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    # Keep JSON pipes consistent on Windows and with non-ASCII project names.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
