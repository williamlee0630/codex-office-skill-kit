---
name: document-writer
description: 依原始素材撰寫或改寫企劃書、提案、商務信函、工作報告，修正文法、段落與專業用語，保留事實並提供正式與精簡 Markdown、DOCX。適用商務寫作；特定會議紀錄及週報使用對應技能。
---

# 商務文件撰寫助理

適用：商務文件新寫與既有文件改寫。先辨識文件類型、目的、讀者與事實；會議分類或週報期間彙整使用對應技能。

## 工作流程

1. 讀取原始 TXT、Markdown 或 DOCX。需擷取文字時執行 `python scripts/_office.py extract "<原始檔>" --output "<文字檔>"`；不可讀就說明限制，不猜內容。
2. 先把可證實的原文列成 facts，再調整段落與語氣。修正文法不改變承諾、金額、日期、責任及不確定性。每段改寫列 fact_ids；新推論與建議明寫『建議』或『待確認』，不加入原始事實。精簡版保留條件與重要事實。若另需易讀版，可由 Codex 用同一 facts 撰寫附加 Markdown。
3. 讀 [輸入契約與驗收](references/workflow.md)，由 Codex 依原始資料建立有來源 JSON；核對語意後再交腳本驗證欄位及產檔。
4. 執行 `python scripts/run.py --input "<證據 JSON>" --output "<指定輸出資料夾>"`。腳本不進行語意理解、不連網、不執行外部發布。
5. 開啟成果核對來源、日期與未知欄位。DOCX 檢查可開啟及畫面版面；程式測試與 Codex 觸發驗收分開回報。

## 缺漏與範例

缺漏可選欄位用 null，呈現「待確認」。缺必要來源或日期基準時先補資料；不得造人名、金額、期限與績效。

獨立練習：先讀 [模擬原始資料](references/source.md)，由 Codex 整理，再參考 [完整證據範例](references/example.json) 比對。所有範例皆為模擬。

提示詞：「請用 $document-writer 依原始素材撰寫正式版與精簡版提案，保留事實與待確認事項。」

產物：document-formal.md、document-concise.md、document-formal.docx、document-concise.docx、evidence.json。
