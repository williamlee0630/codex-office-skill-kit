"""離線講義的結構、內容契約與資源連結驗證。"""
import re
import json
import importlib.util
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "handbook"
SKILLS = ["email-assistant", "receipt-organizer", "presentation-maker", "document-writer",
          "data-analyst", "idea-generator", "research-assistant", "legal-reviewer", "finance-assistant"]


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.ids = set()
        self.links = []
        self.runtime = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append((tag, values))
        if "id" in values:
            self.ids.add(values["id"])
        if "href" in values:
            self.links.append(values["href"])
        if tag == "script" and "src" in values:
            self.runtime.append(values["src"])
        if tag in {"img", "iframe", "source"} and "src" in values:
            self.runtime.append(values["src"])
        if tag == "link" and values.get("rel") == "stylesheet":
            self.runtime.append(values["href"])


class HandbookTests(unittest.TestCase):
    def test_runtime_requests_change_when_handbook_version_changes(self):
        """舊版頁面已快取搜尋索引時，升版應要求不同資源 URL。"""
        sys.path.insert(0, str(BOOK))
        try:
            spec = importlib.util.spec_from_file_location('handbook_build_test', BOOK / 'build.py')
            builder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(builder)
        finally:
            sys.path.remove(str(BOOK))
        temporary_root = ROOT / 'tests/.tmp'
        temporary_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            builder.HERE = Path(temporary)
            builder.VERSION = 'previous'
            builder.layout('index.html', '首頁', '')
            before = Document((builder.HERE / 'index.html').read_text(encoding='utf-8')).runtime
            builder.VERSION = 'current'
            builder.layout('index.html', '首頁', '')
            after = Document((builder.HERE / 'index.html').read_text(encoding='utf-8')).runtime
            self.assertNotEqual(before, after)

    def test_all_lessons_are_substantial_and_have_ten_teaching_sections(self):
        self.assertTrue((BOOK / "index.html").exists(), "尚未建立講義首頁")
        for index, skill in enumerate(SKILLS, 2):
            path = BOOK / f"chapter-{index:02}.html"
            with self.subTest(skill=skill):
                self.assertTrue(path.exists(), str(path))
                source = path.read_text(encoding="utf-8")
                doc = Document(source)
                self.assertIn(f"${skill}", source)
                self.assertGreater(len(re.sub("<[^>]+>", "", source)), 2600)
                for section in range(1, 11):
                    self.assertIn(f"lesson-{section}", doc.ids)
                self.assertIn("模擬", source)
                self.assertIn("待確認", source)
                self.assertIn("data-copy", source)
        for name in ["chapter-01.html", "chapter-11.html", "appendix.html"]:
            self.assertTrue((BOOK / name).exists())

    def test_navigation_links_and_local_anchors_resolve(self):
        paths = list(BOOK.glob("*.html"))
        self.assertEqual(len(paths), 13)
        parsed = {p.resolve(): Document(p.read_text(encoding="utf-8")) for p in paths}
        for path, doc in parsed.items():
            self.assertIn("main", doc.ids)
            self.assertIn("chapter-search", doc.ids)
            for href in doc.links:
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                if target.suffix == ".zip":
                    self.assertTrue(str(target).startswith(str(ROOT / "dist")))
                    continue  # ZIP 實體由發行測試負責，避免建置順序相依。
                self.assertTrue(target.exists(), f"{path.name} 的失效連結：{href}")
                if url.fragment and target in parsed:
                    self.assertIn(unquote(url.fragment), parsed[target].ids, href)

    def test_search_results_follow_current_chapters_and_pagination(self):
        script = (BOOK / "assets/search-index.js").read_text(encoding="utf-8")
        index = json.loads(script.removeprefix("window.HANDBOOK_SEARCH = ").strip().removesuffix(";"))
        for number, skill in enumerate(SKILLS, 2):
            filename = f"chapter-{number:02}.html"
            results = [item for item in index if item["url"].startswith(filename + "#")]
            self.assertEqual(len(results), 10, filename)
            self.assertTrue(all(skill in item["text"] for item in results))
            source = (BOOK / filename).read_text(encoding="utf-8")
            pagination = re.search(r'<nav class="lesson-nav".*?</nav>', source).group(0)
            self.assertIn(f'chapter-{number-1:02}.html', pagination)
            self.assertIn(f'chapter-{number+1:02}.html', pagination)
        for retired in ["meeting-assistant", "project-tracker", "weekly-report", "chapter-12.html"]:
            self.assertNotIn(retired, script)
        self.assertTrue(any(item["url"].startswith("chapter-11.html#") for item in index))

    def test_no_remote_runtime_or_local_fetch(self):
        for path in BOOK.glob("*.html"):
            source = path.read_text(encoding="utf-8")
            for resource in Document(source).runtime:
                self.assertFalse(resource.startswith(("http:", "https:", "//")), resource)
                self.assertTrue((path.parent / urlsplit(resource).path).exists(), resource)
        script = (BOOK / "assets" / "app.js").read_text(encoding="utf-8")
        css = (BOOK / "assets" / "style.css").read_text(encoding="utf-8")
        self.assertNotRegex(script, r"\bfetch\s*\(|XMLHttpRequest|import\s*\(")
        self.assertNotRegex(css, r"@import|https?://")
        self.assertIn("execCommand", script, "file:// 情境需要複製替代方法")
        self.assertIn("aria-expanded", script)
        self.assertIn("Escape", script)

    def test_downloads_and_boundary_are_explained(self):
        source = (BOOK / "index.html").read_text(encoding="utf-8")
        self.assertIn("../dist/office-skills-1.2.0.zip", source)
        self.assertIn("../dist/practice-data-1.2.0.zip", source)
        basics = (BOOK / "chapter-01.html").read_text(encoding="utf-8")
        self.assertIn("SKILL.md", basics)
        self.assertIn(".agents/skills", basics)
        self.assertIn("requirements.txt", basics)
        self.assertIn("原始資料", basics)
        self.assertIn("觸發驗收", basics)


if __name__ == "__main__":
    unittest.main()
