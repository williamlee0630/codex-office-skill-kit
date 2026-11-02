"""主管摘要與本次章首來源的成品核對；不代表 Codex 完整互動或原生 Office 驗收。"""
import json
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from docx import Document
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]


class LegalFinanceQualityTests(unittest.TestCase):
    def setUp(self):
        (ROOT / 'tests/.tmp').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests/.tmp')
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def invoke(self, skill, data):
        source = self.work / 'input.json'
        source.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        result = subprocess.run([sys.executable, '-X', 'utf8',
            str(ROOT / '.agents/skills' / skill / 'scripts/run.py'),
            '--input', str(source), '--output', str(self.work / 'out')],
            capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.work / 'out'

    def test_legal_report_prioritizes_high_risks_and_reopens_deliverables(self):
        data = json.loads((ROOT / 'examples/legal-reviewer/input.json').read_text(encoding='utf-8'))
        data['source']['path'] = str(ROOT / 'examples/quickstart/模擬服務合約_甲方審查.docx')
        # 來源順序刻意從中風險開始；輸出應依風險排序，同級仍保留來源順序及 ID。
        out = self.invoke('legal-reviewer', data)
        paragraphs = [p.text for p in Document(out / '合約審查報告.docx').paragraphs]
        headings = [p.text for p in Document(out / '合約審查報告.docx').paragraphs if p.style.name.startswith('Heading')]
        self.assertEqual(headings[0], '主管風險摘要')
        self.assertLess(headings.index('風險 R2｜期限與自動續約'), headings.index('風險 R1｜當事人與目的'))
        first_detail = paragraphs.index('文件基本資訊')
        first_page_summary = '\n'.join(paragraphs[:first_detail])
        self.assertIn('高風險 5 項', first_page_summary)
        self.assertIn('R2', first_page_summary)
        self.assertIn('承諾期間超出原約且價格不可控', first_page_summary)
        self.assertIn('AI 初步審閱', first_page_summary)
        wb = load_workbook(out / '合約風險清單.xlsx', data_only=True)
        self.assertEqual(wb['風險清單']['A2'].value, 'R2')
        self.assertEqual(wb['風險清單']['F2'].value, '高')
        self.assertTrue(wb['風險清單']['C2'].value.startswith('[P3]'))
        self.assertTrue(wb['審查摘要']['B3'].value)
        audit = json.loads((out / 'audit.json').read_text(encoding='utf-8'))
        self.assertTrue(audit['artifact_checks']['content_reopened'])
        self.assertFalse(audit['artifact_checks']['native_office_opened'])
        self.assertFalse(audit['network_used'])

    def test_finance_summary_keeps_six_categories_and_source_linked_exceptions(self):
        quickstart = ROOT / 'examples/quickstart'
        out = self.invoke('finance-assistant', {
            'mode': 'reconcile', 'source': str(quickstart / '模擬公司內部帳務.csv'),
            'other': str(quickstart / '模擬銀行交易明細.csv'), 'simulation': True})
        doc = Document(out / '財務分析報告.docx')
        headings = [p.text for p in doc.paragraphs if p.style.name.startswith('Heading')]
        self.assertEqual(headings[0], '對帳摘要')
        body = '\n'.join(p.text for p in doc.paragraphs)
        self.assertIn('B｜TWD', body)
        self.assertIn('200.00−210.00＝-10.00', body)
        self.assertIn('內部第 3 列', body)
        self.assertIn('尚有待確認交易', body)
        data = json.loads((out / 'finance-result.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data['counts']), 6)
        self.assertEqual(sum(r['reference'] == 'DUP' for r in data['results']), 2)
        self.assertEqual([r['difference'] for r in data['results'] if r['reference'] == 'B'], ['-10.00'])
        self.assertFalse(data['complete'])
        wb = load_workbook(out / '銀行對帳結果.xlsx', data_only=True)
        self.assertEqual(wb.sheetnames[0], '對帳摘要')
        rows = list(wb['對帳摘要'].values)
        self.assertTrue(any('疑似重複紀錄' in str(row) and '2' in str(row) for row in rows))
        self.assertTrue(data['artifact_checks']['content_reopened'])
        self.assertFalse(data['artifact_checks']['native_office_opened'])

    def test_publish_permission_failure_leaves_no_partial_success(self):
        quickstart = ROOT / 'examples/quickstart'
        for skill in ['legal-reviewer', 'finance-assistant']:
            with self.subTest(skill=skill):
                script = ROOT / '.agents/skills' / skill / 'scripts/run.py'
                sys.path.insert(0, str(script.parent))
                self.addCleanup(lambda: sys.path.pop(0))
                spec = importlib.util.spec_from_file_location(skill.replace('-', '_') + '_quality', script)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                folder = self.work / skill
                folder.mkdir()
                out = folder / 'out'
                if skill == 'legal-reviewer':
                    data = json.loads((ROOT / 'examples/legal-reviewer/input.json').read_text(encoding='utf-8'))
                    data['source']['path'] = str(quickstart / '模擬服務合約_甲方審查.docx')
                    source = folder / 'input.json'
                    source.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
                    execute = lambda: module.run(source, out)
                else:
                    data = {'mode': 'reconcile', 'source': str(quickstart / '模擬公司內部帳務.csv'),
                            'other': str(quickstart / '模擬銀行交易明細.csv'), 'simulation': True}
                    execute = lambda: module.execute(data, out, folder)
                original_rename = Path.rename
                calls = []
                def fail_second(source, target):
                    calls.append(target)
                    if len(calls) == 2:
                        raise PermissionError('模擬第二成品被系統鎖定')
                    return original_rename(source, target)
                with patch.object(Path, 'rename', new=fail_second):
                    with self.assertRaises(PermissionError):
                        execute()
                self.assertFalse(list(out.glob('*')), '產檔中途失敗不可留下單檔冒充完整成功')


if __name__ == '__main__':
    unittest.main()
