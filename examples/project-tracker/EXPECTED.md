# 模擬情境預期成果

正常案例使用 `input.json`，它是 Codex 依 `source.md` 整理的證據資料範例，不能視為已通過自然語言觸發驗收。請先閱讀原始資料，再自行建立 JSON 比對。

缺漏案例：`incomplete.json` 保留待確認，不補造人名、期限或數字。

錯誤案例：`invalid.json` 應顯示繁體中文錯誤並回傳非零，不建立成果。

產物：progress.md、progress.csv、progress.xlsx、evidence.json（含 resolved_tasks、resolved_decisions）。

T1 仍是 in_progress，期限 2026-10-22、基準日 2026-10-23，分類逾期；10/23『先標完成』只是提議。發布範圍仍是先內部試用。T2 不補猜負責人與期限。Excel/CSV 的外來公式字串須以文字保存。

逐欄契約見對應技能的 `references/workflow.md`。

