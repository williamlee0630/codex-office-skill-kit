"""初學者入口的內容契約；不代替瀏覽器、Codex 觸發或 Office 人工驗收。"""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "handbook"
SKILLS = ["email-assistant", "receipt-organizer", "presentation-maker", "document-writer",
          "data-analyst", "idea-generator", "research-assistant", "legal-reviewer", "finance-assistant"]


class LearnerPage(HTMLParser):
    """讀取預設展開內容與各可複製區塊，確認進階資訊確實可收合。"""
    def __init__(self, source):
        super().__init__()
        self.details = []
        self.visible = []
        self.blocks = []
        self.current = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details":
            self.details.append("open" not in attrs)
        if tag == "pre":
            self.current = {"text": "", "collapsed": any(self.details)}

    def handle_endtag(self, tag):
        if tag == "details":
            self.details.pop()
        if tag == "pre" and self.current is not None:
            self.blocks.append(self.current)
            self.current = None

    def handle_data(self, data):
        if not any(self.details):
            self.visible.append(data)
        if self.current is not None:
            self.current["text"] += data


def read(name):
    return (BOOK / name).read_text(encoding="utf-8")


class LearnerHandbookTests(unittest.TestCase):
    def test_home_explains_course_review_and_three_downloads(self):
        source = read("index.html")
        for expected in ["開課方審閱版", "課程目標", "操作方式", "人工確認", "Python",
                         "../dist/office-skills-1.2.0.zip",
                         "../dist/practice-data-1.2.0.zip"]:
            self.assertIn(expected, source)
        for name in ["office-skills-1.2.0.zip", "practice-data-1.2.0.zip"]:
            self.assertIn(f'href="../dist/{name}"', source)
            self.assertTrue((ROOT / "dist" / name).is_file(), f"缺少可下載教材：{name}")
        full_name = "codex-office-skill-kit-1.2.0.zip"
        if (ROOT / "dist" / full_name).is_file():
            # 原始網站仍須提供三份下載；不能用離線包說明替代完整包連結。
            self.assertIn(f'href="../dist/{full_name}"', source)
        else:
            # 完整 ZIP 不包含自己，解壓版改為可用的 README 導覽。
            self.assertNotIn(f"../dist/{full_name}", source)
            self.assertIn('href="../README.md"', source)
            self.assertIn("已解壓", source)
            self.assertTrue((ROOT / "README.md").is_file())
        self.assertNotIn("100%", source)

    def test_v120_course_route_and_no_retired_skill_entries(self):
        homepage = read("index.html")
        for expected in ["30 分鐘", "3 分鐘", "14 分鐘", "4 分鐘", "1 分鐘", "自學", "chapter-02.html"]:
            self.assertIn(expected, homepage)
        for path in BOOK.glob("*.html"):
            source = path.read_text(encoding="utf-8")
            for retired in ["meeting-assistant", "project-tracker", "weekly-report", "1.1.0", "chapter-12.html", "十個技能"]:
                self.assertNotIn(retired, source, path.name)
        self.assertFalse((BOOK / "chapter-12.html").exists())

    def test_new_chapters_teach_materials_verification_limits_downloads_and_extension(self):
        for number, skill, outputs, keywords in [
            (9, "legal-reviewer", ["合約審查報告.docx", "合約風險清單.xlsx", "條款修訂建議.md"],
             ["法域", "掃描", "法律來源", "高、中、低", "專業", "原始條款"]),
            (10, "finance-assistant", ["財務報表.xlsx", "銀行對帳結果.xlsx", "財務差異分析.xlsx", "財務分析報告.docx"],
             ["借貸", "幣別", "同額", "零", "一對一", "data-analyst"]),
        ]:
            source = read(f"chapter-{number:02}.html")
            visible = " ".join(LearnerPage(source).visible)
            for expected in outputs + keywords + ["使用者", "Codex", "需要提供", "學員操作", "成果正確性", "常見問題", "模擬練習資料下載", "修改 Skill", "待確認"]:
                self.assertIn(expected, visible, skill)
            self.assertRegex(source, rf'href="../examples/{skill}/[^"<>]+" download')
            for forbidden in ["run.py", "--input", "input.json", "reviewed-input.json"]:
                self.assertNotIn(forbidden, visible, skill)

    def test_first_chapter_starts_with_daily_work_path(self):
        page = LearnerPage(read("chapter-01.html"))
        visible = " ".join(page.visible)
        previous = -1
        for step in ["安裝並載入技能", "送出 $技能名稱", "依引導說明工作或提供素材", "必要時補答", "開啟並核對成果"]:
            position = visible.find(step)
            self.assertGreater(position, previous, step)
            previous = position
        self.assertIn("資訊同仁", visible)
        self.assertIn("不需要先學 Python 或 JSON 語法", visible)
        self.assertIn("格式套件", visible)

    def test_manual_commands_stay_in_closed_maintainer_details(self):
        for path in BOOK.glob("*.html"):
            page = LearnerPage(path.read_text(encoding="utf-8"))
            for block in page.blocks:
                if re.search(r"(?m)^(?:python |py |\.\\.venv\\|---$|codex-office-skill-kit/)", block["text"]):
                    with self.subTest(page=path.name, block=block["text"].splitlines()[0]):
                        self.assertTrue(block["collapsed"], "手動命令與原始結構應預設收合")

    def test_each_visible_startup_block_is_only_the_skill_token(self):
        for number, skill in enumerate(SKILLS, 2):
            page = LearnerPage(read(f"chapter-{number:02}.html"))
            prompts = [b["text"] for b in page.blocks if not b["collapsed"]]
            with self.subTest(skill=skill):
                self.assertTrue(prompts)
                self.assertEqual(set(prompts), {f"${skill}"})

    def test_daily_work_conversations_do_not_expose_internal_steps(self):
        for number in range(2, 11):
            visible = " ".join(LearnerPage(read(f"chapter-{number:02}.html")).visible)
            with self.subTest(chapter=number):
                for expected in ["使用者", "Codex", "工作", "來源", "待確認"]:
                    self.assertIn(expected, visible)
                for obsolete in ["回報實際載入的絕對路徑", "建立 reviewed-input.json", "貼上整段", "課程範例／自己的資料"]:
                    self.assertNotIn(obsolete, visible)

    def test_special_flows_match_the_existing_script_contracts(self):
        receipt = read("chapter-03.html")
        for expected in ["simulated-receipt.png", "transcription-template.json", "--simulation", "不做 OCR"]:
            self.assertIn(expected, receipt)
        research = read("chapter-08.html")
        for expected in ["sources/plan-a.md", "sources/plan-b.md", "../../examples/research-assistant", "逐字"]:
            self.assertIn(expected, research)
        analysis = read("chapter-06.html")
        self.assertIn("--group-by category --value amount --date-column date", analysis)


if __name__ == "__main__":
    unittest.main()
