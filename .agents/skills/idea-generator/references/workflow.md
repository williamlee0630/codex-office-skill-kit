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

完整輸入見 [example.json](example.json)，原始內容見 [source.md](source.md)。單獨安裝不需先執行其他技能。

## 執行與產物

Python 3.10 以上；DOCX 需要 python-docx，Excel 需要 openpyxl。依工具包安裝說明設定 Python，不需要 API 金鑰。

```powershell
python "<技能資料夾>/scripts/run.py" --input "<技能資料夾>/references/example.json" --output "./practice-out"
```

產物：ideas.md、comparison.csv、selected-plan.md、evidence.json。

來源與輸入完整保留於 evidence.json。Excel/CSV 的外來文字安全保存，避免當成公式執行。

## 預期成果

正常案例剛好十案，評估標主觀且待驗證；I1 已選定，計畫有交付物但不填人名與日期。缺漏案例未選案，計畫待確認。錯誤案例九案不能靜默補成十案。

## 五項驗收

1. 正常：Codex 先讀 source.md 自建 JSON，再對照完整範例實際產檔。
2. 缺漏：使用工具包 examples/idea-generator/incomplete.json，確認待確認資訊沒有補造。
3. 錯誤：使用 examples/idea-generator/invalid.json，確認非零錯誤且不建立新成果。
4. 實際檔案：開啟 Markdown、DOCX、Excel；不能只看副檔名。Word 不可裁切、缺字或溢出。
5. 內容及安全：逐項對照來源、語意分類；不寄信、不部署、不上傳。unittest 通過不等於 Codex 自然語言觸發驗收。

