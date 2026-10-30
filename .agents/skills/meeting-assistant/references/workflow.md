# 會議紀錄整理助理輸入契約與驗收

## 處理邊界

原始資料由 Codex 閱讀判斷。run.py 只驗證有來源 JSON、計算明確日期規則及產檔。欄位驗證成功不代表引文支持語意判斷；執行前核對原檔。

## 共通結構

- JSON 根節點須為物件，UTF-8 編碼。必填 title（非空白文字）與 sources（至少一個）。
- sources 每項含唯一 id、label（來源名稱或檔案位置）、date（YYYY-MM-DD 或 null）。保留原始日期，不以執行日代替。
- evidence 為至少一筆 {"source_id":"s1","quote":"原始資料的原文引句"}。source_id 須存在；引句保留支持判斷的上下文，不把改寫當引文。
- 未知使用 null。日期須有效 YYYY-MM-DD。格式錯誤回傳非零並顯示繁體中文訊息。使用新的輸出資料夾，避免覆寫同名成果。

## 專屬結構

`meeting_date` 為 YYYY-MM-DD 或 null；`items` 是物件陣列，每項含 `kind`（summary/decision/action/question）、`status`（proposed/discussion/confirmed/pending）、`text`、`evidence`。action 另含 `owner`（字串或 null）、`due`（日期或 null）。缺漏可產檔並標待確認；未知 kind/status、無引文均拒絕。

貼上文字可由 Codex 存成來源快照；label 指回實際來源，quote 保留原句。單獨安裝不需先執行其他技能。

## 執行與產物

Python 3.10 以上；DOCX 需要 python-docx，Excel 需要 openpyxl。依本技能 operation.md 與 scripts/requirements.txt 自行檢查環境，不需要課程根目錄或 API 金鑰。

執行方式見 [內部執行](operation.md)，輸入為 Codex 自行整理的工作資料，並非預設示範。

產物：minutes.md、minutes.docx、evidence.json。

來源與輸入完整保留於 evidence.json。Excel/CSV 的外來文字安全保存，避免當成公式執行。
