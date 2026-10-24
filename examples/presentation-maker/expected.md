# 簡報示範與預期結果（全部為模擬）

原始資料：`source.md`，資料日期 2026-10-23。`deck.json` 是供程式演練的已整理範例；自然語言驗收須由 Codex 重新讀原文整理，不能把預填 JSON 當成已完成語意整理。

在工具包根目錄執行：

```powershell
python .agents/skills/presentation-maker/scripts/run.py --input examples/presentation-maker/deck.json --output output/presentation-maker
```

預期產生 `presentation.pptx`、`speaker-notes.md`、`layout-check.json`。

- 正常例：共 4 頁，封面＋試辦目的＋已確認進度＋待確認與下一步。每頁標示模擬，每頁 notes 包含原文來源及日期。不出現捏造的績效百分比、預算或負責人。
- 不完整 `incomplete.json`：共 2 頁，日期與講稿標待確認。
- 錯誤 `invalid.json`：非零結束，指出缺少來源／內容頁。
- 長文 `too-long.json`：非零結束，指出文字過長需拆頁。不能靜默截斷。
- 原始 `source.md` 直接給腳本：明確拒絕，應先由 Codex 建立 JSON。

觸發提示詞：

> 使用 $presentation-maker 閱讀 examples/presentation-maker/source.md，為主管製作共 4 頁的試辦進度簡報，包含封面與講者備註。請由原始文件整理 deck JSON，再產生真正的 PPTX。資料全為模擬，未知人數、預算、日期及負責人保留待確認。

`structure_passed: true` 表示結構檢查通過，不等於畫面驗收。請開啟 PowerPoint 逐頁檢視字型、斷行、頁碼與 notes；未實際開啟時保留視覺檢查待人工確認。
