# v1.2.0 錄製示範準備

使用工具包完整解壓後的專案技能，或複製完整技能資料夾到錄製用工作區。不要覆寫既有全域同名技能。課程主線只需啟動、附檔、展示成果，不讓觀眾操作 Python 或 JSON。

## 法務四分鐘

1. 開啟 Codex，在錄製用工作區輸入 `$legal-reviewer`。
2. 附上 [風險服務合約 DOCX](../examples/legal-reviewer/風險服務合約.docx)，說「這是教學模擬資料，請站在甲方審查商業風險，法域尚待確認；請直接交付審查成果，無法查證現行法律時明示限制。」
3. 展示合約審查報告.docx、合約風險清單.xlsx、條款修訂建議.md。先看風險摘要，再對照原始條款位置及可協商修訂文字。
4. 核對未承諾法規已查證、未把高風險等同違法、未知天數及法域留待確認。可用 [文字 PDF](../examples/legal-reviewer/風險服務合約.pdf) 或 [正常合約](../examples/legal-reviewer/正常服務合約.docx) 做延伸對照。

[模擬預期結果](../examples/legal-reviewer/預期審查結果.md) 僅供教師事先核對；不交給 Codex 代替讀原件。實際語意審閱的風險數量可能與固定迴歸資料不同，必須以原文與判斷理由驗收。

## 財務四分鐘

1. 輸入 `$finance-assistant`。
2. 一起附上 [公司帳 CSV](../examples/finance-assistant/reconciliation/internal.csv) 與 [銀行明細 CSV](../examples/finance-assistant/reconciliation/bank.csv)，說「這是教學模擬資料，幫我對這兩份2026年10月TWD明細，不修改原帳，交付Excel結果與報告。」
3. 開啟銀行對帳結果.xlsx，展示六種分類、來源列及差額；同額交易不直接確認，重複列與未匹配仍保留。
4. 想改展示重點，可改附 [預算實際 XLSX](../examples/finance-assistant/budget/budget-actual.xlsx) 說「分析預算與實際差異」，或附 [會計試算表 XLSX](../examples/finance-assistant/trial-balance/trial-balance.xlsx) 說「編製可核對的財務工作底稿」。展示零基準百分比空白、借貸與資產負債檢查。

三組素材與獨立預期結果見 [財務素材說明](../examples/finance-assistant/README.md)。正式錄影前先在實際桌面 Codex 做一次完整流程；本次自動化、代理、CLI及原生畫面驗收的可用範圍以 [驗收](../ACCEPTANCE.md) 為準。

## 三十分鐘路線

3分鐘概念與安裝、14分鐘七個既有技能成果、4分鐘法務、4分鐘財務、4分鐘修改技能、1分鐘總結。網頁各章延伸自學時間不等於影片片長。
