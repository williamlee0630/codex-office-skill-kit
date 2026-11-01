"""以學員可見內容和可開啟附件驗收，不取代真實 Codex 測試。"""
import csv
import io
import sys
import unittest
from pathlib import Path

from test_handbook_learner import LearnerPage, SKILLS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'handbook'))


class QuickstartTests(unittest.TestCase):
    def test_first_chapter_leads_with_complete_prompt_workflow(self):
        source = (ROOT / 'handbook/chapter-01.html').read_text(encoding='utf-8')
        first = source.split('id="understand"', 1)[1].split('</section>', 1)[0]
        self.assertIn('複製完整提示詞', first)
        self.assertNotIn('先送出', first)
        self.assertNotIn('例如只送出', first)

    def test_finance_default_outputs_do_not_require_advanced_tasks(self):
        source = (ROOT / 'handbook/chapter-10.html').read_text(encoding='utf-8')
        visible = ' '.join(LearnerPage(source).visible)
        self.assertIn('銀行對帳結果.xlsx', visible)
        self.assertNotIn('財務差異分析.xlsx', visible)
        self.assertNotIn('財務報表.xlsx', visible)
        for advanced in ['財務差異分析.xlsx', '財務報表.xlsx']:
            self.assertIn(advanced, source)

    def test_recording_uses_same_prompts_and_preserves_mixed_currency_periods(self):
        recording = (ROOT / 'docs/RECORDING.md').read_text(encoding='utf-8')
        self.assertIn('chapter-09.html#try-now', recording)
        self.assertIn('chapter-10.html#try-now', recording)
        self.assertNotIn('兩份2026年10月TWD明細', recording)
        self.assertIn('全部保留並分開處理', recording)

    def test_nine_chapters_offer_complete_visible_work_prompts(self):
        for number, skill in enumerate(SKILLS, 2):
            source = (ROOT / f'handbook/chapter-{number:02}.html').read_text(encoding='utf-8')
            page = LearnerPage(source)
            with self.subTest(skill=skill):
                self.assertIn('id="try-now"', source)
                prompts = [b['text'] for b in page.blocks if not b['collapsed']]
                self.assertTrue(any(p.startswith('$' + skill + '\n') and len(p) > 70 for p in prompts))
                self.assertLess(source.index('id="try-now"'), source.index('id="lesson-1"'))

    def test_attachment_contract_and_real_formats(self):
        import experiences
        from docx import Document
        from PIL import Image
        attachment_counts = [0, 1, 0, 0, 1, 0, 2, 1, 2]
        for skill, count in zip(SKILLS, attachment_counts):
            exp = experiences.EXPERIENCES[skill]
            self.assertEqual(len(exp['attachments']), count, skill)
            for filename, label in exp['attachments']:
                path = ROOT / 'examples/quickstart' / filename
                self.assertTrue(path.is_file(), filename)
                self.assertIn('模擬', label)
                if path.suffix == '.png':
                    with Image.open(path) as im:
                        im.verify()
                elif path.suffix == '.docx':
                    self.assertTrue(Document(path).paragraphs)
                elif path.suffix == '.csv':
                    self.assertTrue(path.read_bytes().startswith(b'\xef\xbb\xbf'))
                    self.assertGreater(len(list(csv.DictReader(io.StringIO(path.read_text(encoding='utf-8-sig'))))), 1)

    def test_reused_finance_and_sales_preserve_all_source_values(self):
        for source, target in [
            ('data-analyst/sales.csv', '模擬銷售資料.csv'),
            ('finance-assistant/reconciliation/internal.csv', '模擬公司內部帳務.csv'),
            ('finance-assistant/reconciliation/bank.csv', '模擬銀行交易明細.csv'),
        ]:
            before = list(csv.reader(io.StringIO((ROOT / 'examples' / source).read_text(encoding='utf-8-sig'))))
            after = list(csv.reader(io.StringIO((ROOT / 'examples/quickstart' / target).read_text(encoding='utf-8-sig'))))
            self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
