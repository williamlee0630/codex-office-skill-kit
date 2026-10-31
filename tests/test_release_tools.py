import importlib.util
import json
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
TEMP = ROOT / 'tests/.tmp'
TEMP.mkdir(parents=True, exist_ok=True)


class ReleaseToolTests(unittest.TestCase):
    def test_all_nine_skills_run_outside_original_workspace(self):
        inputs = {'data-analyst': 'sales.csv', 'presentation-maker': 'deck.json', 'receipt-organizer': 'receipts.json'}
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            folder = Path(temp)
            for source_skill in (ROOT / '.agents/skills').iterdir():
                if not (source_skill / 'SKILL.md').is_file():
                    continue
                with self.subTest(skill=source_skill.name):
                    target = folder / source_skill.name
                    shutil.copytree(source_skill, target)
                    source = ROOT / 'examples' / source_skill.name / inputs.get(source_skill.name, 'input.json')
                    command = [sys.executable, '-X', 'utf8', str(target / 'scripts/run.py'), '--input', str(source),
                               '--output', str(folder / (source_skill.name + '-output'))]
                    result = subprocess.run(command, cwd=folder, capture_output=True, text=True, encoding='utf-8')
                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_installer_dry_run_and_conflict_preserve_existing(self):
        script = ROOT / 'tools/install_skills.py'
        self.assertTrue(script.exists(), '尚未實作安全安裝工具')
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            target = Path(temp) / 'skills'
            command = [sys.executable, '-X', 'utf8', str(script), '--target', str(target)]
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(target.exists())
            result = subprocess.run(command + ['--apply'], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(list(target.glob('*/SKILL.md'))), 9)
            sentinel = target / 'email-assistant/SKILL.md'
            sentinel.write_text('保留既有內容', encoding='utf-8')
            result = subprocess.run(command + ['--apply'], capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(encoding='utf-8'), '保留既有內容')

    def test_manifest_has_nine_discriminating_skills(self):
        script = ROOT / 'tools/validate_kit.py'
        self.assertTrue(script.exists(), '尚未實作結構驗證工具')
        result = subprocess.run([sys.executable, '-X', 'utf8', str(script)], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
