---
name: data-analyst
description: 分析使用者提供的 CSV 或 XLSX 工作資料，以 Python 真實計算缺漏、型態、描述統計、IQR 異常、分組與日期趨勢，產生 Excel、Markdown 與圖表。適用於表格資料分析與檢核，不適用於純文件摘要、因果推論、預測或即時操控 Excel。
---

# Excel 資料分析助理

把可回算的數字和需要人判斷的解釋分開呈現。所有分析以原始資料為準，未知值不補零、異常列不刪除、不把觀察相關寫成因果。

## 啟動與不適用情境

- 自然語言：「幫我分析這份銷售 CSV 的缺漏與各區差異，產出 Excel 和圖表。」
- 明確指定：「使用 $data-analyst 分析這份 XLSX，檢查數字是否異常。」
- 純文字工作報告請使用文件／週報技能。PDF 表格請先核對轉成 CSV／XLSX。金融決策、因果推論與預測不在此腳本範圍。

## 工作流程

1. 確認來源檔、工作表、資料日期、每列代表的單位，以及要分析的數值與分組。可從檔案取得的資訊直接查看，只問會改變結果的缺漏。
2. 先檢視欄位，避免把員工編號、日期序號或郵遞區號當成業務數值。數字型態只代表格式，不代表業務意義。
3. 執行本技能自己的 `scripts/run.py`。只支援 UTF-8 CSV、XLSX，依賴 Python、openpyxl、Pillow。
4. 讀取 `analysis.json` 與原始資料，核對筆數、合計、排除列、缺漏、IQR 異常。根據資料量解釋趨勢；單一觀察點無法判斷趨勢。
5. 根據來源整理結論，分列「資料事實」「可能解釋」「待確認」。可能解釋需明確標為推測，不將程式統計當作完整語意分析。
6. 檢視圖表和 Excel 的文字、數值、單位與版面。靜態結果修改來源後須重新執行。若未開啟 Excel，不能宣稱完成 Excel 原生畫面驗收。

## 執行方式

在本技能資料夾內執行：

```powershell
python scripts/run.py --input "C:\資料\sales.csv" --output "C:\資料\分析輸出"
python scripts/run.py --input "C:\資料\sales.csv" --output "C:\資料\分組分析" --group-by category --value amount --date-column date
```

XLSX 可加 `--sheet "資料表"`；省略使用啟用工作表。日期趨勢欄位須為 YYYY-MM-DD 或 Excel 真實日期。指定分組／日期時必須同時指定數值 `--value`。

## 輸入與輸出規則

- 欄名不可空白或重複。空白列排除，空表明確拒絕。數值欄至少 60% 非空值可轉為有限數字；無效值仍保留並記錄來源列號。
- 產出 `analysis.json`、`analysis.md`、`analysis.xlsx`。有數值可用時另產 `chart.png`；以日期合計、分組合計、數值分布的順序選圖。PNG 最多顯示前 12 日期／組，完整資料保存在 Excel／JSON。
- IQR 採 inclusive 四分位，至少四筆且 IQR 大於零才標記異常。樣本只有一筆時標準差為 null。
- Excel 的外來公式字串會以安全文字保存，腳本不執行來源公式；需計算公式的檔案請先核對並匯出數值副本。
- 不同幣別、百分比和不同計量單位不可直接合計。資料未提供單位時列為待確認。
- 全部診斷與報告使用繁體中文；不寄送、不上傳、不連網、不修改原始檔。
- 請使用新的輸出資料夾；已有分析成果時明確拒絕，避免把舊圖表誤認成本次結果。

詳細契約與驗收見 [references/workflow.md](references/workflow.md)。完整模擬資料在工具包 `examples/data-analyst/`，其中 `sales.csv` 為正常例、`incomplete.csv` 為缺漏例、`invalid.csv` 為錯誤例；預期結果在 `expected.md`。單獨安裝本技能時可自行提供相同契約的 CSV／XLSX，不依賴其他技能。
