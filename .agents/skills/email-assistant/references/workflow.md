# 郵件內部資料契約

Codex 自行讀原信、判斷與整理，使用者只需提供原文或檔案。

`messages` 至少一封；sender、subject、date、body、source、deadline 為文字或 null。as_of、deadline 為 YYYY-MM-DD，未知可省略。actions 是需回覆／需執行／僅供參考／待確認陣列，可多選；priority 為高／中／低；priority_reason 說明依據；important 為摘要，reply_points 為已核對答覆文字陣列。

擬回信與修改回覆時，將使用者提供的回覆或要求納入 reply_points，保留不確定與承諾邊界。腳本草稿使用固定開頭及三種語氣；如需完整自然信件，Codex 依同一已核對內容再編輯 drafts.md，不能宣稱腳本本身可自由改寫語意。交付前重讀草稿核對。

直接輸入 EML／MBOX 只抽取非附件純文字；HTML-only、附件與編碼問題列待確認。規則初判不理解引文、否定、轉寄與相對期限，Codex 必須覆核，必要時建立核對後 JSON 再產檔。只有明確「期限：YYYY-MM-DD」會自動擷取日期。未提供基準日不判逾期，不阻擋摘要或草稿。

輸出 daily-summary.md、drafts.md、evidence.json，sent 必須是 false。沒有原信或答覆內容才問缺少部分，不要求固定表單。示範另見 demo.md，只有明確要求才讀。
