#!/usr/bin/env python3
"""Validate language pairs and build an isolated, dependency-free preview."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALLOWED_STATUS = {"unreviewed", "reviewed", "stale"}
GROUP_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")
LOCALE_RE = re.compile(r"^[a-z]{2}(?:-[A-Z]{2})?$")
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
INLINE_RE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
FENCE_RE = re.compile(r"```[^\n]*\n(.*?)```", re.S)


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def body(text: str) -> str:
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError("missing YAML frontmatter")
    return parts[2].lstrip("\n")


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def contained_path(base: Path, value: str) -> Path:
    candidate = (base / value).resolve()
    if not candidate.is_relative_to(base.resolve()):
        raise ValueError("content path escapes manifest directory")
    return candidate


def validate(manifest_path: Path) -> tuple[list[str], list[dict]]:
    base = manifest_path.parent
    data = load_manifest(manifest_path)
    errors: list[str] = []
    report: list[dict] = []
    supported = data.get("supported_locales", [])
    if not supported or any(not isinstance(x, str) or not LOCALE_RE.fullmatch(x) for x in supported):
        errors.append("supported_locales contains an illegal language code")
    group_ids: set[str] = set()
    for group in data.get("groups", []):
        gid = group.get("translation_group_id", "")
        if not isinstance(gid, str) or not GROUP_RE.fullmatch(gid) or gid in group_ids:
            errors.append(f"duplicate or unsafe translation_group_id: {gid!r}")
            continue
        group_ids.add(gid)
        source_locale = group.get("source_locale")
        try:
            source = contained_path(base, group.get("source_path", ""))
        except ValueError as exc:
            errors.append(f"{gid}: {exc}")
            continue
        if source_locale not in supported:
            errors.append(f"{gid}: illegal source locale {source_locale!r}")
        if not isinstance(group.get("source_revision"), int) or group["source_revision"] < 1:
            errors.append(f"{gid}: source_revision must be a positive integer")
        if not source.is_file():
            errors.append(f"{gid}: missing source {source}")
            continue
        try:
            source_body = body(source.read_text(encoding="utf-8"))
        except ValueError as exc:
            errors.append(f"{gid}: source {exc}")
            continue
        current_hash = source_hash(source)
        seen = {source_locale}
        translations = group.get("translations", [])
        for item in translations:
            locale = item.get("locale")
            prefix = f"{gid}/{locale}"
            if locale not in supported or not isinstance(locale, str) or not LOCALE_RE.fullmatch(locale):
                errors.append(f"{prefix}: illegal language code")
            if locale in seen:
                errors.append(f"{prefix}: duplicate locale")
            seen.add(locale)
            status = item.get("review_status")
            if status not in ALLOWED_STATUS:
                errors.append(f"{prefix}: invalid review_status {status!r}")
            try:
                path = contained_path(base, item.get("path", ""))
            except ValueError as exc:
                errors.append(f"{prefix}: {exc}")
                continue
            if not path.is_file():
                errors.append(f"{prefix}: missing translation {path}")
                continue
            try:
                translated_body = body(path.read_text(encoding="utf-8"))
            except ValueError as exc:
                errors.append(f"{prefix}: translation {exc}")
                continue
            stale = (item.get("source_hash") != current_hash or
                     item.get("source_revision") != group.get("source_revision"))
            effective_status = "stale" if stale else status
            publishable = effective_status == "reviewed"
            source_code = FENCE_RE.findall(source_body)
            translated_code = FENCE_RE.findall(translated_body)
            if source_code != translated_code:
                errors.append(f"{prefix}: fenced code blocks differ from source")
            source_urls = [url for _, url in LINK_RE.findall(source_body)]
            translated_urls = [url for _, url in LINK_RE.findall(translated_body)]
            if source_urls != translated_urls:
                errors.append(f"{prefix}: link targets differ from source")
            source_without_fences = FENCE_RE.sub("", source_body)
            for token in INLINE_RE.findall(source_without_fences) + ["GitHub Pages"]:
                if token in source_body and token not in translated_body:
                    errors.append(f"{prefix}: protected term missing: {token}")
            if source_body.count("\n> ") != translated_body.count("\n> "):
                errors.append(f"{prefix}: block quote count differs from source")
            report.append({"translation_group_id": gid, "locale": locale,
                           "declared_status": status, "effective_status": effective_status,
                           "publishable": publishable, "source_hash": current_hash})
        missing = set(supported) - seen
        if missing:
            errors.append(f"{gid}: missing translations: {', '.join(sorted(missing))}")
    return errors, report


def markdown(text: str) -> str:
    """Render the deliberately small demo Markdown subset with escaping."""
    out, paragraph, in_code, code = [], [], False, []
    def flush() -> None:
        if paragraph:
            raw = " ".join(paragraph)
            pieces, cursor = [], 0
            for match in LINK_RE.finditer(raw):
                pieces.append(html.escape(raw[cursor:match.start()]))
                pieces.append(f'<a href="{html.escape(match.group(2), quote=True)}">{html.escape(match.group(1))}</a>')
                cursor = match.end()
            pieces.append(html.escape(raw[cursor:]))
            safe = "".join(pieces)
            safe = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", safe)
            out.append(f"<p>{safe}</p>")
            paragraph.clear()
    for line in text.splitlines():
        if line.startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code.clear()
            else:
                flush()
            in_code = not in_code
        elif in_code:
            code.append(line)
        elif not line.strip():
            flush()
        elif line.startswith("# "):
            flush(); out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            flush(); out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("> "):
            flush(); out.append(f"<blockquote>{html.escape(line[2:])}</blockquote>")
        elif re.match(r"\d+\. ", line):
            flush(); out.append(f"<div class=check>{html.escape(line)}</div>")
        else:
            paragraph.append(line)
    flush()
    return "\n".join(out)


STYLE = """body{font:16px/1.65 system-ui;max-width:880px;margin:auto;padding:2rem;color:#243040}nav,.notice{padding:1rem;background:#eef4ff;border-radius:.5rem}nav a{margin-right:1rem}pre{overflow:auto;background:#17202a;color:#f7f7f7;padding:1rem}code{background:#edf0f3;padding:.15rem}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}.card{border:1px solid #ccd5df;padding:1rem}.bad{color:#a22121;font-weight:bold}.good{color:#176b35;font-weight:bold}@media(max-width:700px){.grid{grid-template-columns:1fr}}"""


def page(title: str, nav: str, contents: str, locale: str = "zh-CN") -> str:
    return f'<!doctype html><html lang="{locale}"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{html.escape(title)}</title><style>{STYLE}</style><body><nav>{nav}</nav>{contents}</body></html>'


def build(manifest_path: Path, output: Path) -> None:
    errors, report = validate(manifest_path)
    if errors:
        raise SystemExit("validation failed:\n- " + "\n- ".join(errors))
    data, base = load_manifest(manifest_path), manifest_path.parent
    output = output.resolve()
    base = base.resolve()
    if output == base or base.is_relative_to(output) or output.is_relative_to(base / "content"):
        raise ValueError("output must not overwrite the manifest or content directory")
    output.mkdir(parents=True, exist_ok=True)
    def write_page(relative: Path, contents: str) -> None:
        target = output / relative
        if target.is_symlink() or any(parent.is_symlink() for parent in target.parents if parent != output and parent.is_relative_to(output)):
            raise ValueError("output path must not contain symlinks")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8")
    cards = []
    for group in data["groups"]:
        gid = group["translation_group_id"]
        entries = [{"locale": group["source_locale"], "path": group["source_path"]}] + group["translations"]
        links = "".join(f'<a href="../{x["locale"]}/">{html.escape(x["locale"])}</a>' for x in entries)
        for item in entries:
            locale = item["locale"]
            status = "source" if locale == group["source_locale"] else next(x["effective_status"] for x in report if x["locale"] == locale and x["translation_group_id"] == gid)
            can_publish = status in {"source", "reviewed"}
            notice = f'<p class="notice"><b>synthetic demo</b> · effective status: <span class="{"good" if can_publish else "bad"}">{status}</span> · publishable: {str(can_publish).lower()}</p>'
            rendered = markdown(body((base/item["path"]).read_text(encoding="utf-8")))
            write_page(Path(gid)/locale/"index.html", page(f"{gid} · {locale}", links + '<a href="../../review.html">差异审阅</a>', notice+rendered, locale))
        index_links = "".join(f'<a href="{gid}/{x["locale"]}/index.html">{html.escape(x["locale"])}</a>' for x in entries)
        cards.append(f'<div class="card"><h2>{html.escape(gid)}</h2>{index_links}</div>')
    review_cards = []
    for row in report:
        css = "good" if row["publishable"] else "bad"
        review_cards.append(f'<div class="card"><h2>{html.escape(row["locale"])}</h2><p>declared: {row["declared_status"]}</p><p>effective: <span class="{css}">{row["effective_status"]}</span></p><p>publishable: {str(row["publishable"]).lower()}</p><small>source hash: {row["source_hash"]}</small></div>')
    write_page(Path("index.html"), page("A06 博客多语言发布", '<a href="review.html">差异审阅</a>', '<h1>A06 博客多语言发布</h1><p class="notice"><b>synthetic data / 合成数据。</b> 仅供本地隔离预览，不会发布。</p><div class="grid">'+''.join(cards)+'</div>'))
    write_page(Path("review.html"), page("A06 差异审阅", '<a href="index.html">预览首页</a>', '<h1>来源同步与发布资格审阅</h1><p>代码块、链接目标、行内代码、专名和引用数量已逐项校验。译文语义仍须人工审阅。</p><div class="grid">'+''.join(review_cards)+'</div>'))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate", "build"])
    parser.add_argument("--manifest", type=Path, default=ROOT/"pairs.json")
    parser.add_argument("--output", type=Path, default=ROOT/"site")
    args = parser.parse_args()
    errors, report = validate(args.manifest)
    if errors:
        print("INVALID\n" + "\n".join(f"- {x}" for x in errors), file=sys.stderr)
        return 1
    if args.command == "build":
        build(args.manifest, args.output)
    print(json.dumps({"valid": True, "translations": report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
