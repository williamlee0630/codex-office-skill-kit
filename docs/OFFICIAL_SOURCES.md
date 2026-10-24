# 官方依據與環境界線

查證日期：2026-10-23（Asia/Taipei）。

- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)：本次從 https://developers.openai.com/codex/skills/ 實際開啟後導向此頁。確認 SKILL.md 需 name/description、可有 scripts/references/agents metadata、分階段載入、本機 .agents/skills 範圍、明確與隱含觸發、同名不合併、必要時重新啟動。
- 本機官方 skill-creator 已實際讀取，使用 init_skill.py 初始化，quick_validate.py 驗證。本工具的靜態驗證不代表技能判斷品質。
- `codex --version` 實際回報 `codex-cli 0.163.0-alpha.11.2`；這是 CLI 版本，不冒稱桌面 GUI 版本。
- 桌面按鈕與技能選單因版本可能不同，本課程不使用虛構截圖，也不要求未核實的固定按鈕。

官方目前也建議更廣泛可重用發行可採 plugin；本版依使用者規格提供可解壓的專案技能 ZIP，不冒稱為已上架 plugin。
