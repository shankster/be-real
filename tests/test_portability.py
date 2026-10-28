import errno
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from test_project_store import module, SCRIPT


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()

    def test_platform_roots_and_overrides(self):
        home = self.base / 'home'
        cases = [('darwin', {}, home / 'Library/Application Support/Be Real'),
                 ('linux', {}, home / '.local/share/be-real'),
                 ('linux', {'XDG_DATA_HOME': str(self.base / 'xdg')}, self.base / 'xdg/be-real'),
                 ('linux', {'XDG_DATA_HOME': 'relative'}, home / '.local/share/be-real'),
                 ('win32', {}, home / 'AppData/Local/Be Real'),
                 ('win32', {'LOCALAPPDATA': str(self.base / 'local')}, self.base / 'local/Be Real'),
                 ('win32', {'LOCALAPPDATA': 'relative'}, home / 'AppData/Local/Be Real')]
        for platform, env, expected in cases:
            with self.subTest(platform=platform, env=env), patch.object(module.sys, 'platform', platform), \
                    patch.object(module.Path, 'home', return_value=home), patch.dict(os.environ, env, clear=True):
                self.assertEqual(module.default_root(), expected.resolve())
                with patch.dict(os.environ, {'BE_REAL_HOME': str(self.base / 'override')}):
                    self.assertEqual(module.default_root(), self.base / 'override')
                    self.assertEqual(module.Store(self.base / 'explicit').root, self.base / 'explicit')
        self.assertFalse(home.exists())

    def test_unicode_bom_and_spaces_round_trip(self):
        root = self.base / 'Shared records café'
        workspace = self.base / 'Project space 東京'
        initial = self.base / 'initial.json'
        initial.write_text(json.dumps({'expectations': {'goal': '₹100 — café'}}, ensure_ascii=False), encoding='utf-8-sig')
        command = [sys.executable, str(SCRIPT), '--root', str(root)]
        created = subprocess.run(command + ['create', '--name', 'Café 東京', '--workspace', str(workspace),
                                           '--initial', str(initial)], check=True, capture_output=True, encoding='utf-8')
        record = json.loads(created.stdout)
        self.assertEqual(record['name'], 'Café 東京')
        self.assertEqual(record['expectations']['goal'], '₹100 — café')
        resolved = subprocess.run(command + ['resolve', '--workspace', str(workspace / 'src')],
                                  check=True, capture_output=True, encoding='utf-8')
        self.assertEqual(json.loads(resolved.stdout)['match'], record['id'])

    def test_info_is_read_only(self):
        root = self.base / 'missing'
        result = subprocess.run([sys.executable, str(SCRIPT), '--root', str(root), 'info'],
                                check=True, capture_output=True, encoding='utf-8')
        self.assertEqual(json.loads(result.stdout)['root'], str(root))
        self.assertFalse(root.exists())

    def test_windows_lock_byte_and_contention_contract(self):
        handle = Mock()
        fake = SimpleNamespace(LK_NBLCK=1, LK_UNLCK=0, locking=Mock())
        with patch.object(module.os, 'name', 'nt'), patch.object(module, 'msvcrt', fake, create=True):
            module.lock_file(handle)
            fake.locking.assert_called_once_with(handle.fileno(), fake.LK_NBLCK, 1)
            module.unlock_file(handle)
            self.assertEqual(handle.seek.call_count, 2)
            fake.locking.assert_called_with(handle.fileno(), fake.LK_UNLCK, 1)
            fake.locking.side_effect = OSError(errno.EACCES, 'busy')
            with self.assertRaisesRegex(module.StoreError, 'busy'):
                module.lock_file(handle, timeout=0)
            fake.locking.side_effect = OSError(errno.EBADF, 'bad descriptor')
            with self.assertRaises(OSError):
                module.lock_file(handle, timeout=0)

    def test_native_lock_timeout_and_release_after_process_exit(self):
        root = self.base / 'data'
        code = '''import importlib.util,sys,time
spec=importlib.util.spec_from_file_location("store",sys.argv[1])
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with m.Store(sys.argv[2])._lock():
 print("locked",flush=True)
 time.sleep(30)
'''
        child = subprocess.Popen([sys.executable, '-c', code, str(SCRIPT), str(root)],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        try:
            self.assertEqual(child.stdout.readline().strip(), 'locked')
            with open(root / '.write.lock', 'r+b') as handle:
                with self.assertRaisesRegex(module.StoreError, 'busy'):
                    module.lock_file(handle, timeout=0.1)
        finally:
            child.kill()
            child.communicate(timeout=5)
        # The existing lock file is retained, but no dead process owns its OS lock.
        self.assertEqual(module.Store(root).create('Recovered')['revision'], 1)


if __name__ == '__main__':
    unittest.main()
