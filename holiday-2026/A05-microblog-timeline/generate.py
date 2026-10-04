#!/usr/bin/env python3
"""Build the isolated A05 static microblog preview using only Python stdlib."""
from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime
from pathlib import Path

REQUIRED = ("id", "date", "tags", "body", "draft")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def scalar(value: str):
    value = value.strip()
    if value in ("true", "false"):
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [part.strip().strip("\"'") for part in inner.split(",")]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def load(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{path}: missing YAML frontmatter")
    raw, trailing = text[4:].split("\n---\n", 1)
    data = {}
    for number, line in enumerate(raw.splitlines(), 2):
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}:{number}: unsupported frontmatter")
        key, value = line.split(":", 1)
        data[key.strip()] = scalar(value)
    missing = [key for key in REQUIRED if key not in data]
    if missing:
        raise ValueError(f"{path}: missing fields: {', '.join(missing)}")
    if trailing.strip():
        raise ValueError(f"{path}: content must be stored in frontmatter body")
    if not isinstance(data["id"], str) or not ID_RE.fullmatch(data["id"]):
        raise ValueError(f"{path}: invalid id")
    if not isinstance(data["tags"], list) or not data["tags"] or not all(isinstance(x, str) and x for x in data["tags"]):
        raise ValueError(f"{path}: tags must be a non-empty list")
    if not isinstance(data["body"], str) or not data["body"].strip():
        raise ValueError(f"{path}: body must be non-empty plain text")
    if not isinstance(data["draft"], bool):
        raise ValueError(f"{path}: draft must be true or false")
    try:
        stamp = datetime.fromisoformat(str(data["date"]))
    except ValueError as exc:
        raise ValueError(f"{path}: date must be ISO 8601") from exc
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError(f"{path}: date must include a timezone")
    data["_stamp"] = stamp.timestamp()
    return data


def render(items):
    tags = sorted({tag for item in items for tag in item["tags"]}, key=str.casefold)
    chips = ['<button class="tag active" data-tag="" type="button">全部</button>']
    chips += [f'<button class="tag" data-tag="{html.escape(t, quote=True)}" type="button">#{html.escape(t)}</button>' for t in tags]
    cards = []
    for item in items:
        ident = html.escape(item["id"], quote=True)
        tagdata = html.escape("\x1f".join(item["tags"]), quote=True)
        labels = " ".join(f'<button class="inline-tag" data-pick="{html.escape(t, quote=True)}" type="button">#{html.escape(t)}</button>' for t in item["tags"])
        cards.append(
            f'<article class="post" id="{ident}" data-tags="{tagdata}"><header>'
            f'<a class="permalink" href="#{ident}" aria-label="永久链接">#</a>'
            f'<time datetime="{html.escape(str(item["date"]), quote=True)}">{html.escape(str(item["date"]))}</time>'
            f'</header><p>{html.escape(str(item["body"]))}</p><footer>{labels}</footer></article>'
        )
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A05 短内容／微博客时间流 — DEMO</title><style>
:root{{--bg:#f5f4ef;--card:#fff;--ink:#242424;--muted:#676767;--accent:#8b3d28}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,sans-serif}}main{{width:min(42rem,calc(100% - 2rem));margin:2rem auto 5rem}}h1{{font-size:clamp(1.6rem,5vw,2.5rem);line-height:1.2;margin-bottom:.25rem}}.notice{{color:var(--muted)}}.filters{{display:flex;gap:.5rem;overflow-x:auto;padding:.75rem 0 1.25rem}}button{{font:inherit}}.tag,.inline-tag{{border:1px solid #c9c5bb;border-radius:99px;background:#fff;padding:.35rem .75rem;cursor:pointer;white-space:nowrap}}.tag.active{{background:var(--accent);color:#fff;border-color:var(--accent)}}.post{{background:var(--card);padding:1.1rem 1.25rem;margin:0 0 1rem;border-radius:.6rem;box-shadow:0 1px 4px #0001;overflow-wrap:anywhere}}.post header{{display:flex;gap:.6rem;color:var(--muted);font-size:.85rem}}.permalink{{color:var(--accent);font-weight:bold;text-decoration:none}}.post p{{white-space:pre-wrap}}.inline-tag{{padding:0;border:0;background:none;color:var(--accent);margin-right:.7rem}}#empty{{padding:2rem;text-align:center;color:var(--muted)}}[hidden]{{display:none!important}}@media(max-width:420px){{main{{width:calc(100% - 1rem);margin-top:1rem}}.post{{padding:1rem}}}}
</style></head><body><main><h1>A05 短内容／微博客时间流</h1><p class="notice"><strong>DEMO：</strong>以下均为合成数据，不代表真实人物、事件或发布结果。</p><nav class="filters" aria-label="按标签筛选">{''.join(chips)}</nav><section id="timeline">{''.join(cards)}</section><p id="empty" hidden>该标签暂无短内容。请选择其他标签。</p></main><script>
const buttons=[...document.querySelectorAll('[data-tag]')],posts=[...document.querySelectorAll('.post')],empty=document.querySelector('#empty');function select(tag){{let shown=0;posts.forEach(p=>{{const match=!tag||p.dataset.tags.split('\\x1f').includes(tag);p.hidden=!match;if(match)shown++}});empty.hidden=shown!==0;buttons.forEach(b=>b.classList.toggle('active',b.dataset.tag===tag));history.replaceState(null,'',tag?'#tag='+encodeURIComponent(tag):location.pathname)}}buttons.forEach(b=>b.addEventListener('click',()=>select(b.dataset.tag)));document.querySelectorAll('[data-pick]').forEach(b=>b.addEventListener('click',()=>select(b.dataset.pick)));if(location.hash.startsWith('#tag='))select(decodeURIComponent(location.hash.slice(5)));
</script></body></html>'''


def build(source: Path, output: Path, include_drafts=False):
    if not source.is_dir():
        raise ValueError(f"source directory does not exist: {source}")
    items = [load(path) for path in sorted(source.glob("*.md"))]
    seen = set()
    for item in items:
        if item["id"] in seen:
            raise ValueError(f'duplicate id: {item["id"]}')
        seen.add(item["id"])
    items = [item for item in items if include_drafts or not item["draft"]]
    items.sort(key=lambda item: (-item["_stamp"], item["id"]))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(items), encoding="utf-8")
    return len(items)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path(__file__).with_name("content"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("preview.html"))
    parser.add_argument("--include-drafts", action="store_true")
    args = parser.parse_args()
    try:
        count = build(args.source, args.output, args.include_drafts)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"generated {count} entries: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
