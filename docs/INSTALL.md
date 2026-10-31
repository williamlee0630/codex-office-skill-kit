# 安裝與日常使用

版本 1.2.0｜更新：2026-10-31（台北）

## 安裝並載入技能

1. 下載完整工具包或技能安裝包，使用「全部解壓縮」，不要在 ZIP 預覽裡操作。
2. 在 Codex 開啟解壓後的資料夾，可使用其中 `.agents/skills/` 的技能。要在別的工作區使用，將所需完整技能資料夾複製到該工作區的 `.agents/skills/`；保留 scripts、references、agents，不只複製 SKILL.md。
3. 重新載入技能或重新開啟 Codex，再送出技能名稱。技能不依賴課程根目錄，也不會自行讀教學資料。

```text
$email-assistant
```

依引導說明工作或提供素材 → 必要時補答 → 開啟並核對成果。可貼文字、附檔或提供可讀檔案，不需固定表單、路徑回報、JSON 或長提示詞。已有完整目的與資料時直接處理，補答後自動接續。自然語言仍能自動選用。

## 環境由 Skill 處理

各技能自行讀取規則，檢查 Python 3.10+ 與 `scripts/requirements.txt` 所列格式套件。已有可用環境就沿用；缺少時在目前工作區準備專用環境，選參數並實際執行產檔。沒有 Python、安裝權限或連線時，才具體說明需要資訊同仁協助的部分。

下載包不包含 Python 或第三方套件。講義可雙擊 handbook/index.html 離線閱讀；Codex 使用與首次套件取得依帳號、網路及組織規範。

## 個人技能安裝（選用）

若希望在不同工作區使用，可依 Codex 的個人技能位置安裝完整技能。請 Codex 協助檢查既有同名版本；工具包不自動覆寫全域技能。安裝工具預設預覽，遇同名資料夾拒絕覆寫。

<details><summary>維護者：環境、安裝工具及同名技能排錯</summary>

在工具包根目錄執行；使用者日常工作不必貼這些命令：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools/install_skills.py --target "$HOME/.agents/skills"
```

明確授權安裝後加 `--apply` 才複製；先備份及判斷既有同名技能，不盲目刪除。由 Codex 檢查實際載入來源、規則、環境及錯誤；不要求使用者回報內部路徑。

格式工具可獨立使用各技能 scripts/requirements.txt 安裝；無需課程根目錄的 requirements.txt。參考官方技能位置與歷史查證見 [OFFICIAL_SOURCES](OFFICIAL_SOURCES.md)，桌面介面名稱依版本而定。

</details>

## v1.2.0 升級

本版保留九個技能，新增 legal-reviewer 與 finance-assistant。若舊工作區已安裝 v1.1.0，先備份並確認使用者修改，再由 Codex 協助移除淘汰的 meeting-assistant、project-tracker、weekly-report 與安裝新版；本專案不會自動刪除其他工作區或全域安裝。
