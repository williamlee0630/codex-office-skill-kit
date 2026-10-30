# 明確要求才使用的模擬示範

一般工作不讀本文件。只有使用者明確要求示範、練習或指定範例才進行；全部素材與成果標示「模擬教學」，另存新的示範資料夾。

本技能可獨立安裝，示範來源位於本文件旁的 demo/，不依賴課程根目錄。

先完整讀 demo/source.md 的原始模擬素材，按本技能規則自行判讀並整理新的內部資料，再執行產檔。demo/input.json 僅用來理解契約及比對，不得直接複製預填答案宣稱已獨立理解原文。

依 operation.md 檢查環境、選擇新輸出資料夾、實際執行並開啟核對。示範的查核日與週報期間只從示範需求／來源取得，不沿用到工作任務。

<details><summary>維護者：保留的舊版測試與契約示例</summary>

以下直接執行預填 JSON 僅為程式產檔測試，不代表完成原文語意示範。

# 明確要求才使用的模擬示範與測試

所有本文件示例均為模擬。請先讀原始資料，重新整理後產檔；不可把預填答案冒充原文判讀。一般工作不得讀取本文件代替使用者來源。

# 郵件契約與完整練習

將以下內容存成工作區 mail.json（模擬資料）：

```json
{"as_of":"2026-10-23","messages":[{"sender":"林範例 <training@example.invalid>","subject":"年度課程報價確認","date":"2026-10-23T09:00:00+08:00","body":"請回覆報價確認。期限：2026-10-26。","important":"確認報價，尚未承諾購買。","deadline":"2026-10-26","actions":["需回覆"],"priority":"中","source":"原始郵件第1行","reply_points":["名額與費用仍需內部確認。"]}]}
```

```powershell
python "<本技能路徑>/scripts/run.py" --input "mail.json" --output "outputs/mail"
```

預期：daily-summary.md 列中優先、需回覆、期限2026-10-26；drafts.md 含正式、友善、簡潔三種尚未寄送草稿；evidence.json 的 sent 是 false。不應承諾購買、交期或費用。

`messages` 至少一封，sender/subject/date/body/source/deadline 是文字或null；as_of/deadline 是有效 YYYY-MM-DD，未知可省略。actions 是需回覆／需執行／僅供參考／待確認的陣列，可多選；priority 為高／中／低，priority_reason 可填明確的重要性理由；reply_points 是已核對答覆文字陣列。

直接讀 EML：`python <技能路徑>/scripts/run.py --input inbox.eml --output outputs/mail --as-of 2026-10-23`。MBOX同理。只抽取非附件純文字內文；HTML-only及編碼問題列待確認。內文引用與否定句需要Codex覆核，規則不會可靠理解語意。只有明確「期限：YYYY-MM-DD」會自動擷取日期。

不完整測資 `{"messages":[{"body":"請回覆確認明細。"}]}` 會列寄件人、主旨、日期、期限待確認；`{"messages":"錯誤"}` 回傳非零。專案含 inbox.eml 與三封已整理 input.json；後者只是產檔測資，語意驗收從 source.md 重新開始。

</details>
