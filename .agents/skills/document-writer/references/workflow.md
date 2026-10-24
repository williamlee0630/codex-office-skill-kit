# 商務文件撰寫助理輸入契約與驗收

## 處理邊界

原始資料由 Codex 閱讀判斷。run.py 只驗證有來源 JSON、計算明確日期規則及產檔。欄位驗證成功不代表引文支持語意判斷；執行前核對原檔。

## 共通結構

- JSON 根節點須為物件，UTF-8 編碼。必填 title（非空白文字）與 sources（至少一個）。
- sources 每項含唯一 id、label（來源名稱或檔案位置）、date（YYYY-MM-DD 或 null）。保留原始日期，不以執行日代替。
- evidence 為至少一筆 {"source_id":"s1","quote":"原始資料的原文引句"}。source_id 須存在；引句保留支持判斷的上下文，不把改寫當引文。
- 未知使用 null。日期須有效 YYYY-MM-DD。格式錯誤回傳非零並顯示繁體中文訊息。使用新的輸出資料夾，避免覆寫同名成果。

## 專屬結構

`purpose`、`audience` 可為文字或 null。`facts` 每項含唯一 `id`、`text`、`evidence`。`versions` 必含 `formal`、`concise`；每版至少一段，每段含 `heading`、`text`、`fact_ids`（既有事實 id 陣列）。無事實時可空參照，但只能寫待補資訊。`pending_questions` 為文字陣列。腳本驗證參照存在，不理解改寫語意；執行前由 Codex 核對每段有無新增未有依據的主張。

完整輸入見 [example.json](example.json)，原始內容見 [source.md](source.md)。單獨安裝不需先執行其他技能。

## 執行與產物

Python 3.10 以上；DOCX 需要 python-docx，Excel 需要 openpyxl。依工具包安裝說明設定 Python，不需要 API 金鑰。

```powershell
python "<技能資料夾>/scripts/run.py" --input "<技能資料夾>/references/example.json" --output "./practice-out"
```

產物：document-formal.md、document-concise.md、document-formal.docx、document-concise.docx、evidence.json。

來源與輸入完整保留於 evidence.json。Excel/CSV 的外來文字安全保存，避免當成公式執行。

## 預期成果

兩版保留內部同仁與現有會議時段的事實；預算、日期、負責人保持待確認。沒有數據不新增成本效益。不存在的 fact_ids 拒絕。

## 五項驗收

1. 正常：Codex 先讀 source.md 自建 JSON，再對照完整範例實際產檔。
2. 缺漏：使用工具包 examples/document-writer/incomplete.json，確認待確認資訊沒有補造。
3. 錯誤：使用 examples/document-writer/invalid.json，確認非零錯誤且不建立新成果。
4. 實際檔案：開啟 Markdown、DOCX、Excel；不能只看副檔名。Word 不可裁切、缺字或溢出。
5. 內容及安全：逐項對照來源、語意分類；不寄信、不部署、不上傳。unittest 通過不等於 Codex 自然語言觸發驗收。

