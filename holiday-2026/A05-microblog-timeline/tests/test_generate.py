import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
import generate


def entry(ident, date="2026-01-01T00:00:00Z", tags="[DEMO]", body="safe", draft="false"):
    return f"---\nid: {ident}\ndate: {date}\ntags: {tags}\nbody: \"{body}\"\ndraft: {draft}\n---\n"


class GeneratorTests(unittest.TestCase):
    def build(self, rows, include_drafts=False):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        source = Path(temp.name) / "content"
        source.mkdir()
        for name, text in rows.items():
            (source / name).write_text(text, encoding="utf-8")
        output = Path(temp.name) / "preview.html"
        count = generate.build(source, output, include_drafts)
        return count, output.read_text(encoding="utf-8")

    def test_stable_equal_time_and_timezone_order(self):
        count, page = self.build({"z.md": entry("z-id"), "a.md": entry("a-id")})
        self.assertEqual(count, 2)
        self.assertLess(page.index('id="a-id"'), page.index('id="z-id"'))
        with self.assertRaisesRegex(ValueError, "timezone"):
            self.build({"bad.md": entry("bad", "2026-01-01T00:00:00")})

    def test_duplicate_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate id"):
            self.build({"one.md": entry("same"), "two.md": entry("same")})

    def test_draft_hidden_by_default(self):
        count, page = self.build({"public.md": entry("public"), "draft.md": entry("draft", draft="true")})
        self.assertEqual(count, 1)
        self.assertNotIn('id="draft"', page)

    def test_body_and_tag_are_html_escaped(self):
        _, page = self.build({"safe.md": entry("safe", tags="[<tag>]", body="<script>alert(1)</script>")})
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertIn("&lt;tag&gt;", page)

    def test_empty_tags_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-empty list"):
            self.build({"bad.md": entry("bad", tags="[]")})

    def test_missing_source_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "source directory"):
                generate.build(root / "missing", root / "output.html")
            self.assertFalse((root / "output.html").exists())


if __name__ == "__main__":
    unittest.main()
