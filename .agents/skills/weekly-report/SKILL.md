---
name: weekly-report
description: 將指定一週的工作日誌整理為精簡與詳細週報，以 STAR 呈現有依據的工作成果、阻礙、下週計畫與主管協助，產生 Markdown、Word。適用週期性工作彙報；即時專案狀態表使用 project-tracker。
---

# 智慧週報生成器

適用：有明確起訖日的週報。尚缺期間時先確認；跨週紀錄拆分，不把其他週成果列成本週完成。

## 工作流程

1. 讀取原始 TXT、Markdown 或 DOCX。需擷取文字時執行 `python scripts/_office.py extract "<原始檔>" --output "<文字檔>"`；不可讀就說明限制，不猜內容。
2. STAR 情境、任務、行動、結果分別核對原文。原文只說完成整理時，不改成節省成本或提升百分比。結果可定性表達；沒有結果就留空標待確認。下週計畫與已完成分開，建議不當成承諾。
3. 讀 [輸入契約與驗收](references/workflow.md)，由 Codex 依原始資料建立有來源 JSON；核對語意後再交腳本驗證欄位及產檔。
4. 執行 `python scripts/run.py --input "<證據 JSON>" --output "<指定輸出資料夾>"`。腳本不進行語意理解、不連網、不執行外部發布。
5. 開啟成果核對來源、日期與未知欄位。DOCX 檢查可開啟及畫面版面；程式測試與 Codex 觸發驗收分開回報。

## 缺漏與範例

缺漏可選欄位用 null，呈現「待確認」。缺必要來源或日期基準時先補資料；不得造人名、金額、期限與績效。

獨立練習：先讀 [模擬原始資料](references/source.md)，由 Codex 整理，再參考 [完整證據範例](references/example.json) 比對。所有範例皆為模擬。

提示詞：「請用 $weekly-report 將本週工作紀錄整理成精簡版與詳細版 Word 週報，不補造績效。」

產物：weekly-brief.md、weekly-detailed.md、weekly-brief.docx、weekly-detailed.docx、evidence.json。
