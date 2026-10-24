---
name: meeting-assistant
description: 將單場會議 TXT、Markdown 或 DOCX 筆記整理成正式會議紀錄，區分提議、討論中、已確認決議與待確認事項，擷取待辦、負責人和期限。適用會後整理；跨日期專案追蹤使用 project-tracker。
---

# 會議紀錄整理助理

適用：單場會議逐字稿及筆記。沒有原始紀錄時，先列待補資料。

## 工作流程

1. 讀取原始 TXT、Markdown 或 DOCX。需擷取文字時執行 `python scripts/_office.py extract "<原始檔>" --output "<文字檔>"`；不可讀就說明限制，不猜內容。
2. 閱讀發言上下文，辨別提出者與是否明確定案。沉默、『應該』或最新提議，都不是通過決議的依據。未寫明負責人與期限時留 null。會議日期與引文須可追溯。
3. 讀 [輸入契約與驗收](references/workflow.md)，由 Codex 依原始資料建立有來源 JSON；核對語意後再交腳本驗證欄位及產檔。
4. 執行 `python scripts/run.py --input "<證據 JSON>" --output "<指定輸出資料夾>"`。腳本不進行語意理解、不連網、不執行外部發布。
5. 開啟成果核對來源、日期與未知欄位。DOCX 檢查可開啟及畫面版面；程式測試與 Codex 觸發驗收分開回報。

## 缺漏與範例

缺漏可選欄位用 null，呈現「待確認」。缺必要來源或日期基準時先補資料；不得造人名、金額、期限與績效。

獨立練習：先讀 [模擬原始資料](references/source.md)，由 Codex 整理，再參考 [完整證據範例](references/example.json) 比對。所有範例皆為模擬。

提示詞：「請用 $meeting-assistant 整理我提供的會議記錄，區分已確認決議與提議並產出 Word。」

產物：minutes.md、minutes.docx、evidence.json。
