"""維護時預先產生靜態講義；學員閱讀時不需要執行 Python 或啟動伺服器。"""
from html import escape
import json
from pathlib import Path
import re

from lessons import LESSONS
from experiences import EXPERIENCES

HERE = Path(__file__).resolve().parent
VERSION = "1.2.0"
ASSET_REVISION = "20261101-quickstart"
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


def code(text, label="可以直接複製", learner=False):
    global COPY_ID
    COPY_ID += 1
    identifier = f"copy-{COPY_ID}"
    block = f'<div class="code-block"><div class="code-label"><span>{e(label)}</span><button class="copy-button" type="button" data-copy="{identifier}" aria-label="複製{e(label)}">複製</button></div><pre id="{identifier}"><code>{e(text)}</code></pre></div>'
    if not learner and not re.fullmatch(r"\$[a-z0-9-]+", text.strip()):
        return maintainer(block, label)
    return block


def maintainer(body, topic="手動操作與格式細節"):
    """原始命令與契約仍可查閱、複製，預設留給需要維護的人展開。"""
    return f'<details class="maintainer"><summary>進階：給維護者｜{e(topic)}</summary><div class="details-body">{body}</div></details>'


def work_prompt(lesson):
    return "$" + lesson["skill"]


def experience(skill):
    item = EXPERIENCES[skill]
    body = p(e(item['task']))
    if item['attachments']:
        body += '<h3>先下載附件</h3><div class="actions attachment-actions">'
        for filename, label in item['attachments']:
            body += f'<a class="button" href="../examples/quickstart/{e(filename)}" download="{e(filename)}">{e(label)} ↓</a>'
        body += '</div>' + p('每份檔案分別下載即可，不必打開 ZIP 尋找。把下載的附件拖曳進 Codex；看見附件已加入後，再貼上下方提示詞。')
        if skill == 'receipt-organizer':
            body += '<a href="../examples/quickstart/模擬文具收據.png" target="_blank" rel="noopener">先開啟收據照片預覽 ↗</a>'
    else:
        body += p('不需要下載附件。提示詞已包含這次工作的完整素材，直接複製即可。')
    body += code(item['prompt'], '完整工作提示詞', learner=True)
    body += '<h3>照這個順序操作</h3>' + steps([
        ('介紹工作情境', item['task']),
        ('下載附件（如需要）', '本章下載檔就是工作輸入，不是安裝檔；可用自己的資料取代。' if item['attachments'] else '本章不需附件，素材已寫在提示詞中。'),
        ('複製提示詞', '按「複製」，在已載入技能的 Codex 新對話中貼上完整內容。安裝是一次性準備，每次使用不必重新安裝。'),
        ('Codex 執行', '送出後讓 Codex 讀來源、整理並實際產檔，只補充真正必要的問題。'),
        ('開啟成果', '點選 Codex 回覆中的實際檔案連結，開啟檢查；若只有計畫或沒有檔案，請要求接續產檔。'),
    ])
    body += '<h3>會拿到哪些檔案</h3>' + bullets(item['outputs'])
    body += '<h3>打開後這樣檢查</h3>' + checklist(item['checks'])
    body += note('教學用途', '全部情境與附件均為原創模擬資料，沒有真實個人資料。換成自己的資料時，請同步修改提示詞中的模擬說明、工作背景與日期，以實際來源為準。')
    if skill == 'finance-assistant':
        body += maintainer(p('主示範只做兩份 CSV 對帳。預算差異分析與財務報表編製仍保留，請展開本章進階模擬練習資料區，選用預算／實際或試算表資料，另開一次任務。不要把三種任務混在同一次示範。'), '預算差異分析與財務報表編製')
    return '<div class="experience-card">' + body + '</div>'


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
PAGES += [("chapter-11.html", "建立與修改自己的 Skill", "延伸學習", "11"), ("appendix.html", "附錄與疑難排解", "資源入口", "附")]


def nav(current):
    result = []
    for index, (url, title, category, number) in enumerate(PAGES):
        if index in (0, 2, 11):
            heading = {0: "開始學習", 2: "九個辦公室技能", 11: "繼續探索"}[index]
            result.append(f'<div class="nav-group">{heading}</div>')
        active = ' aria-current="page"' if current == url else ''
        result.append(f'<a href="{url}"{active}><span class="chapter-number">{number}</span><span>{e(title)}</span></a>')
    return "".join(result)


def layout(url, title, inner, home=False):
    breadcrumb = "歡迎來到你的 AI 辦公室" if home else title
    html = f'''<!doctype html>
<html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="原創繁體中文 Codex 辦公室技能教學。九個獨立技能、模擬資料與完整實作，可離線閱讀。"><meta name="color-scheme" content="light"><title>{e(title)}｜AI 辦公室實作指南</title><link rel="stylesheet" href="assets/style.css?v={VERSION}"><script src="assets/search-index.js?v={VERSION}" defer></script><script src="assets/app.js?v={VERSION}" defer></script></head>
<body><a class="skip" href="#main">跳到主要內容</a><div class="mobile-bar"><a class="mobile-brand" href="index.html">AI 辦公室 · 實作指南</a><button type="button" class="menu-button" id="menu-button" aria-controls="sidebar" aria-expanded="false">章節目錄 ☰</button></div>
<aside class="sidebar" id="sidebar" aria-label="課程章節"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"><svg width="22" height="25" viewBox="0 0 22 25" fill="none"><path d="M5 21V5h12v16H5Z" stroke="currentColor" stroke-width="1.3"/><path d="M8 9h6M8 13h6M8 17h3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/><path d="M3 3v17M7 3h12v16" stroke="currentColor" stroke-width="1.3" opacity=".5"/></svg></span><span>AI 辦公室<small>CODEX 實作指南</small></span></a><span class="edition">離線講義 · v{VERSION}</span>
<div class="search-wrap"><span class="search-icon" aria-hidden="true"><svg width="13" height="13" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="4.5" stroke="currentColor" stroke-width="1.5"/><path d="m10.5 10.5 3 3" stroke="currentColor" stroke-width="1.5"/></svg></span><input class="search" id="chapter-search" type="search" placeholder="搜尋章節、技能或問題" aria-label="搜尋講義全文" aria-controls="search-results" autocomplete="off"></div><div class="search-help">Ctrl / ⌘ K 快速搜尋</div><ul class="search-results" id="search-results" aria-label="搜尋結果" aria-live="polite" hidden></ul>
<nav class="chapters" aria-label="章節導覽">{nav(url)}</nav><div class="sidebar-foot">日常工作，隨時可用。<br>保留來源，讓未知保持可見。<br><a href="appendix.html#downloads">下載教材與工具包 ↗</a></div></aside>
<div class="page"><div class="topbar"><span>{e(breadcrumb)}</span><span class="updated"><i class="status-dot" aria-hidden="true"></i>可離線閱讀 · 2026.10</span></div><main class="content" id="main" tabindex="-1">{inner}</main><footer class="footer"><span>AI 辦公室實作指南 · v{VERSION} · 原創繁體中文教材</span><span>練習資料全為模擬 · 無外部網站依賴</span></footer></div><div class="toast" id="toast" role="status" aria-live="polite"></div></body></html>'''
    html = html.replace(f'?v={VERSION}', f'?v={VERSION}-{ASSET_REVISION}')
    html = html.replace('2026.10</span>', '2026.11</span>')
    (HERE / url).write_text(html, encoding="utf-8")


def lesson_shell(url, number, title, deck, sections, skill=None, minutes=20):
    if skill in EXPERIENCES:
        sections = [('try-now', '立即體驗｜複製提示詞，交付工作', experience(skill)), *sections]
    eyebrow = f"CHAPTER {number:02} / 實作課程" if number else "APPENDIX / 隨手查閱"
    meta = f"<span>延伸自學約 {minutes} 分鐘</span><span>Windows / Codex</span><span>日常工作工具</span>"
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
        cards += f'<a class="skill-card" href="chapter-{number:02}.html"><div class="card-top"><span class="card-number">CHAPTER {number:02}</span><span class="card-category">{e(lesson["category"])}</span></div><h3>{e(lesson["title"])}</h3><p>{e(lesson["card"])}</p><div class="card-bottom"><span>{e(lesson["skill"])} · 自學約 {lesson["minutes"]} 分鐘</span><span class="card-arrow" aria-hidden="true">↗</span></div></a>'
    hero = '''<section class="hero"><div><div class="eyebrow">日常辦公工具 · 給沒有程式基礎的辦公室夥伴</div><h1>把日常工作，<br><span>整理成可靠成果。</span></h1><p class="intro">技能安裝一次即可。選擇工作情境，下載附件（如需要），複製完整提示詞交給 Codex。Codex 會自行讀取規則、檢查環境、整理資料並產檔；你負責核對成果。</p><div class="actions"><a class="button primary" href="chapter-01.html">開始使用 <span aria-hidden="true">→</span></a><a class="button" href="../dist/codex-office-skill-kit-1.2.0.zip" download>下載完整學員工具包 ↓</a></div><div class="quiet">不需程式背景 · 自備 Codex · 練習資料全為模擬</div></div><div class="flow-card" aria-label="日常工作操作"><div class="flow-label">安裝後，每次都能直接開始</div><div class="flow-row"><div class="flow-icon">01</div><div><strong>介紹工作情境</strong><small>技能已安裝後，直接選擇章節</small></div></div><div class="flow-arrow"></div><div class="flow-row"><div class="flow-icon">02</div><div><strong>下載附件（如需要）</strong><small>各章直接下載，拖曳進 Codex</small></div></div><div class="flow-arrow"></div><div class="flow-row"><div class="flow-icon">03</div><div><strong>複製提示詞，Codex 執行</strong><small>完整工作需求已備妥</small></div></div><div class="flow-last"><span>04　開啟並核對成果</span><span>✓</span></div></div></section>'''
    review = section("course-review", "日常使用與教學安排", table(["審閱重點", "課程安排"], [
        ["課程目標", "讓沒有程式基礎的學員，能用自然語言交代工作，取得實際檔案，並依來源核對事實、數字與待確認事項。"],
        ["九個技能用途", "郵件、收據、簡報、商務文件、資料分析、創意企劃、來源研究、法務審查、財務對帳；下方各卡片可直接進入對應實作。"],
        ["操作方式", "安裝是一次性準備。每次使用：介紹工作情境 → 下載附件（如需要）→ 複製提示詞 → Codex 執行 → 開啟成果。"],
        ["可帶走的教材", "完整 ZIP 內有 13 頁離線講義、九個技能、模擬來源與範例成果、安裝及維護文件。另提供技能包及練習資料包。"],
        ["環境與人工確認限制", "產檔確實需要 Python 與格式套件，由 Codex 或資訊同仁準備；Codex 使用依帳號及連線。學員不需先學語法。Office 版面、收據模糊欄位、未知資料與正式使用前的內容仍需人工確認。"],
        ["審閱狀態", '歷史開課方審閱版已更新為日常工作入口，未宣稱全面驗收。程式測試、Codex 觸發與語意、瀏覽器操作、Office 畫面各有邊界；請讀 <a href="../ACCEPTANCE.md">實際驗收報告</a>。'],
    ]))
    overview = '<div class="overview-strip"><div><strong>9 個獨立技能</strong><span>依工作選擇，無須依序啟動</span></div><div><strong>11 章完整教學</strong><span>從第一次操作到調整自己的技能</span></div><div><strong>7 份獨立附件</strong><span>章內直接下載，全部為教學模擬</span></div></div>'
    learning = '<section class="two-col"><div><h2>Skill 是什麼？</h2><p>把 Skill 想成 Codex 隨時可讀的工作說明書：它約定這類工作怎麼處理、要保留什麼，以及交出哪些成果。你不需先理解程式架構，就能開始使用。</p><p>各章「立即體驗」已準備完整提示詞；郵件、簡報、文件、創意不需附件，其餘五章先下載工作素材。只輸入技能名稱也能開始，由技能詢問必要素材。每次仍要檢查來源、未知欄位與實際檔案。</p></div><div><h2>怎麼安排學習？</h2><ol><li>讀第一章，安裝並載入要用的技能。</li><li>挑熟悉的工作，下載附件（如需要），複製章首完整提示詞。</li><li>讓 Codex 準備環境並產檔，再開啟成果回查原文。</li><li>需要改流程時，再讀第十一章；進階內容可稍後展開。</li></ol></div></section>'
    downloads = section("downloads", "教材帶著走，離線也能讀。", p("初次使用建議下載完整學員工具包，講義、技能與模擬資料一次備齊。ZIP 不包含 Python 與第三方套件；首次準備套件與 Codex 使用仍依帳號、權限及連線環境。") + '<div class="actions"><a class="button primary" href="../dist/codex-office-skill-kit-1.2.0.zip" download>完整學員工具包 v1.2.0 ↓</a><a class="button" href="../dist/office-skills-1.2.0.zip" download>只下載技能工具包 ↓</a><a class="button" href="../dist/practice-data-1.2.0.zip" download>只下載模擬練習資料 ↓</a><a class="button" href="appendix.html">安裝入口與常見問題 →</a></div>')
    route = section("course-route", "30 分鐘錄製課程路線", p("這是影片的成果展示安排；每張技能卡及各章標示的時間是延伸自學練習時間，兩者分開計算。各段統一錄製：介紹工作情境 → 下載附件（如需要）→ 複製提示詞 → Codex 執行 → 開啟成果。先安裝一次，示範時不必重新安裝。") + table(["影片時間", "內容與觀看重點"], [
        ["3 分鐘", '<a href="chapter-01.html">Skill 概念與安裝</a>：認識啟動、提供素材、核對成果。'],
        ["14 分鐘", "七個既有 Skill 的成果展示：郵件、收據、簡報、商務文件、資料分析、創意企劃、資料研究。"],
        ["4 分鐘", '<a href="chapter-09.html">法務助理成果展示</a>：由原始條款回查風險及修訂建議。'],
        ["4 分鐘", '<a href="chapter-10.html">財務助理成果展示</a>：核對交易、差額與可重算的 Excel。'],
        ["4 分鐘", '<a href="chapter-11.html">修改自己的 Skill</a>：用工作語言指定一項可驗收的變更。'],
        ["1 分鐘", "總結：保留來源、開啟成果，將未知與待人工確認事項留在結果中。"],
    ]))
    inner = hero + overview + review + route + '<section aria-labelledby="skills-title"><div class="section-head"><h2 id="skills-title">今天，先解決哪件工作？</h2><span>選一個熟悉情境，開始動手</span></div>' + cards + '</section><div class="start-card"><div><div class="eyebrow" style="margin-bottom:8px">第一次接觸 SKILL？</div><h2>從眼前的一件工作開始。</h2><p>例如提供郵件，整理待辦與回覆草稿。直接複製該章完整郵件情境，不必尋找工具包裡的練習檔。</p></div><a class="button" href="chapter-02.html">前往郵件技能 →</a></div>' + learning + downloads
    layout("index.html", "課程首頁", inner, True)
    SEARCH.append({"title": "課程首頁與下載", "chapter": "開始學習", "url": "index.html", "text": "開課方審閱版 課程目標 Skill Prompt 下載 工具包 學習順序 模擬 教材"})


def basics():
    sections = [
        ("understand", "五步開始，日常工作直接用", p("這九個 Skill 是可長期使用的日常辦公工具。課程是介紹與教學管道，技能執行時依你的實際工作處理。不需要先學 Python 或 JSON 語法，也不需要教 AI 讀取規則；環境、格式套件與產檔都由 Codex 接手，遇到具體權限限制才請資訊同仁協助。") + steps([
            ("安裝並載入技能", "下載工具包並完整解壓縮；依安裝說明放到 Codex 可發現的技能位置，載入後可在一般工作區使用。"),
            ("選擇工作情境，下載附件（如需要）", "各章立即體驗已準備工作素材；不需要找工具包內部檔案，附件可換成自己的資料。"),
            ("複製完整提示詞", "按該章的複製按鈕，提示詞已包含 $技能名稱 與工作需求；有附件先拖曳進 Codex，再貼上送出。"),
            ("Codex 執行，必要時補答", "讀來源、準備環境與產檔交給 Codex；只補會影響結果的關鍵資訊，已有素材時直接執行。"),
            ("開啟並核對成果", "檢查可開啟的檔案連結、來源、數字與待確認事項；直接用日常語言要求修改。"),
        ])),
        ("files", "你的工作資料就是起點", p("原始來源可以是郵件、會議筆記、工作紀錄、收據、報告或表格。無須固定檔名、表單或提示格式；Codex 會檢查可讀檔案、工作表與欄位。一般工作不會自動讀取工具包模擬資料來替代你的內容。") + p("技能內含自身規則、參考文件及執行資源，安裝時保留完整資料夾。工作成果預設另存到目前工作區 outputs 下的新資料夾，避免覆寫原檔及舊成果；最後依實際連結開啟。")),
        ("install", "安裝一次，之後直接使用", p("安裝工具包是一次性準備工作；每次使用 Skill 不需要重新安裝。各章下載的照片、CSV 與 Word 是本次工作的輸入，不是安裝檔，可用自己的資料取代。ZIP 直接拖曳安裝尚未逐環境驗證，不能保證所有環境成功；以下完整解壓與手動安裝為備案。") + p('完整解壓下載包，在 Codex 開啟解壓資料夾即可使用其中的專案技能。要帶到其他工作區，可複製完整技能資料夾到該工作區的 .agents/skills/，或依 <a href="../docs/INSTALL.md">安裝說明</a>選用個人技能安裝。重新載入後送出技能名稱。') + p("Python 及格式套件由技能自行檢查；可用就沿用，缺少時在目前工作區準備。ZIP 沒有包入 Python。首次安裝可能需要網路或組織權限；限制會具體回報。講義可離線閱讀，Codex 使用仍依帳號與連線。") + maintainer(p("每支技能含 SKILL.md、scripts/run.py、scripts/requirements.txt、references/operation.md 與 workflow.md。不要只複製 SKILL.md。同名技能疑難由 Codex 自行檢查已載入來源，不要求使用者回報路徑，也不自動覆寫全域技能。"), "安裝結構、環境與同名版本排錯")),
        ("activate", "複製完整需求即可開始", p('第一次練習請開啟 <a href="chapter-02.html#try-now">郵件章「立即體驗」</a>，複製包含三封完整郵件的提示詞。九章都有自己的工作情境；有附件的章節先下載並拖曳附件，再貼提示詞。下方保留只用技能名稱啟動的另一種用法，適合有自己資料時使用。') + code("$email-assistant", "啟動郵件技能") + table(["對話角色", "日常工作示意"], [["Codex", "請提供要整理或回覆的郵件，貼上內文或提供檔案都可以。我會整理待辦、回覆草稿與待確認事項，不直接寄送。"], ["使用者", "請整理附件郵件並擬回覆；沒有寫明期限的地方先留待確認。"], ["Codex", "讀取原信並實際產生每日摘要與多種語氣的回覆草稿，交付檔案連結及待確認事項。"]]) + p("也可以自然地說『幫我整理這批郵件』，技能仍可自動選用。已提供完整資料時不必先單獨啟動，也不會要求再選功能。")),
        ("workflow", "只問必要資訊", table(["情況", "處理方式"], [["沒有原始素材", "簡短請你提供需要的內容，不先讀示範答案。"], ["財務會計期間或合約適用法域有歧義", "先從需求與來源判斷，仍不明確才問關鍵背景。"], ["沒有標題、檔名或一般版式", "採合理預設，不為此停止。"], ["人名、期限、成效數字未提供", "保留待確認，完成其餘可用成果。"], ["補充或修正資訊", "沿用前文與來源更新，保留舊成果，不要求重貼。"]])),
        ("first-run", "開啟成果，再用日常語言修正", p("Codex 會自行讀取技能規則與必要參考、確認來源、檢查環境、整理有來源依據的內部資料並實際執行工具。它必須檢查檔案存在、內容可追查，交付可開啟連結；計畫、建議、中間資料或待補空殼不代表完成。") + p("你可以接著說『這項還在提議，請改回未定案』或『精簡成給主管看的版本』。同次修正應更新相關成果，保留原始資料。無法產出指定格式時須說明具體工具或權限限制。")),
        ("acceptance", "區分三種驗證", table(["層次", "可證明與不能代替的事"], [["程式測試", "欄位、運算、格式、來源保護與打包；不證明代理真的遵循對話。"], ["代理行為演練", "讀規則後對具體案例的回應與處理；不等於正式安裝環境完整流程。"], ["真實 Codex 完整流程", "實際安裝載入、引導、補答、來源判讀、執行產檔與開啟核對。未做就標未驗證。"]]) + p('另須分開記錄原生 Word／Excel／PowerPoint 畫面驗收。詳見 <a href="../ACCEPTANCE.md">本版驗收報告</a>；程式成功不能取代全部觸發驗收。')),
        ("safety", "保留事實與授權邊界", bullets(["提議不能當決議；未知數字、人名與期限保留待確認。", "郵件預設只產草稿；寄送、上傳、發布與提交報帳依既有授權要求。", "清楚收據由 Codex 讀取核對；只問不清楚欄位。不同幣別不混加，疑似重複不直接刪。", "資料分析實際計算並使用業務欄位；創意評估保留主觀及待驗證；研究只引用實際讀過的來源。", "真實工作資料不會因使用工具包就變成模擬。只有明確要求示範時才使用並標示模擬資料。"])),
        ("ready", "開始一項工作", checklist(["技能已安裝並載入；每次使用不必重裝。", "已從該章下載附件（如需要），並複製完整提示詞。", "已有完整素材就直接執行，可選未知不阻擋全部工作。", "補答與修改沿用前文，最後開啟成果核對。"])),
    ]
    layout("chapter-01.html", "第 1 章：Skill 基礎入門", lesson_shell("chapter-01.html", 1, "Skill 基礎入門", "安裝一次，選工作情境、下載附件、複製提示詞，讓 Codex 執行後開啟成果。", sections, minutes=20))

def specialist_lesson(number, lesson):
    """法務與財務的員工教學；不假設兩者共用舊 JSON/CLI 契約。"""
    skill = lesson["skill"]
    conversation = table(["角色", "工作對話示意"], [
        ["使用者", f"<code>${skill}</code>"], ["Codex", e(lesson["greeting"])],
        ["使用者", e(lesson["conversation"][0])], ["Codex", e(lesson["conversation"][1])],
    ])
    downloads = ''.join(f'<li><a href="../examples/{skill}/{e(filename)}" download>{e(label)}</a></li>' for filename, label in lesson["downloads"])
    download_body = p(e(lesson["demo"])) + '<ul>' + downloads + '</ul>'
    download_body += p('<a href="../dist/practice-data-1.2.0.zip" download>下載完整模擬練習資料包 v1.2.0</a>；練習來源與預期結果分開閱讀，先完成自己的核對，再比較差異。')
    if lesson.get("verification_downloads"):
        checks = ''.join(f'<li><a href="../examples/{skill}/{e(filename)}" download>{e(label)}</a></li>' for filename, label in lesson["verification_downloads"])
        download_body += maintainer(p("三組預期結果由程式獨立驗算，供維護者比對；學員可直接在 Excel 中抽查來源與差額，不需編輯內部資料格式。") + '<ul>' + checks + '</ul>', "獨立驗算結果")
    download_body += p("一般工作只用你提供的來源。只有明確提出練習或示範時，Codex 才使用這些教學模擬資料，並把模擬標記留在成果裡。")
    outputs = lesson['outputs']
    verification = lesson['verification']
    advanced_outputs = ''
    advanced_verification = ''
    if skill == 'finance-assistant':
        outputs = [item for item in outputs if item[0] in {'銀行對帳結果.xlsx', '財務分析報告.docx'}]
        advanced_outputs = maintainer(table(['進階成果檔案', '適用任務'], [[f'<code>{e(name)}</code>', e(description)] for name, description in lesson['outputs'] if (name, description) not in outputs]), '預算差異與財務報表的成果')
        verification = [lesson['verification'][0], lesson['verification'][3]]
        advanced_verification = maintainer(checklist(lesson['verification'][1:3]), '預算差異與財務報表的核對')
    sections = [
        ("lesson-1", "這個 Skill 能幫員工做什麼", paragraphs(lesson["problem"])),
        ("lesson-2", "適合哪些工作情境", bullets(lesson["audience"])),
        ("lesson-3", "日常使用的另一種啟動方式", code(work_prompt(lesson), "可複製的啟動內容") + p("也可以自然地說「" + e(lesson["natural"]) + "」。已有完整工作需求與附件時直接開始，補答後沿用前文接續處理，不重問已知內容。") + conversation),
        ("lesson-4", "需要提供什麼資料", paragraphs(lesson["materials"])),
        ("lesson-5", "學員操作步驟", steps([('介紹工作情境', EXPERIENCES[skill]['task']), ('下載附件並複製提示詞', '使用章首下載按鈕，將附件拖曳進 Codex，再貼上完整提示詞。'), ('Codex 執行', '已有完整需求與來源時直接處理；只補真正必要的問題。'), ('開啟成果', '從實際檔案連結開啟，回查來源、數字與待確認項目。')]) + p("讀規則、準備環境、整理內部資料與執行產檔都由 Codex 完成。你只需提供工作來源、補必要背景、開啟成果核對；計畫、說明或中間模板不代表已經交付。") + maintainer(steps(lesson['steps']), '其他工作類型的原有操作說明')),
        ("lesson-6", "實際產出的成果", table(["成果檔案", "你能查看的內容"], [[f"<code>{e(name)}</code>", e(description)] for name, description in outputs]) + advanced_outputs + p("產物另存新資料夾，交付實際可開啟的檔案連結，保留來源與舊成果。指定格式無法完成時，應具體說明未完成部分與原因，不能只說已產生卻沒有檔案。")),
        ("lesson-7", "如何核對成果正確性", checklist(verification) + advanced_verification + p("程式檢查、Codex 啟動與完整工作流程、原生 Word／Excel 畫面驗收分開記錄。程式可讀取檔案不代表所有環境的版面都已驗證；未執行的檢查應保留未驗證。")),
        ("lesson-8", "常見問題與使用限制", table(["常見問題", "處理方式與限制"], [[e(question), e(answer)] for question, answer in lesson["errors"]])),
        ("lesson-9", "進階：模擬練習資料下載", maintainer(download_body, "原有案例、進階練習與預期結果")),
        ("lesson-10", "想進一步修改 Skill，可以調整哪些規則", paragraphs(lesson["extension"]) + p('<a href="chapter-11.html">第 11 章：建立與修改自己的 Skill</a> 提供專案內複本、成果核對與進階維護入口。') + maintainer(p(f'<a href="../.agents/skills/{skill}/SKILL.md">完整技能規則</a> · <a href="../.agents/skills/{skill}/references/workflow.md">維護工作流程</a>；新增行為先建立失敗測試，再實作並驗證來源與產物。'), "技能規則與維護入口")),
    ]
    url = f"chapter-{number:02}.html"
    layout(url, f"第 {number} 章：{lesson['title']}", lesson_shell(url, number, lesson["title"], lesson["deck"], sections, skill, lesson["minutes"]))


def skill_lesson(number, lesson):
    if lesson.get("specialist"):
        specialist_lesson(number, lesson)
        return
    skill = lesson["skill"]
    root = f"examples/{skill}"
    source = (HERE.parent / ".agents/skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    greeting = re.search(r"^> (.+)$", source, re.M).group(1)
    work = {
        "email-assistant": ("請幫我修改這封回覆：已收到需求，交期還要確認。改得友善一些，保留交期未定。", "會依原信及現有回覆修改草稿，保留未確認的交期；整理後提供草稿檔案連結，不寄出。"),
        "receipt-organizer": ("這批出差收據請整理成報帳明細；其中一張幣別看不清。", "會先讀原件並轉錄清楚欄位，只針對那張的幣別詢問；其餘資料繼續整理，分幣別合計並產生 Excel。"),
        "presentation-maker": ("附件是工作進度，請做給主管決定下一階段範圍的簡報，頁數你安排。", "會依來源安排精簡商務簡報，保留提議與未決項目，產生可編輯 PPTX 及講者備註。"),
        "document-writer": ("請把這份草稿改成給主管的提案，預算和負責人還沒決定。", "會保留可證實事實，把預算和負責人標待確認，完成正式及精簡文件，不為補齊欄位停止。"),
        "data-analyst": ("請看附件銷售表，檢查缺漏並比較各區銷售金額，員工編號只是識別資料。", "會自行查看工作表與欄位，使用銷售金額實際計算，不把員工編號當績效；交付分析、Excel 及可用圖表。"),
        "idea-generator": ("想減少跨部門交接遺漏，先用現有工具，預算與負責人還沒定。", "會提出不同做法並比較資源、難度與預期價值，標明主觀評估和待驗證；選案後接續建立執行計畫。"),
        "research-assistant": ("請比較附件兩份供應商方案，重點是服務範圍與限制，不查外網。", "會逐一讀來源、比較條件與日期，區分事實、推論和缺口，附來源清單；不宣稱已搜尋網路。"),
    }[skill]
    technical = p(e(lesson["materials"])) + steps(lesson["steps"]) + p(e(lesson["practice"]))
    technical += code(f"python .agents/skills/{skill}/scripts/run.py --input {root}/{lesson['input']} --output outputs/{skill}" + lesson.get("arguments", ""), "維護者產檔測試")
    technical += p(f'<a href="../.agents/skills/{skill}/SKILL.md">技能規則</a> · <a href="../.agents/skills/{skill}/references/workflow.md">內部資料契約</a> · <a href="../{root}/{lesson["source"]}">模擬來源</a> · <a href="../{root}/{lesson["input"]}">範例結構資料</a>')
    if skill == "receipt-organizer":
        technical += p('教學可用 <a href="../examples/receipt-organizer/simulated-receipt.png">模擬收據 PNG</a> 或 <a href="../examples/receipt-organizer/simulated-receipt.pdf">PDF</a>。原始影像測試加 --simulation；第一次只建 transcription-template.json，不做 OCR。Codex 接著自行看圖、核對及轉錄，再產報帳 Excel，不能把模板交付為完成。')
    elif skill == "research-assistant":
        technical += p('教學原文：<a href="../examples/research-assistant/sources/plan-a.md">sources/plan-a.md</a>、<a href="../examples/research-assistant/sources/plan-b.md">sources/plan-b.md</a>。摘錄須逐字存在。若內部 JSON 位於 outputs/research-assistant，可用 ../../examples/research-assistant/sources/plan-a.md；相對路徑由 Codex 處理。')
    elif skill == "data-analyst":
        technical += p("僅此教學 sales.csv 的測試參數為 --group-by category --value amount --date-column date；實際工作依真實欄位選擇，禁止套用示範欄名。")
    demo = p('初次操作請使用章首「立即體驗」的完整提示詞與下載附件。下方保留舊有技術測試，供需要維護時展開。') + maintainer(technical, "模擬來源、保留的手動命令與測試細節")
    expected = p("這裡保留教學範例的預期成果，供明確練習時核對；不能當作一般工作的預填答案。實際成果仍依你的來源。") + maintainer(bullets(lesson["expected"]) + code(lesson["expected_sample"], "模擬預期摘錄"), "模擬範例預期內容")
    expected += table(["本技能實際產物", "核對方式"], [[f"<code>{e(item)}</code>", "開啟檔案，抽查來源、日期、數字及待確認欄位"] for item in lesson["outputs"]])
    sections = [
        ("lesson-1", "這個 Skill 解決什麼工作", paragraphs(lesson["problem"])),
        ("lesson-2", "哪些工作適合使用", bullets(lesson["audience"]) + p("這是日常工作工具，可反覆用於真實工作。自然語言也能選用，不需要依序啟動其他技能；已有完整目的與素材時直接執行。")),
        ("lesson-3", "提供必要素材即可", p("直接貼文字、附檔或提供可讀檔案，無須固定檔名、表單或長提示詞。Codex 會先讀目前對話與來源，自行查看能取得的檔案、欄位、工作表與環境；只問會阻止正確完成或實質改變結果的缺漏。") + p("標題、檔名、輸出位置與一般呈現方式採合理預設。未知人名、期限與成效數字保留待確認；有依據的內容先完成，不拿範例資料填空。")),
        ("lesson-4", "日常使用的另一種啟動方式", code(work_prompt(lesson), "可複製的啟動內容") + p("只有名稱時會依工作用途引導；已有素材或正在補答時沿用前文，不重新介紹功能或要求選擇。")),
        ("lesson-5", "實務工作對話示意", p("以下是對話方式示意，不是技能自動載入的來源，也不代表已在你的電腦產檔。你可用自己的話回答，不必回覆編號。") + table(["角色", "內容"], [["使用者", f"<code>${skill}</code>"], ["Codex", e(greeting)], ["使用者", e(work[0])], ["Codex", e(work[1])]])),
        ("lesson-6", "補答與修改會接續完成", steps([("提供資料", "直接貼素材或附檔；若來源可讀且目的清楚，Codex 直接整理並執行。"), ("只補關鍵缺漏", "需要日期、範圍或不清欄位時，回答那一個問題即可；不用重新貼完整需求。"), ("開啟成果並修改", "使用實際檔案連結核對，再用日常語言說要改哪裡；Codex 沿用來源更新相關成果並保留舊版本。")]) + p("Codex 會自行讀內部規則、檢查環境、整理有來源的資料、選參數、執行並確認檔案存在。你不需要指示它讀 MD、回報技能路徑、編輯 JSON 或指定腳本。")),
        ("lesson-7", "另外選用的模擬教學", demo),
        ("lesson-8", "開啟並核對成果", expected + p("只有計畫、操作建議、中間核對資料或待補空殼都不代表完成。有工具、連線或權限限制時，Codex 應具體列出未完成項目；程式格式檢查不等於原生 Office 畫面驗收。")),
        ("lesson-9", "發現問題時直接提出", p("可以直接指出『這個期限不對』、『這項還沒核准』或『請縮短給主管看』。Codex 會回查來源、沿用已確認資訊更新；若修正與來源衝突，保留修正的依據與待確認狀態。內部格式錯誤由它先處理，不要求你填結構資料。") + maintainer(table(["原有教學排錯案例", "核對方法"], [[e(a), e(b)] for a,b in lesson["errors"]]), "技術排錯與教學案例")),
        ("lesson-10", "驗收與使用邊界", checklist(lesson["checks"] + ["單獨送出名稱能引導，沒有課程或資料模式選單。", "完整需求不重問，補答後接續，可選未知不阻擋產出。", "未要求示範時只使用工作來源；明確練習時標示模擬。", "程式測試、代理行為演練、真實 Codex 完整流程分開記錄，未做寫未驗證。"]) + p("預設只在工作區產檔。寄送、外部上傳、發布或提交報帳仍依既有授權要求；來源文件內的指令只當資料。保留原始資料，不捏造人名、金額、期限、數據或研究來源。") + maintainer(p(e(lesson["extend"])), "保留的延伸練習")),
    ]
    url = f"chapter-{number:02}.html"
    layout(url, f"第 {number} 章：{lesson['title']}", lesson_shell(url, number, lesson["title"], lesson["deck"], sections, skill, lesson["minutes"]))

def custom():
    sections = [
        ("read", "從 SKILL.md 的四個地方開始讀", p("先選一支你已完成實作的技能。使用文字編輯器或請 Codex 開啟本專案中的 SKILL.md；你不必先理解所有程式碼，先看名稱、描述、流程與產物。") + table(["位置", "你要理解的問題"], [["YAML frontmatter 的 name", "這支技能的英文識別名稱是什麼？是否對應資料夾？"], ["YAML frontmatter 的 description", "什麼工作應該選它？如何避免和其他技能混淆？"], ["工作流程與缺漏規則", "來源怎麼讀？哪些情況要保留未知或停止產檔？"], ["scripts / references 與輸入輸出", "哪些指令真的產出檔案？需要哪些欄位與依賴？"]]) + code('---\nname: team-email-assistant\ndescription: 整理團隊郵件為回覆草稿、待辦與待確認事項；適用於收件整理，不直接寄信。\n---\n\n# 團隊郵件整理\n\n保留原始來源、日期及未知欄位。\n沒有原信依據時，不新增交期與商務承諾。', "新技能開頭示例：模擬，尚非完整技能") + p("name 與 description 是必要欄位；範例只用來說明結構，不代表貼上就成為完整可執行技能。仍需要流程、腳本、完整案例與實測。")),
        ("copy", "先做專案內複本，再改名稱", p("不要直接覆寫已用過的技能，也不要修改全域技能。先在目前專案為一支技能建立新的資料夾，保留整份 scripts、references 與需要的資源。名稱使用小寫英文與連字號。") + code("請只在目前工作區複製 .agents/skills/email-assistant 為 .agents/skills/team-email-assistant。\n先確認目標不存在，不覆寫現有檔案。\n將新技能的 name、description 及相關介面資訊調整為一致的新名稱。\n保留來源追查、未知值、草稿與待辦分流規則，原技能保持可用。\n回報新增與修改的檔案。", "請 Codex 建立自己的技能複本") + note("不要讓兩個名稱共用模糊描述", "新 description 要寫出適用與非適用情境。比如『團隊收件整理』與『正式文件撰寫』是不同工作；只寫『協助辦公室工作』，難以可靠選擇。")),
        ("workflow", "調整觸發條件與工作流程", p("先把你想改的行為說成可觀察結果。例如：每份郵件摘要最後多一段『需要主管確認』，其內容只能來自原文中的未決事項。不要只要求『更專業』，因為那很難驗收。") + steps([("定義觸發情境", "寫出兩句應該使用新技能的自然語言提示，再寫一句不適用提示。避免和原本技能完全相同。"), ("說明流程變更", "指出要在哪一步增加、刪除或重排內容。保留來源、未知與確認狀態，語氣調整不能改變事實。"), ("指定產物變更", "明確寫出新增章節或欄位的名稱與資料來源。新增 Markdown 標題可能只需改產檔規則，新增檔案格式則要改腳本。"), ("列出驗收案例", "至少準備正常、缺漏及錯誤資料。寫出你預期看到什麼，再請 Codex 動手修改。")]) + code("請修改目前專案的新技能 team-email-assistant。\n需求：輸出摘要最後加入『需要主管確認』，僅彙整原始資料中尚未確認的事項與來源。\n沒有這類事項時寫『本次原始資料未列出』，不得新增提議。\n先說明會修改哪些檔案與可觀察的驗收案例，再只修改本專案的新技能。\n保留原技能與所有未知值規則。", "把改動說成可驗收需求")),
        ("format", "加入新輸出格式時，要有實際產檔", p("你可以請 Codex 增加 CSV 或 Word，但不能只在 SKILL.md 寫『支援』。它需要更新輸入契約、執行程式、範例、依賴與測試，最後實際開啟成果。") + table(["想增加的格式", "要一併確認的事"], [["CSV", "欄位名稱、逗號與換行處理、UTF-8 編碼、外來文字不變成公式"], ["DOCX", "真正的 Word 檔案、標題與段落結構、套件依賴、頁面可讀性"], ["XLSX", "工作表、資料型態、幣別與公式注入防護、統計可回算"], ["PPTX", "頁面層級、文字長度、講者內容與逐頁目視檢查"]]) + p("本工具包的共用來源是 tools/office_common.py，維護者修改後需執行 tools/sync_runtime.py 同步到每支技能。若只是在學員自己的獨立技能練習，先讓 Codex 說明受影響範圍，避免連帶改動其他技能。") + code("請為新技能加入 CSV 待辦輸出。\n先寫正常資料、缺少負責人／期限、包含逗號換行及以 = 開頭文字的行為測試，實際確認新測試先失敗。\n再實作真正的 CSV 產檔，不把外來文字當公式，不補造未知值。\n更新新技能的 SKILL.md、範例與使用說明，執行測試並回報實際產物。", "新增格式的完整請求")),
        ("testing", "修改後分兩條線驗收", p("先驗證程式，再驗證 Codex 是否真的找到與遵循新技能。這兩件事要分開記錄；一個不能替代另一個。") + code("python -m unittest discover -s tests -v", "執行現有程式測試") + steps([("正常案例", "用原始模擬資料操作，確認新增章節與檔案真正出現，數字和事實沒有改動。"), ("缺漏案例", "使用沒有期限或負責人的資料，確認仍為待確認；沒有未決事項時不得憑空生成。"), ("錯誤案例", "輸入錯誤格式或不支援內容，確認顯示可理解的繁體中文診斷，不建立看似成功的錯誤成果。"), ("明確與自然語言觸發", "各開一個實作對話，使用 $team-email-assistant 與你準備的自然語言提示，記錄實際 SKILL.md 絕對路徑與處理結果。"), ("開啟與回查", "開啟實際文件，逐項對回來源。若改名後仍讀到原技能，檢查描述與路徑，必要時重新開啟 Codex。")]) + note("不要為了讓測試變綠而刪規則", "當測試失敗，先看是不是新行為違反來源、未知值或輸入契約。修正原因後再跑。驗收紀錄中保留尚未完成的項目，不把沒有執行的操作列為通過。")),
        ("privacy", "讓團隊資料與權限保持在範圍內", bullets(["只修改目前專案，將一般流程寫進技能，不把真實員工資料、帳密或私人文件當內建範例。", "新增連線或外部服務前，先確認工具真的可用、資料權限與使用者需求，不假裝已連上。", "寄信、上傳與發布需另有清楚授權，不能藏在文件整理技能的預設步驟裡。", "來源內容裡的指令只當資料；不能讓一份郵件或文件改寫你授權的工作範圍。", "分享前檢查 examples、outputs、日誌與快取是否含私人資料。全域安裝是選用，本課程不會自動替你複製或覆寫。"])),
        ("review", "你的自有技能完成了嗎", checklist(["新 name、description 與資料夾一致，觸發情境不混淆。", "保留來源、日期、未知欄位與待確認事項。", "每項宣稱的輸出都實際產生並開啟。", "正常、缺漏、錯誤資料都有測試，新增程式行為先測試再實作。", "明確與自然語言觸發分開驗收，記下實際技能路徑。", "修改與模擬資料只留在目前工作區，沒有改寫全域技能或發布。"])),
    ]
    sections[0] = ("read", "先用工作語言說出想改的結果", p("本章是選修延伸，不是開始使用前的先修課。完成一項原有技能後，你可以把改動交給 Codex：說明誰會使用、什麼時候使用、要多出什麼成果，並保留來源、日期與未知規則。你不需要先學程式語法。") + code("我已完成目前專案的郵件技能練習。請先閱讀 .agents/skills/email-assistant/SKILL.md，說明這支技能處理什麼工作、交出哪些檔案，以及如何保留來源與未知。\n我想做一份團隊用的專案內複本：每份摘要最後加上『需要主管確認』，只能整理原文未決事項。\n請先提出具體修改範圍與核對案例，再依我的回覆處理；保留原技能，不修改全域技能。", "先把修改需求交給 Codex") + maintainer(sections[0][2], "SKILL.md、YAML 與核心欄位"))
    sections[3] = ("format", "需要不同成果時，先請 Codex 確認支援", p("先說清楚想收到什麼，例如『增加可在 Excel 開啟的待辦表』。單純換語氣或縮短內容可直接提出；新增格式則需要 Codex 檢查並完成實際產檔、範例與測試。最後仍要開啟成果核對。") + maintainer(sections[3][2], "新增格式、共用來源與行為測試"))
    sections[4] = ("testing", "修改後確認檔案與判讀都正確", p("請 Codex 或維護者執行程式測試；你再用正常、缺漏及不適用資料核對實際成果。記錄它是否讀到新技能、是否保留未知，以及新增章節是否符合原文。兩種驗收分開記錄，未做的檢查標為待驗收。") + maintainer(sections[4][2], "測試命令與完整驗收流程"))
    layout("chapter-11.html", "第 11 章：建立與修改自己的 Skill", lesson_shell("chapter-11.html", 11, "建立與修改自己的 Skill", "選修延伸：用工作需求交代修改，讓 Codex 處理細節，再核對新技能的實際成果。", sections, minutes=35))


def appendix():
    rows=[]
    for number,lesson in enumerate(LESSONS,2):
        skill=lesson["skill"]
        rows.append([f'<a href="chapter-{number:02}.html">{e(lesson["title"])}</a>', f'<code>${skill}</code>', e(lesson["card"])])
    sections=[
        ("downloads", "下載與安裝", p("技能可長期用於日常工作。安裝並載入後，送出 $技能名稱，依引導提供素材、必要時補答，再開啟成果。完整包保留離線講義、技能與另外選用的模擬教學；技能包可帶到一般工作區。") + '<div class="actions"><a class="button primary" href="../dist/codex-office-skill-kit-1.2.0.zip" download>完整工具包 v1.2.0 ↓</a><a class="button" href="../dist/office-skills-1.2.0.zip" download>技能安裝包 ↓</a><a class="button" href="../dist/practice-data-1.2.0.zip" download>模擬教學資料包 ↓</a></div>' + p('<a href="../docs/INSTALL.md">安裝說明</a> · <a href="../dist/manifest.json">版本、SHA-256 與內容清單</a>') + table(["技能教學", "啟動名稱", "工作用途"],rows)),
        ("faq", "常見問題", ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in [
            ("只輸入名稱就可以嗎？", "可以。只有名稱時，Skill 依用途詢問必要素材；已有工作內容時直接沿用。"),
            ("一定要會 Python 或 JSON 嗎？", "不用。環境檢查、讀規則、資料整理與執行都由 Codex 完成，不需長提示詞。"),
            ("可以直接貼文字嗎？", "可以，也可提供附件或可讀檔案，不必固定表單或檔名。"),
            ("會自動跑課程資料嗎？", "不會。只有明確要求示範、練習或指定範例時，才使用並標示模擬資料。"),
            ("資料沒填完會停止嗎？", "只缺可選人名、期限或成效數字時仍完成可用成果；真正影響結果的範圍與日期才補問。"),
            ("可以離線閱讀嗎？", "講義無外部執行依賴，可雙擊 HTML 離線閱讀；Codex 與初次取得套件仍依帳號及連線。"),
        ])),
        ("troubleshooting", "遇到問題，用日常語言說明", p("直接說哪個檔案打不開、哪個欄位不對、哪項尚未確認。Codex 會沿用工作脈絡自行查來源、環境與錯誤；只有真正缺內容或權限時才具體請求協助。") + maintainer(table(["維護項目", "檢查位置"], [["技能未載入或同名版本", ".agents/skills/ 下完整技能資料夾、agents/openai.yaml；由 Codex 核對實際載入來源，必要時重新載入。"], ["套件與命令", "各技能 scripts/requirements.txt、references/operation.md；可用環境優先，缺少才在工作區準備。"], ["來源或內部格式錯誤", "references/workflow.md；修正格式不補造事實。"], ["發行與部署", "tools/verify.py、build_release.py、check_release.py、build_site.py 及 Actions。"]]), "技術排錯與維護入口")),
        ("terms", "常用名詞", table(["名詞", "意思"], [["Skill", "可重複使用的工作規則與執行資源。"], ["來源", "本次實際提供、讀取並可追查的工作資料。"], ["待確認", "未知、不清楚或來源衝突，不用猜測填滿。"], ["模擬資料", "另外選用的教學與測試內容，不代表工作資料。"]])),
    ]
    layout("appendix.html", "附錄與疑難排解", lesson_shell("appendix.html", None, "附錄與疑難排解", "安裝、技能入口、離線下載與排錯。", sections, minutes=10))

def main():
    global COPY_ID
    COPY_ID = 0
    SEARCH.clear()
    # 只移除已淘汰的生成章節；其餘靜態資源沿用。
    obsolete = HERE / "chapter-12.html"
    if obsolete.exists():
        obsolete.unlink()
    home()
    basics()
    for number, lesson in enumerate(LESSONS, 2):
        skill_lesson(number, lesson)
    custom()
    appendix()
    (HERE / "assets" / "search-index.js").write_text("window.HANDBOOK_SEARCH = " + json.dumps(SEARCH, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print("離線講義已產生：13 頁 HTML、全文搜尋索引；無外部執行依賴。")


if __name__ == "__main__":
    main()
