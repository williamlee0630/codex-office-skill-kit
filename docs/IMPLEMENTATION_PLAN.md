# 1.1.0 日常工作更新計畫（2026-10-30）

本次依使用者八項要求直接修改、驗證、提交並推送 main；保留既有來源、測試與原始模擬教材。使用者已明確授權本儲存庫推送及既有 Pages 發布。

- 十個技能：各自實務引導、沿用對話與補答、必要資訊判斷、內部環境／整理／執行／產檔／檢查及成果連結。
- 教學隔離：明確示範才讀資料；每支技能攜帶獨立示範與依賴，不依賴課程根目錄。
- 講義及入門：14 頁、README、安裝；可複製啟動只有 $名稱，技術細節收合，保留離線導覽與搜尋。
- 驗證：修改前基準、實際程式回歸、80 則代理演練、十次 CLI 啟動及個別產檔分開記錄；未完成完整流程保留未驗證。
- 發行：1.1.0、三種 ZIP、manifest、相對連結／公開內容、解壓測試；提交推送與 Actions／公開頁面確認。

實際完成狀態以 ACCEPTANCE.md、PROGRESS.md 與 qa/daily-work-* 為準。

---

以下保留 1.0.0 初始計畫作歷史參考。

# 實作計畫

依使用者指定的五階段交付。規格：USER_REQUEST.md；設計：DESIGN.md。

## 共用契約

- CLI：`python .agents/skills/<name>/scripts/run.py --input <file> --output <dir>`。
- 共用模組：`_office.py`，來源 tools/office_common.py。提供 `load_json(path)`, `read_text(path)`, `write_json(path, data)`, `write_markdown(path, text)`, `write_docx(path, title, sections)`, `write_xlsx(path, headers, rows, sheet_name='明細')`, `require(condition, message)`, `safe_cell(value)`。
- `write_docx` 的 sections 是 `(heading, body)` tuple 清單；body 為字串或字串清單。`write_xlsx` 回傳檔案 Path。所有寫檔函式會建立父目錄。
- 語意技能輸入採有來源的 JSON；原始 TXT / MD / DOCX / PDF 用 `python scripts/_office.py extract <path> --output <txt>` 讀取，Codex 根據原始資料建立 JSON，不以預填 JSON 冒充語意測試。
- 所有腳本無網路、無寄信、無發布行為。錯誤回傳非零並給繁體中文可理解訊息。

## 第一階段：骨架與工具（主工作者）

- [ ] 建立共同規範、依賴與離線框架；測試共用讀檔與安全試算表輸出。
- [ ] 官方 skill-creator 初始化與驗證十個技能。

## 第二階段：基礎技能（foundation 工作者）

- [ ] meeting-assistant、project-tracker、weekly-report、document-writer、idea-generator。
- [ ] 每項先建立正常、缺漏、錯誤與實際產檔測試，再寫 scripts/run.py、references/workflow.md、examples/<name> 資料與完整 SKILL.md。
- [ ] 專案明確 as-of、週報明確期間，缺漏保留待確認，提議不當決議、創意分數為主觀評估。

## 第三階段：檔案技能（artifacts 工作者）

- [ ] data-analyst、presentation-maker、receipt-organizer。
- [ ] 先測試再實作 Python 真實計算、PPTX 與 notes、Excel 報帳。驗證混合幣別、空資料、公式注入、長文字。

## 第四階段：資訊技能（主工作者）

- [ ] email-assistant、research-assistant 與來源契約、自動測試；郵件只輸出草稿；研究明確離線來源。

## 第五階段：整合發行（handbook 工作者與主工作者）

- [ ] handbook 工作者完成首頁、12 章、附錄、離線導覽與複製、行動版、專屬教學與驗收。
- [ ] 主工作者整合安裝 / 開發文件、測試所有技能、執行官方 validator、產檔檢查與視覺抽查、ZIP、最終驗收。

## 優先檢查的邊界

1. 缺少負責人與期限保留未知；不把最新提議覆寫已確認決議。
2. 不同幣別分別合計；重複收據不可靜默刪除。
3. Excel 中以 =、+、-、@ 開頭的外來文字不得變成公式。
4. 長簡報文字必須分頁或明確拒絕；圖表與統計必須能回算原始資料。
5. 離線研究及程式產檔不得冒稱完成網路或自然語言觸發測試。
