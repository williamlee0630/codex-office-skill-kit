# 繁體中文 AI 辦公室 Skill 工具包

版本 1.0.0｜開課方審閱版｜Windows 與 Codex 本機工作區｜原創模擬資料

正式講義：[AI 辦公室實作指南](https://williamlee0630.github.io/codex-office-skill-kit/)。Repository：[williamlee0630/codex-office-skill-kit](https://github.com/williamlee0630/codex-office-skill-kit)。2026-10-24 已實際完成公開網址、頁面及下載檢查；這是開課方審閱版，人工驗收缺口另列於下方報告。

用十個獨立技能，把郵件、會議、工作紀錄、表格與收據整理成可開啟的實際成果。Codex 負責依原文判讀；本機 Python 負責驗證、計算與產檔。講義可離線閱讀，Codex 模型與初次安裝套件仍依帳號及網路環境。

## 先從這裡開始

1. [開啟電子講義](handbook/index.html)：首頁、12章與附錄，共14頁，含可複製提示詞及逐步實作。
2. [Windows 安裝說明](docs/INSTALL.md)：整包開啟、Python準備、單一技能與選用全域安裝。
3. [最終驗收報告](ACCEPTANCE.md)：完成、部分完成、尚未驗證項目分開列示。
4. [開發進度](docs/PROGRESS.md)：五階段測試與剩餘工作。

## 十個技能

| 技能 | 工作用途 | 實際成果 |
|---|---|---|
| email-assistant | 郵件分類與每日待辦、三種語氣草稿 | Markdown、證據JSON；不寄信 |
| meeting-assistant | 單場會議決議／提議／待辦 | Markdown、DOCX |
| project-tracker | 跨日期更新、決策變更與風險 | Markdown、CSV、XLSX |
| weekly-report | 一週工作紀錄、STAR與主管協助 | 精簡／詳細 Markdown、DOCX |
| receipt-organizer | 收據欄位、分類、重複與各幣合計 | XLSX、確認清單、原檔與抽取證據 |
| presentation-maker | 來源轉簡報、資訊層級、講稿 | 可編輯PPTX、內嵌notes、版面結構檢查 |
| document-writer | 企劃、提案、商務信函、工作報告 | 正式／精簡 Markdown、DOCX |
| data-analyst | CSV／XLSX真實計算、缺漏、異常與圖表 | XLSX、Markdown、JSON、PNG |
| idea-generator | 預設10案、主觀比較、選案工作計畫 | Markdown、CSV |
| research-assistant | 有來源調查、比較、日期與資訊缺口 | Markdown、來源CSV、證據JSON |

## 在 Codex 使用

在 Codex 開啟本工具包根目錄，輸入：

```text
使用 $meeting-assistant，先回報本次實際載入的 SKILL.md 絕對路徑。
請讀 examples/meeting-assistant/source.md，分清提議與已確認決議，
保留負責人、期限與待確認事項，產生正式紀錄到 outputs/meeting-practice。
```

也可自然描述：「幫我整理這份會議記錄，列出已定案與尚未定案事項。」若你原本已裝同名技能，請明確指定本專案 `.agents/skills/meeting-assistant/SKILL.md` 的完整路徑，再核對回報。官方發現與觸發依據見 [查證紀錄](docs/OFFICIAL_SOURCES.md)。

先下載完整教材並解壓，在 Codex 開啟資料夾後，把工作需求與資料位置貼進聊天。請 Codex 自行檢查可用環境、準備處理資料並產生真正成果，你不必先學會 Python 或 JSON。若電腦缺少格式工具，請 Codex 或資訊同仁依安裝說明協助，不要只改檔案副檔名。

範例提示詞可以依工作目標、語氣、輸出格式與實際資料靈活調整；請保留來源與未知資訊，不要求 Codex 編造沒有依據的內容。

<details><summary>進階：給維護者的手動產檔命令</summary>

若只想先試產檔，準備環境後執行：

```powershell
python .agents/skills/meeting-assistant/scripts/run.py --input examples/meeting-assistant/input.json --output outputs/meeting-practice
```

input.json 是已整理的模擬測資。完整工作練習須從 source.md 開始，讓 Codex 整理有來源資料後再產檔。

</details>

## 發行檔

- [完整學員工具包](dist/codex-office-skill-kit-1.0.0.zip)：技能、完整講義、模擬資料、實際範例成果、測試與文件。
- [技能安裝包](dist/office-skills-1.0.0.zip)：十個完整技能、模擬資料、測試與安裝入口；適合已有講義的學員。
- [模擬資料包](dist/practice-data-1.0.0.zip)：十組來源、正常／缺漏／錯誤案例及實際範例成果。
- [SHA-256與內容清單](dist/manifest.json)。完整包包含後兩個ZIP，解壓後講義下載仍可使用；完整ZIP不遞迴包含自己。

## 維護與限制

結構及測試命令見 [開發說明](docs/DEVELOPMENT.md)。技能不會自行修改個人全域技能、寄送郵件、上傳或發布；本次GitHub部署是維護者另獲明確授權的課程發布。沒有OCR時交付待確認轉錄表；網路／Gmail是視工具與授權可選的分支，不能從本機示範推論已連線。

程式測試、Codex明確指定行為、自然語言路由、Office畫面驗收各有不同範圍，實際結果以驗收報告為準。
