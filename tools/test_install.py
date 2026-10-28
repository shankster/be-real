#!/usr/bin/env python3
"""Exercise Skills CLI installation in disposable projects, never global agent folders."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
AGENTS = {
    'claude-code': '.claude/skills/be-real',
    'codex': '.agents/skills/be-real',
    'cursor': '.agents/skills/be-real',
    'github-copilot': '.agents/skills/be-real',
    'gemini-cli': '.agents/skills/be-real',
    'opencode': '.agents/skills/be-real',
    'cline': '.agents/skills/be-real',
    'windsurf': '.windsurf/skills/be-real',
}


def run(command, cwd, env):
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, encoding='utf-8',
                            errors='replace', timeout=180)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def main():
    npx = shutil.which('npx')
    if not npx:
        raise SystemExit('Install Node.js 22.20+ with npm before running this optional integration check.')
    source = ROOT / 'skills/be-real'
    expected = {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                and p.suffix != '.pyc' and p.name != '.DS_Store'}
    with tempfile.TemporaryDirectory(prefix='be-real-install-') as temporary:
        base = Path(temporary).resolve()
        env = dict(os.environ, DISABLE_TELEMETRY='1', DO_NOT_TRACK='1',
                   npm_config_cache=str(base / 'npm-cache'), PYTHONDONTWRITEBYTECODE='1',
                   BE_REAL_HOME=str(base / 'assessment-data'))
        # Each agent gets an independent install: a shared path cannot hide a failed target.
        record = None
        for agent, relative in AGENTS.items():
            workspace = base / agent
            workspace.mkdir()
            run([npx, '-y', 'skills@1.7.4', 'add', str(ROOT), '--skill', 'be-real',
                 '--agent', agent, '--copy', '-y'], workspace, env)
            installed = workspace / relative
            for name, digest in expected.items():
                target = installed / name
                if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                    raise RuntimeError(f'{agent}: missing or changed bundled file {name}')
            helper = [sys.executable, str(installed / 'scripts/project_store.py')]
            if record is None:
                record = json.loads(run(helper + ['create', '--name', 'Installation fixture'], workspace, env))
            shown = json.loads(run(helper + ['show', record['id']], workspace, env))
            if shown != record:
                raise RuntimeError(f'{agent}: installed helpers did not reuse the same store')
            print(f'PASS {agent}: complete bundle, executable helper, shared data', flush=True)
    print('Installation checks passed. This does not execute the agents or evaluate their model responses.')


if __name__ == '__main__':
    main()
