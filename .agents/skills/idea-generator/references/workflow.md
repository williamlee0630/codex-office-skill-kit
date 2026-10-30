# AI 創意企劃助理輸入契約與驗收

## 處理邊界

原始資料由 Codex 閱讀判斷。run.py 只驗證有來源 JSON、計算明確日期規則及產檔。欄位驗證成功不代表引文支持語意判斷；執行前核對原檔。

## 共通結構

- JSON 根節點須為物件，UTF-8 編碼。必填 title（非空白文字）與 sources（至少一個）。
- sources 每項含唯一 id、label（來源名稱或檔案位置）、date（YYYY-MM-DD 或 null）。保留原始日期，不以執行日代替。
- evidence 為至少一筆 {"source_id":"s1","quote":"原始資料的原文引句"}。source_id 須存在；引句保留支持判斷的上下文，不把改寫當引文。
- 未知使用 null。日期須有效 YYYY-MM-DD。格式錯誤回傳非零並顯示繁體中文訊息。使用新的輸出資料夾，避免覆寫同名成果。

## 專屬結構

必填 `goal`、頂層 `evidence`。`target_count` 預設 10，可 1–30。`constraints` 每項含唯一 `id`、`text`、`evidence`。`ideas` 長度須等於 target_count，每項含唯一 `id`、不同 `title`、`description`、`resources`（文字陣列）、`cost`、`difficulty`、`value`、`pros`/`cons`（文字陣列）、`rationale`、`constraint_ids`。`recommendation` 可 null。`selected_id` 可 null 或既有 id；指定時須有 `plan` 步驟，含 step、deliverable、owner（可 null）、due（日期或 null）。`validation_plan` 為建議驗證方式，可 null。

貼上文字可由 Codex 存成來源快照；label 指回實際來源，quote 保留原句。單獨安裝不需先執行其他技能。

## 執行與產物

Python 3.10 以上；DOCX 需要 python-docx，Excel 需要 openpyxl。依本技能 operation.md 與 scripts/requirements.txt 自行檢查環境，不需要課程根目錄或 API 金鑰。

執行方式見 [內部執行](operation.md)，輸入為 Codex 自行整理的工作資料，並非預設示範。

產物：ideas.md、comparison.csv、selected-plan.md、evidence.json。

來源與輸入完整保留於 evidence.json。Excel/CSV 的外來文字安全保存，避免當成公式執行。
