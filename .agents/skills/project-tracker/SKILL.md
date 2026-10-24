---
name: project-tracker
description: 整合同一專案的待辦、會議及更新，依明確基準日辨識完成、進行中、逾期與受阻工作，保留已確認決策變更並輸出 Markdown、CSV、Excel。適用跨日期專案追蹤；單場逐字稿整理使用 meeting-assistant。
---

# 專案進度追蹤助理

適用：同一專案跨日期的進度整合。先確認專案範圍與 as_of；不同專案不得混為同一工作。未指定基準日時先確認。

## 工作流程

1. 讀取原始 TXT、Markdown 或 DOCX。需擷取文字時執行 `python scripts/_office.py extract "<原始檔>" --output "<文字檔>"`；不可讀就說明限制，不猜內容。
2. 決策及狀態以有依據的已確認更新為準；新提議不能覆寫已確認決策。同日矛盾的已確認更新標待確認，不依檔名、排列順序或語氣猜測。缺少負責人及期限保持 null。逾期只以明確期限與基準日計算。
3. 讀 [輸入契約與驗收](references/workflow.md)，由 Codex 依原始資料建立有來源 JSON；核對語意後再交腳本驗證欄位及產檔。
4. 執行 `python scripts/run.py --input "<證據 JSON>" --output "<指定輸出資料夾>"`。腳本不進行語意理解、不連網、不執行外部發布。
5. 開啟 Markdown、CSV 與 XLSX 成果，核對工作狀態、來源、日期與未知欄位，確認 Excel 欄位與換行可讀；程式測試與 Codex 觸發驗收分開回報。

## 缺漏與範例

缺漏可選欄位用 null，呈現「待確認」。缺必要來源或日期基準時先補資料；不得造人名、金額、期限與績效。

獨立練習：先讀 [模擬原始資料](references/source.md)，由 Codex 整理，再參考 [完整證據範例](references/example.json) 比對。所有範例皆為模擬。

提示詞：「請用 $project-tracker 依我指定的基準日整合專案紀錄，產出進度表、風險及 Excel。」

產物：progress.md、progress.csv、progress.xlsx、evidence.json（含 resolved_tasks、resolved_decisions）。
