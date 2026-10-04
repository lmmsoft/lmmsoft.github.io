import copy
import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import language_pairs as lp


class LanguagePairTests(unittest.TestCase):
    def setUp(self):
        self.original = lp.load_manifest(lp.ROOT / "pairs.json")

    def fixture(self, mutate=None):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        for source in (lp.ROOT / "content").glob("*.md"):
            (root / "content").mkdir(exist_ok=True)
            (root / "content" / source.name).write_bytes(source.read_bytes())
        data = copy.deepcopy(self.original)
        if mutate:
            mutate(data, root)
        manifest = root / "pairs.json"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        return temp, manifest

    def assert_invalid(self, mutate, phrase):
        temp, manifest = self.fixture(mutate)
        try:
            errors, _ = lp.validate(manifest)
            self.assertTrue(any(phrase in x for x in errors), errors)
        finally:
            temp.cleanup()

    def test_valid_and_publishable(self):
        errors, report = lp.validate(lp.ROOT / "pairs.json")
        self.assertEqual([], errors)
        self.assertTrue(all(x["publishable"] for x in report))

    def test_missing_translation(self):
        self.assert_invalid(lambda d, _: d["groups"][0]["translations"].pop(), "missing translations")

    def test_duplicate_locale(self):
        def mutate(data, _):
            data["groups"][0]["translations"][1]["locale"] = "en"
        self.assert_invalid(mutate, "duplicate locale")

    def test_illegal_language_code(self):
        def mutate(data, _):
            data["supported_locales"].append("english")
        self.assert_invalid(mutate, "illegal language code")

    def test_source_change_marks_translation_stale(self):
        temp, manifest = self.fixture()
        try:
            source = Path(temp.name) / self.original["groups"][0]["source_path"]
            source.write_text(source.read_text() + "\n安全更新。\n", encoding="utf-8")
            errors, report = lp.validate(manifest)
            self.assertEqual([], errors)
            self.assertTrue(all(x["effective_status"] == "stale" for x in report))
            self.assertFalse(any(x["publishable"] for x in report))
        finally:
            temp.cleanup()

    def test_unreviewed_is_not_publishable(self):
        def mutate(data, _):
            data["groups"][0]["translations"][0]["review_status"] = "unreviewed"
        temp, manifest = self.fixture(mutate)
        try:
            errors, report = lp.validate(manifest)
            self.assertEqual([], errors)
            self.assertFalse(report[0]["publishable"])
        finally:
            temp.cleanup()

    def test_changed_code_block_fails(self):
        def mutate(data, root):
            path = root / data["groups"][0]["translations"][0]["path"]
            path.write_text(path.read_text().replace("http.server 8000", "http.server 9000"))
        self.assert_invalid(mutate, "code blocks differ")

    def test_changed_link_fails(self):
        def mutate(data, root):
            path = root / data["groups"][0]["translations"][0]["path"]
            path.write_text(path.read_text().replace("a=1&b=2", "a=1&b=3"))
        self.assert_invalid(mutate, "link targets differ")

    def test_unsafe_group_rejected(self):
        self.assert_invalid(lambda d, _: d["groups"][0].update(translation_group_id="../../outside"), "unsafe translation_group_id")

    def test_source_outside_manifest_rejected(self):
        self.assert_invalid(lambda d, _: d["groups"][0].update(source_path="../outside.md"), "escapes manifest")

    def test_build_preserves_files_and_links_resolve(self):
        import re
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "site"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("keep")
            lp.build(lp.ROOT / "pairs.json", output)
            self.assertEqual("keep", sentinel.read_text())
            for href in re.findall(r'href="([^"]+)"', (output / "index.html").read_text()):
                self.assertTrue((output / href).is_file(), href)
            self.assertIn('lang="en"', (output / "safe-static-preview-2026/en/index.html").read_text())

    def test_build_rejects_content_output(self):
        temp, manifest = self.fixture()
        try:
            with self.assertRaisesRegex(ValueError, "must not overwrite"):
                lp.build(manifest, manifest.parent)
        finally:
            temp.cleanup()

    def test_build_rejects_output_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "site"
            output.mkdir()
            outside = Path(temp) / "outside"
            outside.mkdir()
            (output / "safe-static-preview-2026").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlinks"):
                lp.build(lp.ROOT / "pairs.json", output)
            self.assertEqual([], list(outside.iterdir()))

    def test_link_attribute_is_escaped(self):
        rendered = lp.markdown("[x](https://example.com/?a=1&b=2)")
        self.assertIn('href="https://example.com/?a=1&amp;b=2"', rendered)
        self.assertNotIn('href="https://example.com/?a=1&b=2"', rendered)


if __name__ == "__main__":
    unittest.main()
