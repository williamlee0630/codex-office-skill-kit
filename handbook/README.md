# 離線講義維護說明

本網站為原創台灣繁體中文教材，版本 1.0.0。首頁、12 章及附錄共 14 頁，直接以瀏覽器開啟 `index.html`；不需本機伺服器、外部 JavaScript、字型或 CDN。所有練習情境均為模擬。

- `lessons.py`：十個技能的教學內容與原始模擬資料核對摘錄。
- `build.py`：以 Python 標準函式庫預先生成 HTML 與搜尋索引；學員閱讀時不必執行。
- `assets/style.css`：桌面、手機、鍵盤焦點與列印樣式。
- `assets/app.js`：章節導覽、全站搜尋與一鍵複製；包含 `file://` 複製替代方法。
- `assets/search-index.js`：建置時輸出完整搜尋資料，不透過 `fetch` 讀本機 JSON。

維護者於專案根目錄執行：

```powershell
python handbook/build.py
python -m unittest tests.test_handbook -v
```

下載連結指向發行工具產生的 `dist/office-skills-1.0.0.zip` 與 `dist/practice-data-1.0.0.zip`。完整發行 ZIP 包含以上兩個下載檔，避免網站下載連結因 ZIP 自我遞迴排除而失效。

自動化測試檢查章節、內容契約、本機連結、錨點與離線依賴，不能替代桌面／手機畫面、複製互動或 Codex 實際技能觸發與原文語意驗收。這些結果由主工作者分別記錄於 `docs/PROGRESS.md`。
