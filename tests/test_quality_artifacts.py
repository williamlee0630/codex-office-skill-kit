"""v1.3.0 成品品質：原始值保留、可回算摘要與真正 Office 結構。"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class QualityArtifacts(unittest.TestCase):
    def setUp(self):
        base = ROOT / 'tests/.tmp'
        base.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_skill(self, name, source, *extra):
        out = self.work / name
        run = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / '.agents/skills' / name / 'scripts/run.py'),
                              '--input', str(source), '--output', str(out), *extra], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(run.returncode, 0, run.stderr)
        return out

    def test_receipt_quantity_source_and_review_sheet(self):
        from openpyxl import load_workbook
        source = self.work / 'receipt.json'
        source.write_text(json.dumps({'source': '模擬照片.png', 'simulation': True, 'receipts': [
            {'id': 'R1', 'date': '2026-10-23', 'vendor': '模擬商店', 'items': '筆', 'quantity': 3,
             'amount': 60, 'currency': 'TWD', 'evidence': '照片中段：筆 3 60'}]}, ensure_ascii=False), encoding='utf-8')
        out = self.run_skill('receipt-organizer', source)
        book = load_workbook(out / 'receipts.xlsx', data_only=True)
        sheet = book['報帳明細']
        headers = [c.value for c in sheet[1]]
        self.assertEqual(sheet.cell(2, headers.index('數量') + 1).value, 3)
        self.assertEqual(sheet.cell(2, headers.index('來源') + 1).value, '模擬照片.png')
        self.assertIn('人工確認', book.sheetnames)
        self.assertIn('教學', (out / 'receipts-report.md').read_text(encoding='utf-8'))
        book.close()

    def test_sales_summary_uses_computed_outlier_share_and_missing_fields(self):
        from openpyxl import load_workbook
        out = self.run_skill('data-analyst', ROOT / 'examples/quickstart/模擬銷售資料.csv',
                             '--group-by', 'category', '--value', 'amount', '--date-column', 'date')
        result = json.loads((out / 'analysis.json').read_text(encoding='utf-8'))
        self.assertEqual(result['columns']['amount']['sum'], 33900)
        self.assertAlmostEqual(result['outlier_impact']['amount']['share_percent'], 25000 / 33900 * 100)
        report = (out / 'analysis.md').read_text(encoding='utf-8')
        for text in ['73.7%', '資料事實', '可能解釋', '建議', '待確認', '商品', '幣別', '長期']:
            self.assertIn(text, report)
        self.assertNotIn('4166.666666666667', report)
        from PIL import Image
        with Image.open(out / 'chart.png') as chart:
            self.assertIn('待確認', chart.info['ValueUnit'])
            self.assertIn('2026-10-01', chart.info['DataRange'])
            self.assertIn('2026-10-06', chart.info['DataRange'])
        book = load_workbook(out / 'analysis.xlsx', data_only=True)
        for name in ['資料概覽', '資料品質', '異常資料']:
            self.assertIn(name, book.sheetnames)
        self.assertEqual(book['異常資料'].cell(2, 3).value, 25000)
        book.close()

    def test_word_table_is_editable_and_artifact_can_be_reopened(self):
        from docx import Document
        spec = importlib.util.spec_from_file_location('quality_office', ROOT / 'tools/office_common.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        path = self.work / 'review.docx'
        module.write_docx(path, '主管摘要', [('待確認', '| 項目 | 狀態 |\n|---|---|\n| 上線日 | 待核准 |')])
        doc = Document(path)
        self.assertEqual(len(doc.tables), 1)
        self.assertEqual(doc.tables[0].cell(1, 1).text, '待核准')
        self.assertEqual(module.verify_artifact(path), path)

    def test_presentation_cover_notes_and_incomplete_notes_are_reported(self):
        from pptx import Presentation
        source = self.work / 'deck.json'
        source.write_text(json.dumps({'title': '遠端協作指南', 'source': '模擬原始素材',
            'cover_notes': '請先說明這是協作建議。固定回覆時限及實際工具皆未指定，不能視為已核准制度。',
            'slides': [{'title': '先記錄決定再追蹤', 'bullets': ['決定寫入任務看板'], 'notes': '決定寫入任務看板'}]}, ensure_ascii=False), encoding='utf-8')
        out = self.run_skill('presentation-maker', source)
        deck = Presentation(out / 'presentation.pptx')
        self.assertIn('固定回覆時限', deck.slides[0].notes_slide.notes_text_frame.text)
        check = json.loads((out / 'layout-check.json').read_text(encoding='utf-8'))
        self.assertEqual(check['notes_review_required'], [2])
        self.assertFalse(check['visual_review_completed'])

    def test_review_sheet_keeps_foreign_identifier_as_text(self):
        from openpyxl import load_workbook
        source = self.work / 'receipt.json'
        source.write_text(json.dumps({'source': '模擬', 'receipts': [{'id': identifier, 'amount': 50,
            'currency': 'TWD', 'evidence': '原始模擬文字'} for identifier in ['=1+1', 'ID2', 'ID3']]}, ensure_ascii=False), encoding='utf-8')
        out = self.run_skill('receipt-organizer', source)
        book = load_workbook(out / 'receipts.xlsx', data_only=False)
        self.assertNotEqual(book['人工確認']['A2'].data_type, 'f')
        self.assertIn('=1+1', book['人工確認']['A2'].value)
        self.assertEqual(book['人工確認'].auto_filter.ref, 'A1:D4')
        book.close()

    def test_word_table_preserves_escaped_pipe_and_rejects_extra_cells(self):
        from docx import Document
        spec = importlib.util.spec_from_file_location('quality_table', ROOT / 'tools/office_common.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        path = self.work / 'escaped.docx'
        module.write_docx(path, '原始文字保留', [('', '| 名稱 | 值 |\n|---|---|\n| 顯示 | 甲\\|乙 |')])
        self.assertEqual(Document(path).tables[0].cell(1, 1).text, '甲|乙')
        with self.assertRaisesRegex(ValueError, '欄位'):
            module.write_docx(self.work / 'bad.docx', '不能截斷', [('', '| 名稱 | 值 |\n|---|---|\n| 一 | 二 | 三 |')])
        self.assertFalse((self.work / 'bad.docx').exists())


if __name__ == '__main__':
    unittest.main()
