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
