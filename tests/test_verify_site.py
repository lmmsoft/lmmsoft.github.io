from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]
VERIFY = REPOSITORY / "scripts" / "verify_site.py"


class VerifySiteTest(unittest.TestCase):
    def make_site(self, root: Path) -> None:
        files = {
            "index.html": "<html></html>",
            "404.html": "<html></html>",
            "archives/index.html": "<html></html>",
            "category/index.html": "<html></html>",
            "tags/index.html": "<html></html>",
            "travel/index.html": '<html><ul class="travel-posts-list"><li><a href="/trip/">游记</a></li></ul></html>',
            "trip/index.html": '<html><script src="https://lmm333.disqus.com/embed.js"></script></html>',
            "feed.xml": (
                '<?xml version="1.0"?><rss xmlns:atom="http://www.w3.org/2005/Atom">'
                '<channel><atom:link href="https://lmmsoft.github.io/feed.xml" '
                'rel="self" type="application/rss+xml"/></channel></rss>'
            ),
            "feed.atom": '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"/>',
            "images/favicon.ico": "fixture",
        }
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def run_verify(self, site: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VERIFY), str(site)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_accepts_compatible_site(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.make_site(site)
            result = self.run_verify(site)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("兼容性验证通过", result.stdout)

    def test_rejects_wrong_rss_self_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.make_site(site)
            feed = site / "feed.xml"
            feed.write_text(feed.read_text().replace("/feed.xml", "/zfeed.xml"))
            result = self.run_verify(site)
        self.assertEqual(result.returncode, 1)
        self.assertIn("RSS self link", result.stderr)

    def test_rejects_malformed_rss_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.make_site(site)
            (site / "feed.xml").write_text("<rss>")
            result = self.run_verify(site)
        self.assertEqual(result.returncode, 1)
        self.assertIn("不是有效 XML", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_navigation_is_not_an_article(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.make_site(site)
            (site / "travel/index.html").write_text('<a href="/archives/">归档</a>')
            result = self.run_verify(site)
        self.assertEqual(result.returncode, 1)
        self.assertIn("没有生成任何相关文章链接", result.stderr)

    def test_rejects_missing_article_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.make_site(site)
            (site / "trip/index.html").unlink()
            result = self.run_verify(site)
        self.assertEqual(result.returncode, 1)
        self.assertIn("相关文章目标不存在", result.stderr)


if __name__ == "__main__":
    unittest.main()
