# 研究內部來源契約

`question` 必填；`as_of` 為 YYYY-MM-DD 或 null。sources、claims、comparison、gaps 可為空陣列；plan 是調查方向文字。

sources 每項有唯一 id、title、本機 path、published_at（可 null）、kind、quality；可加 url、accessed_at。path 相對於內部輸入 JSON 所在目錄，也可用實際絕對路徑；支援 TXT／MD／DOCX／文字 PDF。由 Codex 自行保存實際讀取的線上摘錄及網址、發布／查閱日期，不能只填 URL 就當已讀。

claims 每項有 text、kind（fact／interpretation／recommendation）、source_ids、excerpts（來源 ID 到逐字摘錄）。每個事實主張必須引用已讀來源，摘錄需存在於本機來源且語意支持主張。ID、路徑、摘錄與格式錯誤由 Codex 先修復；不能虛構來源來通過驗證。

腳本只做離線核對與產檔，evidence.json 的 network_used=false 描述的是腳本。若 Codex 另用了搜尋工具，另保存 search-log.md，記錄實際工具、查詢、成功／失敗及查閱日期，並在研究報告清楚說明線上查讀與本機核對的範圍；不改稱腳本已搜尋。沒有來源時只有缺口報告，不能宣稱調查已完成。

產物 research-report.md、sources.csv、evidence.json。未知日期不宣稱最新；資訊衝突並列，不拿教學結論或模擬限制代替工作問題。示範另見 demo.md，只有明確要求才讀。
