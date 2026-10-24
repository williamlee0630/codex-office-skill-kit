# 模擬情境預期成果

正常案例使用 `input.json`，它是 Codex 依 `source.md` 整理的證據資料範例，不能視為已通過自然語言觸發驗收。請先閱讀原始資料，再自行建立 JSON 比對。

缺漏案例：`incomplete.json` 保留待確認，不補造人名、期限或數字。

錯誤案例：`invalid.json` 應顯示繁體中文錯誤並回傳非零，不建立成果。

產物：document-formal.md、document-concise.md、document-formal.docx、document-concise.docx、evidence.json。

兩版保留內部同仁與現有會議時段的事實；預算、日期、負責人保持待確認。沒有數據不新增成本效益。不存在的 fact_ids 拒絕。

逐欄契約見對應技能的 `references/workflow.md`。

