"""本次學員入口、成果預覽與自然語言客製化契約；非真實 Codex 驗收。"""
import sys
import unittest
from pathlib import Path

from test_handbook_learner import LearnerPage, SKILLS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'handbook'))


class QualityHandbookTests(unittest.TestCase):
    def test_nine_preview_blocks_are_visible_and_honestly_labeled(self):
        for number, skill in enumerate(SKILLS, 2):
            source = (ROOT / f'handbook/chapter-{number:02}.html').read_text(encoding='utf-8')
            visible = ' '.join(LearnerPage(source).visible)
            with self.subTest(skill=skill):
                self.assertIn('成果預覽｜完成後應看到什麼', visible)
                self.assertIn('示意畫面', visible)
                self.assertIn('人工核對', visible)
                self.assertIn('成功判斷', visible)
                self.assertLess(source.index('成果預覽｜'), source.index('id="lesson-1"'))

    def test_customization_is_one_complete_visible_natural_language_prompt(self):
        import experiences
        source = (ROOT / 'handbook/chapter-11.html').read_text(encoding='utf-8')
        page = LearnerPage(source)
        prompt = experiences.CUSTOMIZATION_PROMPT
        self.assertTrue(any(block['text'] == prompt and not block['collapsed'] for block in page.blocks))
        self.assertIn('複製完整提示詞</button>', source)
        for required in ['team-email-assistant', '完整執行資源', '不要覆寫', '不要只修改說明文字',
                         '同一批郵件資料', '不要擅自讀取其他私人郵件', '本次原始資料未列出需主管確認事項']:
            self.assertIn(required, prompt)
        for forbidden in ['.agents/', 'python ', 'YAML']:
            self.assertNotIn(forbidden, prompt)
        visible = ' '.join(page.visible)
        for required in ['選擇已完成的郵件 Skill', '複製完整的修改提示詞',
                         '讓 Codex 建立新 Skill 副本並修改', '使用相同來源測試新 Skill',
                         '比較修改前後的摘要', '$team-email-assistant', '示意', '工作流程', '分析規則']:
            self.assertIn(required, visible)
        for forbidden in ['YAML frontmatter', 'tools/sync_runtime.py', 'python -m unittest']:
            self.assertNotIn(forbidden, visible)
            self.assertIn(forbidden, source)

    def test_new_case_boundaries_and_signed_finance_difference(self):
        expected = {
            3: ['370', '690', '舊案例', '數量'],
            5: ['客服案件交接 SOP', '內部知識分享提案', '舊案例', '版本', '例外'],
            6: ['33,900', '25,000', '73.7%', '六天', '沒有商品欄', '幣別'],
            7: ['ideas.md', 'comparison.csv', '非必要', 'XLSX'],
            8: ['24', '20', '1,200', '950', '新年度'],
            10: ['-10', '內部減銀行', '產檔可用', '計算核對', '完整互動'],
        }
        for chapter, phrases in expected.items():
            visible = ' '.join(LearnerPage((ROOT / f'handbook/chapter-{chapter:02}.html').read_text(encoding='utf-8')).visible)
            for phrase in phrases:
                self.assertIn(phrase, visible, (chapter, phrase))

    def test_all_pages_have_current_version_and_history_is_fixed_commit(self):
        pages = list((ROOT / 'handbook').glob('*.html'))
        self.assertEqual(len(pages), 13)
        for page in pages:
            self.assertIn('離線講義 · v1.3.0', page.read_text(encoding='utf-8'))
        appendix = (ROOT / 'handbook/appendix.html').read_text(encoding='utf-8')
        self.assertIn('影片對照', appendix)
        self.assertIn('5f631a9fb08b4d7b59865e2ddd3366233b7796f7', appendix)
        self.assertIn('codex-office-skill-kit-1.2.0.zip', appendix)


if __name__ == '__main__':
    unittest.main()
