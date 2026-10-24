"""重建原創模擬收據 PNG / PDF；不含真實商家、個資或報帳憑證。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas


def main():
    folder = Path(__file__).resolve().parent
    lines = ['SIMULATED RECEIPT', 'NOT VALID FOR CLAIMS', '', 'SIMULATED CAFE',
             'DATE 2026-10-01', '', 'LUNCH                 120.00', '',
             'TOTAL TWD 120.00', '', 'ORIGINAL TRAINING DATA', 'NOT A REAL TRANSACTION']
    image = Image.new('RGB', (800, 1100), '#FDFCF8')
    draw = ImageDraw.Draw(image)
    font_path = Path('C:/Windows/Fonts/consola.ttf')
    font = ImageFont.truetype(str(font_path), 31) if font_path.exists() else ImageFont.load_default(size=31)
    for index, line in enumerate(lines):
        draw.text((60, 60 + index * 73), line, fill='#182925', font=font)
    image.save(folder / 'simulated-receipt.png')
    pdf = canvas.Canvas(str(folder / 'simulated-receipt.pdf'), pagesize=(400, 550))
    pdf.setTitle('SIMULATED RECEIPT - NOT VALID FOR CLAIMS')
    pdf.setAuthor('AI Office Skill Kit - simulated training data')
    pdf.setFont('Courier', 14)
    for index, line in enumerate(lines):
        pdf.drawString(30, 510 - index * 35, line)
    pdf.save()
    print('已建立模擬收據 PNG 與文字型 PDF。')


if __name__ == '__main__':
    main()
