import importlib.util
from pathlib import Path
import sys, unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from publication import SKILLS, VERSION
from test_publication import fixture, put, load_module, TEMP
import tempfile
class V12ReleaseTests(unittest.TestCase):
    def test_canonical_registry_has_exact_required_names(self):
        self.assertEqual(VERSION,'1.2.0')
        self.assertEqual(tuple(SKILLS),('email-assistant','receipt-organizer','presentation-maker','document-writer','data-analyst','idea-generator','research-assistant','legal-reviewer','finance-assistant'))
    def test_wrong_nine_names_are_rejected_before_build(self):
        release=load_module('build_release')
        with tempfile.TemporaryDirectory(dir=TEMP) as tmp:
            root=fixture(Path(tmp))
            old=root/'.agents/skills/legal-reviewer/SKILL.md'
            old.unlink();old.parent.rmdir()
            put(root,'.agents/skills/meeting-assistant/SKILL.md')
            with self.assertRaisesRegex(ValueError,'9個技能'):
                release.build(root)
    def test_raw_extra_skill_directory_is_rejected(self):
        validator=load_module('validate_kit')
        with tempfile.TemporaryDirectory(dir=TEMP) as tmp:
            root=fixture(Path(tmp))
            (root/'.agents/skills/retired-empty').mkdir()
            validator.ROOT=root
            # Supply the shared module so failure diagnoses the inventory itself.
            put(root,'tools/office_common.py','pass\n')
            errors=validator.validate()
            self.assertTrue(any('清單' in e for e in errors))
if __name__=='__main__': unittest.main()
