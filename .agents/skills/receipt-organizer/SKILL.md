---
name: receipt-organizer
description: 整理使用者提供的收據 PDF、圖片及可解析 JSON／CSV。先檢查文字抽取與 OCR 工具，保留原始證據，再依確認欄位產生 Excel 報帳明細、分類、各幣合計與疑似重複清單。適用收據整理，不適用於猜測模糊金額、自動報稅、換匯或自動提交報帳。
---

# 發票與收據整理助理

先保存辨識依據，再整理金額。看不清楚的欄位保持未知，疑似重複不直接刪除，不把不同幣別相加。

## 啟動與不適用情境

- 自然語言：「幫我整理這批收據，標出看不清楚和可能重複的資料，產出報帳 Excel。」
- 明確指定：「使用 $receipt-organizer 整理這份收據 JSON，依幣別合計。」
- 本技能不提交報帳、不判定可抵稅、不換匯。不確定用途或類別須待人工確認。

## PDF／影像流程

1. 先執行本技能 `scripts/run.py`，腳本檢查 pypdf、Pillow、tesseract、pdftoppm 是否可用。文字型 PDF 可抽取原文，圖片只檢查格式與尺寸；此腳本不自動執行 OCR。
2. 原始檔複製至輸出 `originals/`，SHA-256、工具清單、PDF 頁碼文字保存在 `extraction-evidence.json`。
3. Codex 使用實際可用的視覺工具檢視影像，或請人工逐欄轉錄。若沒有視覺／OCR 能力，清楚說明限制，不假裝已辨識。
4. 填妥 `transcription-template.json`。日期、店家、品項、金額、幣別、類別逐一核對；證據填來源頁碼／區域與可辨識原文。模糊欄位填 null，分類由 Codex 依品項或使用者確認，不依店名武斷推測。
5. 保留原始影像和辨識證據，再以確認後 JSON 為輸入，產生報帳 Excel。PDF／圖片第一次處理不會產生虛假的報帳明細。

## JSON／CSV 流程

1. 先核對來源及資料日期。每筆使用唯一 id，未提供則以內部列號識別，不補造外部單據號碼。
2. 執行腳本，讀取 `receipts-summary.json` 的缺漏、格式與疑似重複標記。
3. 核對各幣含重複合計與暫排除疑似重複合計。兩者都是檢核用結果，是否排除由人決定，所有明細均保留。
4. 逐筆與原始收據比對。沒有有效金額或幣別的記錄不納入合計，必須在人工確認清單中顯示。
5. 檢查 Excel 畫面、欄位與單位。靜態結果修改來源後需重新執行，不能宣稱自動連動。

## 輸入契約

```json
{
  "simulation": true,
  "source": "模擬收據轉錄，2026-10-01",
  "receipts": [{
    "id": "R1", "date": "2026-10-01", "vendor": "模擬餐館",
    "items": "午餐", "amount": "120.00", "currency": "TWD",
    "category": "餐飲", "evidence": "模擬收據第 1 頁下方：總計 TWD 120"
  }]
}
```

CSV 欄位為 `id,date,vendor,items,amount,currency,category,evidence`，來源名稱預設為 CSV 檔名。空欄保留未知。JSON 必須提供 `source`、非空 `receipts`；`simulation` 只在確實為模擬資料時設為 true。

日期使用 YYYY-MM-DD；幣別為三碼大寫代碼。金額以十進位計算，不接受 NaN、無限值、負值或超過兩位小數。退款及其他精度的幣別須人工另行處理，腳本不擅自四捨五入。缺漏值不補零。

## 執行與輸出

```powershell
python scripts/run.py --input "C:\資料\模擬收據.png" --output "C:\資料\辨識輸出" --simulation
python scripts/run.py --input "C:\資料\receipts.json" --output "C:\資料\報帳輸出"
```

在本技能資料夾執行。需要 Python、openpyxl；PDF 加 pypdf，影像加 Pillow。每次演練使用新的輸出資料夾，避免誤用上次報表。PNG／PDF／CSV 的模擬演練加 `--simulation` 明確標示，不根據檔名猜測。

- PDF／影像：`extraction-evidence.json`、`transcription-template.json`、`review-required.md`、`originals/`。
- JSON／CSV：`receipts.xlsx`、`receipts-summary.json`、`receipts-report.md`、`originals/`。Excel 有各幣統計、分類統計、報帳明細；外來公式字串以安全文字保存。
- 以相同日期、店家、品項、金額、幣別標記疑似重複，不能據此認定重複報帳。辨識證據未提供時列待確認。

詳細流程與驗收見 [references/workflow.md](references/workflow.md)。工具包 `examples/receipt-organizer/` 提供正常 `receipts.json`／`receipts.csv`、缺漏 `incomplete.json`、錯誤 `invalid.json`、實際模擬 `simulated-receipt.png` 與 `simulated-receipt.pdf`；預期結果在 `expected.md`。單獨安裝本技能即可使用相同契約的資料。
