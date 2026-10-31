# 本機財務運算與欄位規格

本頁由 Codex 維護；一般使用者只提供資料與需求。所有範例皆為教學模擬資料。

## 執行

在本機工作區虛擬環境安裝 `requirements.txt`，執行 `python scripts/run.py --input <原始資料或內部設定> --output <新輸出目錄>`。原始 CSV／XLSX／TXT 可加 `--mode statements|reconcile|variance`、`--other <另一來源>`、`--period YYYY-MM`、`--currency TWD`。TXT 支援逗號或 Tab 分欄；Markdown 支援有標題的表格。自由文字先保留原文再轉成有來源列號的表格。

內部 JSON 只指定來源與欄位，不接受已算好的報表數字。路徑相對於該設定檔；Codex 自行建立，學員不用填寫：

```json
{"mode":"reconcile","source":"internal.csv","other":"bank.csv","simulation":true,"date_tolerance_days":3}
```

`columns`／`other_columns` 將標準欄位映射到來源欄名，例如 `{"amount":"收付金額","reference":"流水號"}`；`sheet`／`other_sheet` 指定工作表。未指定時讀作用中的第一個工作表，報告記錄實際表名；多表帳本需明確選表。來源每個有效列保留檔名、工作表、原始列、原始值與 SHA256。

沒有必需欄位的列仍保留並列待確認，不自動視為零。金額可含千分位、括號負數；拒絕 NaN、無限值、非數值及未確認公式。所有核心運算使用 Decimal，原始精度累加後 ROUND_HALF_UP 輸出，通常兩位；JPY/KRW/VND/CLP 零位，BHD/KWD 三位。不換匯。只接受程式中明列的主要 ISO 幣別，其餘先確認並擴充幣別清單。輸出 Excel 用數值欄位；超出 Excel 15 位有效數字時以十進位文字保留精度，JSON 保留確切值。來源外來文字防止公式注入。

## 報表

`mode=statements`：`account` 科目、`class` 分類、`debit` 借方、`credit` 貸方、`currency`、`period`（YYYY-MM 或 YYYY）。支援中文欄名及分類。分類是 asset／資產、liability／負債、equity／權益、revenue／收入、expense／費用或成本。餘額表可用 `balance` 與明確 `direction=debit|credit` 取代借貸兩欄；不從科目名稱擅自推斷方向。總帳可同科目多筆累加，完整重複列標待查並保留總額。

資產與費用＝借−貸；負債、原始權益、收入＝貸−借；損益＝收入−費用；資產負債差額＝資產−負債−原始權益−本期損益。請確認來源是否為尚未結帳試算表；已結帳來源不應重複列入本期損益。來源已結帳而又含本期損益會產生差額，必須核對，不自動調整。

每幣別／期間各自核對，借貸不平、科目／方向缺漏、分類不足均不宣稱完整。`complete` 僅為輸入層級核對，不代表正式財報、完整揭露或會計查核。`accounting_standard` 可記錄使用者指定準則；未指定保留待確認。

現金流量表必須另有每列 `cash_flow_class=operating|investing|financing|noncash`、`cash_flow_amount`（非現金列明填 0），加設定 `cash_flow={"opening_cash":"0","closing_cash":"100","currency":"TWD","period":"2026-10"}`。所有列可完整分類且期初＋三活動淨流量＝期末，才編表；試算餘額本身不足以推導現金流量。

## 對帳

`mode=reconcile`，source 是內部、other 是銀行或另一來源。欄位：`date`、`reference`、`amount`（流入正、流出負，或借−貸）、`currency`、`counterparty`，`period` 可由有效日期推得。來源收付符號必須先確認；腳本不自動反轉銀行符號。缺日期／金額／幣別／期間列仍交付待確認，不配對。

同幣別同期間，雙方唯一識別碼、金額一致、日期差不超過 `date_tolerance_days`（預設 3，0–31），且對象不衝突，才確認。相同識別碼但金額不同列金額不符；識別碼金額一致而日期／對象衝突列疑似。無一致識別碼時，只有日期＋金額＋非空白對象的雙向唯一候選才列疑似。相同金額單獨不匹配。每列最多一對一使用一次。

同來源同期間幣別的重複識別碼，或無識別碼的完整重複列，全部隔離為疑似重複，不自動刪除。無配對內部列為「銀行或另一來源缺漏」；無配對銀行列為「內部帳務缺漏」。分幣期間原始合計包含重複列，並明示限制；不把隔離重複數字當作已核定餘額。

## 差異

`mode=variance`，單表欄位：`item`、`budget`、`actual`、`currency`、`period`，可加 `department`。中文預算／實際／幣別／期間可直接使用。

兩來源用 `amount`，source 永遠為比較基準、other 為本期／實際；`comparison=budget|month|year|department`。用項目＋幣別＋部門配對（department 模式跨部門但要求同期間）；保留雙方期間。重複候選不擅自聚合，缺另一方留待確認。預算與部門比較要求同期間；月份／年度比較允許不同期間，請由 Codex 根據使用者指明的兩份資料確認前後期。

差額＝實際−基準；百分比＝差額÷基準×100。零基準留空；負基準使用原始分母符號，金額增減方向另列。異常門檻 `anomaly_percent` 預設 20（百分比絕對值），零基準非零實際也標異常；異常原因無原始證據則列待查。不同幣別、雙方期間各自累加，僅包含可計算且無重複候選列。可從 `exact_base`、`exact_actual`、`exact_difference` 回算輸出。

## 示範

明確要求練習才讀 `references/demo/input.json`（銀行對帳）或 `references/demo/budget/input.json`、`references/demo/trial-balance/input.json`。模擬公司、交易、金額皆虛構。各資料夾 `expected.json` 為獨立列示的預期結果；`verify_expected.py` 直接讀三組來源，以另一套明確加總及配對清單驗算，不呼叫正式腳本。
