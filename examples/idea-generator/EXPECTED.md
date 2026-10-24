# 模擬情境預期成果

正常案例使用 `input.json`，它是 Codex 依 `source.md` 整理的證據資料範例，不能視為已通過自然語言觸發驗收。請先閱讀原始資料，再自行建立 JSON 比對。

缺漏案例：`incomplete.json` 保留待確認，不補造人名、期限或數字。

錯誤案例：`invalid.json` 應顯示繁體中文錯誤並回傳非零，不建立成果。

產物：ideas.md、comparison.csv、selected-plan.md、evidence.json。

正常案例剛好十案，評估標主觀且待驗證；I1 已選定，計畫有交付物但不填人名與日期。缺漏案例未選案，計畫待確認。錯誤案例九案不能靜默補成十案。

逐欄契約見對應技能的 `references/workflow.md`。

