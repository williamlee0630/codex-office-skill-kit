# 專案規則

本專案是繁體中文 AI 辦公室 Skill 工具包，版本 1.0.0。使用者介面、講義與診斷訊息使用台灣繁體中文；程式識別字及技能資料夾使用英文。

- 僅修改目前工作區。不得覆寫全域技能、部署、推送或寄信。
- 十個技能各自包含 SKILL.md、可執行資源、範例及測試；腳本只做可驗證的資料處理，語意判斷由 Codex 依原始資料進行。
- 所有教學資料標示模擬。保留來源、日期、未知欄位與待確認事項；不補造人名、金額、期限或來源。
- 每階段更新 docs/PROGRESS.md，分別記錄程式測試與 Codex 觸發驗收，不以其中一種代替另一種。
- 共用腳本來源為 tools/office_common.py；tools/sync_runtime.py 複製至每個技能的 scripts/_office.py，讓單一技能仍能獨立安裝。修改共用來源後重新同步。
- 測試使用 Python unittest：python -m unittest discover -s tests -v。新增運算或檔案處理前先寫行為測試並確認失敗。
- 發行使用 tools/build_release.py；排除快取、私人檔案與舊 ZIP，保留講義與範例。
- 分工範圍以 docs/IMPLEMENTATION_PLAN.md 為準；不要覆寫其他工作者檔案。以實際測試結果決定完成狀態。
