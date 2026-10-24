---
name: presentation-maker
description: 根據使用者的文件、工作報告或主題，先由 Codex 依來源安排頁面與重點，再用 Python 產生實際可編輯 PPTX、內嵌講者備註與版面結構檢查。適用商務簡報與內訓投影片，不以大綱代替 PPTX，不適用於無來源數據的自動補寫或既有複雜簡報樣板保真改版。
---

# AI 簡報製作助理

先依來源決定每頁要說什麼，再產生可編輯的 PowerPoint。腳本負責格式與可驗證結構，Codex 負責原始資料的語意整理。

## 啟動情境與邊界

- 自然語言：「把這份工作報告整理成主管看的簡報，附講者備註，給我真正的 PPTX。」
- 明確指定：「使用 $presentation-maker，以這份 Markdown 做內訓簡報。」
- 純大綱諮詢不必產檔。需保留複雜既有 PPTX 樣板時，先說明此腳本產生新簡報，不能宣稱保真改版。

## 工作流程

1. 確認受眾、目的、頁數與來源。預設採 16:9 商務文字版，內容頁 32pt 標題、24pt 內文，另加 1 頁封面。使用者指定總頁數時，內容頁數為總頁數減一。
2. 讀取原始 TXT／MD；DOCX／文字型 PDF 可用本技能 `python scripts/_office.py extract <來源> --output <文字檔>` 擷取。掃描文件需可用視覺工具或人工轉錄。
3. Codex 依原文建立有來源的 deck JSON。每頁只放一個主題，區分已確認事實、提議與未知。不得補造數字、負責人、日期、來源或已完成事項。
4. 執行 `scripts/run.py` 產生真正 PPTX。若長文字被拒絕，回到原文調整頁面並拆頁，不刪去重要限制、不靜默截斷。
5. 重新核對每頁與原文，檢查講者備註。`layout-check.json` 的結構檢查只驗證字量、物件邊界、頁數與 notes 存在。
6. 用可用的 PowerPoint 或渲染工具逐頁視覺檢查：字型替代、斷行、重疊與文字溢出。沒有渲染工具時明列「待人工開啟 PowerPoint 檢查」，不可宣稱畫面已驗收。

## JSON 契約與執行

```json
{
  "simulation": true,
  "title": "模擬內訓報告",
  "source": "source.md，第 1 至 3 段",
  "date": "2026-10-23",
  "slides": [{
    "title": "目前進度",
    "bullets": ["已完成模擬操作演練", "實際上線日期待確認"],
    "notes": "來源：source.md 第 2 段。請說明演練不等於正式上線。",
    "source": "source.md，第 2 段"
  }]
}
```

```powershell
python scripts/run.py --input "C:\資料\deck.json" --output "C:\資料\簡報輸出"
```

在本技能資料夾執行。需要 Python 和 python-pptx，不依賴其他技能、網路或 API 金鑰。腳本拒絕原始 TXT／MD 直接作為 deck，因為它不進行語意摘要。

## 缺漏與產出

- `title`、`source`、至少一頁 `slides` 必填。每頁 `title` 與 1 至 5 個 `bullets` 必填。`notes`、`date` 未提供時保留待確認，不自行創作講稿事實。
- 全形字計 2 寬度單位：頁標最多 54、每點最多 84、每頁所有重點合計最多 260。超量明確拒絕，請 Codex 拆頁。封面標題最多 72。
- `presentation.pptx` 包含封面、內容頁與內嵌 notes；`speaker-notes.md` 可另行閱讀；`layout-check.json` 保留結構檢查與未完成的視覺驗收。
- `simulation` 僅在確實為模擬資料時設為 true，會在每頁標示。來源及日期寫入講者備註。原始資料保持不變，不發布、不寄送。

詳細流程與驗收見 [references/workflow.md](references/workflow.md)。完整模擬資料在工具包 `examples/presentation-maker/`，先讀 `source.md` 再核對 `deck.json`；`incomplete.json`、`invalid.json`、`too-long.json` 供邊界演練，`expected.md` 列出預期產物。
