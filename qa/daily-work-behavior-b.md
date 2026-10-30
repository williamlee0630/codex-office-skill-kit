# Revised office skill rehearsal B

## Scope and method

This is an independent agent rehearsal against the currently edited repository, not an installed-Codex end-to-end test. I read each of the following skills' `SKILL.md`, `references/operation.md`, and `references/workflow.md`: presentation-maker, document-writer, data-analyst, idea-generator, research-assistant. I also read each `references/demo.md` solely to evaluate the explicitly requested demo cases. After a maintainer update during the rehearsal, I rechecked all five demo files and included raw source files; fixed/current status is recorded below. No repository files were edited by this agent. All paths in this report are relative or symbolic, with personal filesystem prefixes removed.

Each skill has eight cases below. Case 2 independently tests the first natural-language response for an unsolicited mode/menu, in addition to case 1's bare invocation. These are verbatim next-response rehearsals, not assertions about how an unobserved installed model behaved. Except for data case 3, responses that start work are the next conversational message before internal source preparation and file-generation tools; they do not claim uncreated files exist. Only the separate data task was actually executed. All people, organizations and work scenarios below are synthetic; ordinary-work cases are phrased as ordinary user requests to test that an assistant would not incorrectly label real user work as a demo. Dates in new work content differ from bundled example dates.

Assessment labels: **Pass (rehearsal)** means the actual response written here follows the revised instructions. It does not establish installed trigger reliability, tool execution or Office visual acceptance. **Gap** means a remaining concrete ambiguity or broken internal path was observed.

## 1. presentation-maker

### P1 — Bare skill invocation

User: `$presentation-maker`

Actual next response:

> 請提供要做成簡報的工作素材，並說明要給誰看、希望對方了解或決定什麼；已有草稿也可以直接提供。

Evaluation: **Pass (rehearsal)**. One natural-language prompt. No classroom mode, demo/data selection, numbered menu, Python setup instruction, MD-reading request or JSON form.

### P2 — First natural-language response / unsolicited-mode audit

User:「我要在下週營運會議報告客服排班試辦，幫我做成主管看的簡報。」

Actual next response:

> 請貼上客服排班試辦的紀錄或草稿，尤其是目前做法、觀察到的結果，以及希望主管決定的事。我會依素材整理成精簡簡報。

Evaluation: **Pass (rehearsal)**. Requests missing source facts, not a mode choice. Does not ask the user to find a skill path, supply a script or confirm starting.

### P3 — Complete raw work request

User:

> 這是2026-11-09客服主管的工作紀錄。給營運主管看，請做5頁含封面的PPTX，附講者備註，目的是決定是否延長試辦。11月2日至6日，晚班改為兩人輪值，記錄48件詢問，首回覆中位數18分鐘；前週為31分鐘，但前週沒有記錄案件類型，不能直接歸因排班。兩位同仁反映交接表重複填寫。建議再試兩週，先把交接欄位合併。延長是否核准、誰負責合併欄位都還沒決定。

Actual next response:

> 我會做成含封面的5頁簡報，依序呈現試辦做法、48件詢問與回覆時間、交接問題，以及延長試辦的待決事項。前週案件類型未記錄的限制會保留；延長兩週會標為建議，核准狀態與欄位負責人列為待確認，並附來源與講者備註。

Evaluation: **Pass (rehearsal)**. Starts directly. Correctly counts cover in total and retains the causal limitation, proposal status, unknown owner and approval. Does not re-ask audience/date/page count.

### P4 — Essential source missing

User:「請把剛才那份附件做成給採購主管決定是否續約的簡報。」No attachment or prior source is readable in this test conversation.

Actual next response:

> 我目前沒有讀到附件。請附上文件或貼上續約相關內容；我會沿用給採購主管決定是否續約的目的整理簡報。

Evaluation: **Pass (rehearsal)**. Does not invent contract terms or substitute an example. Only asks for the essential unreadable source, preserving the already-known audience and purpose.

### P5 — Optional metadata missing

User:

> 給倉庫主管看，說明為何需要先試行退貨分類。現在退貨先堆同一區，現場同仁要重新找品項；目前沒計時資料。建議先分「可重售、待檢、報廢」，用既有層架，試行是否核准仍待主管決定。做成簡報即可。

Actual next response:

> 我會依這些內容安排精簡的16:9簡報，將現況、三類分類建議、既有層架限制及待核准事項分開呈現。沒有計時資料就不寫節省工時；資料日期標為未提供，講者姓名不影響製作。

Evaluation: **Pass (rehearsal)**. No request for title, filename, output folder, speaker, date or page count. Does not replace the unknown source date with execution date.

### P6 — Clarification follow-up to P4

User:

> 附件改貼這裡：2026-11-16，甲物流目前每月固定費18,000元，臨時加車另計。最近兩次加車的費用還沒對帳。合約11月30日到期；採購建議延長一個月，這只是建議，續約尚未核准。

Actual next response:

> 我會接續製作給採購主管決定續約的簡報，保留每月固定費18,000元、加車另計、兩次費用未對帳及11月30日到期。延長一個月會列為待決建議，不寫成已核准；未對帳費用不補估。

Evaluation: **Pass (rehearsal)**. Continues original task without reintroducing the skill or asking whether to start. Preserves user source date and conditions.

### P7 — Ordinary work while demos exist

User:

> 把這段做成內訓簡報：2026-11-23的新版出貨規則是先核對訂單編號，再掃商品碼；品項不符就放待查區，不得直接出貨。給新進同仁看，讓他們記住操作順序。沒有指定頁數。

Actual next response:

> 我會依新進同仁的操作順序安排精簡內訓簡報，清楚呈現核對訂單、掃商品碼及品項不符時放入待查區的步驟，並把「不得直接出貨」放在異常處理頁的重點。

Evaluation: **Pass (rehearsal)**. Uses only supplied work facts, no demo path or example claims. Does not label this ordinary work as 模擬 merely because the toolkit has demos.

### P8 — Explicit new demo

User:

> 請示範一次，用這份模擬紀錄：2026-12-07，模擬門市測試電子取號，有12位受測者；其中2位需要店員協助。沒有測量等候時間。做一份給店長看的簡報，請明確標模擬。

Actual next response:

> 我會用這份模擬紀錄製作示範PPTX並標示模擬，呈現12位受測者中2位需要協助，以及未測量等候時間的限制；不寫成已證明縮短等候時間。講者備註也會保留資料日期與限制。

Evaluation: **Pass (rehearsal)** for explicit demo gating and new source. **Initially observed gap, now fixed and rechecked**: the first-read demo lacked its own raw-source path. Current `references/demo.md` now explicitly directs Codex to read included `demo/source.md`, independently derive new input, and treat `demo/deck.json` only as contract/reference material. Both files exist. Portable demo source discovery is no longer an open finding; no bundled demo execution was performed here.

## 2. document-writer

### D1 — Bare skill invocation

User: `$document-writer`

Actual next response:

> 你想撰寫企劃、提案、信函或工作報告，還是修改現有文件？請提供素材或草稿，並說明希望達成的目的。

Evaluation: **Pass (rehearsal)**. Natural short prompt; document types are examples within a question, not selectable course modes or numbered choices.

### D2 — First natural-language response / unsolicited-mode audit

User:「我想請你把給合作廠商的說明寫得正式一點。」

Actual next response:

> 請貼上原稿，或說明要向合作廠商交代的事情及希望對方採取的行動，我會整理成正式文字。

Evaluation: **Pass (rehearsal)**. Asks for essential content, not demo versus own-data selection. No environment questions.

### D3 — Complete raw work request

User:

> 幫我寫給廠商的正式通知及精簡版，請產DOCX。2026-11-10紀錄：原本11月18日交12組展示架，目前樣品卡在表面處理。請廠商11月12日前回覆可交日期和分批方案；這是我們希望的回覆期限，不代表廠商已承諾。採購已確認訂單數量12組，但沒有同意加價。不要寫違約或賠償。

Actual next response:

> 我會整理正式版與精簡版並產出DOCX，保留12組、原訂11月18日交貨及表面處理待完成的情況。通知會請廠商於11月12日前回覆可交日期與分批方案，將其寫成我方要求；不加入廠商已承諾、同意加價、違約或賠償等主張。

Evaluation: **Pass (rehearsal)**. Starts work, retains deadlines' modality and all important commercial restrictions. Does not ask for a recipient name that can remain unknown.

### D4 — Essential facts missing

User:「請寫一封退款通知給客戶。」No transaction, reason or refund decision is supplied.

Actual next response:

> 請提供退款原因，以及目前已確認可通知客戶的退款決定；若金額或入帳時間尚未確定，我會保留待確認，不先承諾。

Evaluation: **Pass (rehearsal)**. Needs essential decision/context, not a complete intake form. Does not invent eligibility or processing time.

### D5 — Optional metadata missing

User:

> 幫我整理一份給主管確認的提案：每月一次用現有晨會最後15分鐘分享客服常見問題，不加購軟體；先試辦兩次再決定是否常態化。時間與負責人還沒定。請有正式版和精簡版。

Actual next response:

> 我會以「客服常見問題分享試辦提案」為題，整理正式版與精簡版，保留現有晨會15分鐘、不加購軟體及先試兩次的條件。日期、負責人與核准狀態會列待確認，不影響先完成草案。

Evaluation: **Pass (rehearsal)**. No metadata blocking; source date remains unknown. Does not add a fabricated budget, cost benefit or owner.

### D6 — Clarification follow-up to D4

User:

> 是重複付款，財務在2026-11-17已核准退回多付的1,250元，入帳日期還沒確認。客戶稱謂先寫您好，不要要求他再提供資料。

Actual next response:

> 我會接續撰寫退款通知，以「您好」開頭，說明重複付款的1,250元已獲核准退回；入帳日期尚未確認，不承諾固定天數，也不向客戶索取資料。正式版與精簡版會使用相同事實。

Evaluation: **Pass (rehearsal)**. Uses original document goal and follow-up facts, no restart or selection question. Does not convert refund approval into completed bank transfer.

### D7 — Ordinary work while demos exist

User:

> 修順這段給內部同仁的通知：2026-11-24下午盤點，這次只盤展示區，不盤倉庫；展示區下午3點起暫停取貨，恢復時間未定，請先把急件交接給值班窗口。窗口姓名還在排班，別補名字。

Actual next response:

> 我會整理成清楚的內部通知，保留僅盤展示區、下午3點起暫停取貨、恢復時間未定及急件先交接的限制；值班窗口姓名列為待確認。

Evaluation: **Pass (rehearsal)**. No bundled “工作技巧分享” content leaks into the new source. No simulation label or demo offer.

### D8 — Explicit new demo

User:

> 請用模擬情境示範正式與精簡兩版通知：2026-12-08模擬辦公室要更換印表機，當天上午10點至11點暫停列印；不能承諾提早恢復。

Actual next response:

> 我會用這份模擬情境製作正式與精簡兩版通知，兩版都標示模擬，保留12月8日上午10點至11點暫停列印的時段，不承諾提早恢復，並產出Markdown與DOCX供比對。

Evaluation: **Pass (rehearsal)**. Explicit demo authorizes simulated source. Current portable demo entry points are `references/demo/source.md` and `demo/input.json`; source-first instructions explicitly prohibit copying prefilled answers as semantic acceptance. The next response uses the new supplied scenario rather than silently swapping examples.

## 3. data-analyst

### A1 — Bare skill invocation

User: `$data-analyst`

Actual next response:

> 請提供要分析的CSV或Excel表格，也可以貼上表格內容。你最想了解什麼？若還沒有特定問題，我會先檢查資料品質與主要數值。

Evaluation: **Pass (rehearsal)**. No forced question when the user has no specific analysis goal; no mode or template menu.

### A2 — First natural-language response / unsolicited-mode audit

User:「我有一份出貨表，想知道哪裡要注意，但還不知道要看哪個指標。」

Actual next response:

> 請提供出貨表或貼上表格，我會先查看欄位和樣本，檢查缺漏、重複及有業務意義的數值，再整理需要注意的地方。

Evaluation: **Pass (rehearsal)**. Requests the essential table, not field names the assistant can later inspect. Does not demand metric selection or suggest a demo.

### A3 — Complete new raw request; actually executed

User request saved as `behavior-b-data/request.md`:

> 請分析這份已結算服務收入；每列是一筆交易，淨收入是新台幣且負數為沖銷。檢查缺漏，分服務區比較，並按結算日看觀察值，產出Excel與圖表。record_id只是交易編號，不是績效。

Raw source saved as new synthetic `service-revenue-raw.csv`:

```csv
record_id,settled_date,service_region,net_revenue_twd
8101,2026-11-02,北區,2400
8102,2026-11-02,南區,1800
8103,2026-11-03,北區,-200
8104,2026-11-03,南區,3200
8105,2026-11-04,北區,
8106,2026-11-04,南區,2600
8107,,北區,1200
8108,2026-11-05,,700
```

Actual next response before tools:

> 我會以新台幣淨收入作業務數值，按服務區與結算日分析，保留沖銷負數與缺漏。交易編號只用來追溯來源；我會在另存的分析副本排除編號欄，保留原始列號對照，再產出Excel與圖表。

Verified result response after actual execution:

> 8筆交易中有7筆有效淨收入，合計新台幣11,700元。北區合計3,400元、南區7,600元；另有700元缺少服務區，因此未納入分區合計。日期圖納入有結算日的10,500元，缺少日期的1,200元未放入日期觀察值。
>
> 淨收入、服務區、結算日各缺1筆；缺漏未補零、負200元沖銷保留。Excel與圖表已產生，交易編號未當成績效。已重新讀回Excel並檢查圖表；尚未以原生Excel開啟檢查畫面。

Evaluation: **Pass (actual script task + agent semantic selection)**. Correct measure chosen, not numeric-ID sum64,836. Artifacts and verified calculations are detailed below. This proves one isolated script task, not installed automatic routing.

### A4 — Essential unit ambiguity

User:

> 幫我比較以下兩組的收入，不用問我欄位：
> `日期,組別,收入`
> `2026-11-11,A,1000`
> `2026-11-11,B,800`
> `2026-11-12,A,1200`
> 來源說部分是新台幣、部分是美元，但沒有標各筆幣別。

Actual next response:

> 表格有3筆、收入欄沒有空值，但目前無法比較或加總混合幣別。請補上各筆幣別；拿到後我會分幣別比較A、B組，不直接把新台幣和美元相加。

Evaluation: **Pass (rehearsal)**. Asks a conclusion-changing essential, while completing independent quality observations. “不用問欄位” does not authorize invented units or exchange rates.

### A5 — Optional metadata missing

User:

> 這張表每列是一張工單，工時單位是小時。幫我看缺漏和部門差異，沒有特別的報告名稱：
> `工單號,部門,處理工時`
> `601,客服,2`
> `602,維修,3.5`
> `603,客服,`
> `604,維修,1.5`

Actual next response:

> 我會以處理工時分析缺漏與部門差異，工單號作識別用途。資料日期未提供就保留未提供，不影響本次分組統計；報告名稱與輸出位置採預設。

Evaluation: **Pass (rehearsal)**. Does not ask for date, title, sheet name or column names. No date trend inferred from IDs.

### A6 — Clarification follow-up to A4

User:「剛剛來源註記寫錯了，三筆收入都是新台幣，每列是一張已入帳發票。」

Actual next response:

> 我會接續按已入帳發票比較，以新台幣計算：A組兩筆合計2,200元，B組一筆800元。接著依同一份表產出檢核、分組結果與圖表，不套用匯率。

Evaluation: **Pass (rehearsal)**. Carries forward table, grouping and goal; arithmetic is directly supported. Does not re-ask file, fields or whether to begin.

### A7 — Ordinary work while demos exist

User:

> 這是2026-11-25匯出的加班彙總，每列一位同仁當週總時數。請看各單位合計；編號不是工時。
> `員編,單位,加班時數`
> `2301,倉務,4`
> `2302,客服,2`
> `2303,倉務,1`

Actual next response:

> 我會按單位加總加班時數，員編只保留作來源對照；倉務合計5小時、客服2小時。這是同一週的彙總，不能據此推論上升或下降，我會產出分組分析與圖表。

Evaluation: **Pass (rehearsal)**. Actual source fields used; no category/amount/date demo arguments copied. Ordinary work not labeled simulation.

### A8 — Explicit new demo

User:

> 用下面模擬資料示範資料檢查並做Excel和圖表：
> `盤點日,品類,盤差件數`
> `2026-12-09,文具,-2`
> `2026-12-09,耗材,3`
> `2026-12-10,文具,0`
> `2026-12-10,耗材,`

Actual next response:

> 我會把這份模擬盤點資料另存並標示模擬，以盤差件數分析品類與日期，保留負值、零和缺漏，產出Excel及圖表。四筆資料中一筆盤差未填，不會補成零；樣本很少，不將觀察值推論為長期趨勢。

Evaluation: **Pass (rehearsal)**. Explicit demo authorizes simulated source. **Initially observed gap, now fixed and rechecked**: current `references/demo.md` names included `demo/sales.csv`, explicitly scopes category/amount/date and the expected33,900 TWD total to this demo, and requires actual execution and checking. The CSV exists within the installable skill. Portable demo discovery is no longer an open finding; no second actual data task/demo run was performed here.

## 4. idea-generator

### I1 — Bare skill invocation

User: `$idea-generator`

Actual next response:

> 你想解決什麼工作問題，或達成什麼目標？有已知限制也可以一起說，我會提出方案並比較做法。

Evaluation: **Pass (rehearsal)**. No demo/classroom choice, intake sheet or attachment requirement.

### I2 — First natural-language response / unsolicited-mode audit

User:「想請你幫忙想想怎麼改善跨班交接。」

Actual next response:

> 我會先提出十種改善跨班交接的做法，比較需要的資源、執行難度與可能限制，再推薦適合先試的方向。尚未提供的成本與成效會標為規劃假設，不當成已驗證結果。

Evaluation: **Pass (rehearsal)**. Goal is sufficient to begin. Does not invent a fixed headcount/budget constraint, force questions, require an attachment or introduce a mode menu.

### I3 — Complete raw work request

User:

> 2026-11-13店務會議：希望降低同仁忘記登記冷藏溫度的情況，不能新增付費服務，每班可多花的時間最多3分鐘；目前只有紙表和公司共用平板，尚未量出漏填率。請想十種做法，比較後推薦一案，不要先假裝知道誰負責，也還沒選定。

Actual next response:

> 我會提出十種做法有實質差異的方案，逐案對照不新增付費服務、每班最多3分鐘、紙表與共用平板的限制，並推薦先試的方向。成本、難度與價值會標為規劃假設或主觀評估；漏填率未知，不寫保證改善幅度。尚未選案就先交付比較與推薦，負責人保留待確認。

Evaluation: **Pass (rehearsal)**. Ten by default/user request; no selected_id fabricated; no claimed efficacy. Does not delay comparison pending a selection.

### I4 — Essential objective missing

User:「幫我想十個方案，越有創意越好。」No prior objective.

Actual next response:

> 這十個方案要解決什麼問題，或希望達成什麼目標？一句話說明即可。

Evaluation: **Pass (rehearsal)**. One essential question. No demand for budget, owner, date, attachment or JSON.

### I5 — Optional metadata missing

User:「想提高新人主動問問題的意願，先給我可比較的方案。預算、誰負責、什麼時候開始都還沒定。」

Actual next response:

> 我會先整理十種促進新人提問的做法與比較表，成本和預期價值標為規劃假設，預算、負責人與日期列待確認。先推薦可小範圍驗證的方向，未選案前不把建議當成已決定的執行計畫。

Evaluation: **Pass (rehearsal)**. Completes comparison without optional blocking. Does not fill people or dates from demos.

### I6 — Selection/clarification follow-up

Context: I3's delivered comparison included a candidate “交班雙人覆核卡,” with a shared tablet as a possible tool. User:

> 我選「交班雙人覆核卡」，不用平板，先試三個班次；班長負責收卡，實際開始日期仍未定。

Actual next response:

> 我會接續為「交班雙人覆核卡」建立三個班次的試行計畫，改用紙卡並由班長收卡。每班新增時間仍以3分鐘內為限制；開始日期保留待確認，驗證項目會包含漏填與覆核是否完成，不預填成效。

Evaluation: **Pass (rehearsal)**. Preserves original constraints while applying clarified choice. No new ten-idea round, repeated menu or start confirmation.

### I7 — Ordinary work while demos exist

User:

> 2026-11-26的門市主管提到週末結帳排隊會讓客人走掉，但沒有流失數據。請發想改善排隊的方案，不能擴大店面，這次只要6案。

Actual next response:

> 我會提出六種改善週末結帳排隊的不同做法，比較空間、現場人力與執行難度，保留不能擴大店面的限制。客人流失目前只有現場觀察，成本與改善價值會標為假設，並附可驗證的方式。

Evaluation: **Pass (rehearsal)**. target_count follows user six, no example short-talk relay or company training scenario leaks in. Ordinary content not labeled simulation.

### I8 — Explicit new demo

User:

> 請示範一次，用2026-12-10的模擬情境：小型圖書室希望讓借閱者準時還書，不能使用罰款，也不能購買系統。先給十案，這次先不選。

Actual next response:

> 我會以這份模擬情境示範十案比較，明確標示模擬並保留不能罰款、不能購買系統的限制。先提供推薦與驗證方式，未選案就不建立已核定的執行計畫；成本和預期價值都標為主觀規劃評估。

Evaluation: **Pass (rehearsal)**. Demo gating explicit; no auto-selection inherited from bundled I1/example.json. Unknown dates/owners not invented.

## 5. research-assistant

### R1 — Bare skill invocation

User: `$research-assistant`

Actual next response:

> 你想調查或比較什麼問題？可以直接說明，也可以提供參考文件；若有特定地區、期間或比較對象，一起告訴我即可。

Evaluation: **Pass (rehearsal)**. Does not require an attachment or offer an unsolicited offline/demo mode menu.

### R2 — First natural-language response / unsolicited-mode audit

User:「我想調查倉庫標籤的問題。」

Actual next response:

> 你希望查清楚哪個問題：例如標籤容易脫落的原因，或比較可用的標籤做法？說明主要問題即可，我會據此確認可用來源。

Evaluation: **Pass (rehearsal)**. Two examples clarify an essential research question, not numbered modes. Does not demand a completed research brief.

### R3 — Complete raw offline comparison

User:

> 只根據以下兩份2026-11-14供應方回覆，調查哪個方案已能確認容納18人內訓，不要上網，也不要把價格不同直接解讀為比較便宜。
> A回覆：「可容納20人；費用30,000元未稅；含一次60分鐘課後諮詢；取消規則另議。」
> B回覆：「單場18人；費用32,000元含稅；諮詢另計；開課前7日取消收50%。」
> 給採購作第一輪比較，報告基準日2026-11-15。

Actual next response:

> 我會只用這兩份回覆建立來源對照與研究報告。兩方案的自述名額都能容納18人；A未稅、B含稅，且諮詢內容不同，價格不直接排名。A取消規則另議、B開課前7日取消收50%的差異會保留，供應方自述也會列為尚未獨立查核。

Evaluation: **Pass (rehearsal)**. Respects no-web scope, preserves comparability limits and exact cancellation wording. Does not invent tax rate, duration for B or quality ranking.

### R4 — Essential legal jurisdiction missing

User:「幫我查餐廳在2026-11-18是否一定要裝油脂截留設備，我要拿來決定裝修。」No place is specified.

Actual next response:

> 餐廳位於哪個縣市或國家？設備義務會受當地規定與適用條件影響；確認地區後，我會查讀主管機關的現行原文並列出適用限制。

Evaluation: **Pass (rehearsal)**. Jurisdiction essential, one focused question, no guessed law. This is a response rehearsal only; no legal conclusion or unperformed search is claimed.

### R5 — Optional metadata missing / no attachment required

User:「請調查QR Code的M、Q兩種錯誤更正等級有什麼差異，整理它們對資料容量的取捨，給印刷同仁當術語參考。」

Actual next response:

> 我會查讀QR Code規格或官方技術資料，比較M、Q兩種錯誤更正等級與資料容量的取捨，保留版本、編碼模式等會影響容量的條件。你不需要先提供附件；報告會記錄實際來源及查閱日期。

Evaluation: **Pass (rehearsal)**. Research question sufficient, no forced geography or title. Does not give uncertain niche facts from memory or claim the search already happened. In actual execution this request requires opening primary sources with an available web tool.

### R6 — Clarification follow-up to R2

User:

> 是比較做法，只用兩份2026-11-19內部測試，不要上網。普通紙標籤低溫放一夜後5張有2張翹邊；合成紙5張有1張翹邊。沒測黏膠種類，也沒有比較價格。想知道能不能直接選合成紙。

Actual next response:

> 我會接續比較兩份內部測試。普通紙為5張中2張翹邊、合成紙為5張中1張；這只能描述本次小樣本，尚不足直接判定材質優劣。報告會列出黏膠未控制、價格未比較等缺口，並提出補測建議，不擅自定案或另上網擴大範圍。

Evaluation: **Pass (rehearsal)**. Carries forward original label question, applies no-web/source limit and preserves sample limitation. Does not restart with a topic-selection prompt.

### R7 — Ordinary research while demos exist; tools usable

User:

> 請找官方文件，比較CSV與XLSX作為長期保存工作表的限制，說清楚公式與格式哪些能保留，不需要採購建議。整理給2026-11-27的內部讀書會。

Actual next response:

> 我會查讀官方檔案格式文件，逐項比較CSV與XLSX對公式、格式及多工作表的保存能力，將文件可確認的事實與保存建議分開，附來源和實際查閱日期。這次以格式限制為範圍，不加入產品採購評比。

Evaluation: **Pass (rehearsal)**. No attachment demand or bundled “甲方案24人” conclusion. Does not incorrectly label ordinary research a demo. Actual execution must browse/open primary sources, save excerpts and search-log, then run offline verifier.

### R8 — Explicit new offline demo

User:

> 請示範可追溯研究報告，僅用這兩段模擬資料，基準日2026-12-11：模擬甲教室12月8日回覆「教室有22席，投影機另租」；模擬乙教室12月9日回覆「教室有18席，含投影機」。問題是能否容納20人並提供投影，不要查真實場地。

Actual next response:

> 我會用兩段模擬資料建立可追溯示範報告，標示模擬與離線來源。甲教室席位足夠，但投影機需另租且是否已預訂未知；乙教室雖含投影機，18席不足20人。費用與可用日期未提供，不補造，也不搜尋真實場地。

Evaluation: **Pass (rehearsal)**. Only explicit demo uses simulation; source dates and as-of differ from bundled examples. Does not convert “另租” into already booked or assert current real availability.

## Actual data task: commands, artifacts, calculations and limits

Isolated sibling workspace: `work/behavior-b-data`, outside the repository. Original synthetic CSV is immutable input; the business-only projection and a row/ID map are new files. Numeric IDs remain traceable in `source-row-map.csv`, never summed as a business measure. One invocation of data-analyst/run.py was performed, not two alternative dataset runs.

The skill's instructions correctly warn that run.py profiles **every** numeric-looking column. Merely passing `--value net_revenue_twd` would not prevent an unfiltered numeric ID summary. I therefore followed its documented working-copy option. The final script input contains settled_date, service_region, net_revenue_twd, with the same row order and count. No raw data or repository code was changed.

Equivalent sanitized commands from sibling workspace are shown below. The actual executions used these same programs and arguments with fully resolved paths; variables remove personal filesystem prefixes from this report:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$repoRoot = (Resolve-Path '..\codex-office-skill-kit').Path
$taskPython = Join-Path $repoRoot '.venv\Scripts\python.exe'
$analysisScript = Join-Path $repoRoot '.agents\skills\data-analyst\scripts\run.py'
& $taskPython '.\prepare_data.py'

& $taskPython $analysisScript --input '.\service-revenue-business.csv' --output '.\outputs\data-analyst\new-service-revenue' --group-by service_region --value net_revenue_twd --date-column settled_date

$env:PYTHONIOENCODING = 'utf-8'
& $taskPython '.\verify_result.py'
```

All three commands returned exit 0. Runtime: Python3.13.3, openpyxl3.1.5, Pillow12.3.0. The script's console success line was mojibake under the first inherited stdout encoding; output files were valid UTF-8. The verifier used PYTHONIOENCODING=utf-8 and printed correctly. No packages were installed; no network or external mutation was used.

Verification script independently recalculated from the untouched raw CSV, then loaded the real analysis.json and analysis.xlsx. Assertions covered row count, selected numeric columns, all aggregate values, row exclusions, sheet names, chart presence, PNG integrity and the input SHA-256. Full machine evidence is `behavior-b-data/verification.json`.

| Check | Verified actual value |
| --- | --- |
| Raw data rows / duplicates | 8 / 0 |
| Business numeric column | net_revenue_twd only |
| Valid amounts / missing | 7 / 1 |
| Amount sum | 11,700 TWD |
| Mean / median | 1,671.4285714285713 / 1,800 |
| Min / max | -200 / 3,200 |
| Sample standard deviation | 1,184.2216652219095 |
| IQR flagged rows | none; not a claim all entries are error-free |
| Missing service_region / settled_date | 1 / 1 |
| 北區 | 2,400 - 200 + 1,200 = 3,400, three valid amounts |
| 南區 | 1,800 + 3,200 + 2,600 = 7,600, three valid amounts |
| Group exclusions | CSV rows6 and9: missing amount; missing region |
| Group reconciliation | 3,400 + 7,600 + 700 unassigned = 11,700 |
| Date2026-11-02 | 2,400 + 1,800 = 4,200 |
| Date2026-11-03 | -200 + 3,200 = 3,000 |
| Date2026-11-04 / 05 | 2,600 / 700 |
| Date exclusions | CSV rows6 and8: missing amount; missing date |
| Date reconciliation | 4,200 + 3,000 + 2,600 + 700 + 1,200 undated = 11,700 |
| ID arithmetic deliberately not used | 8,101 through8,108 sum64,836 |
| Input SHA before and after | 605624d152a538867812873e61b7eeb61084ed939e37bec67c86a55bdf4cfd5c |

Reopened workbook sheets: 分析摘要, 原始資料, 分組統計, 日期趨勢. The two latter sheets each contain one real openpyxl chart. Summary's net_revenue_twd sum cell is11,700; no record_id summary row exists. The workbook's 原始資料 is explicitly the prepared business projection, not the full untouched raw CSV, so the source-row-map/preparation manifest must accompany audit use.

Actual files in `behavior-b-data/outputs/data-analyst/new-service-revenue/`:

| File | Bytes at verification |
| --- | ---: |
| analysis.json | 2300 |
| analysis.md | 1295 |
| analysis.xlsx | 11617 |
| chart.png | 34743 |

The PNG was opened through view_image after generation. It is1200×720, has a readable Chinese title, four date labels, values4200/3000/2600/700 and a visible zero baseline; no clipping or overlap was seen. The column title carries the TWD suffix, although the plotting API has no separate unit argument. The workbook was reopened programmatically; it was not opened in native Excel. I do not claim native Excel visual acceptance. No statistical significance, stable trend, causal effect or prediction was inferred.

## Concrete corrections and remaining acceptance gaps

1. **Portable demo gap: fixed and rechecked.** All five current demo documents now open with explicit-only gating and include standalone `references/demo/` assets. presentation-maker includes source.md/deck.json; data-analyst includes sales.csv; document-writer and idea-generator include source.md/input.json; research-assistant includes input.json and sources/plan-a.md/plan-b.md. Source-first semantic steps precede a clearly marked maintainer-only section for preserved old commands. No remaining portable-source blocker was observed. Demo execution itself was not retested.
2. **Resolve research output wording when Codex actually browses.** Revised workflow correctly says the script is offline and Codex must save search-log.md and explain online reading in the report. However run.py always emits “模式：離線來源分析” and “網址僅為使用者提供的來源資訊”; a script-only report will misdescribe agent-discovered web sources. Explicitly require a separate “Codex線上查讀範圍” report paragraph after execution, or add validated metadata/report fields. Preserve script network_used=false as the script's scope, not a statement that the agent never browsed. This is a static code/doc conflict observed here, not an executed online research failure.
3. **Clarify numeric-ID handling precisely.** Current business-column warning worked in the real task. Add that CSV quoting alone does not make numeric-looking identifiers nonnumeric to this script; `--value` controls grouped/trend measures but does not suppress other column profiles and is not the fallback histogram selector. Recommend the demonstrated business-column copy plus row-map (or an explicitly reversible text representation). Keep originals unchanged.
4. **Clarify delivery wording.** Shared operation step7 says “交付可開啟的Markdown檔案連結”. Replace with “以Markdown連結交付可開啟的主要成果檔（如PPTX、DOCX、XLSX及報告）” so it cannot be mistaken for Markdown-only delivery. Existing skill-specific contracts already require actual Office files, so this is wording hardening, not a proven execution failure.
5. **Keep evidence labels honest.** These40 written next responses show instructions are coherent enough to rehearse. They do not demonstrate installed discovery, actual trigger selection, missing-dependency installation, demo execution, or PPTX/DOCX visual quality. The single real data task verifies actual local artifacts and business measure selection; native Excel UI inspection remains unperformed.

No original sources, global skills, repositories, external apps or accounts were mutated. The only new files were this report and files under the sibling behavior-b-data workspace.


## 根代理後續修正紀錄（2026-10-30）

上列為演練當時的實際回覆與發現，保留歷程。其後已補齊獨立示範素材、將舊版預填 JSON 命令明定為程式測試、修正各技能格式清單、郵件非必要日期／輸出詢問、業務欄位／數字識別碼處理、Office 成果絕對連結與研究程式的來源網址措辭。這些修正不把未執行的完整流程改列通過。
