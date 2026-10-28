from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/be-real'


class PackageTests(unittest.TestCase):
    def test_bundle_license_and_entrypoint(self):
        self.assertEqual((ROOT / 'LICENSE').read_bytes(), (SKILL / 'LICENSE').read_bytes())
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\n'))
        header = text.split('---', 2)[1]
        self.assertIn('name: be-real', header)
        description = re.search(r'^description: (.+)$', header, re.M)
        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1)), 1024)

    def test_relative_document_links_resolve(self):
        paths = [ROOT / 'README.md', *SKILL.rglob('*.md'), * (ROOT / 'docs').rglob('*.md')]
        for path in paths:
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' in target or target.startswith('#'):
                    continue
                with self.subTest(path=path, target=target):
                    self.assertTrue((path.parent / target.split('#')[0]).exists())

    def test_bundle_is_not_personal_data(self):
        forbidden = {'project.json', 'portfolio.json', '.write.lock', '.env'}
        for path in SKILL.rglob('*'):
            self.assertNotIn(path.name, forbidden)
