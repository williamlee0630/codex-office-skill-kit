# 郵件內部資料契約

Codex 自行讀原信、判斷與整理，使用者只需提供原文或檔案。

`messages` 至少一封；sender、subject、date、body、source、deadline 為文字或 null。as_of 為 YYYY-MM-DD；deadline 可為 YYYY-MM-DD 或 ISO 日期時間（例如 2026-10-26T17:00:00+08:00），輸出完整保留原期限，日期比較只用日期。未知可省略。`deadline_status` 為 confirmed（已確認）、requested（對方要求尚未承諾）、uncommitted（未承諾／性質待確認）、unspecified（未指定）；沒填時不自動認定已承諾。actions 是需回覆／需執行／僅供參考／待確認陣列，可多選；priority 為高／中／低；priority_reason 說明依據；important 為摘要，reply_points 為已核對答覆文字陣列。頂層 scope_note 記錄實際讀取範圍與缺漏，simulation=true 僅用於教學模擬。

擬回信與修改回覆時，將使用者提供的回覆或要求納入 reply_points，保留不確定與承諾邊界。腳本草稿帶入主旨及三種語氣；如需完整自然信件，Codex 依同一已核對內容再編輯 drafts.md，不能宣稱腳本本身可自由改寫語意。交付前重讀草稿核對。有時區的期限先換算台北日期作優先性初判，輸出保留來源原時間；無時區的時間不得自行宣稱時區已確定。

直接輸入 EML／MBOX 只抽取非附件純文字；HTML-only、附件與編碼問題列待確認。規則初判不理解引文、否定、轉寄與相對期限，Codex 必須覆核，必要時建立核對後 JSON 再產檔。只有明確「期限：YYYY-MM-DD」會自動擷取日期。未提供基準日不判逾期，不阻擋摘要或草稿。

輸出 daily-summary.md、drafts.md、evidence.json，sent 必須是 false。沒有原信或答覆內容才問缺少部分，不要求固定表單。示範另見 demo.md，只有明確要求才讀。
