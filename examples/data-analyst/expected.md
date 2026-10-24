# 資料分析示範與預期結果（全部為模擬）

資料來源：本工具包原創模擬資料，日期 2026-10-01 至 2026-10-06。每列是一筆模擬交易，amount 單位為 TWD，units 單位為件。來源未說明高額原因，不得猜測活動、客戶或輸入錯誤。

在工具包根目錄執行：

```powershell
python .agents/skills/data-analyst/scripts/run.py --input examples/data-analyst/sales.csv --output output/data-analyst --group-by category --value amount --date-column date
```

預期產生 `analysis.json`、`analysis.md`、`analysis.xlsx`、`chart.png`，不修改來源。

- 正常 `sales.csv`：6 筆，amount 合計 33,900、平均 5,650、中位數 1,950；北區 4,800、南區 29,100。第 7 來源列的 25,000 超過 IQR 上限，保留且待核對。日期圖顯示 6 個觀察值。
- 不完整 `incomplete.csv`：amount 有效數字 3 筆、合計 600、缺漏 1、非有效值 1；日期缺漏／格式不符、分組缺漏皆保留。`--group-by category --value amount --date-column date` 的分組及趨勢排除列見 JSON，不能把缺漏補零。
- 錯誤 `invalid.csv`：非零結束，提示欄位名稱不可重複。`empty.csv`：非零結束，提示沒有可計算資料。
- 單點輸入：可產報告，樣本標準差為 null；不能推論趨勢。

可以給 Codex 的觸發提示詞：

> 使用 $data-analyst 分析 examples/data-analyst/sales.csv。這是模擬 TWD 銷售交易，每列一筆，依 category 分組、依 date 觀察 amount，檢查缺漏與異常，產生 Excel 和圖表。請把事實、可能解釋與待確認分開，不推論因果。

以上預期值用於程式驗證，不代表已完成自然語言觸發驗收。還要實際請 Codex 從原始 CSV 分析並開啟圖表核對。
