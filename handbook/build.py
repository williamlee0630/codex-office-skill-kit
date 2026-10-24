"""維護時預先產生靜態講義；學員閱讀時不需要執行 Python 或啟動伺服器。"""
from html import escape
import json
from pathlib import Path
import re

from lessons import LESSONS

HERE = Path(__file__).resolve().parent
VERSION = "1.0.0"
SEARCH = []
COPY_ID = 0


def e(value):
    return escape(str(value), quote=True)


def p(text):
    return f"<p>{text}</p>"


def paragraphs(items):
    return "".join(p(e(item)) for item in items)


def bullets(items):
    return "<ul>" + "".join(f"<li>{e(item)}</li>" for item in items) + "</ul>"


def table(headers, rows):
    return '<div class="table-wrap"><table><thead><tr>' + "".join(f"<th scope=\"col\">{e(item)}</th>" for item in headers) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{item}</td>" for item in row) + "</tr>" for row in rows) + "</tbody></table></div>"


def code(text, label="可以直接複製"):
    global COPY_ID
    COPY_ID += 1
    identifier = f"copy-{COPY_ID}"
    block = f'<div class="code-block"><div class="code-label"><span>{e(label)}</span><button class="copy-button" type="button" data-copy="{identifier}" aria-label="複製{e(label)}">複製</button></div><pre id="{identifier}"><code>{e(text)}</code></pre></div>'
    if re.search(r"(?m)^(?:python |py |\.\\.venv\\|---$|codex-office-skill-kit/)", text):
        return maintainer(block, label)
    return block


def maintainer(body, topic="手動操作與格式細節"):
    """原始命令與契約仍可查閱、複製，預設留給需要維護的人展開。"""
    return f'<details class="maintainer"><summary>進階：給維護者｜{e(topic)}</summary><div class="details-body">{body}</div></details>'


def work_prompt(lesson):
    """每章一份完整委派，不要求學員先接合命令或填寫結構資料。"""
    skill = lesson["skill"]
    preparation = "先檢查本機 Python 與 requirements.txt 的格式套件；已可用就沿用，缺少時請自行在目前專案準備專用環境。若安裝需要組織權限或連線，列出具體限制交由資訊同仁處理，不假稱已完成。"
    if skill == "data-analyst":
        execution = "直接讀原始 sales.csv，使用 category 分組、amount 作數值、date 作日期，請自行選用對應參數並實際執行本技能 scripts/run.py 計算與產檔。所有統計與圖表以程式結果為依據，不由模型估算。"
    else:
        execution = "請自行依 SKILL.md 與 references/workflow.md 備妥有來源的結構資料，保存於輸出資料夾，再實際執行本技能 scripts/run.py 產檔；不需要我撰寫 JSON。可以參考範例欄位，不能複製預填答案冒充重新閱讀原始資料。"
    return (f"使用 ${skill}，先閱讀目前專案 .agents/skills/{skill}/SKILL.md，回報實際載入的絕對路徑。\n\n"
            + preparation + "\n\n工作目標：" + lesson["request"]
            + f"\n\n原始資料：{lesson.get('prompt_source', 'examples/' + skill + '/' + lesson['source'])}"
            + f"\n輸出位置：outputs/{skill}/\n" + execution
            + "\n" + lesson.get("execution_note", "")
            + "\n請完成真正可開啟的檔案，不只回覆大綱或計畫；完成後列出實際產物路徑、執行結果、來源與待確認事項。若有既有成果請另建新資料夾避免覆寫。"
            + "\n所有練習資料皆為模擬。保留來源、日期與未知，不捏造人名、金額、期限、成效或來源。只在目前工作區操作，不寄信、不發布、不修改全域技能。")


def note(title, text, warning=False):
    return f'<aside class="note{" warning" if warning else ""}"><strong>{e(title)}</strong><p>{text}</p></aside>'


def steps(items):
    return '<ol class="steps">' + "".join(f"<li><strong>{e(title)}</strong>{e(body)}</li>" for title, body in items) + "</ol>"


def checklist(items):
    return '<ul class="checklist">' + "".join(f'<li><label><input type="checkbox"><span>{e(item)}</span></label></li>' for item in items) + "</ul>" + '<p class="quiet">核取方塊供本次閱讀自行檢查；重新開啟頁面會重設，不會上傳或儲存個人紀錄。</p>'


def section(identifier, title, body, number=None):
    prefix = f'<span class="section-num">{number:02}</span>' if number else ''
    return f'<section id="{identifier}"><h2>{prefix}{e(title)}</h2>{body}</section>'


PAGES = [("index.html", "首頁", "學習起點", "⌂"), ("chapter-01.html", "Skill 基礎入門", "基礎與準備", "01")]
for number, lesson in enumerate(LESSONS, 2):
    PAGES.append((f"chapter-{number:02}.html", lesson["title"], lesson["category"], f"{number:02}"))
PAGES += [("chapter-12.html", "建立與修改自己的 Skill", "延伸學習", "12"), ("appendix.html", "附錄與疑難排解", "資源入口", "附")]


def nav(current):
    result = []
    for index, (url, title, category, number) in enumerate(PAGES):
        if index in (0, 2, 12):
            heading = {0: "開始學習", 2: "十個辦公室技能", 12: "繼續探索"}[index]
            result.append(f'<div class="nav-group">{heading}</div>')
        active = ' aria-current="page"' if current == url else ''
        result.append(f'<a href="{url}"{active}><span class="chapter-number">{number}</span><span>{e(title)}</span></a>')
    return "".join(result)


def layout(url, title, inner, home=False):
    breadcrumb = "歡迎來到你的 AI 辦公室" if home else title
    html = f'''<!doctype html>
<html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="原創繁體中文 Codex 辦公室技能教學。十個獨立技能、模擬資料與完整實作，可離線閱讀。"><meta name="color-scheme" content="light"><title>{e(title)}｜AI 辦公室實作指南</title><link rel="stylesheet" href="assets/style.css"><script src="assets/search-index.js" defer></script><script src="assets/app.js" defer></script></head>
<body><a class="skip" href="#main">跳到主要內容</a><div class="mobile-bar"><a class="mobile-brand" href="index.html">AI 辦公室 · 實作指南</a><button type="button" class="menu-button" id="menu-button" aria-controls="sidebar" aria-expanded="false">章節目錄 ☰</button></div>
<aside class="sidebar" id="sidebar" aria-label="課程章節"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"><svg width="22" height="25" viewBox="0 0 22 25" fill="none"><path d="M5 21V5h12v16H5Z" stroke="currentColor" stroke-width="1.3"/><path d="M8 9h6M8 13h6M8 17h3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/><path d="M3 3v17M7 3h12v16" stroke="currentColor" stroke-width="1.3" opacity=".5"/></svg></span><span>AI 辦公室<small>CODEX 實作指南</small></span></a><span class="edition">離線講義 · v{VERSION}</span>
<div class="search-wrap"><span class="search-icon" aria-hidden="true"><svg width="13" height="13" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="4.5" stroke="currentColor" stroke-width="1.5"/><path d="m10.5 10.5 3 3" stroke="currentColor" stroke-width="1.5"/></svg></span><input class="search" id="chapter-search" type="search" placeholder="搜尋章節、技能或問題" aria-label="搜尋講義全文" aria-controls="search-results" autocomplete="off"></div><div class="search-help">Ctrl / ⌘ K 快速搜尋</div><ul class="search-results" id="search-results" aria-label="搜尋結果" aria-live="polite" hidden></ul>
<nav class="chapters" aria-label="章節導覽">{nav(url)}</nav><div class="sidebar-foot">從模擬練習到可靠成果。<br>保留來源，讓未知保持可見。<br><a href="appendix.html#downloads">下載教材與工具包 ↗</a></div></aside>
<div class="page"><div class="topbar"><span>{e(breadcrumb)}</span><span class="updated"><i class="status-dot" aria-hidden="true"></i>可離線閱讀 · 2026.10</span></div><main class="content" id="main" tabindex="-1">{inner}</main><footer class="footer"><span>AI 辦公室實作指南 · v{VERSION} · 原創繁體中文教材</span><span>練習資料全為模擬 · 無外部網站依賴</span></footer></div><div class="toast" id="toast" role="status" aria-live="polite"></div></body></html>'''
    (HERE / url).write_text(html, encoding="utf-8")


def lesson_shell(url, number, title, deck, sections, skill=None, minutes=20):
    eyebrow = f"CHAPTER {number:02} / 實作課程" if number else "APPENDIX / 隨手查閱"
    meta = f"<span>約 {minutes} 分鐘</span><span>Windows / Codex</span><span>模擬資料練習</span>"
    if skill:
        meta += f'<span><code>{e(skill)}</code></span>'
    body = f'<header class="lesson-head"><div class="eyebrow">{eyebrow}</div><h1>{e(title)}</h1><p class="lesson-deck">{e(deck)}</p><div class="lesson-meta">{meta}</div></header>'
    toc = '<aside class="toc" aria-label="本章內容"><div class="toc-title">本章內容</div>' + "".join(f'<a href="#{identifier}">{e(heading)}</a>' for identifier, heading, content in sections) + '</aside>'
    article = ''
    for index, (identifier, heading, content) in enumerate(sections, 1):
        article += section(identifier, heading, content, index)
        SEARCH.append({"title": heading, "chapter": title, "url": f"{url}#{identifier}", "text": re.sub(r"<[^>]+>", " ", content) + " " + (skill or "")})
    index = next(index for index, page in enumerate(PAGES) if page[0] == url)
    previous = PAGES[max(0, index - 1)]
    following = PAGES[min(len(PAGES) - 1, index + 1)]
    pagination = f'<nav class="lesson-nav" aria-label="上下章節"><a href="{previous[0]}"><small>← 上一章</small>{e(previous[1])}</a><a href="{following[0]}"><small>{"回到課程首頁" if index == len(PAGES)-1 else "下一章 →"}</small>{e("首頁" if index == len(PAGES)-1 else following[1])}</a></nav>'
    if index == len(PAGES) - 1:
        pagination = pagination.replace(f'href="{following[0]}"', 'href="index.html"')
    return body + '<div class="reading-layout"><article class="article">' + article + pagination + '</article>' + toc + '</div>'


def home():
    cards = ''
    for number, lesson in enumerate(LESSONS, 2):
        cards += f'<a class="skill-card" href="chapter-{number:02}.html"><div class="card-top"><span class="card-number">CHAPTER {number:02}</span><span class="card-category">{e(lesson["category"])}</span></div><h3>{e(lesson["title"])}</h3><p>{e(lesson["card"])}</p><div class="card-bottom"><span>{e(lesson["skill"])} · 約 {lesson["minutes"]} 分鐘</span><span class="card-arrow" aria-hidden="true">↗</span></div></a>'
    hero = '''<section class="hero"><div><div class="eyebrow">開課方審閱版 · 給沒有程式基礎的辦公室夥伴</div><h1>把日常工作，<br><span>整理成可靠成果。</span></h1><p class="intro">下載教材，在 Codex 貼上工作需求，讓它讀取來源、備妥資料並產生檔案。你專心說清楚需求，再核對會議紀錄、文件、報表與簡報。</p><div class="actions"><a class="button primary" href="chapter-01.html">從四步開始 <span aria-hidden="true">→</span></a><a class="button" href="../dist/codex-office-skill-kit-1.0.0.zip" download>下載完整學員工具包 ↓</a></div><div class="quiet">不需程式背景 · 自備 Codex · 練習資料全為模擬</div></div><div class="flow-card" aria-label="初學者四步操作"><div class="flow-label">從下載到第一次工作成果</div><div class="flow-row"><div class="flow-icon">01</div><div><strong>下載並解壓縮</strong><small>完整教材、技能與模擬資料</small></div></div><div class="flow-arrow"></div><div class="flow-row"><div class="flow-icon">02</div><div><strong>在 Codex 開啟專案</strong><small>環境交由 Codex 或資訊同仁準備</small></div></div><div class="flow-arrow"></div><div class="flow-row"><div class="flow-icon">03</div><div><strong>貼上工作需求</strong><small>完整提示詞可依工作調整</small></div></div><div class="flow-last"><span>04　開啟並核對成果</span><span>✓</span></div></div></section>'''
    review = section("course-review", "開課方快速理解這套課程", table(["審閱重點", "課程安排"], [
        ["課程目標", "讓沒有程式基礎的學員，能用自然語言交代工作，取得實際檔案，並依來源核對事實、數字與待確認事項。"],
        ["十個技能用途", "郵件、會議、專案、週報、收據、簡報、商務文件、資料分析、創意企劃、來源研究；下方各卡片可直接進入對應實作。"],
        ["操作方式", "下載解壓 → Codex 開專案 → 貼工作需求 → 核對成果。每章有一貼即用參考提示詞，可改目標、語氣、格式與資料來源。"],
        ["可帶走的教材", "完整 ZIP 內有 14 頁離線講義、十個技能、模擬來源與範例成果、安裝及維護文件。另提供技能包及練習資料包。"],
        ["環境與人工確認限制", "產檔確實需要 Python 與格式套件，由 Codex 或資訊同仁準備；Codex 使用依帳號及連線。學員不需先學語法。Office 版面、收據模糊欄位、未知資料與正式使用前的內容仍需人工確認。"],
        ["審閱狀態", '本頁為開課方審閱版，未宣稱全面驗收。程式測試、Codex 觸發與語意、瀏覽器操作、Office 畫面各有邊界；請讀 <a href="../ACCEPTANCE.md">實際驗收報告</a>。'],
    ]))
    overview = '<div class="overview-strip"><div><strong>10 個獨立技能</strong><span>依工作選擇，無須依序啟動</span></div><div><strong>12 章完整教學</strong><span>從第一次操作到調整自己的技能</span></div><div><strong>1 套模擬教材</strong><span>先練習，再換成有權使用的資料</span></div></div>'
    learning = '<section class="two-col"><div><h2>Skill 是什麼？</h2><p>把 Skill 想成 Codex 隨時可讀的工作說明書：它約定這類工作怎麼處理、要保留什麼，以及交出哪些成果。你不需先理解程式架構，就能開始使用。</p><p>你貼上的需求說明這一次的目標；技能協助重複使用可靠的處理流程。每次仍要檢查來源、未知欄位與實際檔案。</p></div><div><h2>怎麼安排學習？</h2><ol><li>讀第一章，解壓教材並在 Codex 開啟專案。</li><li>挑熟悉的工作，貼上完整提示詞。</li><li>讓 Codex 準備環境並產檔，再開啟成果回查原文。</li><li>需要改流程時，再讀第十二章；進階內容可稍後展開。</li></ol></div></section>'
    downloads = section("downloads", "教材帶著走，離線也能讀。", p("初次使用建議下載完整學員工具包，講義、技能與模擬資料一次備齊。ZIP 不包含 Python 與第三方套件；首次準備套件與 Codex 使用仍依帳號、權限及連線環境。") + '<div class="actions"><a class="button primary" href="../dist/codex-office-skill-kit-1.0.0.zip" download>完整學員工具包 v1.0.0 ↓</a><a class="button" href="../dist/office-skills-1.0.0.zip" download>只下載技能工具包 ↓</a><a class="button" href="../dist/practice-data-1.0.0.zip" download>只下載模擬練習資料 ↓</a><a class="button" href="appendix.html">安裝入口與常見問題 →</a></div>')
    inner = hero + overview + review + '<section aria-labelledby="skills-title"><div class="section-head"><h2 id="skills-title">今天，先解決哪件工作？</h2><span>選一個熟悉情境，開始動手</span></div>' + cards + '</section><div class="start-card"><div><div class="eyebrow" style="margin-bottom:8px">第一次接觸 SKILL？</div><h2>先做一份不亂下結論的會議紀錄。</h2><p>使用模擬逐字稿，練習區分「提議」與「已確認決議」，再開啟真正的 Word 成果。</p></div><a class="button" href="chapter-03.html">前往會議練習 →</a></div>' + learning + downloads
    layout("index.html", "課程首頁", inner, True)
    SEARCH.append({"title": "課程首頁與下載", "chapter": "開始學習", "url": "index.html", "text": "開課方審閱版 課程目標 Skill Prompt 下載 工具包 學習順序 模擬 教材"})


def basics():
    sections = [
        ("understand", "先認識 Codex 與 Skill", paragraphs(["Codex 是能協助讀取檔案、整理內容及執行工具的工作夥伴。這套教材以 Codex 為執行環境；網站本身只負責教學，不會替你執行 Python 或把資料送到其他服務。", "Skill 是可重複使用的工作流程。一般 Prompt 說明這次要做什麼；Skill 的 SKILL.md 再約定何時適用、需要哪些資料、怎麼保留未知，以及要用什麼腳本產出成果。你仍需提供清楚來源，並核對最後結果。", "這十個技能都能獨立使用。例如要整理會議時，不需要先啟動郵件或專案技能。它們不要求額外 API 金鑰，也不會自行寄信、部署或發布資料。"])),
        ("files", "看懂資料夾，不必先學寫程式", p("先記住四個位置：技能、模擬資料、成果、講義。以本章的會議練習為例：") + code("codex-office-skill-kit/\n├─ .agents/skills/meeting-assistant/\n│  ├─ SKILL.md                 工作規則與觸發說明\n│  ├─ scripts/run.py           產生實際檔案\n│  ├─ scripts/_office.py       隨技能攜帶的共用功能\n│  └─ references/workflow.md   詳細流程\n├─ examples/meeting-assistant/ 原始模擬資料與格式範例\n├─ outputs/meeting-assistant/  執行後的成果\n├─ handbook/index.html        這份講義\n└─ requirements.txt           Python 所需套件", "資料夾位置示意") + p("名稱前面有點的 <code>.agents</code> 仍是正常資料夾；Windows 檔案總管若看不到，可開啟顯示隱藏項目。不要只複製一份 SKILL.md，因為獨立技能也需要它自己的 scripts 與 references。")),
        ("install", "解壓縮、開啟專案、準備 Python", steps([("完整解壓縮下載檔", "先下載完整工具包，使用『全部解壓縮』放在你能寫入的工作資料夾。不要在 ZIP 預覽畫面中直接操作。"), ("在 Codex 開啟整個專案資料夾", "選擇包含 AGENTS.md、requirements.txt 與 .agents 的那一層。桌面介面名稱可能因版本不同；確認 Codex 能讀到實際檔案即可。"), ("請 Codex 檢查 Python", "請它執行 python --version 並回報結果。如果尚未安裝，依組織規範安裝 Python 後重新開啟終端機。"), ("建立專案專用環境並安裝依賴", "在專案根目錄執行下方指令。虛擬環境將套件留在這份專案，不需要你修改系統的 Python 套件。你也可以把指令交給 Codex 代執行。")]) + code("python -m venv .venv\n.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt", "Windows PowerShell：在專案根目錄執行") + note("先準備一次，之後重複使用", "首次安裝套件需要可取得 Python 套件的連線環境。講義網站本身無需安裝套件。後續章節中的 <code>python</code> 代表已安裝依賴的 Python；可請 Codex 改用 <code>.venv\\Scripts\\python.exe</code>。不必手動變更 PowerShell 的執行原則。") + code("請在目前專案檢查 Python 與 requirements.txt，建立 .venv 並安裝套件。不要修改全域技能或工作區以外檔案。完成後回報 Python 路徑與安裝結果。", "交給 Codex 準備環境")),
        ("activate", "明確指定，然後核對實際載入路徑", p("在 Codex 對話直接輸入技能名稱，可以清楚表達你要使用哪一支技能。部分版本的選單或選取方式可能顯示 <code>$</code> 或 <code>@</code>，不必尋找教材未能確認的固定按鈕。先用以下文字：") + code("使用 $meeting-assistant。\n先回報實際載入的 SKILL.md 絕對路徑，確認來自目前專案的 .agents/skills/meeting-assistant/SKILL.md。\n再閱讀 examples/meeting-assistant/source.md 的模擬會議，說明你會如何區分提議與已確認決議。", "明確指定技能與核對來源") + p("你也可以自然地說『請把這份會議逐字稿整理成決議、待辦與待確認事項』，讓 Codex 依 description 選擇技能。自然語言匹配需要實際測試，不代表每一個說法都一定觸發。") + note("同名技能可能並存", "Codex 會發現專案 <code>.agents/skills</code> 等位置的技能；同名技能不會自動合併。若已安裝相同名稱的全域技能，務必核對實際讀取的絕對路徑。變更通常會自動偵測，必要時重新開啟 Codex；不要為排錯而覆寫全域技能。")),
        ("workflow", "理解兩條實作路線", table(["工作類型", "實際流程", "要核對什麼"], [["會議、郵件、文件、研究等語意工作", "原始資料 → Codex 閱讀判斷 → 有來源 JSON → Python 產檔 → 人工核對", "來源、決議狀態、未知欄位與實際成果"], ["CSV / XLSX 資料分析", "原始工作表 → Python 真正計算 → Codex 解讀 → 人工回算", "資料範圍、有效筆數、數字口徑與圖表"], ["圖片 / 掃描收據", "實際視覺／可用 OCR／人工轉錄 → 核對 JSON → Python 產檔", "實際辨識方式、看不清的欄位、幣別與重複"]]) + p("範例 input.json 是產檔程式的輸入契約與測試資料。跑通它只能證明程式能產檔；要驗收語意技能，必須請 Codex 直接閱讀原始 source.md、TXT 或 DOCX，再重新建立 JSON。不能把預填答案複製一次就宣稱理解原文。") + code("請先閱讀本技能 SKILL.md、references/workflow.md 與原始模擬資料。\n可以參考 input.json 的欄位格式，但不要把其內容當成原文判讀結果。\n將你從原文獨立整理、有來源的結構資料寫入 outputs/meeting-assistant/reviewed-input.json。\n缺少負責人或期限就保留待確認，產檔前請列出你判定為已確認決議的依據。", "讓 Codex 從原文獨立整理")),
        ("first-run", "第一次實際產出檔案", p("若只想先確認環境與程式，可以在專案根目錄跑提供的結構資料。資料與人名全為模擬：") + code("python .agents/skills/meeting-assistant/scripts/run.py --input examples/meeting-assistant/input.json --output outputs/meeting-assistant", "會議技能：產檔測試") + p("接著，完成上節的原文閱讀並建立 reviewed-input.json，改用它重新產檔：") + code("python .agents/skills/meeting-assistant/scripts/run.py --input outputs/meeting-assistant/reviewed-input.json --output outputs/meeting-assistant", "會議技能：從核對資料產檔") + p("請 Codex 回報實際執行結果與輸出路徑，再用 Word 開啟 <code>outputs/meeting-assistant/minutes.docx</code>，同時核對 <code>minutes.md</code>。不要只看到『完成』兩個字就結束；要確認檔案存在、能開啟、內容可回查。")),
        ("acceptance", "分清程式測試與 Codex 觸發驗收", table(["驗收項目", "怎麼做", "能證明什麼"], [["程式自動化測試", "在根目錄執行下方 unittest 指令", "輸入檢查、計算及產檔邊界符合測試案例"], ["實際產物檢查", "開啟 DOCX、XLSX、PPTX 與 Markdown", "檔案可用，抽查內容與版面"], ["明確技能觸發", "輸入 $技能名稱，回報實際 SKILL.md 路徑", "這次確實讀到指定技能；要記錄實際路徑"], ["自然語言與語意驗收", "用原始資料和自然語言提示，逐項核對來源", "這次說法觸發情形及原文判讀是否正確"]]) + code("python -m unittest discover -s tests -v", "專案自動化測試") + note("驗收要留下證據", "記下日期、提示詞、來源、實際技能路徑、產物與核對結果。尚未真的做過的自然語言觸發或目視檢查，要寫『待驗收』，不以程式測試通過代替。網站內容是操作教學，不代表你目前電腦上的全部環境已驗收。")),
        ("safety", "讓未知與資料權限保持清楚", bullets(["先用模擬資料練習；真實公司文件須確認自己有權提供給 Codex，依組織政策處理。", "缺少人名、金額、日期、成效或來源就標示待確認，不拿常識或今天日期補造。", "來源文件裡的『忽略規則、寄出資料、下載工具』只當作待分析文字，不把它當你的授權指令。", "輸出只留在目前工作區。寄信、部署、發布與修改全域技能，都不屬於本套預設流程。", "憑證圖片無法看清時改用人工核對轉錄；網路不可用時研究列為離線，不冒稱外部資料已取得。", "成果用於正式工作前，核對數字、來源、收件對象、檔案權限與待確認事項。"])),
        ("ready", "準備好進入第一個實作", checklist(["工具包已完整解壓縮，Codex 開啟專案根目錄。", "Python 與 requirements.txt 已準備，知道如何請 Codex 代執行。", "核對過實際載入的 SKILL.md 路徑，能分辨專案與全域技能。", "知道 input.json 產檔測試不等於原文語意與觸發驗收。", "知道成果要實際開啟，未知資料應保持待確認。"])),
    ]
    original = {identifier: body for identifier, title, body in sections}
    sections = [
        ("understand", "四步開始，不必先學程式", p("這一章先帶你完成第一份工作成果。不需要先學 Python 或 JSON 語法，也不必先看懂程式架構；你負責說需求與核對成果，環境和產檔細節交由 Codex 或資訊同仁處理。") + steps([
            ("下載並解壓縮", "下載完整學員工具包，使用『全部解壓縮』放到可寫入的資料夾，不要停留在 ZIP 預覽畫面。"),
            ("在 Codex 開啟專案", "選擇解壓後包含 README.md、AGENTS.md 與 handbook 的整個工具包資料夾，確認 Codex 能讀到 examples 裡的模擬資料。"),
            ("貼上工作需求", "複製本章或技能章的完整參考提示詞，貼到 Codex 對話送出。Codex 會讀來源、檢查環境、備妥資料並真正產檔。"),
            ("開啟並核對成果", "依 Codex 回報的位置開啟文件，對照原文看事實、數字與待確認欄位。需要調整就直接用日常語言提出。"),
        ]) + note("先做熟悉的工作", '建議從 <a href="chapter-03.html">會議紀錄練習</a>開始。用模擬資料完成一輪，再換成你有權提供的工作資料。') + maintainer(original["understand"], "Codex、Skill 與工作資源")),
        ("files", "先知道來源與成果放在哪裡", table(["位置", "學員要做什麼"], [["examples/", "本次使用的模擬來源；請 Codex 讀取，你可開啟原文核對。"], ["outputs/", "Codex 真正執行後的成果，依回報路徑開啟；同名成果可另存新資料夾。"], ["handbook/index.html", "這份離線講義，雙擊可閱讀；沒有網路也能查教材。"]]) + p("其他資料夾讓 Codex 依技能指引處理即可。若它讀到同名的其他版本，要求它改讀目前專案的技能並回報路徑。") + maintainer(original["files"], "完整資料夾與腳本位置")),
        ("install", "把環境準備交給 Codex 或資訊同仁", p("實際產出 Word、Excel、PowerPoint 與 PDF 等格式，需要本機 Python 與 requirements.txt 所列格式套件；它們沒有包在下載 ZIP 裡。你不必先學語法或手打命令。先請 Codex 檢查；若受安裝權限、網路或組織規範限制，將它回報的具體需求交給資訊同仁。") + code("請檢查目前工具包所需的 Python 與 requirements.txt 格式套件。可用就沿用；缺少時請在目前專案備妥專用環境並實際檢查。不要修改全域技能或工作區以外檔案。如果需要安裝權限或連線，列出要交給資訊同仁的具體需求；不要假稱環境已就緒。完成後回報可用的環境與仍需協助項目。", "可先貼給 Codex：準備環境") + note("閱讀離線，執行依環境", "講義不需伺服器或套件；Codex 使用依帳號與連線，第一次取得套件也可能需要網路。準備完成後可重複使用同一環境。") + maintainer(original["install"], "手動安裝與環境命令")),
        ("activate", "告訴 Codex 要做什麼", p("完整提示詞已包含技能與來源位置，不必先記住觸發語法。第一次可直接使用下節的整段需求，之後用自己的話提出工作。請 Codex 回報實際讀取的技能路徑，確認它來自目前專案。") + note("提示詞是參考，可以調整", "可依工作修改工作目標、讀者、語氣、格式與資料來源，例如『給主管看的五句摘要』或『改用我的逐字稿』。保留不捏造、來源、日期、未知與實際產檔規則；尚未確定的內容不要改寫成已確認。") + maintainer(original["activate"], "明確指定與自然語言觸發")),
        ("workflow", "你提供來源，Codex 完成整理與產檔", table(["你提供的資料", "交由 Codex 處理", "你核對的成果"], [["會議、郵件、工作紀錄與文件", "讀原文，區分事實和提議，備妥產檔資料並執行工具", "來源、決議狀態、未知欄位與實際文件"], ["CSV／Excel 工作表", "真正計算品質、統計、分組與日期觀察，再解讀結果", "有效筆數、數字範圍、分組與圖表"], ["圖片／掃描收據", "檢查可讀方式，保留憑證、整理能確認的欄位", "模糊欄位、幣別與疑似重複；必要時人工確認"]]) + p("你不需要手工準備程式用的中間資料。只要要求從原始資料重新整理，避免把範例答案再次產檔就當成理解原文。") + maintainer(original["workflow"], "中間資料、JSON 契約與兩種測試")),
        ("first-run", "一貼即用：完成第一份會議紀錄", p("先在目前專案的 Codex 對話貼上整段需求。這一段已包含環境檢查、讀原文、準備資料、執行產檔與回報成果，不需要接著貼手動命令。") + code(work_prompt(LESSONS[1]), "第一次完整工作提示詞") + p("完成後開啟 outputs/meeting-assistant/ 內的 minutes.md 與 minutes.docx。回查原文，確認『下月全面上線』仍屬未定案，未知負責人與期限保持待確認。檔案無法開啟或內容不符，就把具體問題交回 Codex 修正。") + maintainer(original["first-run"], "範例產檔與原文產檔命令")),
        ("acceptance", "成果要核對，測試與觸發驗收分開記錄", table(["檢查面向", "你可以怎麼做"], [["檔案與內容", "實際開啟成果，檢查事實、數字、來源與版面。"], ["Codex 觸發與語意", "記下讀取的技能路徑與提示詞，對照原文核對判讀。"], ["程式測試", "讓 Codex 或維護者執行，驗證指定資料的計算與產檔；不能替代前兩項。"]]) + note("只記錄真的完成的檢查", "程式測試、HTML 結構、瀏覽器操作與 Office 畫面檢查各有範圍；沒有實際執行就記『待驗收』，不把其中一項通過說成全部成功。") + maintainer(original["acceptance"], "程式測試與觸發驗收方法")),
        ("safety", "讓未知與資料權限保持清楚", original["safety"]),
        ("ready", "準備好進入第一個實作", checklist(["工具包已完整解壓縮，Codex 能讀到模擬來源。", "知道可把環境檢查交給 Codex，權限限制交資訊同仁處理。", "會貼上完整工作需求，也知道可以調整目標、語氣、格式與資料來源。", "知道成果要實際開啟，事實與數字要回查來源，未知保持待確認。", "分開記錄產檔結果、Codex 觸發與內容核對；未做的檢查不當成通過。"])),
    ]
    sections[3] = (sections[3][0], sections[3][1], sections[3][2] + '<p class="quiet">技能規範查證日期：2026-10-23。依 <a href="https://learn.chatgpt.com/docs/build-skills">OpenAI 官方 Build skills 文件</a>；CLI 檢查版本為 0.163.0-alpha.11.2，桌面版版本未確認。桌面操作文字以實際版本為準。</p>')
    layout("chapter-01.html", "第 1 章：Codex Skill 基礎入門", lesson_shell("chapter-01.html", 1, "Codex Skill 基礎入門", "從下載解壓到第一份成果，用工作需求開始，讓 Codex 處理環境與產檔細節。", sections, minutes=25))


def skill_lesson(number, lesson):
    skill = lesson["skill"]
    root = f"examples/{skill}"
    semantic = skill != "data-analyst"
    prompt = work_prompt(lesson)
    example_command = f"python .agents/skills/{skill}/scripts/run.py --input {root}/{lesson['input']} --output outputs/{skill}" + lesson.get("arguments", "")
    command = f"python .agents/skills/{skill}/scripts/run.py --input outputs/{skill}/reviewed-input.json --output outputs/{skill}" if semantic else example_command
    materials = p(e(lesson["materials"])) + table(["位置", "用途"], [[f'<a href="../{root}/{lesson["source"]}"><code>{e(root + "/" + lesson["source"])}</code></a>', "本章練習來源；請先讀完整內容"], [f'<a href="../{root}/{lesson["input"]}"><code>{e(lesson["input"])}</code></a>', "範例輸入；語意技能可參考欄位，不當作判讀證據" if semantic else "Python 直接計算的原始工作表"], [f'<a href="../.agents/skills/{skill}/SKILL.md"><code>SKILL.md</code></a>', "本技能的適用情境、規則與輸入輸出契約"], [f'<code>outputs/{skill}/</code>', "實際執行後建立，保留產物與核對資料"]]) + note("開始前的準備", "請先完成第 1 章的 Python 環境與 <code>requirements.txt</code> 安裝。你可以請 Codex 代執行下方命令。保留原始模擬資料；延伸練習先做複本，所有成果留在目前專案內。")
    if skill == "receipt-organizer":
        materials += p('原始憑證：<a href="../examples/receipt-organizer/simulated-receipt.png">開啟模擬 PNG</a> · <a href="../examples/receipt-organizer/simulated-receipt.pdf">開啟同張模擬 PDF</a>。只對應 R1。')
    if skill == "research-assistant":
        materials += p('必讀原始來源：<a href="../examples/research-assistant/sources/plan-a.md">模擬甲方案 S1</a> · <a href="../examples/research-assistant/sources/plan-b.md">模擬乙方案 S2</a>。input.json 是問題及整理契約，不能取代逐一讀原文。')
        materials += note("將 JSON 放到新位置時，來源路徑也要對上", "研究技能的 <code>sources[].path</code> 以輸入 JSON 所在資料夾為起點。若建立 <code>outputs/research-assistant/reviewed-input.json</code>，S1 路徑應為 <code>../../examples/research-assistant/sources/plan-a.md</code>，S2 比照；也可請 Codex 使用目前來源的絕對路徑。摘錄必須逐字存在於原文，並另行核對是否支持主張。")
    materials = p(e(lesson["learner_materials"])) + p(f'本章資料放在 <code>{root}/</code>，成果放在 <code>outputs/{skill}/</code>。請 Codex 自行確認環境；Python 與格式套件需要備妥，但你不需要先學語法。') + maintainer(materials, "輸入契約、來源位置與準備細節")
    if skill == "receipt-organizer":
        materials += p('可先開啟：<a href="../examples/receipt-organizer/simulated-receipt.png">模擬 R1 收據 PNG</a> · <a href="../examples/receipt-organizer/simulated-receipt.pdf">同張收據 PDF</a>。')
    elif skill == "research-assistant":
        materials += p('本章原始來源：<a href="../examples/research-assistant/sources/plan-a.md">模擬甲方案</a> · <a href="../examples/research-assistant/sources/plan-b.md">模擬乙方案</a>。')
    elif not lesson["source"].endswith(".json"):
        materials += p(f'<a href="../{root}/{lesson["source"]}">開啟本章原始模擬資料 ↗</a>')
    activation = p(f"明確指定 <code>${skill}</code>，再要求 Codex 回報實際技能路徑。若已有同名全域技能，這一步能確認它是否讀到本專案版本。") + code(f"使用 ${skill}。先閱讀目前專案 .agents/skills/{skill}/SKILL.md，回報實際載入的絕對路徑，再依本章處理模擬資料。", "明確指定這支技能") + p("自然語言也可以描述同一工作；是否觸發要以這次實際讀取的技能為準：") + code(lesson["natural"], "自然語言觸發練習")
    practice = p(e(lesson["practice"])) + p("先執行範例產檔，確認環境可以正常工作：") + code(example_command, "範例輸入：程式產檔測試")
    if semantic:
        practice += p("完成原始資料判讀後，讓 Codex 依本技能契約建立 reviewed-input.json，接著產出自己的實作成果：") + code(command, "從原文核對資料產檔") + note("這兩次測試要分開記錄", "範例 JSON 產檔成功是程式測試；Codex 直接讀原始資料並建立有來源 JSON，才有語意驗收的材料。請在紀錄中分開列出，不把前者說成後者已完成。")
    else:
        practice += note("數值一定由程式計算", "本章直接讀取 CSV / XLSX 計算。請保留執行結果與回算過程；Codex 的文字解讀要以實際計算檔案為依據，不讓模型憑空估出統計值。")
    if skill == "receipt-organizer":
        practice += p("另做一次原始影像流程，觀察程式如何保留憑證與建立待核對模板：") + code("python .agents/skills/receipt-organizer/scripts/run.py --input examples/receipt-organizer/simulated-receipt.png --output outputs/receipt-image-review --simulation", "原始 PNG：先保留來源與轉錄模板") + p("此步驟第一次不產報帳 Excel，也不做 OCR。請檢查 <code>originals/</code>、<code>extraction-evidence.json</code>、<code>transcription-template.json</code> 與 <code>review-required.md</code>。實際看圖核對 R1 後再填轉錄模板；未知欄位維持 null，確認後改用填好的 JSON 當輸入並輸出到新的資料夾。PDF 可將輸入換成同名 PDF，仍須核對抽取文字。")
    practice = p("完整實作只需把第 5 節的整段參考提示詞貼入 Codex。請它從本章原始來源開始，完成環境檢查、整理與實際產檔；不要停在摘要或操作計畫。Codex 若提出缺漏，先核對來源，再決定補資料或保留待確認。") + steps([
        ("貼需求並等候實際產檔", "使用本章模擬來源；讓 Codex 自行處理資料格式與工具執行。保留它回報的技能路徑與結果。"),
        ("開啟第 8 節列出的成果", "核對檔案是否存在且能開啟，抽查一項已知事實與一項未知欄位，再對照下方預期摘錄。"),
        ("用日常語言提出修正", "例如『這件事仍在提議，請保留未定案，重建所有版本並列出改動』。同一次修正的版本要一致。"),
    ]) + maintainer(practice, "保留原有範例、手動命令與兩輪驗證")
    if skill == "receipt-organizer":
        practice += note("這次的五筆資料來自兩種證據", "R1 可對照原圖；R2 至 R5 只依模擬清單。看不清的欄位需人工確認，沒有 OCR 就記錄實際視覺或人工轉錄方式。圖片第一步只會保留原件與建立待核對模板；整理並核對後才產報帳表。")
    expected = '<div class="expected"><div class="eyebrow">正確成果的核對重點 · 模擬實作</div>' + bullets(lesson["expected"]) + '</div>' + code(lesson["expected_sample"], "預期內容摘錄：依原始模擬資料核對") + table(["預期檔案", "如何確認"], [[f'<code>{e(item)}</code>', "在輸出資料夾找到實體檔案，用對應軟體開啟，抽查來源與內容"] for item in lesson["outputs"]]) + p("除主要成果外，部分技能另包含 evidence.json 或檢查資訊。以上摘錄是教學核對標準，並非聲稱本次 Codex 已獨立讀原文並驗收。每項都要自己核對，不能只以終端機顯示成功替代。")
    sections = [
        ("lesson-1", "這個 Skill 解決什麼問題", paragraphs(lesson["problem"])),
        ("lesson-2", "哪些員工適合使用", bullets(lesson["audience"]) + p("先選一件你熟悉的日常工作練習，因為你越清楚原始內容，就越能看出摘要是否漏掉重要限制、誤解狀態，或新增了來源沒有的資訊。")),
        ("lesson-3", "所需資料與準備步驟", materials),
        ("lesson-4", "如何在 Codex 中啟動", activation),
        ("lesson-5", "可以直接複製的操作提示詞", code(prompt, "完整工作提示詞：一貼即用") + note("這是可調整的參考提示詞", "你可以依工作修改工作目標、讀者、語氣、格式與資料來源，也能加上自己的限制。若要改成不同檔案格式，請 Codex 先確認本技能是否支援；需要新增功能就另行說明。持續保留不捏造、來源、日期、未知值與實際產檔要求。")),
        ("lesson-6", "完整操作步驟", steps(lesson["learner_steps"]) + maintainer(steps(lesson["steps"]), "原有詳細操作與結構資料流程")),
        ("lesson-7", "用模擬資料完成一次實作", practice),
        ("lesson-8", "正確的預期輸出範例", expected),
        ("lesson-9", "常見錯誤與解決方式", table(["發現的問題", "怎麼處理"], [[e(a), e(b)] for a, b in lesson["errors"]]) + p("如果腳本顯示輸入不符合格式，先請 Codex 對照本技能 SKILL.md 的契約修正資料。不要刪除檢查或把未知欄位亂填成確定值來通過。需要排錯時，保留實際錯誤訊息與使用命令。")),
        ("lesson-10", "延伸練習與驗收清單", p("先複製原始模擬資料，再請 Codex 加入一個明確標示模擬的變動或缺漏，用相同需求重新產檔。也可調整讀者、語氣或呈現格式，核對新舊成果是否保留相同事實與未知規則。") + maintainer(p(e(lesson["extend"])), "本技能延伸練習的細節") + checklist(lesson["checks"]) + code(f"實作日期：\n技能名稱：{skill}\n實際載入 SKILL.md 路徑：\n原始資料與日期：\n程式產檔測試結果：\nCodex 明確／自然語言觸發結果：\n原文語意或數值核對結果：\n已開啟的產物：\n仍待確認：", "可複製的實作驗收紀錄")),
    ]
    url = f"chapter-{number:02}.html"
    layout(url, f"第 {number} 章：{lesson['title']}", lesson_shell(url, number, lesson["title"], lesson["deck"], sections, skill, lesson["minutes"]))


def custom():
    sections = [
        ("read", "從 SKILL.md 的四個地方開始讀", p("先選一支你已完成實作的技能。使用文字編輯器或請 Codex 開啟本專案中的 SKILL.md；你不必先理解所有程式碼，先看名稱、描述、流程與產物。") + table(["位置", "你要理解的問題"], [["YAML frontmatter 的 name", "這支技能的英文識別名稱是什麼？是否對應資料夾？"], ["YAML frontmatter 的 description", "什麼工作應該選它？如何避免和其他技能混淆？"], ["工作流程與缺漏規則", "來源怎麼讀？哪些情況要保留未知或停止產檔？"], ["scripts / references 與輸入輸出", "哪些指令真的產出檔案？需要哪些欄位與依賴？"]]) + code('---\nname: team-meeting-assistant\ndescription: 整理團隊內部會議逐字稿為決議、待辦與待確認事項；適用於會後紀錄，不處理跨來源專案週報。\n---\n\n# 團隊會議整理\n\n保留原始來源、日期及未知欄位。\n提議未經明確確認前，不列為已確認決議。', "新技能開頭示例：模擬，尚非完整技能") + p("name 與 description 是必要欄位；範例只用來說明結構，不代表貼上就成為完整可執行技能。仍需要流程、腳本、完整案例與實測。")),
        ("copy", "先做專案內複本，再改名稱", p("不要直接覆寫已用過的技能，也不要修改全域技能。先在目前專案為一支技能建立新的資料夾，保留整份 scripts、references 與需要的資源。名稱使用小寫英文與連字號。") + code("請只在目前工作區複製 .agents/skills/meeting-assistant 為 .agents/skills/team-meeting-assistant。\n先確認目標不存在，不覆寫現有檔案。\n將新技能的 name、description 及相關介面資訊調整為一致的新名稱。\n保留來源追查、未知值、提議與決議分流規則，原技能保持可用。\n回報新增與修改的檔案。", "請 Codex 建立自己的技能複本") + note("不要讓兩個名稱共用模糊描述", "新 description 要寫出適用與非適用情境。比如『團隊會後紀錄』與『跨來源專案追蹤』是不同工作；只寫『協助辦公室工作』，難以可靠選擇。")),
        ("workflow", "調整觸發條件與工作流程", p("先把你想改的行為說成可觀察結果。例如：每份會議紀錄最後多一段『需要主管確認』，其內容只能來自原文中的未決事項。不要只要求『更專業』，因為那很難驗收。") + steps([("定義觸發情境", "寫出兩句應該使用新技能的自然語言提示，再寫一句不適用提示。避免和原本技能完全相同。"), ("說明流程變更", "指出要在哪一步增加、刪除或重排內容。保留來源、未知與確認狀態，語氣調整不能改變事實。"), ("指定產物變更", "明確寫出新增章節或欄位的名稱與資料來源。新增 Markdown 標題可能只需改產檔規則，新增檔案格式則要改腳本。"), ("列出驗收案例", "至少準備正常、缺漏及錯誤資料。寫出你預期看到什麼，再請 Codex 動手修改。")]) + code("請修改目前專案的新技能 team-meeting-assistant。\n需求：輸出紀錄最後加入『需要主管確認』，僅彙整原始資料中尚未確認的事項與來源。\n沒有這類事項時寫『本次原始資料未列出』，不得新增提議。\n先說明會修改哪些檔案與可觀察的驗收案例，再只修改本專案的新技能。\n保留原技能與所有未知值規則。", "把改動說成可驗收需求")),
        ("format", "加入新輸出格式時，要有實際產檔", p("你可以請 Codex 增加 CSV 或 Word，但不能只在 SKILL.md 寫『支援』。它需要更新輸入契約、執行程式、範例、依賴與測試，最後實際開啟成果。") + table(["想增加的格式", "要一併確認的事"], [["CSV", "欄位名稱、逗號與換行處理、UTF-8 編碼、外來文字不變成公式"], ["DOCX", "真正的 Word 檔案、標題與段落結構、套件依賴、頁面可讀性"], ["XLSX", "工作表、資料型態、幣別與公式注入防護、統計可回算"], ["PPTX", "頁面層級、文字長度、講者內容與逐頁目視檢查"]]) + p("本工具包的共用來源是 tools/office_common.py，維護者修改後需執行 tools/sync_runtime.py 同步到每支技能。若只是在學員自己的獨立技能練習，先讓 Codex 說明受影響範圍，避免連帶改動其他技能。") + code("請為新技能加入 CSV 待辦輸出。\n先寫正常資料、缺少負責人／期限、包含逗號換行及以 = 開頭文字的行為測試，實際確認新測試先失敗。\n再實作真正的 CSV 產檔，不把外來文字當公式，不補造未知值。\n更新新技能的 SKILL.md、範例與使用說明，執行測試並回報實際產物。", "新增格式的完整請求")),
        ("testing", "修改後分兩條線驗收", p("先驗證程式，再驗證 Codex 是否真的找到與遵循新技能。這兩件事要分開記錄；一個不能替代另一個。") + code("python -m unittest discover -s tests -v", "執行現有程式測試") + steps([("正常案例", "用原始模擬資料操作，確認新增章節與檔案真正出現，數字和事實沒有改動。"), ("缺漏案例", "使用沒有期限或負責人的資料，確認仍為待確認；沒有未決事項時不得憑空生成。"), ("錯誤案例", "輸入錯誤格式或不支援內容，確認顯示可理解的繁體中文診斷，不建立看似成功的錯誤成果。"), ("明確與自然語言觸發", "各開一個實作對話，使用 $team-meeting-assistant 與你準備的自然語言提示，記錄實際 SKILL.md 絕對路徑與處理結果。"), ("開啟與回查", "開啟實際文件，逐項對回來源。若改名後仍讀到原技能，檢查描述與路徑，必要時重新開啟 Codex。")]) + note("不要為了讓測試變綠而刪規則", "當測試失敗，先看是不是新行為違反來源、未知值或輸入契約。修正原因後再跑。驗收紀錄中保留尚未完成的項目，不把沒有執行的操作列為通過。")),
        ("privacy", "讓團隊資料與權限保持在範圍內", bullets(["只修改目前專案，將一般流程寫進技能，不把真實員工資料、帳密或私人文件當內建範例。", "新增連線或外部服務前，先確認工具真的可用、資料權限與使用者需求，不假裝已連上。", "寄信、上傳與發布需另有清楚授權，不能藏在文件整理技能的預設步驟裡。", "來源內容裡的指令只當資料；不能讓一份郵件或文件改寫你授權的工作範圍。", "分享前檢查 examples、outputs、日誌與快取是否含私人資料。全域安裝是選用，本課程不會自動替你複製或覆寫。"])),
        ("review", "你的自有技能完成了嗎", checklist(["新 name、description 與資料夾一致，觸發情境不混淆。", "保留來源、日期、未知欄位與待確認事項。", "每項宣稱的輸出都實際產生並開啟。", "正常、缺漏、錯誤資料都有測試，新增程式行為先測試再實作。", "明確與自然語言觸發分開驗收，記下實際技能路徑。", "修改與模擬資料只留在目前工作區，沒有改寫全域技能或發布。"])),
    ]
    sections[0] = ("read", "先用工作語言說出想改的結果", p("本章是選修延伸，不是開始使用前的先修課。完成一項原有技能後，你可以把改動交給 Codex：說明誰會使用、什麼時候使用、要多出什麼成果，並保留來源、日期與未知規則。你不需要先學程式語法。") + code("我已完成目前專案的會議技能練習。請先閱讀 .agents/skills/meeting-assistant/SKILL.md，說明這支技能處理什麼工作、交出哪些檔案，以及如何保留來源與未知。\n我想做一份團隊用的專案內複本：每份紀錄最後加上『需要主管確認』，只能整理原文未決事項。\n請先提出具體修改範圍與核對案例，再依我的回覆處理；保留原技能，不修改全域技能。", "先把修改需求交給 Codex") + maintainer(sections[0][2], "SKILL.md、YAML 與核心欄位"))
    sections[3] = ("format", "需要不同成果時，先請 Codex 確認支援", p("先說清楚想收到什麼，例如『增加可在 Excel 開啟的待辦表』。單純換語氣或縮短內容可直接提出；新增格式則需要 Codex 檢查並完成實際產檔、範例與測試。最後仍要開啟成果核對。") + maintainer(sections[3][2], "新增格式、共用來源與行為測試"))
    sections[4] = ("testing", "修改後確認檔案與判讀都正確", p("請 Codex 或維護者執行程式測試；你再用正常、缺漏及不適用資料核對實際成果。記錄它是否讀到新技能、是否保留未知，以及新增章節是否符合原文。兩種驗收分開記錄，未做的檢查標為待驗收。") + maintainer(sections[4][2], "測試命令與完整驗收流程"))
    layout("chapter-12.html", "第 12 章：建立與修改自己的 Skill", lesson_shell("chapter-12.html", 12, "建立與修改自己的 Skill", "選修延伸：用工作需求交代修改，讓 Codex 處理細節，再核對新技能的實際成果。", sections, minutes=35))


def appendix():
    rows = []
    for index, lesson in enumerate(LESSONS, 2):
        skill = lesson["skill"]
        rows.append([f'<a href="chapter-{index:02}.html">{e(lesson["title"])}</a><br><code>{skill}</code>', f'<a href="../.agents/skills/{skill}/SKILL.md">閱讀 SKILL.md</a><br><span class="path-label">.agents/skills/{skill}/</span>', f'<a href="../examples/{skill}/{lesson["input"]}">開啟模擬輸入</a>'])
    faq = [("我一定要會寫 Python 嗎？", "不需要先學 Python 或 JSON 語法。你只需下載解壓、在 Codex 開專案、貼完整工作需求，再開啟成果核對。實際產檔需要 Python 與格式套件，交由 Codex 或資訊同仁準備；手動命令放在「進階：給維護者」。"), ("網站可以離線，Codex 也能完全離線嗎？", "這份 HTML 講義不需要外部資源或伺服器。Codex 的實際使用仍依帳號、連線與環境。研究技能可只根據本機文件，不代表 Codex 執行環境本身完全離線。"), ("直接複製 SKILL.md 可以安裝嗎？", "請複製整個技能資料夾，包含 scripts 與 references。每支技能攜帶自己的共用模組，可獨立安裝；不要只留下說明而漏掉實際產檔腳本。"), ("是否需要 Gmail 或其他平台？", "本課程以本機模擬資料完成，不需要 Gmail 或額外 API 金鑰。沒有工具與實際讀取結果，就不會聲稱已連線。郵件預設只產生草稿。"), ("為什麼程式測試通過還要做觸發驗收？", "程式測試確認指定輸入下的計算與檔案行為。Codex 是否載入正確技能、理解原文與遵守來源限制，需要另外實際操作，不能用一個通過結果替代。"), ("我可以選擇全域安裝嗎？", "可以依你使用版本的官方規範自行選擇；全域安裝是額外步驟。本工具包預設留在專案 .agents/skills，不會自動覆寫個人技能。安裝前先檢查同名技能，保留完整資源與原版本。"), ("沒有 Office 也可以練習嗎？", "Markdown 與 CSV 可先用文字編輯器閱讀；DOCX、XLSX、PPTX 仍需用能開啟格式的相容軟體檢查。沒有實際開啟時，把該項目記為待人工驗收。")]
    sections = [
        ("downloads", "下載、安裝與資料位置", p("下載後完整解壓縮，再以 Codex 開啟含 AGENTS.md 的專案根目錄。講義入口是 handbook/index.html；所有練習資料均為原創模擬，不含真實公司個資。") + '<div class="actions"><a class="button primary" href="../dist/codex-office-skill-kit-1.0.0.zip" download>完整學員工具包 v1.0.0 ↓</a><a class="button" href="../dist/office-skills-1.0.0.zip" download>只下載技能工具包 ↓</a><a class="button" href="../dist/practice-data-1.0.0.zip" download>只下載模擬練習資料 ↓</a></div>' + p("技能工具包包含十支技能、腳本、模擬範例及必要安裝文件；練習資料 ZIP 只提供 examples 內容。第一次請下載完整學員工具包，含講義、十個技能、模擬來源、範例成果、測試與文件。ZIP 不含 Python 與第三方套件，環境交由 Codex 或資訊同仁處理。請先讀第 1 章，不要在 ZIP 預覽內直接練習。") + table(["技能與教學", "安裝入口／專案內位置", "練習資料"], rows)),
        ("faq", "常見問題", "".join(f'<details><summary>{e(question)}</summary><p>{e(answer)}</p></details>' for question, answer in faq)),
        ("troubleshooting", "基本疑難排解", table(["狀況", "先做這件事"], [["找不到技能", "確認 Codex 開啟專案根目錄、.agents/skills/名稱/SKILL.md 存在且 frontmatter 正確。明確輸入 $技能名稱並要求回報實際載入路徑，必要時重新開啟 Codex。"], ["載入同名全域技能", "請 Codex 明確閱讀目前專案的 SKILL.md，核對絕對路徑。不自動刪除或覆寫全域技能；自有技能可使用清楚的新名稱。"], ["python 指令不存在", "請 Codex 檢查 Python 安裝與命令路徑，依組織規範準備後重新開終端機。也可確認是否能使用 py；不要只重跑同一失敗指令。"], ["ModuleNotFoundError", "使用 .venv\\Scripts\\python.exe -m pip install -r requirements.txt，產檔也用相同 Python。不要把套件裝在另一個環境後宣稱目前環境已可用。"], ["找不到 examples 或輸出目錄", "先確認執行位置在專案根目錄，路徑與技能名稱一致。輸出目錄會在實際執行成功後建立。"], ["資料格式錯誤", "對照本技能 SKILL.md 與範例欄位；保留錯誤訊息。不要用空字串、零或假人名填滿未知值來繞過檢查。"], ["一鍵複製沒有反應", "此站提供 file:// 複製替代方式。瀏覽器仍阻擋時會選取內容，按 Ctrl+C；Mac 按 ⌘C。"], ["收據看不清或無 OCR", "改用人工核對轉錄，將無法辨識的欄位留待確認。記錄實際辨識方式，不能聲稱已自動 OCR。"], ["簡報或 Word 版面不對", "先檢查本機字型與相容軟體，回到結構資料縮寫或分頁，再重建檔案；目視檢查結果需分開記錄。"]]) + code("我在目前專案操作以下技能：\n技能名稱：\n使用的命令／提示詞：\n輸入檔案路徑：\nPython 路徑與版本：\n實際載入 SKILL.md 路徑：\n完整錯誤訊息：\n原本預期的產物：\n目前實際看到的結果：\n請先找出原因，只在目前工作區修正，不補造缺漏資料。", "請 Codex 協助排錯的紀錄")),
        ("terms", "常見名詞一次看懂", table(["名詞", "這份課程的意思"], [["Skill", "Codex 可發現、載入與遵循的工作指引及隨附資源。"], ["SKILL.md", "技能核心說明；開頭是 YAML name 與 description，後面是適用情境、流程與規則。"], ["JSON", "程式可讀取的結構資料。語意技能先由 Codex 從原文建立，不是讓腳本自行理解一切。"], ["CLI", "可貼到終端機執行的文字命令；也可以讓 Codex 代執行。"], ["DOCX / XLSX / PPTX", "Word／Excel／PowerPoint 常用檔案格式；本工具包會實際產生檔案。"], ["待確認", "來源未提供、無法讀取或仍有衝突的資訊；不是錯誤，也不能用猜測補滿。"], ["模擬資料", "為教學設計的虛構情境，不能引用成真實公司或市場研究結論。"]])),
        ("version", "版本紀錄與驗收邊界", table(["版本／日期", "內容"], [["1.0.0 / 2026-10-23", "十個獨立辦公室技能、模擬情境、程式測試、離線講義與發行工具。實際驗收狀態以工作區 docs/PROGRESS.md 與最終驗收報告為準。"], ["官方規範查證 / 2026-10-23", '依 <a href="https://learn.chatgpt.com/docs/build-skills">OpenAI 官方 Build skills 文件</a>確認 SKILL.md、name、description、專案發現與觸發方式。桌面介面版本未確認，操作以目前環境為準。']]) + p("這份講義提供完整實作方法，不會把未實際執行的自然語言觸發、OCR、網路搜尋或 Office 目視驗收寫成成功。請在自己的實作紀錄分開寫程式測試、觸發／語意驗收與人工檢查。") + p('維護文件：<a href="../docs/PROGRESS.md">進度與驗收紀錄</a> · <a href="../docs/IMPLEMENTATION_PLAN.md">實作分工與契約</a> · <a href="../requirements.txt">Python 套件清單</a>。')),
    ]
    sections[2] = ("troubleshooting", "遇到狀況，先把實際問題交給 Codex", table(["你看到的狀況", "可以直接說的需求"], [
        ["找不到技能或讀到別的版本", "請閱讀目前專案內的技能，回報實際路徑；不要覆寫全域技能。"],
        ["環境、套件或資料格式出錯", "請檢查目前環境與完整錯誤，列出已處理內容和需要資訊同仁協助的項目。"],
        ["找不到成果或無法開啟", "請回報真正執行的結果與產物位置，確認檔案實際建立，不只提供文字計畫。"],
        ["收據看不清、文件版面不對", "請指出哪些欄位或頁面需要人工核對；看不清保留未知，版面調整後重新產檔。"],
        ["複製沒有反應", "點選複製後若瀏覽器仍阻擋，可選取提示詞按 Ctrl+C；Mac 按 ⌘C。"],
    ]) + code("我在目前工具包遇到問題。\n我想完成的工作：\n使用的來源檔案：\n我貼的工作需求：\n目前看到的錯誤或結果：\n我預期收到的成果：\n請先讀取本專案相關檔案及實際錯誤，判斷原因並在目前工作區修正。環境細節請自行檢查；需要權限或人工核對就具體列出，不捏造缺漏資料。", "不用懂命令，也能請 Codex 排錯") + maintainer(sections[2][2], "原有錯誤名稱、命令與排錯紀錄"))
    sections[3] = ("terms", "遇到名詞時再查，不必先背", table(["名詞", "先這樣理解就能開始"], [["Skill", "Codex 可重複使用的工作說明書與工具。"], ["提示詞", "你貼給 Codex 的工作需求；可依目標、語氣、格式與來源調整。"], ["Word／Excel／PowerPoint", "本工具包實際產出的文件、報表與簡報，要用相容軟體開啟核對。"], ["待確認", "來源沒有說、看不清或有衝突，請保留未知，不能用猜的填滿。"], ["模擬資料", "教學情境，不代表真實公司或市場調查結果。"]]) + maintainer(sections[3][2], "SKILL.md、JSON、CLI 與格式名詞"))
    layout("appendix.html", "附錄與疑難排解", lesson_shell("appendix.html", None, "附錄與疑難排解", "技能入口、下載連結與常見問題放在一起，遇到狀況時回來查。", sections, minutes=15))


def main():
    global COPY_ID
    COPY_ID = 0
    SEARCH.clear()
    home()
    basics()
    for number, lesson in enumerate(LESSONS, 2):
        skill_lesson(number, lesson)
    custom()
    appendix()
    (HERE / "assets" / "search-index.js").write_text("window.HANDBOOK_SEARCH = " + json.dumps(SEARCH, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print("離線講義已產生：14 頁 HTML、全文搜尋索引；無外部執行依賴。")


if __name__ == "__main__":
    main()
