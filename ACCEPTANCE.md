# v1.2.0 驗收

日期：2026-10-31（台北）。本版為九技能改版；下列程式、代理、真實CLI、原生Office及網站驗證分開列示。未知或未實測項目不當作通過。

## 修改與範圍

保留 email-assistant、receipt-organizer、presentation-maker、document-writer、data-analyst、idea-generator、research-assistant；新增 legal-reviewer 與 finance-assistant。移除 meeting-assistant、project-tracker、weekly-report 的技能執行目錄、範例及最新入口。未修改全域安裝或其他課程，初始工作樹乾淨。

## 已執行的驗收

| 層級 | 實際結果 | 證據與界線 |
|---|---|---|
| 改版前基準 | UTF-8環境77/77通過 | 首次裸命令遇CP950子程序解碼錯誤後中止，重跑既有verify入口通過。 |
| 最終自動化 | unittest及verify各103項通過，0失敗、0錯誤、0略過 | [機器結果](qa/v1.2-tests.json)；涵蓋保留七技能回歸與獨立複製執行。 |
| 法務程式 | 9項測試通過；正常／風險DOCX、文字PDF、貼文、引用、未知法域、缺漏、未核法源、OCR及防覆寫 | 固定JSON的產檔回歸不等於語意判讀。 |
| 法務獨立完整流程 | 僅讀raw DOCX，獨立建立11項風險、9類分析及具體修訂；33筆引用回查，三檔實際開啟核對 | [完整代理紀錄](qa/v1.2-legal-behavior.json)。風險數量依語意判斷可與固定案例不同；未執行現行法規查證。 |
| 財務程式 | 14項測試通過，含大額精度、KWD3位、原始行號、零／負數、缺漏、不平衡、跨期間與幣別、現金流量條件 | XLSX金額與分類均有斷言，非僅檔案存在。 |
| 財務獨立完整流程 | 三組raw來源；339項核對、229個原始儲存格、37列來源保留；最終程式重播通過 | [完整紀錄](qa/v1.2-finance-behavior.json)。TWD預算169100.10、實際206800.21、差額37700.11；借貸各450000、損益100000。 |
| 獨立審查 | CSV漏列／行號及三位小數顯示的三項重現缺陷已修正、獨立複驗 | [審查與主代理補充](qa/v1.2-review.md)。 |
| 九技能範例 | tools/run_examples.py 九項實際產檔成功 | 標示模擬；輸出之本機路徑已以既有sanitize機制轉可攜式相對來源。 |
| 名稱引導代理演練 | 法務／財務短引導符合規則；完整需求不重問功能選項 | 屬代理演練，不冒稱真實產品新聊天已通過。 |
| 真實Codex CLI啟動 | **兩項未通過**：內部讀SKILL.md遭環境執行政策拒絕 | [真實失敗紀錄](qa/v1.2-startup.json)。回合結束非成功；未繞過政策。 |
| DOCX／XLSX內容 | 函式庫重開與來源、數字、修訂文字核對通過 | 原生Word首頁／末頁、Excel對帳前列抽查可讀；[原生抽查](qa/v1.2-office-smoke.json)。不是全頁全表視覺保證。 |
| 模擬PDF畫面 | 兩份合約使用內嵌字型，Poppler單頁圖像檢視可讀 | PDF文字擷取及引用測試通過；掃描頁明確回報OCR限制。 |
| 講義與ZIP | 13頁重建、九入口、搜尋／章序靜態測試、三ZIP之CRC、SHA256及完整包本機連結通過 | [最新ZIP檢查](qa/release-check.json)；完整包實際解壓103/103、技能包74/74適用測試通過，見 [解壓測試](qa/v1.2-extracted-tests.json)。公開部署結果另列。 |

## 未驗證與限制

- 桌面Codex完整安裝、裸名稱載入、補答及修改流程尚未完成；真實CLI遭環境政策阻擋，不由代理演練取代。
- 瀏覽器URL政策拒絕file://，未操作離線雙擊；靜態資源與相對連結已檢查，不等同實際離線畫面驗收。
- bundled DOCX renderer缺少soffice.exe，未完成逐頁PNG渲染；Word／Excel僅做上述原生抽查。
- 法務報告為AI初步審閱；引用存在不等於法律結論已證實。本次未進行最新法規查證。財務成果不是正式會計查核，不調帳或補造交易。

[正式講義](https://williamlee0630.github.io/codex-office-skill-kit/handbook/index.html) · [錄製準備](docs/RECORDING.md) · [v1.1.0歷史驗收](qa/v1.1.0-acceptance.md)
