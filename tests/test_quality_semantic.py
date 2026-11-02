"""v1.3.0 semantic output contracts; prepared evidence is not agent E2E."""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SemanticQualityTests(unittest.TestCase):
    def setUp(self):
        temp_root = ROOT / 'tests/.tmp'
        temp_root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=temp_root)
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def execute(self, skill, data):
        source = self.work / 'input.json'
        source.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        out = self.work / skill
        result = subprocess.run([sys.executable, str(ROOT / '.agents/skills' / skill / 'scripts/run.py'),
                                 '--input', str(source), '--output', str(out)], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        return out

    def test_email_preserves_requested_time_and_parallel_actions(self):
        out = self.execute('email-assistant', {'as_of': '2026-10-23', 'messages': [{
            'sender': '模擬客戶', 'subject': '活動初稿', 'date': '2026-10-22T10:00:00+08:00',
            'body': '請回覆並請提供初稿，時間尚未承諾。', 'source': 'source.md 郵件一',
            'deadline': '2026-10-27T12:00:00+08:00', 'deadline_status': 'requested',
            'actions': ['需回覆', '需執行'], 'reply_points': ['初稿時間仍待內部確認。']}]})
        summary = (out / 'daily-summary.md').read_text(encoding='utf-8')
        self.assertIn('需回覆 1', summary)
        self.assertIn('需執行 1', summary)
        self.assertIn('對方要求，尚未承諾', summary)
        self.assertIn('2026-10-27T12:00:00+08:00', summary)
        drafts = (out / 'drafts.md').read_text(encoding='utf-8')
        self.assertEqual(drafts.count('初稿時間仍待內部確認。'), 3)
        self.assertGreaterEqual(drafts.count('活動初稿'), 6)

    def test_document_has_version_approval_and_preserves_two_versions(self):
        data = json.loads((ROOT / 'examples/document-writer/input.json').read_text(encoding='utf-8-sig'))
        data['document_version'] = '草案 v0.1'
        data['approval_status'] = '待主管核准'
        out = self.execute('document-writer', data)
        from docx import Document
        for version in ('formal', 'concise'):
            body = '\n'.join(p.text for p in Document(out / f'document-{version}.docx').paragraphs)
            self.assertIn('草案 v0.1', body)
            self.assertIn('待主管核准', body)
            for fact in data['facts']:
                self.assertIn(fact['text'], body)

    def test_email_deadline_comparison_uses_taipei_day_without_changing_source(self):
        out = self.execute('email-assistant', {'as_of': '2026-10-22', 'messages': [{
            'sender': '模擬', 'subject': '跨時區期限', 'date': '2026-10-22T08:00:00Z',
            'body': '請回覆', 'deadline': '2026-10-22T20:00:00Z', 'deadline_status': 'requested',
            'source': '模擬跨時區原信'}]})
        message = json.loads((out / 'evidence.json').read_text(encoding='utf-8'))['messages'][0]
        self.assertEqual(message['priority'], '中')
        self.assertEqual(message['deadline'], '2026-10-22T20:00:00Z')

    def test_ideas_keep_required_outputs_and_defer_unselected_plan(self):
        data = json.loads((ROOT / 'examples/idea-generator/input.json').read_text(encoding='utf-8-sig'))
        data['selected_id'] = None
        data['plan'] = []
        for idea in data['ideas']:
            idea['staffing'] = '兩位籌辦人員；主持與材料各一人'
            idea['cost_assumptions'] = '以20人及自有場地為估算假設；人數待確認'
            idea['risks'] = ['參與人數不足，先做意願調查']
        out = self.execute('idea-generator', data)
        self.assertFalse((out / 'selected-plan.md').exists())
        self.assertFalse((out / 'comparison.xlsx').exists())
        self.assertIn(data['validation_plan'], (out / 'ideas.md').read_text(encoding='utf-8'))
        with (out / 'comparison.csv').open(encoding='utf-8-sig', newline='') as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[0]['人力'], '兩位籌辦人員；主持與材料各一人')
        self.assertIn('20人', rows[0]['估算假設'])
        self.assertIn('人數不足', rows[0]['主要風險'])

    def test_research_conclusion_and_comparison_preserve_source_ids(self):
        source = self.work / 'plan-a.md'
        source.write_text('方案A提供24名額，每人1200元。', encoding='utf-8')
        (self.work / 'plan-b.md').write_text('方案B最多20名額，每人950元。', encoding='utf-8')
        out = self.execute('research-assistant', {'question': '24人訓練選擇', 'as_of': '2026-10-23',
            'conclusion': '先向A確認正式條件；B容量不足。',
            'sources': [{'id': 'S1', 'path': 'plan-a.md', 'published_at': None},
                        {'id': 'S2', 'path': 'plan-b.md', 'published_at': None}],
            'claims': [{'text': 'A提供24名額', 'kind': 'fact', 'source_ids': ['S1'],
                        'excerpts': {'S1': '方案A提供24名額'}}],
            'comparison_table': [{'dimension': '名額', 'a': '24人 [S1]', 'b': '20人，少4人 [S2]', 'source_ids': ['S1', 'S2']}],
            'gaps': ['含稅與取消條款待確認']})
        body = (out / 'research-report.md').read_text(encoding='utf-8')
        self.assertLess(body.index('先向A確認'), body.index('## 調查方向'))
        self.assertIn('| 名額 | 24人 [S1] | 20人，少4人 [S2] |', body)
        self.assertIn('方案A提供24名額', body)


if __name__ == '__main__':
    unittest.main()
