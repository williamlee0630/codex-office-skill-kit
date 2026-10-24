# 獨立最終驗收審查

日期：2026-10-24（Asia/Taipei）｜版本：1.0.0｜資料：本次重現資料全為模擬

## 結論

本次獨立審查找到兩項已實際重現的 Important 程式缺陷，以及一項公開前必須確認的 Important 隱私風險；未發現已實證的 Critical 問題。兩個缺陷應修正並補回歸測試，再依發布內容重新掃描私人資訊。本報告是審查當時的觀察，主工作者之後的修正與發布驗證應另外記錄，不把本報告當作已修正證據。

技能大致清楚區分 Codex 的語意判讀與 Python 的驗證、計算和產檔。講義、README 與驗收文件也有區分程式測試、明確指定技能、自然語言路由及 Office 畫面驗收，沒有將這些關卡混寫成全面通過。

## 審查範圍與限制

- 靜態審查：AGENTS.md、README.md、docs/ACCEPTANCE.md、十支技能的 SKILL.md 與 scripts/run.py、一份共用 scripts/_office.py 的完整內容及十份副本雜湊、七個現有自動化測試模組與 tests/manual/trigger-cases.md、handbook 的來源與生成頁面、互動 JavaScript。講義以首頁、入門、附錄、自建技能章的完整文字，以及十個技能章的流程、可複製提示、命令與驗收內容交叉核對。
- 實際執行：僅本報告下列兩個針對性重現；模擬檔案與結果留在 tests/.tmp/final-audit-20261024/。未修改主產品、全域技能或舊課程儲存庫，未發布或寄信。
- 隱私檢查：限定 docs/qa 中可讀的文字類檔案，以檔名及命中行數回報，不抄錄實際私人路徑。沒有讀取權杖、全域私人設定或其他帳號資料。
- 依分工未重跑既有 55 項測試；這由主工作者執行。也未重做十支自然語言路由、真實 Gmail、公開網路研究、OCR、Office 逐頁渲染及學員一般瀏覽器 file:// 操作。
- 初學者講義改寫與 Pages 相對路徑打包正在由主工作者進行，本報告不把尚在施工的內容當作未實作缺陷。未審查其尚未定版的發布腳本、最終 Git 索引、遠端 Git 歷史或最終下載 ZIP；不能據此宣稱公開發布已無私人資訊。

## Important：抽取命令可覆寫原始 DOCX

位置：.agents/skills/meeting-assistant/scripts/_office.py:174–181。審查時十份共用副本的 SHA-256 相同，因此相同問題存在於十支技能攜帶的抽取工具。

重現：在暫存資料夾建立含「模擬原始文件，應保持 DOCX 格式。」的有效 DOCX，呼叫：

```powershell
python .agents/skills/meeting-assistant/scripts/_office.py extract tests/.tmp/final-audit-20261024/simulated-original.docx --output tests/.tmp/final-audit-20261024/simulated-original.docx
```

實際結果：回傳碼 0；來源檔雜湊改變，原本可解析的 DOCX ZIP 被純文字覆寫，zipfile.is_zipfile 回傳 False。main 直接把 read_text 的結果交給 write_markdown，沒有比較輸入與輸出的實際路徑。run.py 的 protect_input 無法保護這個獨立 CLI。

影響：一次輸出路徑誤填即可破壞唯一原始文件，與技能要求保留原始資料的流程不符。

建議驗收：在共用來源修正，先比較輸入／輸出的 resolve 路徑；同路徑或等價相對路徑須拒絕，來源位元組保持不變，再同步十份副本。補 CLI 行為測試，包含有效 DOCX、文字來源與正常不同輸出路徑。

## Important：附加 EML 的內文被當成主信，產生錯誤待辦

位置：.agents/skills/email-assistant/scripts/run.py:23–26（parse_message）。

重現：建立一封主信，內文只有「本信僅供參考，附件待另行核對。」；附加一份 message/rfc822 類型的 attached-message.eml，附件內文為「請提交附件內的模擬資料。截止：2026-10-24」。以 2026-10-24 為基準日執行郵件技能。

實際結果：回傳碼 0；evidence.json 的主信 important 同時含主信與附件內文，actions 為「需執行」，deadline 為 2026-10-24。這與主信的「僅供參考」不符。

原因：message.walk 會深入附加郵件；程式只檢查每個純文字子 part 自己的 Content-Disposition，沒有排除祖先已是 attachment 的整個子樹。附加 EML 裡的 text/plain 通常沒有自己的 attachment 標記，因此被收進主信。

影響：SKILL.md 宣告 EML/MBOX 僅讀非附件純文字內文，附件須另確認；實際卻把附件中的工作和期限當成主信要求。這不是單純關鍵詞語意誤判，而是解析範圍超出所宣告的邊界。

建議驗收：父層為附件時跳過整個 MIME 子樹，並補附加 EML、一般文字附件及正常 multipart/alternative 的測試。附件仍可另走明確授權閱讀流程，但不能混入主信內文。

## Important：歷史 QA 不適合直接加入公開儲存庫

這是發布前風險，尚未斷言資料已上傳。審查時以下八個文字檔合計 71 行含本機使用者絕對路徑：

| 檔案 | 命中行數 |
| --- | ---: |
| docs/qa/behavior-artifacts.md | 11 |
| docs/qa/behavior-information.md | 10 |
| docs/qa/environment.json | 1 |
| docs/qa/examples-results.json | 3 |
| docs/qa/trigger-meeting-events.log | 11 |
| docs/qa/trigger-meeting.txt | 2 |
| docs/qa/behavior-foundation/run-logs.json | 25 |
| docs/qa/office-render/open-results.json | 8 |

本次限定掃描未找到非範例網域的電子郵件地址；這不代表所有檔案、二進位成果或 Git 歷史都沒有私人資訊。

另外，資料分析腳本把 resolve 後的來源路徑寫進 analysis.json，並寫進 analysis.xlsx 的「原始資料」工作表；收據摘要與研究證據也保存絕對路徑。因此重新產出的 examples／outputs 成果可能重新帶入主機路徑。保留本機證據有其用途，但公開範例需要去識別。

建議發布關卡：採公開檔案白名單，排除內部原始事件日誌及未去識別的 QA；公開驗收摘要的連結需指向可公開的證據或清楚說明內部保留。掃描實際待提交內容與每份 ZIP，也解開 DOCX/XLSX/PPTX 的 XML 檢查。只掃文字副檔名或只建立 Pages 白名單，不能證明 GitHub 儲存庫與下載包也安全。

## Minor：兩支技能的人工檢查步驟寫到未提供的 DOCX

.agents/skills/project-tracker/SKILL.md:16 與 .agents/skills/idea-generator/SKILL.md:16 均要求「DOCX 檢查可開啟及畫面版面」，但前者產物為 MD/CSV/XLSX/JSON，後者為 MD/CSV/JSON。建議改為各技能實際產物的開啟檢查，以免初學者誤以為少了 Word 檔。

## 可保留的驗收界線

docs/ACCEPTANCE.md 已清楚保留 Word 視覺驗收、九支尚未獨立自然路由、一般瀏覽器 file://、真實 Gmail／網路與 OCR 的未完成或不提供範圍。這些不能被本次靜態審查或兩項重現自動改列通過。初學者能否獨立完成，仍需以定版後的講義和完整解壓縮包完成一次實際操作記錄。

## 修正與後續驗收回覆（2026-10-24）

- 來源覆寫與附件EML問題均先新增測試確認失敗，再修正並通過；共用副本已同步十份。
- 兩項不存在DOCX的說明已更正。公開白名單、UTF-8／UTF-16與ZIP／OOXML掃描、範例去識別均有回歸測試；原始QA留本機。
- 修改後完整72項程式測試通過；十項自然選擇已觀察，完整工作流程仍有未完成項。此段為維護者回覆，不冒充獨立審查者重新執行的終審。
- 最新範圍與缺口以根目錄ACCEPTANCE.md及qa/natural-trigger-results.json為準。
