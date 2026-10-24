from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EmptyPdfTests(unittest.TestCase):
    def test_empty_receipt_pdf_does_not_claim_extracted_text(self):
        from pypdf import PdfWriter
        temp_root = ROOT / 'tests/.tmp'
        temp_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as temp:
            folder = Path(temp)
            writer = PdfWriter()
            writer.add_blank_page(width=400, height=600)
            writer.write(folder / 'blank.pdf')
            result = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / '.agents/skills/receipt-organizer/scripts/run.py'),
                                     '--input', str(folder / 'blank.pdf'), '--output', str(folder / 'output')],
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (folder / 'output/review-required.md').read_text(encoding='utf-8')
            self.assertIn('未擷取到文字', text)
            self.assertNotIn('已擷取 PDF 文字', text)


if __name__ == '__main__':
    unittest.main()
