# 明確要求才使用的模擬示範

一般工作不讀本文件。只有使用者明確要求示範、練習或指定範例才進行；全部素材與成果標示「模擬教學」，另存新的示範資料夾。

本技能可獨立安裝，示範來源位於本文件旁的 demo/，不依賴課程根目錄。

先完整讀 demo/source.md 的原始模擬素材，按本技能規則自行判讀並整理新的內部資料，再執行產檔。demo/input.json 僅用來理解契約及比對，不得直接複製預填答案宣稱已獨立理解原文。

依 operation.md 檢查環境、選擇新輸出資料夾、實際執行並開啟核對。示範的查核日與週報期間只從示範需求／來源取得，不沿用到工作任務。

<details><summary>維護者：保留的舊版測試與契約示例</summary>

以下直接執行預填 JSON 僅為程式產檔測試，不代表完成原文語意示範。

# 明確要求才使用的模擬示範與測試

所有本文件示例均為模擬。請先讀原始資料，重新整理後產檔；不可把預填答案冒充原文判讀。一般工作不得讀取本文件代替使用者來源。

# 智慧週報生成器輸入契約與驗收

## 處理邊界

原始資料由 Codex 閱讀判斷。run.py 只驗證有來源 JSON、計算明確日期規則及產檔。欄位驗證成功不代表引文支持語意判斷；執行前核對原檔。

## 共通結構

- JSON 根節點須為物件，UTF-8 編碼。必填 title（非空白文字）與 sources（至少一個）。
- sources 每項含唯一 id、label（來源名稱或檔案位置）、date（YYYY-MM-DD 或 null）。保留原始日期，不以執行日代替。
- evidence 為至少一筆 {"source_id":"s1","quote":"原始資料的原文引句"}。source_id 須存在；引句保留支持判斷的上下文，不把改寫當引文。
- 未知使用 null。日期須有效 YYYY-MM-DD。格式錯誤回傳非零並顯示繁體中文訊息。使用新的輸出資料夾，避免覆寫同名成果。

## 專屬結構

必填 `period_start`、`period_end`（YYYY-MM-DD，起日不得晚於末日）。`records` 每項含 `date`（日期或 null）、`category`（completed/progress/problem/next_plan/support）、`summary`、`evidence`。可選 `star` 物件含 situation/task/action/result，各為文字或 null。除 next_plan 外，有日期紀錄須在期間內；next_plan 日期須晚於末日。缺結果、日期與空類別均保留待確認。

完整輸入見 [example.json](example.json)，原始內容見 [source.md](source.md)。單獨安裝不需先執行其他技能。

## 執行與產物

Python 3.10 以上；DOCX 需要 python-docx，Excel 需要 openpyxl。依工具包安裝說明設定 Python，不需要 API 金鑰。

```powershell
python "<技能資料夾>/scripts/run.py" --input "<技能資料夾>/references/example.json" --output "./practice-out"
```

產物：weekly-brief.md、weekly-detailed.md、weekly-brief.docx、weekly-detailed.docx、evidence.json。

來源與輸入完整保留於 evidence.json。Excel/CSV 的外來文字安全保存，避免當成公式執行。

## 預期成果

完成試用名單但成果數字未提供，STAR R 必須保留待確認，不能寫提升百分比。下週 2026-10-26 調整回饋表不列本週完成。結束日早於起始日拒絕。

## 五項驗收

1. 正常：Codex 先讀 source.md 自建 JSON，再對照完整範例實際產檔。
2. 缺漏：使用工具包 examples/weekly-report/incomplete.json，確認待確認資訊沒有補造。
3. 錯誤：使用 examples/weekly-report/invalid.json，確認非零錯誤且不建立新成果。
4. 實際檔案：開啟兩版 Markdown 與 DOCX；不能只看副檔名。Word 不可裁切、缺字或溢出。
5. 內容及安全：逐項對照來源、語意分類；不寄信、不部署、不上傳。unittest 通過不等於 Codex 自然語言觸發驗收。


</details>
