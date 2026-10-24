# 收據示範與預期結果（全部為模擬）

所有收據、店名、交易及清單均為原創模擬資料，不能用於真實報帳。來源日期 2026-10-01 至 2026-10-03。`simulated-receipt.png` 與 `simulated-receipt.pdf` 是同一張模擬收據的兩種格式，並非兩筆交易。

## 可解析資料練習

```powershell
python .agents/skills/receipt-organizer/scripts/run.py --input examples/receipt-organizer/receipts.json --output output/receipt-organizer
```

預期產生 `receipts.xlsx`、`receipts-summary.json`、`receipts-report.md` 與 `originals/` 原始資料副本。

- 保留 5 筆。R2 疑似重複於 R1，仍留在 Excel。
- TWD 含疑似重複合計 690.00，暫排除合計 570.00；USD 含重複及排除合計均 12.50。不能相加成單一幣別總金額。
- R5 日期、店家、金額、幣別、類別未知，待人工確認，不當成零元。
- 分類合計：TWD 餐飲 240.00、辦公用品 450.00；USD 交通 12.50。分類合計明確包含疑似重複。
- `receipts.csv` 支援同樣的資料欄位與金額，來源依 CSV 檔名，不自動判定是否模擬。執行時加 `--simulation` 明確標示本次為模擬演練。
- `incomplete.json`：保留一筆待確認，無各幣金額合計，不捏造欄位。
- `invalid.json`：非零結束，指出 NaN 為錯誤金額，不產出貌似有效的報表。

## 原始影像／PDF 練習

```powershell
python .agents/skills/receipt-organizer/scripts/run.py --input examples/receipt-organizer/simulated-receipt.png --output output/receipt-image-review --simulation
python .agents/skills/receipt-organizer/scripts/run.py --input examples/receipt-organizer/simulated-receipt.pdf --output output/receipt-pdf-review --simulation
```

預期保留 originals、工具清單、SHA-256、PDF 可擷取原文與轉錄模板。PNG 不會自動辨識，`ocr_performed` 為 false，第一次不產報帳 Excel。PDF 能抽出英文原文，但仍需核對欄位。

影像／PDF 可見：SIMULATED RECEIPT / NOT VALID、SIMULATED CAFE、DATE 2026-10-01、LUNCH、TOTAL TWD 120.00。只有 R1 對應這張影像；其他記錄是清單演練資料，不得假稱已核對影像。若 Codex 具有可用視覺工具，請實際查看再轉錄；否則保留待人工確認。

觸發提示詞：

> 使用 $receipt-organizer 處理 examples/receipt-organizer/simulated-receipt.png。先檢查抽取工具並保留原始檔，再依實際可見內容建立有證據的轉錄 JSON。這是模擬資料，看不清楚就填 null，不要假裝做過 OCR。確認後產生 Excel，按幣別統計並標示未知欄位。

程式測試、Codex 視覺／語意觸發、Excel 原生畫面檢查要分別記錄。
