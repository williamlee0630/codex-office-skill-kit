from pathlib import Path
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from email.message import EmailMessage

ROOT = Path(__file__).resolve().parents[1]
TEMP = ROOT / 'tests/.tmp'
TEMP.mkdir(parents=True, exist_ok=True)


def execute(name, source, output, *extra):
    script = ROOT / '.agents/skills' / name / 'scripts/run.py'
    return subprocess.run([sys.executable, '-X', 'utf8', str(script), '--input', str(source),
                           '--output', str(output), *extra], capture_output=True, text=True,
                          encoding='utf-8', cwd=ROOT)


class InformationTests(unittest.TestCase):
    def test_attached_message_is_not_treated_as_main_mail_body(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            folder = Path(temp)
            mail = EmailMessage()
            mail['From'] = 'notice@example.invalid'
            mail['Subject'] = '僅供參考的公告'
            mail.set_content('僅供參考，不需要執行。')
            attached = EmailMessage()
            attached['Subject'] = '附件內另一封信'
            attached.set_content('請提交設備清單。期限：2026-10-24。')
            mail.add_attachment(attached, filename='attached-message.eml')
            source = folder / 'mail.eml'
            source.write_bytes(mail.as_bytes())
            result = execute('email-assistant', source, folder / 'output', '--as-of', '2026-10-24')
            self.assertEqual(result.returncode, 0, result.stderr)
            evidence = json.loads((folder / 'output/evidence.json').read_text(encoding='utf-8'))
            self.assertEqual(evidence['messages'][0]['actions'], ['僅供參考'])
            self.assertEqual(evidence['messages'][0]['deadline'], '待確認')
            self.assertNotIn('設備清單', (folder / 'output/daily-summary.md').read_text(encoding='utf-8'))

    def test_research_preserves_local_source_named_like_report(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            folder = Path(temp)
            original = '原始研究資料應保留。'
            source = folder / 'research-report.md'
            source.write_text(original, encoding='utf-8')
            data = {'question': '核對', 'sources': [{'id': 'S1', 'path': source.name}]}
            config = folder / 'input.json'
            config.write_text(json.dumps(data), encoding='utf-8')
            result = execute('research-assistant', config, folder)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_text(encoding='utf-8'), original)
    def test_email_refuses_to_overwrite_input_evidence(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            source = Path(temp) / 'evidence.json'
            original = json.dumps({'messages': [{'body': '應完整保留的原始郵件'}]})
            source.write_text(original, encoding='utf-8')
            result = execute('email-assistant', source, Path(temp))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_text(encoding='utf-8'), original)
    def test_email_preserves_priority_reason_without_new_commitments(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            source = Path(temp) / 'input.json'
            source.write_text(json.dumps({'messages': [{'body': '請回覆報價確認。', 'actions': ['需回覆'],
                                                       'priority': '中', 'priority_reason': '期限尚未提供，先確認需求。'}]}), encoding='utf-8')
            result = execute('email-assistant', source, Path(temp) / 'out')
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = (Path(temp) / 'out/daily-summary.md').read_text(encoding='utf-8')
            drafts = (Path(temp) / 'out/drafts.md').read_text(encoding='utf-8')
            self.assertIn('期限尚未提供，先確認需求。', summary)
            self.assertNotIn('確認後再回覆', drafts)
            self.assertNotIn('再與您回覆', drafts)

    def test_email_real_eml_decoded_drafts_only(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            output = Path(temp)
            result = execute('email-assistant', ROOT / 'examples/email-assistant/inbox.eml', output,
                             '--as-of', '2026-10-23')
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (output / 'daily-summary.md').read_text(encoding='utf-8')
            self.assertIn('年度課程報價確認', text)
            self.assertIn('2026-10-26', text)
            drafts = (output / 'drafts.md').read_text(encoding='utf-8')
            for tone in ['正式', '友善', '簡潔']:
                self.assertIn(tone, drafts)
            self.assertIn('尚未寄送', drafts)
            self.assertFalse(any(p.suffix == '.sent' for p in output.iterdir()))

    def test_email_incomplete_preserves_unknown(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            source = Path(temp) / 'input.json'
            source.write_text(json.dumps({'messages': [{'body': '請回覆確認明細。'}]}), encoding='utf-8')
            result = execute('email-assistant', source, Path(temp) / 'out')
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (Path(temp) / 'out/daily-summary.md').read_text(encoding='utf-8')
            self.assertIn('待確認', text)
            self.assertIn('需回覆', text)

    def test_email_wrong_format_and_invalid_date_rejected(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            source = Path(temp) / 'bad.exe'
            source.write_bytes(b'not mail')
            result = execute('email-assistant', source, Path(temp) / 'out')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('不支援', result.stderr)
            source = ROOT / 'examples/email-assistant/inbox.eml'
            result = execute('email-assistant', source, Path(temp) / 'out', '--as-of', '2026-99-23')
            self.assertNotEqual(result.returncode, 0)

    def test_research_local_sources_traceable(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            result = execute('research-assistant', ROOT / 'examples/research-assistant/input.json', temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (Path(temp) / 'research-report.md').read_text(encoding='utf-8')
            self.assertIn('離線', text)
            self.assertIn('S1', text)
            self.assertIn('模擬', text)
            self.assertIn('2026-10-23', text)
            with (Path(temp) / 'sources.csv').open(encoding='utf-8-sig', newline='') as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 2)

    def test_research_missing_fields_outputs_gaps(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            source = Path(temp) / 'input.json'
            source.write_text(json.dumps({'question': '要不要改方案？', 'sources': []}), encoding='utf-8')
            result = execute('research-assistant', source, Path(temp) / 'out')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('無足夠來源', (Path(temp) / 'out/research-report.md').read_text(encoding='utf-8'))

    def test_research_rejects_dangling_citations_and_wrong_format(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            source = Path(temp) / 'bad.json'
            source.write_text(json.dumps({'question': '比較', 'sources': [],
                                         'claims': [{'text': '假的結論', 'source_ids': ['GHOST']}]}), encoding='utf-8')
            result = execute('research-assistant', source, Path(temp) / 'out')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('來源', result.stderr)
            source = Path(temp) / 'bad.csv'
            source.write_text('question\n比較\n', encoding='utf-8')
            self.assertNotEqual(execute('research-assistant', source, Path(temp) / 'out').returncode, 0)

    def test_research_does_not_claim_uncached_web_fetch(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as temp:
            source = Path(temp) / 'bad.json'
            source.write_text(json.dumps({'question': '比較', 'sources': [{'id': 'S1', 'url': 'https://example.invalid'}]}), encoding='utf-8')
            result = execute('research-assistant', source, Path(temp) / 'out')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('本機', result.stderr)


if __name__ == '__main__':
    unittest.main()
