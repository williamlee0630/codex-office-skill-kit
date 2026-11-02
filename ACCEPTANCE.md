# v1.3.0 最新驗收（2026-11-02）

本次實際修改九個 Skill 規則、產檔程式、共用品質契約、講義來源及發行內容；正式數量仍為九個，講義仍為13頁。影片案例、啟動名稱、章序與七份輸入附件保留，v1.2.0 固定歷史下載見附錄。

本版請先看[成果與分層驗收](qa/quality-acceptance.md)、[自動化結果](qa/quality-tests.json)、[九技能實際成品與來源雜湊](qa/quality-artifacts.json)、[原生 Office 範圍](qa/quality-office.json)、[瀏覽器驗證](qa/quality-browser.json)及[獨立審查](qa/quality-review.md)。各章實際成果連結為來源核對與程式產檔，不冒稱全新對話全部通過。

Gmail 真實帳號讀取仍未測；創意新 Codex CLI 在600秒逾時且未取得必要成品。法務、財務的產檔可讀與內容／運算核對通過，完整新對話仍未驗證。客製化副本有獨立代理的八項行為測試與實際前後成果，但桌面／真實 CLI 載入仍未驗證。未把舊版成功、逾時、權限失敗或用量中斷改標成功。

部署屬另一關卡；實際提交、Actions 及正式下載結果以本次部署紀錄為準。

---

# 歷史：2026-11-01 講義流程更新

郵件章最新主示範已改成讀取已連接 Gmail，範圍與限制見 [Gmail 示範驗收](qa/gmail-demo-acceptance.md)。先前郵件貼文情境的通過結果保留為歷史，不代表新連接流程已端到端實測。

九章已改為完整提示詞與獨立附件入口；本次最新驗收請先看 [附件即用驗收](qa/attachment-first-acceptance.md) 與 [乾淨 Codex 測試記錄](qa/attachment-first-codex.json)。以下原有紀錄保留作歷史，不代表本次九項全部通過。


---

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
| 講義與ZIP | 13頁重建、九入口、搜尋／章序靜態測試、三ZIP之CRC、SHA256及完整包本機連結通過 | [最新ZIP檢查](qa/release-check.json)；完整包實際解壓103/103、技能包74/74適用測試通過，見 [解壓測試](qa/v1.2-extracted-tests.json)。公開部署及13頁HTTP、三ZIP實際下載均已通過；[公開結果](qa/v1.2-public-site.json)。 |

## GitHub與公開瀏覽器

功能提交 `322952f84e47d8bab7b9b1d7b86aa43b690ffe14` 已推送原main。既有Actions build及deploy均成功，雲端日誌實際103項測試通過（17.878秒）。[部署紀錄](qa/v1.2-deployment.json) · [Actions](https://github.com/williamlee0630/codex-office-skill-kit/actions/runs/41186582014)。

公開13頁HTTP均200、版本1.2.0；九技能入口、111筆搜尋索引及章節目標有效；三ZIP實際下載之CRC與SHA-256均符合正式站台manifest。瀏覽器實際法務搜尋、兩個啟動指令複製至剪貼簿、法務下一章到財務、手機選單展開及換頁收合通過。1280px桌面與390px兩新章無水平溢出；[瀏覽器紀錄](qa/v1.2-browser.json)。這些不替代以下未驗證項目。

## 未驗證與限制

- 桌面Codex完整安裝、裸名稱載入、補答及修改流程尚未完成；真實CLI遭環境政策阻擋，不由代理演練取代。
- 瀏覽器URL政策拒絕file://，未操作離線雙擊；靜態資源與相對連結已檢查，不等同實際離線畫面驗收。
- bundled DOCX renderer缺少soffice.exe，未完成逐頁PNG渲染；Word／Excel僅做上述原生抽查。
- 法務報告為AI初步審閱；引用存在不等於法律結論已證實。本次未進行最新法規查證。財務成果不是正式會計查核，不調帳或補造交易。

[正式講義](https://williamlee0630.github.io/codex-office-skill-kit/handbook/index.html) · [錄製準備](docs/RECORDING.md) · [v1.1.0歷史驗收](qa/v1.1.0-acceptance.md)
