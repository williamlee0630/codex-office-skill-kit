# Codex 觸發與語意驗收

本文件是實際操作案例，不是自動通過紀錄。使用新聊天、指定本工具包工作目錄。每項先自然描述，再另開聊天明確指定 `$技能名稱`；不要把名稱比對或 Python CLI 成功當成自然觸發通過。

記錄：日期、Codex版本／環境、完整提示、實際讀取 SKILL.md 絕對路徑、原始資料、語意結果、實際產物及人工核對。若同名全域技能被選中，記失敗／不適用並明確指定本專案檔案；不能把其他技能的成果算成本包通過。

| 目標技能 | 自然語言案例（從原文開始） | 必須核對 |
|---|---|---|
| email-assistant | 整理 examples/email-assistant/source.md 的郵件，列今日待辦與回覆草稿，基準2026-10-23。 | 分類、未知期限、三種語氣、不寄送 |
| meeting-assistant | 整理 examples/meeting-assistant/source.md，區分決議、提議與待辦。 | 全面上線未定案；負責人及期限來源 |
| project-tracker | 整合 examples/project-tracker/source.md，列2026-10-23進度及決策變更。 | 提議不取代確認；未來資料不混入基準日 |
| weekly-report | 用 examples/weekly-report/source.md 寫10/19–10/23精簡與詳細週報。 | STAR、不造績效、期間與下週計畫 |
| receipt-organizer | 整理 examples/receipt-organizer/simulated-receipt.png 成報帳Excel，不確定值待確認。 | 實際看圖／轉錄、幣別分計、沒有假OCR |
| presentation-maker | 用 examples/presentation-maker/source.md 製作真正簡報與講稿。 | PPTX可開、notes、無溢出、來源事實 |
| document-writer | 依 examples/document-writer/source.md 撰寫正式與精簡企劃。 | DOCX與MD、保留事實、不造數字 |
| data-analyst | 分析 examples/data-analyst/sales.csv，檢查缺漏、統計與圖表。 | Python真計算、異常保留、不推因果 |
| idea-generator | 依 examples/idea-generator/source.md 提10個方案並為選案排工作計畫。 | 十案不同、主觀評估、未知負責人不補猜 |
| research-assistant | 比較 examples/research-assistant/sources/兩方案，僅用現有檔案，供24人課程選擇。 | 真來源、日期、差異及缺口、離線標示 |

每項加做缺漏案例及錯誤格式，確認不補猜與能解釋錯誤。具Gmail／網路工具時另以明確授權資料測讀取，不在本機模擬驗收中宣稱已完成。Word/Excel/PPTX逐頁核對為獨立關卡。

本次已執行的公開範圍見 ACCEPTANCE.md 與 qa/natural-trigger-results.json；原始日誌僅留本機，尚未執行的項目保持「未測試」。
