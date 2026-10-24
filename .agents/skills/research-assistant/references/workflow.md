# 來源契約與完整練習

先將以下模擬文字存為 source.md：

```text
模擬甲方案，資料日期2026-10-01。
甲方案提供24個名額，包含一次課後諮詢。
```

同目錄儲存 input.json：

```json
{"question":"甲方案是否適合24人訓練？","as_of":"2026-10-23","sources":[{"id":"S1","title":"模擬甲方案","path":"source.md","published_at":"2026-10-01","kind":"模擬供應方資料","quality":"供應方自述，未經獨立查核"}],"claims":[{"text":"甲方案名額可容納24人。","kind":"fact","source_ids":["S1"],"excerpts":{"S1":"甲方案提供24個名額"}},{"text":"應先取得正式報價。","kind":"recommendation","source_ids":["S1"]}],"comparison":["只有單一方案，尚不能跨方案比較。"],"gaps":["總費用、日期與取消條款未提供。"]}
```

```powershell
python "<本技能路徑>/scripts/run.py" --input "input.json" --output "outputs/research"
```

預期：research-report.md 標明離線、模擬與資料日期，引用S1並列報價缺口；sources.csv 與 evidence.json 包含來源雜湊。不推論諮詢時數、效果或供應商排名。

sources[].path 相對於輸入JSON；支援TXT/MD/DOCX/文字型PDF。來源需唯一id、實際本機path；日期可null。url只是metadata，不會連線。線上工具實際讀取後可保存摘錄附url/accessed_at，回覆另外說明搜尋過程。

claims[].kind 為fact/interpretation/recommendation。每個fact要有source_ids及每個來源的逐字excerpts；腳本驗證摘錄存在，語意仍需核對。comparison、gaps是文字陣列，plan是調查方向文字。

缺漏：`{"question":"是否適用？","sources":[]}` 只產生資訊缺口。錯誤：只有url沒有path、重複或無效ID、摘錄不在原文都回傳非零，不編造來源。
