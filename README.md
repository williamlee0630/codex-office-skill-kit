# 繁體中文 AI 辦公室 Skill 工具包

版本 1.1.0｜日常辦公工具｜Windows 與 Codex 本機工作區

十個可長期用於真實工作的獨立技能。課程提供介紹與教學；技能以你目前的工作需求及來源執行，只有明確要求示範時才讀模擬資料。

[正式講義](https://williamlee0630.github.io/codex-office-skill-kit/handbook/index.html) · [安裝說明](docs/INSTALL.md) · [驗收與未驗證項目](ACCEPTANCE.md)

## 開始使用

安裝並載入技能 → 送出 `$技能名稱` → 依引導說明工作或提供素材 → 必要時補答 → 開啟並核對成果。

例如在對話送出：

```text
$meeting-assistant
```

它會請你提供會議筆記或逐字稿。可以直接貼文字、提供附件或可讀檔案，不必固定表單、檔名或長提示詞。已有完整需求與素材時直接執行；補答與修改沿用前文，不必重貼全部需求或再問是否開始。也可自然地說「幫我整理這份會議筆記」，保留自動選用能力。

Codex 自行讀取規則、檢查環境、整理有來源的內部資料、選擇參數、執行工具並實際產檔。你不用指示它讀 MD、回報技能路徑、填 JSON 或手動指定腳本。只缺可選人名、期限或成效數字時，保留待確認並完成可用成果。

## 十個技能

| 技能 | 只有名稱時的引導 | 實際成果與邊界 |
|---|---|---|
| email-assistant | 郵件待辦、擬回信或修改回覆；可直接貼郵件 | Markdown 草稿與證據；預設不寄送 |
| meeting-assistant | 提供會議筆記或逐字稿 | Markdown、DOCX；提議與決議分開 |
| project-tracker | 同一專案更新與查核日，已有資料沿用 | Markdown、CSV、XLSX；追蹤逾期及決策變更 |
| weekly-report | 工作紀錄及必要的週報期間 | 精簡／詳細 Markdown、DOCX；不補造績效 |
| receipt-organizer | 收據、憑證、PDF、圖片或明細 | XLSX、原件及證據；只問不清欄位，不提交報帳 |
| presentation-maker | 工作素材、受眾與簡報目的 | 可編輯 PPTX、notes；不保真改版複雜樣板 |
| document-writer | 企劃、提案、信函、報告或修改草稿 | 正式／精簡 Markdown、DOCX；保留事實 |
| data-analyst | 表格與想了解的問題，無問題先查品質 | 實際計算 XLSX、Markdown、JSON、可用圖表 |
| idea-generator | 工作問題、目標與已知限制 | 預設十案、主觀比較；選案後接續計畫 |
| research-assistant | 研究問題及相關範圍，可提供文件 | 報告、來源 CSV、證據；不虛構搜尋或來源 |

## 安裝與一般工作區

完整解壓工具包並在 Codex 開啟資料夾，可使用其中的專案技能。要帶到一般工作區，把完整技能資料夾（含 scripts、references、agents）放到該工作區的 `.agents/skills/`；個人安裝見安裝說明。重新載入後送出技能名稱即可，不依賴課程資料夾。

每支技能攜帶執行資源及自己的 `scripts/requirements.txt`。Python 3.10+ 與格式套件由 Codex 檢查，缺少時在目前工作區準備；首次取得套件可能需要網路或權限。ZIP 不包含 Python；具體限制請交資訊同仁協助，不把未產檔說成完成。

## 下載與教學

- [完整工具包](dist/codex-office-skill-kit-1.1.0.zip)：技能、14 頁離線講義、另外選用的模擬素材、範例成果、測試與文件。
- [技能安裝包](dist/office-skills-1.1.0.zip)：十個完整技能、示範及必要安裝入口。
- [模擬教學資料包](dist/practice-data-1.1.0.zip)：原創模擬來源、預期成果與測試資料。
- [版本、SHA-256 與內容清單](dist/manifest.json)。完整包內含後兩包，不遞迴包含自己。

講義可離線閱讀。模擬資料只有明確要求示範、練習或指定範例時使用，產物清楚標示模擬；不混入工作成果。真實工作資料不會因使用工具包就自動標成模擬。

## 驗證與維護

程式測試、代理行為演練、真實 Codex 完整流程與原生 Office 畫面驗收分開記錄。未實際執行的檢查標未驗證；詳見 [本版報告](ACCEPTANCE.md)。

預設在目前工作區產檔，保留原始資料及舊成果。寄信、外部上傳、發布及其他外部影響仍依既有授權要求；不因啟動技能自動取得授權。

<details><summary>維護者：程式測試、手動操作與排錯</summary>

```powershell
python -m pip install -r requirements.txt
python tools/verify.py
python handbook/build.py
python tools/validate_kit.py
python tools/build_release.py
python tools/check_release.py
```

完整開發及打包說明見 [DEVELOPMENT](docs/DEVELOPMENT.md)。腳本只做驗證、計算與產檔，語意判斷由 Codex 從原文完成；預填 JSON 的產檔測試不代表原始來源已判讀。

</details>
