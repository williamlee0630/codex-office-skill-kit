---
name: idea-generator
description: 依問題、目標及限制規劃具體且不同的創意方向，預設十案，對照資源、成本、難度、預期價值及優缺點，為選定方案建立執行計畫。適用方案發想比較；現有文件事實摘要不適用。
---

# AI 創意企劃助理

適用：有問題與目標的創意發想。先取得限制與成功判準；預算、負責人或日期不足明列待確認，不用範例替代真實要求。

## 工作流程

1. 讀取原始 TXT、Markdown 或 DOCX。需擷取文字時執行 `python scripts/_office.py extract "<原始檔>" --output "<文字檔>"`；不可讀就說明限制，不猜內容。
2. 由 Codex 產生十個做法有實質差異的方案，再檢查換名但內容重複的方案。使用者另指定數量時調整 target_count。成本、難度與價值均標規劃假設及主觀評估，不冒稱真實報價、研究或成效。只為已選定 selected_id 建立計畫；未選時可建議，selected_id 留 null。計畫人名及日期須有依據或明寫為建議並待確認。
3. 讀 [輸入契約與驗收](references/workflow.md)，由 Codex 依原始資料建立有來源 JSON；核對語意後再交腳本驗證欄位及產檔。
4. 執行 `python scripts/run.py --input "<證據 JSON>" --output "<指定輸出資料夾>"`。腳本不進行語意理解、不連網、不執行外部發布。
5. 開啟 Markdown 方案、CSV 比較表與選定方案計畫，核對來源、日期與未知欄位，確認主觀評估有標示；程式測試與 Codex 觸發驗收分開回報。

## 缺漏與範例

缺漏可選欄位用 null，呈現「待確認」。缺必要來源或日期基準時先補資料；不得造人名、金額、期限與績效。

獨立練習：先讀 [模擬原始資料](references/source.md)，由 Codex 整理，再參考 [完整證據範例](references/example.json) 比對。所有範例皆為模擬。

提示詞：「請用 $idea-generator 依我的目標與限制提出十個不同方案，比較後為我選定的方案建立計畫。」

產物：ideas.md、comparison.csv、selected-plan.md、evidence.json。
