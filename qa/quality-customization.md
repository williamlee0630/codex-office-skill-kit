# 第 11 章自然語言客製化：獨立前向測試

日期：2026-11-02。範圍：獨立代理讀取原 Skill、依原始模擬郵件實際產檔，再執行 `handbook/experiences.py` 的完整 `CUSTOMIZATION_PROMPT`。不是桌面 Codex 或真實 CLI 的產品載入測試。

## 實際執行

- 在 chat 工作區 `work/customization-test` 只複製完整 `email-assistant` 專案技能；原始資料只取 `EMAIL_PASTE_FALLBACK` 的三封全文，未讀工具包 examples 預填輸入／答案或私人信箱。
- 先由 Codex 讀原文建立語意分類、期限與回覆內容，執行原技能產出摘要、兩封各三種語氣草稿及證據。草稿交付修飾另存 final 版本，原始腳本輸出保留。
- 建立完整獨立 `team-email-assistant`，改 `SKILL.md`、`agents/openai.yaml`、`references/workflow.md`、`scripts/run.py`，新增副本內 `tests/test_manager_confirmations.py`；名稱、描述與預設提示一致。
- 新摘要末尾實際新增「需要主管確認」，每項保留逐字引文、來源與語意判斷依據。無事項須明填空陣列；未覆核不能默認為空。腳本拒絕已決、非主管、無來源及不在該信內文的引文。

## 結果與保留範圍

原副本的八項新增行為測試先出現六個失敗、兩個缺章節錯誤；客製後八項通過，副本內獨立測試再執行八項通過。標準 `quick_validate.py` 以 Python UTF-8 模式通過；初次預設 cp950 讀取 UTF-8 失敗後改用程序參數重跑，未變更全域設定。結構驗證不能代表成功載入。

同源比對確認：原始三信快照、原隔離 Skill 全檔案、原始及 final 成果的 SHA-256 均未變；新摘要在主管末章之前與舊摘要一致；除新增主管欄位外，原 evidence 各欄位一致，最終草稿逐位元一致。10/26 17:00 仍為已確認內部期限；10/27 中午仍是客戶要求、尚未承諾。

主管章節收錄主管信中的「內部檢視後確認客戶交期」及「預算核准結果／核准權責」兩項。核准權責未知保留未知，不宣稱主管已有核准權。夥伴變更、主持人、費用與會議日期沒有指明由主管決定，因此保留一般待確認。額外一封提到主管但提案已核准的模擬信，章節正文精確為「本次原始資料未列出需主管確認事項」，沒有新編事項。

實際副本及所有前後產物保留在 chat 工作區 `work/customization-test`；原摘要與新摘要分別為 `artifacts/before-final/daily-summary.md`、`artifacts/after-final/daily-summary.md`；空結果為 `artifacts/no-manager/daily-summary.md`。這些是本機 QA 產物，不打包成第十個正式 Skill。

## 證據界線

取得的隔離基線 `SKILL.md` SHA-256：`ae9fa1e939585d7b276f470a50d4fdc283b671e581d5d0e732d50d509ffd3721`；`scripts/run.py`：`7e4b728a9dbe0937cd78d55fc62817cc2f9e1de11bf00157380105bf25dc8a95`。完整清單保留在隔離工作區 `integrity-before.json`。

測試期間，正式 repo 的 email 技能由另一分工更新跨時區／契約，根代理已確認為預期。本次沒有覆寫其修改，且結果只適用於上述隔離基線，不宣稱驗證最終 repo 版本。獨立代理確有讀取並執行副本；桌面 Codex 載入、真實 CLI 載入與使用者介面端到端均未驗證。未寄信、未改信箱、未改全域安裝；九個正式技能未因本次客製測試增加。
