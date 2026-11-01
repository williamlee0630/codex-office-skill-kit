"""重建學員附件；來源資料原樣保留，僅改名稱／CSV 編碼／文件容器。"""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def prepare(root=ROOT):
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    root = Path(root)
    destination = root / 'examples/quickstart'
    destination.mkdir(parents=True, exist_ok=True)
    mapping = {
        'data-analyst/sales.csv': '模擬銷售資料.csv',
        'finance-assistant/reconciliation/internal.csv': '模擬公司內部帳務.csv',
        'finance-assistant/reconciliation/bank.csv': '模擬銀行交易明細.csv',
        'legal-reviewer/風險服務合約.docx': '模擬服務合約_甲方審查.docx',
    }
    manifest = []
    for source, target in mapping.items():
        original = root / 'examples' / source
        path = destination / target
        if path.suffix == '.csv':
            path.write_text(original.read_text(encoding='utf-8-sig'), encoding='utf-8-sig', newline='')
        else:
            shutil.copyfile(original, path)
        manifest.append({'file': target, 'source': 'examples/' + source, 'conversion': 'UTF-8 BOM' if path.suffix == '.csv' else '原檔複製'})
    for letter in ['A', 'B']:
        source = f'research-assistant/sources/plan-{letter.lower()}.md'
        text = (root / 'examples' / source).read_text(encoding='utf-8')
        name = f'模擬員工訓練方案{letter}.docx'
        doc = Document()
        for section in doc.sections:
            section.top_margin = section.bottom_margin = Cm(2.5)
            section.left_margin = section.right_margin = Cm(2.5)
        style = doc.styles['Normal']
        style.font.name = 'Microsoft JhengHei'
        style.font.size = Pt(12)
        style.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), 'Microsoft JhengHei')
        style.paragraph_format.space_after = Pt(10)
        style.paragraph_format.line_spacing = 1.3
        for line in text.splitlines():
            if line.startswith('# '):
                doc.add_heading(line[2:], level=0)
            elif line.strip():
                doc.add_paragraph(line)
        doc.add_paragraph('僅供教學模擬，非真實供應商報價。內容沿用原方案文件，未新增費用或服務條件。')
        doc.core_properties.author = '星嶼辦公研究室（教學模擬）'
        doc.core_properties.title = f'教學模擬員工訓練方案 {letter}'
        doc.save(destination / name)
        manifest.append({'file': name, 'source': 'examples/' + source, 'conversion': '原文轉為 Word；附教學用途說明'})
    receipt = destination / '模擬文具收據.png'
    if not receipt.is_file():
        raise ValueError('請先保存已逐項核對的原創繁中收據 PNG，不自動生成或代用其他收據。')
    manifest.append({'file': receipt.name, 'source': '原創 imagegen 模擬照片，2026-11-01；人工逐欄核對', 'conversion': '日期 2026-10-23；240+60+70=370 TWD；無真實個資'})
    for item in manifest:
        data = (destination / item['file']).read_bytes()
        item.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), simulation=True)
    (destination / 'manifest.json').write_text(json.dumps({'teaching_only': True, 'files': manifest}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'已準備 {len(manifest)} 份可獨立下載的教學附件。')


if __name__ == '__main__':
    prepare()
