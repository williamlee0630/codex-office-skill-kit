# v1.2.0 改版實作計畫（2026-10-31）

使用者已指定完整規格並授權直接實作、測試、commit、推送原遠端與既有 GitHub Pages 部署，不逐步詢問。原始要求為本次附件；下方保留歷史計畫。

**目標**：九個可獨立執行的辦公 Skill；新法務提供可回查審查文件，新財務實算並核對數字。
**架構**：沿用 Python CLI、tools/office_common.py 與 sync_runtime.py；語意判讀由 Codex 執行，程式驗證來源並產檔。講義維持 lessons.py / build.py 來源與既有 CSS/JS。法務與財務各有獨立 scripts、references、agents、requirements 及明確選用的模擬素材。
**範圍**：只改此儲存庫，不覆寫全域 Skill 或其他課程。工作樹初始乾淨；main 與 origin 指向指定專案。

## 工作與檔案責任

- [x] 法務：.agents/skills/legal-reviewer/**、examples/legal-reviewer/**、tests/test_legal.py。先寫失敗測試，再做 TXT/MD/DOCX/文字 PDF 讀取、位置與引用核對、三種產檔、缺漏及來源未查證限制。保留原件，掃描 PDF 明確拒絕假讀。
- [x] 財務：.agents/skills/finance-assistant/**、examples/finance-assistant/**、tests/test_finance.py。先寫失敗測試，再做 Decimal 計算、CSV/XLSX/文字明細、對帳六類與一對一匹配、差異百分比、借貸與資產負債平衡檢查、三組獨立預期結果。
- [x] 講義：handbook/lessons.py、handbook/build.py、tests/test_handbook*.py。九課重排至第 10 章、自訂第 11 章、首頁郵件示例、30 分鐘路線、兩新課的十項教學內容、重建 13 頁與搜尋索引；保留 CSS/JS 及離線設計。
- [x] 整合：移除指定三技能執行目錄、教材、測試登錄；保留其歷史 QA。更新現有七技能回歸清單、validate/install/publication/build_release/check_release、版本及文件。
- [x] 驗收：unittest、verify、講義重建、validate、三包實際打包與 check_release、獨立複製執行、來源核對、輸出數字驗算、瀏覽器及代理啟動／完整流程分開記錄。未實測的桌面／Office 不宣稱通過。
- [ ] 發行：隱私白名單、九技能集合、ZIP 解壓與 checksum；更新 ACCEPTANCE、PROGRESS、CHANGELOG；commit/push；檢查既有 Actions 與公開網站及下載。

## 驗收焦點

同額異筆與重複引用不能重配；未知幣別／期間不能混算；零分母不能填假百分比；借貸不平不能補造交易；法務結論必須可回到原文、未知法域與未核實法律不能假裝確定。完整附件不重問，只有名稱時簡短引導，模擬來源不默默套入真實工作。

---

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
