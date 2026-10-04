#!/usr/bin/env python3
"""Verify the generated site's small, migration-safe compatibility contract."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit


REQUIRED_PATHS = (
    "index.html",
    "404.html",
    "archives/index.html",
    "category/index.html",
    "tags/index.html",
    "travel/index.html",
    "feed.xml",
    "feed.atom",
    "images/favicon.ico",
)


class PageSignals(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.images: list[str] = []
        self.scripts: list[str] = []
        self.article_links: list[str] = []
        self.article_list_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "ul" and (self.article_list_depth or "travel-posts-list" in (values.get("class") or "").split()):
            self.article_list_depth += 1
        if tag == "a" and values.get("href") and self.article_list_depth:
            self.article_links.append(values["href"] or "")
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        elif tag == "img" and values.get("src"):
            self.images.append(values["src"] or "")
        elif tag == "script" and values.get("src"):
            self.scripts.append(values["src"] or "")


    def handle_endtag(self, tag: str) -> None:
        if tag == "ul" and self.article_list_depth:
            self.article_list_depth -= 1


def parse_page(path: Path) -> PageSignals:
    parser = PageSignals()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", nargs="?", default="_site", type=Path)
    args = parser.parse_args()
    site = args.site.resolve()
    errors: list[str] = []

    for relative in REQUIRED_PATHS:
        if not (site / relative).is_file():
            errors.append(f"缺少兼容路径: /{relative}")

    feeds: dict[str, ET.Element] = {}
    for name in ("feed.xml", "feed.atom"):
        path = site / name
        if path.is_file():
            try:
                feeds[name] = ET.parse(path).getroot()
            except ET.ParseError as error:
                errors.append(f"/{name} 不是有效 XML: {error}")

    if "feed.xml" in feeds:
        root = feeds["feed.xml"]
        self_links = [
            node.attrib.get("href")
            for node in root.findall("./channel/{http://www.w3.org/2005/Atom}link")
            if node.attrib.get("rel") == "self"
        ]
        expected = "https://lmmsoft.github.io/feed.xml"
        if self_links != [expected]:
            errors.append(f"RSS self link 应为 {expected}，实际为 {self_links}")

    travel = site / "travel/index.html"
    if travel.is_file():
        signals = parse_page(travel)
        if not signals.article_links:
            errors.append("旅行页没有生成任何相关文章链接")
        for link in signals.article_links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path.startswith("/") or parsed.path == "/":
                errors.append(f"旅行页相关文章不是站内链接: {link}")
                continue
            target = (site / unquote(parsed.path).lstrip("/")).resolve()
            if not target.is_relative_to(site):
                errors.append(f"旅行页相关文章越出站点目录: {link}")
                continue
            if not target.is_file() and not (target / "index.html").is_file():
                errors.append(f"旅行页相关文章目标不存在: {link}")

    post_pages = sorted(site.glob("**/*.html"))
    has_disqus = False
    for path in post_pages:
        if "disqus.com/embed.js" in path.read_text(encoding="utf-8", errors="ignore"):
            has_disqus = True
            break
    if not has_disqus:
        errors.append("生成页面中未发现 Disqus 评论嵌入")

    if errors:
        print("兼容性验证失败:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"兼容性验证通过: {len(REQUIRED_PATHS)} 个固定入口、2 个 feed、旅行文章链接和评论嵌入")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
