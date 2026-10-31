"""法務：以原件驗證語意審查，不把關鍵字掃描當成法律判斷。"""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / '.agents/skills/legal-reviewer'
SCRIPT = SKILL / 'scripts/run.py'
TOPICS = ['parties_purpose', 'term_renewal', 'payment', 'liability', 'confidentiality_privacy', 'ip', 'termination', 'law_disputes', 'special']


class LegalTests(unittest.TestCase):
    def setUp(self):
        (ROOT / 'work').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / 'work')
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)

    def invoke(self, data, out='out', script=SCRIPT):
        inp = self.path / 'input.json'
        inp.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        return subprocess.run([sys.executable, str(script), '--input', str(inp), '--output', str(self.path / out)], capture_output=True, text=True, encoding='utf-8')

    def data(self):
        text = '教學模擬資料：甲乙合作。\n付款於驗收後三十日內完成。\n雙方得提前三十日終止。'
        return {'document_name': '模擬合作文件', 'document_type': '合作協議', 'perspective': '甲方', 'jurisdiction': None,
                'source': {'text': text}, 'checked_locations': ['L1', 'L2', 'L3'],
                'review_topics': [{'topic': t, 'status': 'not_applicable', 'analysis': '本次文件未涉及此項；需依合作範圍確認是否另訂附件。', 'citations': []} for t in TOPICS],
                'findings': [], 'legal_check': {'status': 'unverified', 'reason': '法域未提供，未取得可核實現行法規。'}, 'legal_sources': [], 'questions': ['請確認適用法域及完整附件。']}

    def test_normal_review_creates_real_artifacts_and_unknown_jurisdiction(self):
        data = self.data()
        data['review_topics'][2] = {'topic': 'payment', 'status': 'present', 'analysis': '付款須驗收後三十日，期限明確，但需確認驗收標準。', 'citations': [{'location': 'L2', 'quote': '付款於驗收後三十日內完成。'}]}
        proc = self.invoke(data)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        from docx import Document
        from openpyxl import load_workbook
        out = self.path / 'out'
        report = '\n'.join(p.text for p in Document(out / '合約審查報告.docx').paragraphs)
        self.assertIn('法域待確認', report)
        self.assertIn('未完成最新法規查證', report)
        self.assertIn('付款於驗收後三十日內完成。', report)
        self.assertIn('條款檢查', load_workbook(out / '合約風險清單.xlsx').sheetnames)
        self.assertTrue((out / '條款修訂建議.md').is_file())
        audit = json.loads((out / 'audit.json').read_text(encoding='utf-8'))
        self.assertFalse(audit['network_used'])
        self.assertEqual(audit['source']['blocks'][1]['text'], '付款於驗收後三十日內完成。')

    def test_quote_mismatch_rejected_before_any_artifact(self):
        data = self.data()
        data['review_topics'][2] = {'topic': 'payment', 'status': 'present', 'analysis': '付款不合理。', 'citations': [{'location': 'L2', 'quote': '立即支付一百萬元'}]}
        proc = self.invoke(data)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('原文', proc.stderr)
        self.assertFalse((self.path / 'out/合約審查報告.docx').exists())

    def test_missing_clause_requires_finding_and_full_source_review(self):
        data = self.data()
        data['review_topics'][7]['status'] = 'missing'
        self.assertNotEqual(self.invoke(data).returncode, 0)
        data['findings'] = [{'id': 'R1', 'topic': 'law_disputes', 'missing_clause': True, 'citations': [], 'issue': '未訂定準據法與爭議解決。', 'impact': '爭議發生時增加管轄及程序成本。', 'level': '中', 'reason': '合作跨境範圍尚未明確。', 'action': '協商適用法及法院。', 'professional_confirmation': True, 'draft_terms': '本協議準據法為【待雙方確認法域】法律；爭議先協商三十日，未成時由【待確認法院或仲裁機構】處理。', 'revision_reason': '降低爭議程序不確定性。', 'questions': ['合作是否跨境？'], 'legal_basis_status': 'unverified', 'legal_source_ids': []}]
        self.assertEqual(self.invoke(data).returncode, 0)
        data['checked_locations'] = ['L1']
        proc = self.invoke(data, 'incomplete')
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('完整', proc.stderr)

    def test_raw_file_read_and_preserved_and_stale_output_refused(self):
        data = self.data()
        raw = self.path / 'contract.md'
        raw.write_text(data['source']['text'], encoding='utf-8')
        before = raw.read_bytes()
        data['source'] = {'path': 'contract.md'}
        self.assertEqual(self.invoke(data).returncode, 0)
        old = (self.path / 'out/條款修訂建議.md').read_bytes()
        self.assertNotEqual(self.invoke(data).returncode, 0)
        self.assertEqual(old, (self.path / 'out/條款修訂建議.md').read_bytes())
        self.assertEqual(before, raw.read_bytes())

    def test_missing_topics_and_unverified_claimed_law_rejected(self):
        data = self.data()
        data['review_topics'].pop()
        self.assertNotEqual(self.invoke(data).returncode, 0)

    def test_quote_at_wrong_location_and_changed_original_rejected(self):
        data = self.data()
        data['review_topics'][2] = {'topic': 'payment', 'status': 'present', 'analysis': '付款期限明確。', 'citations': [{'location': 'L1', 'quote': '付款於驗收後三十日內完成。'}]}
        self.assertNotEqual(self.invoke(data).returncode, 0)
        raw = self.path / 'original.txt'
        raw.write_text('原件已改為六十日付款。', encoding='utf-8')
        data['source'] = {'path': 'original.txt'}
        data['checked_locations'] = ['L1']
        self.assertNotEqual(self.invoke(data, 'changed').returncode, 0)

    def test_law_snapshots_metadata_and_mismatch(self):
        data = self.data()
        data['jurisdiction'] = '教學虛構法域'
        raw = self.path / 'official-snapshot.txt'
        raw.write_text('教學模擬資料：本段是來源比對測試文字，不是真實法律。', encoding='utf-8')
        data['legal_sources'] = [{'id': 'LAW1', 'law_name': '教學模擬規範（非真實法律）', 'article': '模擬第一條', 'jurisdiction': '教學虛構法域', 'authority': '虛構機關（僅測資料流程）', 'url': 'https://example.invalid/training-law', 'checked_at': '2026-10-30', 'path': raw.name, 'quote': '本段是來源比對測試文字，不是真實法律。'}]
        data['legal_check'] = {'status': 'checked', 'as_of': '2026-10-30'}
        proc = self.invoke(data)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        audit = json.loads((self.path / 'out/audit.json').read_text(encoding='utf-8'))
        self.assertIn('本機快照', audit['legal_sources'][0]['verification'])
        self.assertIn('sha256', audit['legal_sources'][0])
        data['legal_sources'][0]['quote'] = '不存在的法條'
        self.assertNotEqual(self.invoke(data, 'bad-law').returncode, 0)
        data['legal_sources'][0]['quote'] = '本段是來源比對測試文字，不是真實法律。'
        data['jurisdiction'] = None
        self.assertNotEqual(self.invoke(data, 'unknown-law').returncode, 0)
        data = self.data()
        data['legal_check'] = {'status': 'checked', 'as_of': '2026-10-31'}
        self.assertNotEqual(self.invoke(data).returncode, 0)

    def test_docx_table_order_pdf_and_scan_limit(self):
        from docx import Document
        from reportlab.pdfgen import canvas
        doc = Document()
        doc.add_paragraph('Training contract')
        doc.add_table(rows=1, cols=1).cell(0, 0).text = 'Pay within thirty days.'
        doc.add_paragraph('End of contract')
        doc.save(self.path / 'raw.docx')
        for filename, contains in [('raw.docx', 'Pay within thirty days.'), ('raw.pdf', 'Payment due in thirty days.')]:
            if filename.endswith('.pdf'):
                c = canvas.Canvas(str(self.path / filename))
                c.drawString(50, 750, contains)
                c.save()
            proc = subprocess.run([sys.executable, str(SCRIPT), '--extract', str(self.path / filename), '--output', str(self.path / (filename + '-out'))], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(proc.returncode, 0, proc.stderr)
            extracted = json.loads((self.path / (filename + '-out/source-index.json')).read_text(encoding='utf-8'))
            self.assertIn(contains, '\n'.join(b['text'] for b in extracted['blocks']))
        c = canvas.Canvas(str(self.path / 'scan.pdf'))
        c.showPage()
        c.save()
        proc = subprocess.run([sys.executable, str(SCRIPT), '--extract', str(self.path / 'scan.pdf'), '--output', str(self.path / 'scan-out')], capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('OCR', proc.stderr)

    def test_complete_bundled_risky_normal_and_standalone(self):
        copied = self.path / 'legal-reviewer'
        shutil.copytree(SKILL, copied)
        for sample in ['input.json', 'normal-input.json', 'pdf-input.json']:
            proc = subprocess.run([sys.executable, str(copied / 'scripts/run.py'), '--input', str(copied / 'references/demo' / sample), '--output', str(self.path / sample)], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(proc.returncode, 0, proc.stderr)
            audit = json.loads((self.path / sample / 'audit.json').read_text(encoding='utf-8'))
            self.assertEqual(len(audit['review_topics']), 9)
            if sample == 'input.json':
                self.assertTrue(any(f['level'] == '高' for f in audit['findings']))
                self.assertEqual(sum(f['level'] == '高' for f in audit['findings']), 5)
                self.assertEqual(sum(f['level'] == '中' for f in audit['findings']), 4)
                from docx import Document
                from openpyxl import load_workbook
                self.assertIn('教學模擬資料', Document(self.path / sample / '合約審查報告.docx').paragraphs[0].text)
                self.assertIn('教學模擬資料', load_workbook(self.path / sample / '合約風險清單.xlsx').active['A1'].value)
            if sample == 'normal-input.json':
                self.assertFalse(any(f['level'] == '高' for f in audit['findings']))


if __name__ == '__main__':
    unittest.main()
