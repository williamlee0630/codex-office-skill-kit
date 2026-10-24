# Windows 安裝與快速開始

本版為 1.0.0，文件查證日 2026-10-23。主要執行環境是 Codex 桌面版本機工作區；不需要其他 AI 平台或 API 金鑰。需有可使用 Codex 的帳號與權限；模型本身仍需依帳號服務連線，只有講義與本機產檔器可離線使用。

## 建議方法：整包開啟

1. 下載 dist/codex-office-skill-kit-1.0.0.zip，在檔案總管按「全部解壓縮」。不要在 ZIP 預覽裡操作。
2. 把整個資料夾放在自己的工作目錄，例如 `C:\OfficePractice`。確認裡面有 README.md、handbook 與 `.agents`；隱藏資料夾可能需要開啟顯示。
3. 在 Codex 開啟這個資料夾作為本機專案／工作區。各桌面版本選單可能不同，重點是聊天的工作目錄必須是這個資料夾。
4. 輸入：「請使用 `$meeting-assistant`，先回報本次實際讀取的 SKILL.md 絕對路徑，再整理 examples/meeting-assistant/source.md，保留提議與待確認。」
5. 若技能未出現，重新開啟工作區或重啟 Codex，再確認 `.agents/skills/meeting-assistant/SKILL.md` 存在。遇同名技能時請指定本專案的完整路徑，核對實際載入檔案。
6. 雙擊 handbook/index.html 開啟講義；不必啟動伺服器。依章節複製提示詞，讓 Codex 代為執行本機命令。

## Python 與格式套件

腳本適用 Python 3.10 以上。可以直接請 Codex 檢查現有 Python；若缺少，從 Python 官方網站安裝，完成後重新開啟終端機。建議在本專案建立虛擬環境，命令均在工具包根目錄的 PowerShell 執行：

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

不需要啟用虛擬環境的 Activate.ps1，也不需修改系統執行原則。初次安裝套件需可連線套件來源；本版 ZIP 不包含 Python 或第三方 wheel。受限網路可請資訊部準備對應平台的離線 wheelhouse：`python -m pip install --no-index --find-links <wheel資料夾> -r requirements.txt`。不具備套件時只能使用不需該套件的格式，不能宣稱 Word/Excel/PPTX 已產生。

若 Codex 桌面已提供工作區內建 Python 與套件，可讓 Codex 使用其實際回報的路徑；不要把開發者電腦上的絕對路徑直接搬到其他電腦。

## 第一個真實產檔練習

```powershell
.\.venv\Scripts\python.exe .agents/skills/meeting-assistant/scripts/run.py --input examples/meeting-assistant/input.json --output outputs/meeting-assistant
```

這一步是已整理測資的產檔練習。完整技能練習須讓 Codex 從 source.md 原文重新整理有來源的 JSON，再呼叫腳本並比對原文。不能把兩者當成同一種驗收。

## 選用：單一技能帶到另一工作區

複製某個完整資料夾（含 scripts、references、agents）到目標工作區 `.agents/skills/`，例如 `.agents/skills/data-analyst/`。不可只複製 SKILL.md。各技能帶有自己的執行資源，不需要先啟動其他技能；格式套件仍須安裝。references 內有獨立例檔或完整範例，根目錄 examples 是整套課程的練習。

## 選用：個人全域安裝

官方目前列出個人技能位置為 `$HOME/.agents/skills`。本專案不會自動寫入它。若確實需要全域使用，可先預覽：

```powershell
.\.venv\Scripts\python.exe tools/install_skills.py --target "$HOME/.agents/skills"
```

確認清單後自行加入 `--apply`。工具遇到同名目錄會拒絕整次安裝，沒有覆寫選項；先自行備份與判斷，不要盲目刪除既有技能。也可以將 --target 指向其他已授權工作區，做專案安裝。

來源：[OpenAI 官方技能文件](https://learn.chatgpt.com/docs/build-skills)。官方頁面可能調整 UI 或產品名稱；本講義以本機檔案、技能路徑與實際回報作為核對依據。
