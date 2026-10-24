# 專案進度追蹤助理輸入契約與驗收

## 處理邊界

原始資料由 Codex 閱讀判斷。run.py 只驗證有來源 JSON、計算明確日期規則及產檔。欄位驗證成功不代表引文支持語意判斷；執行前核對原檔。

## 共通結構

- JSON 根節點須為物件，UTF-8 編碼。必填 title（非空白文字）與 sources（至少一個）。
- sources 每項含唯一 id、label（來源名稱或檔案位置）、date（YYYY-MM-DD 或 null）。保留原始日期，不以執行日代替。
- evidence 為至少一筆 {"source_id":"s1","quote":"原始資料的原文引句"}。source_id 須存在；引句保留支持判斷的上下文，不把改寫當引文。
- 未知使用 null。日期須有效 YYYY-MM-DD。格式錯誤回傳非零並顯示繁體中文訊息。使用新的輸出資料夾，避免覆寫同名成果。

## 專屬結構

必填 `as_of`（YYYY-MM-DD）。`tasks` 每項含唯一 `id`、`title`、`updates`。更新含 `date`、`confirmation`（confirmed/proposed）、`status`（not_started/in_progress/completed/blocked）、`owner`（可 null）、`due`（日期或 null）、`evidence`。`decisions` 每項含 `topic`、`text`、`date`、`confirmation`、`evidence`，同 topic 形成歷史。基準日以後的更新保留證據但不影響進度。無已確認更新標待確認。

完整輸入見 [example.json](example.json)，原始內容見 [source.md](source.md)。單獨安裝不需先執行其他技能。

## 執行與產物

Python 3.10 以上；DOCX 需要 python-docx，Excel 需要 openpyxl。依工具包安裝說明設定 Python，不需要 API 金鑰。

```powershell
python "<技能資料夾>/scripts/run.py" --input "<技能資料夾>/references/example.json" --output "./practice-out"
```

產物：progress.md、progress.csv、progress.xlsx、evidence.json（含 resolved_tasks、resolved_decisions）。

來源與輸入完整保留於 evidence.json。Excel/CSV 的外來文字安全保存，避免當成公式執行。

## 預期成果

T1 仍是 in_progress，期限 2026-10-22、基準日 2026-10-23，分類逾期；10/23『先標完成』只是提議。發布範圍仍是先內部試用。T2 不補猜負責人與期限。Excel/CSV 的外來公式字串須以文字保存。

## 五項驗收

1. 正常：Codex 先讀 source.md 自建 JSON，再對照完整範例實際產檔。
2. 缺漏：使用工具包 examples/project-tracker/incomplete.json，確認待確認資訊沒有補造。
3. 錯誤：使用 examples/project-tracker/invalid.json，確認非零錯誤且不建立新成果。
4. 實際檔案：開啟 Markdown、DOCX、Excel；不能只看副檔名。Word 不可裁切、缺字或溢出。
5. 內容及安全：逐項對照來源、語意分類；不寄信、不部署、不上傳。unittest 通過不等於 Codex 自然語言觸發驗收。

