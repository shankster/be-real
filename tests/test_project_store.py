import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "skills/be-real/scripts/project_store.py"
spec = importlib.util.spec_from_file_location("project_store", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ProjectStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.store = module.Store(self.base / "data")

    def create(self, name="Example", workspace=None, initial=None):
        return self.store.create(name, workspace, initial)

    def test_read_only_commands_do_not_create_data(self):
        self.assertEqual(self.store.summaries(), [])
        self.assertIsNone(self.store.resolve(self.base / "repo")["match"])
        self.assertEqual(self.store.portfolio_show()["revision"], 0)
        self.assertEqual(module.check_portfolio(self.store.portfolio_show()), {})
        self.assertFalse(self.store.root.exists())

    def test_portfolio_uses_remaining_capacity_and_separate_months(self):
        first, second = self.create("First"), self.create("Second")
        allocations = {p["id"]: {"mode": "priority", "hours": 8} for p in (first, second)}
        record = self.store.portfolio_update({"months": {
            "2026-10": {"capacity": {"max_hours": 40, "used_hours": 30},
                        "plan": {"buffer_hours": 2, "allocations": allocations}},
            "2026-11": {"capacity": {"max_hours": 24, "remaining_hours": 24},
                        "plan": {"buffer_hours": 4, "allocations": allocations}},
        }}, 0, "Two independent months")
        checked = module.check_portfolio(record)
        self.assertEqual(checked["2026-10"]["available_hours"], 10)
        self.assertEqual(checked["2026-10"]["overallocated_hours"], 8)
        self.assertEqual(checked["2026-10"]["budget_state"], "exceeds")
        self.assertEqual(checked["2026-11"]["unallocated_hours"], 4)
        self.assertEqual(checked["2026-11"]["budget_state"], "fits")
        self.assertEqual(self.store.show(first["id"]), first)
        self.assertEqual(self.store.show(second["id"]), second)

    def test_portfolio_unknown_zero_and_inconsistent_capacity(self):
        project = self.create()
        record = {"schema_version": 1, "revision": 0, "months": {"2026-10": {
            "capacity": {"max_hours": 30}, "plan": {"buffer_hours": 0, "allocations": {
                project["id"]: {"mode": "priority", "hours": 3}}}}}}
        month = record["months"]["2026-10"]
        self.assertEqual(module.check_portfolio(record)["2026-10"]["budget_state"], "unknown")
        month["capacity"]["remaining_hours"] = 0
        self.assertEqual(module.check_portfolio(record)["2026-10"]["overallocated_hours"], 3)
        month["plan"]["allocations"][project["id"]]["hours"] = 0
        self.assertEqual(module.check_portfolio(record)["2026-10"]["budget_state"], "fits")
        month["plan"]["allocations"][project["id"]]["hours"] = None
        checked = module.check_portfolio(record)["2026-10"]
        self.assertEqual(checked["unknown_allocations"], [project["id"]])
        self.assertIsNone(checked["unallocated_hours"])
        self.assertEqual(checked["budget_state"], "unknown")
        month["plan"]["allocations"][project["id"]]["hours"] = 0
        month["capacity"].update(used_hours=28, remaining_hours=10)
        self.assertEqual(module.check_portfolio(record)["2026-10"]["budget_state"], "unknown")
        month["capacity"].update(used_hours=31, remaining_hours=0)
        self.assertEqual(module.check_portfolio(record)["2026-10"]["budget_state"], "unknown")

    def test_portfolio_warns_about_three_priorities_even_with_spare_hours(self):
        projects = [self.create(str(i)) for i in range(3)]
        record = self.store.portfolio_update({"months": {"2026-11": {
            "capacity": {"remaining_hours": 30}, "plan": {"buffer_hours": 5,
            "allocations": {p["id"]: {"mode": "priority", "hours": 2} for p in projects}}}}}, 0, "User chose three")
        checked = module.check_portfolio(record)["2026-11"]
        self.assertEqual(checked["priority_count"], 3)
        self.assertEqual(checked["unallocated_hours"], 19)
        self.assertTrue(any("More than two" in item for item in checked["warnings"]))

    def test_portfolio_partial_updates_history_and_revision_conflict(self):
        first = self.store.portfolio_update({"months": {"2026-10": {"capacity": {"remaining_hours": 8}}}}, 0, "Initial capacity")
        second = self.store.portfolio_update({"months": {"2026-11": {"capacity": {"remaining_hours": 4}}}}, 1, "Next month is busy")
        self.assertEqual(second["months"]["2026-10"], first["months"]["2026-10"])
        self.assertEqual(module.read_json(self.store.root / "portfolio-history/000001.json"), first)
        with self.assertRaisesRegex(module.StoreError, "Revision conflict"):
            self.store.portfolio_update({"months": {"2026-10": {"capacity": {"remaining_hours": 9}}}}, 1, "Stale")
        self.assertEqual(self.store.portfolio_show(), second)
        self.assertEqual(self.store.portfolio_update({"months": {}}, 2, "No changes"), second)

    def test_portfolio_invalid_hours_and_missing_projects_preserve_data(self):
        first = self.store.portfolio_update({"months": {"2026-10": {}}}, 0, "Unknown capacity")
        for number in (-1, True, float("nan"), float("inf"), "10"):
            with self.subTest(number=number), self.assertRaises(module.StoreError):
                self.store.portfolio_update({"months": {"2026-10": {"capacity": {"remaining_hours": number}}}}, 1, "Invalid")
        with self.assertRaises(module.StoreError):
            self.store.portfolio_update({"months": {"2026-10": {"plan": {"allocations": {
                "absent-000000000000": {"mode": "priority", "hours": 1}}}}}}, 1, "Missing project")
        self.assertEqual(self.store.portfolio_show(), first)

    def test_portfolio_interrupted_replace_preserves_current_and_retry(self):
        first = self.store.portfolio_update({"months": {"2026-10": {}}}, 0, "Start")
        replace = os.replace

        def fail_current(source, destination):
            if Path(destination).name == "portfolio.json":
                raise OSError("Simulated interruption")
            return replace(source, destination)

        update = {"months": {"2026-11": {"capacity": {"remaining_hours": 12}}}}
        with patch.object(module.os, "replace", side_effect=fail_current):
            with self.assertRaises(OSError):
                self.store.portfolio_update(update, 1, "Interrupted")
        self.assertEqual(self.store.portfolio_show(), first)
        second = self.store.portfolio_update(update, 1, "Reconciled and retried")
        self.assertEqual(second["revision"], 2)

    def test_concurrent_portfolio_cli_updates_share_one_revision(self):
        processes = []
        for hours in (10, 20):
            patch_file = self.base / f"portfolio-{hours}.json"
            patch_file.write_text(json.dumps({"months": {"2026-10": {
                "capacity": {"remaining_hours": hours}, "plan": {"buffer_hours": 2}}}}))
            command = [sys.executable, str(SCRIPT), "--root", str(self.store.root), "portfolio-update",
                       "--patch", str(patch_file), "--expected-revision", "0", "--note", "Concurrent update"]
            processes.append(subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
        outputs = [p.communicate(timeout=10) for p in processes]
        self.assertEqual(sorted(p.returncode for p in processes), [0, 1])
        self.assertTrue(any("Revision conflict" in err for _, err in outputs))
        self.assertEqual(self.store.portfolio_show()["revision"], 1)
        for command in ("portfolio-show", "portfolio-check"):
            result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.store.root), command],
                                    capture_output=True, text=True, check=True)
            self.assertIsInstance(json.loads(result.stdout), dict)

    def test_merge_history_and_unknown_values(self):
        first = self.create(initial={"expectations": {"goal": "Paid pilot", "budget": None},
                                    "research": {"competitors": [{"name": "Example", "basis": "inferred"}]}})
        second = self.store.update(first["id"], {"expectations": {"weekly_hours": 4}}, 1, "User supplied capacity")
        self.assertEqual(second["expectations"], {"goal": "Paid pilot", "budget": None, "weekly_hours": 4})
        self.assertEqual(second["research"], first["research"])
        self.assertEqual(second["revision"], 2)
        history = self.store.projects / first["id"] / "history/000001.json"
        self.assertEqual(module.read_json(history), first)
        self.assertEqual(self.store.show(first["id"]), second)
        if os.name != "nt":
            self.assertEqual((self.store.projects / first["id"] / "project.json").stat().st_mode & 0o777, 0o600)

    def test_stale_update_preserves_newer_work(self):
        first = self.create()
        new = self.store.update(first["id"], {"priority": "main"}, 1, "User prioritized this")
        with self.assertRaisesRegex(module.StoreError, "Revision conflict"):
            self.store.update(first["id"], {"status": "paused"}, 1, "Stale update")
        self.assertEqual(self.store.show(first["id"]), new)

    def test_same_names_moves_and_nested_workspaces(self):
        old = self.base / "old"
        new = self.base / "new"
        first = self.create("Same name", str(old))
        second = self.create("Same name")
        self.assertNotEqual(first["id"], second["id"])
        moved = self.store.update(first["id"], {"workspace_paths": [str(old), str(new)]}, 1, "Repository moved")
        self.assertEqual(moved["id"], first["id"])
        self.assertEqual(self.store.resolve(new / "src")["match"], first["id"])
        nested = self.create("Nested", str(new / "nested"))
        self.assertEqual(self.store.resolve(new / "nested/src")["match"], nested["id"])
        self.assertIsNone(self.store.resolve(self.base / "new-unrelated")["match"])

    def test_duplicate_workspace_and_protected_fields(self):
        first = self.create(workspace=str(self.base / "repo"))
        with self.assertRaisesRegex(module.StoreError, "already belongs"):
            self.create(workspace=str(self.base / "repo"))
        for bad in ({"revision": 77}, {"status": []}, {"expectations": None}, {"commitments": {"hours": float("nan")}}):
            with self.assertRaises(module.StoreError):
                self.store.update(first["id"], bad, 1, "Invalid update")
        self.assertEqual(self.store.show(first["id"]), first)

    def test_corruption_is_reported_and_preserved(self):
        first = self.create()
        record = self.store.projects / first["id"] / "project.json"
        record.write_text("broken record")
        with self.assertRaises(module.StoreError):
            self.store.update(first["id"], {"priority": "main"}, 1, "Do not reset")
        self.assertEqual(record.read_text(), "broken record")

    def test_paths_cannot_escape_project_folder(self):
        with self.assertRaises(module.StoreError):
            self.store.show("../../outside")
        first = self.create()
        outside = self.base / "outside"
        outside.mkdir()
        try:
            (self.store.projects / first["id"] / "history").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            if os.name == "nt" and getattr(exc, "winerror", None) == 1314:
                self.skipTest("Windows symlink privilege unavailable")
            raise
        with self.assertRaises(module.StoreError):
            self.store.update(first["id"], {"priority": "main"}, 1, "No symlink writes")
        self.assertEqual(list(outside.iterdir()), [])
        self.assertEqual(self.store.show(first["id"]), first)

    def test_interrupted_replace_preserves_current_and_can_retry(self):
        first = self.create()
        replace = os.replace

        def fail_current(source, destination):
            if Path(destination).name == "project.json":
                raise OSError("Simulated interruption")
            return replace(source, destination)

        with patch.object(module.os, "replace", side_effect=fail_current):
            with self.assertRaises(OSError):
                self.store.update(first["id"], {"priority": "main"}, 1, "Save failed")
        self.assertEqual(self.store.show(first["id"]), first)
        self.assertEqual(list((self.store.projects / first["id"]).glob(".write-*")), [])
        new = self.store.update(first["id"], {"priority": "main"}, 1, "Retry after checking")
        self.assertEqual(new["revision"], 2)

    def test_simultaneous_process_updates_allow_only_one_revision(self):
        first = self.create()
        processes = []
        for label in ("main", "secondary"):
            patch_file = self.base / f"{label}.json"
            patch_file.write_text(json.dumps({"priority": label}))
            command = [sys.executable, str(SCRIPT), "--root", str(self.store.root), "update", first["id"],
                       "--patch", str(patch_file), "--expected-revision", "1", "--note", label]
            processes.append(subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
        outputs = [p.communicate(timeout=10) for p in processes]
        self.assertEqual(sorted(p.returncode for p in processes), [0, 1])
        self.assertTrue(any("Revision conflict" in err for _, err in outputs))
        self.assertEqual(self.store.show(first["id"])["revision"], 2)

    def test_noop_and_array_replacement_are_explicit(self):
        first = self.create(initial={"open_questions": ["One", "Two"]})
        same = self.store.update(first["id"], {"name": "Example"}, 1, "No change")
        self.assertEqual(same["revision"], 1)
        new = self.store.update(first["id"], {"open_questions": []}, 1, "Questions answered")
        self.assertEqual(new["open_questions"], [])

    def test_environment_override_and_cli_round_trip(self):
        env = dict(os.environ, BE_REAL_HOME=str(self.base / "alternate"))
        created = subprocess.run([sys.executable, str(SCRIPT), "create", "--name", "CLI"],
                                 env=env, check=True, capture_output=True, text=True)
        record = json.loads(created.stdout)
        shown = subprocess.run([sys.executable, str(SCRIPT), "show", record["id"]],
                               env=env, check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(shown.stdout), record)
        self.assertFalse(self.store.root.exists())


if __name__ == "__main__":
    unittest.main()
