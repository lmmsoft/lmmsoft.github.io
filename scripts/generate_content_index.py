#!/usr/bin/env python3
"""
生成配置（固定参数，不提供 CLI 选项）:
- 输入目录: _posts/, _drafts/（兼容 _post/, _draft/）
- 支持扩展名: .md/.markdown/.html
- 输出文件: CONTENT_INDEX.md（仓库根目录）
- 表头: 日期 | 标题 | 是否发布 | 类型(post/draft) | 有图片 | 格式 | 相对路径 | 备注
- 排序: 日期降序；按年份分组，年份降序，并展示每年 发布/待发布/草稿 数量
"""
from __future__ import annotations

import datetime as dt
import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple, Union
from urllib.parse import quote


ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
OUTPUT_FILE = os.path.join(ROOT_DIR, "CONTENT_INDEX.md")
SEARCH_DIRS = ["_posts", "_drafts", "_post", "_draft"]  # 后两个用于兼容容错
_YAML_FALLBACK_WARNED = False
SITE_BASE = "https://lmmsoft.github.io"
ALLOWED_EXTS = (".md", ".markdown", ".html")


IMAGE_PATTERNS = [
    re.compile(r"!\[[^\]]*?\]\((?P<src>[^)]+)\)", re.DOTALL),
    re.compile(r'<img[^>]*?src=["\'](?P<src>[^"\']+)["\'][^>]*?>', re.IGNORECASE),
]


@dataclass
class Record:
    path: str
    rel_path: str
    date: dt.datetime
    year: int
    title: str
    published: bool
    content_type: str  # post/draft
    image_label: str  # ➖/🖼️/🌐/🔀/❓
    remark: str = ""
    permalink_url: Optional[str] = None
    fmt: str = ""


def list_markdown_files() -> List[str]:
    candidates: List[str] = []
    for rel_dir in SEARCH_DIRS:
        abs_dir = os.path.join(ROOT_DIR, rel_dir)
        for root, _, files in os.walk(abs_dir):
            for name in files:
                lower = name.lower()
                if lower.endswith(ALLOWED_EXTS):
                    candidates.append(os.path.join(root, name))
    return candidates


def split_front_matter(content: str) -> Tuple[Dict, str]:
    """返回 front matter 字典与正文（若未找到，front matter 为空）。"""
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}, content
    yaml_block = match.group(1)
    body = content[match.end() :]
    data = parse_front_matter_yaml(yaml_block)
    return data if isinstance(data, dict) else {}, body


def parse_front_matter_yaml(yaml_block: str) -> Dict:
    """优先使用 PyYAML；缺失或解析失败则降级为简易行级解析。"""
    try:
        import yaml  # type: ignore

        return yaml.safe_load(yaml_block) or {}
    except ModuleNotFoundError:
        return parse_yaml_fallback(yaml_block, reason="PyYAML 未安装")
    except Exception as exc:  # pragma: no cover - 容错
        print(f"[WARN] front matter YAML 解析失败: {exc}", file=sys.stderr)
        return parse_yaml_fallback(yaml_block, reason="YAML 解析失败")


def parse_yaml_fallback(text: str, *, reason: str) -> Dict[str, Union[str, bool]]:
    """简易解析：仅处理 key: value/true/false；复杂结构需依赖 PyYAML。"""
    meta: Dict[str, Union[str, bool]] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = coerce_simple_value(value.strip())
    global _YAML_FALLBACK_WARNED
    if meta and not _YAML_FALLBACK_WARNED:
        print(
            f"[INFO] front matter 使用简易解析（原因: {reason}；复杂结构可能无法还原完整 front matter）",
            file=sys.stderr,
        )
        _YAML_FALLBACK_WARNED = True
    return meta


def coerce_simple_value(text: str) -> Union[str, bool]:
    stripped = text.strip()
    if (stripped.startswith('"') and stripped.endswith('"')) or (
        stripped.startswith("'") and stripped.endswith("'")
    ):
        stripped = stripped[1:-1].strip()
    lowered = stripped.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    return stripped


def parse_date(value: object) -> Optional[dt.datetime]:
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime.combine(value, dt.time())

    text = str(value).strip()
    # 尝试 ISO 解析
    try:
        return dt.datetime.fromisoformat(text)
    except Exception:
        pass

    formats = [
        "%Y-%m-%d %H:%M:%S %z",
        "%Y-%m-%d %H:%M %z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return dt.datetime.strptime(text, fmt)
        except Exception:
            continue
    return None


def normalize_datetime(value: dt.datetime) -> dt.datetime:
    """将有时区的 datetime 转换为 UTC 再去掉 tzinfo，便于统一排序。"""
    if value.tzinfo:
        return value.astimezone(dt.timezone.utc).replace(tzinfo=None)
    return value


def derive_date(meta: Dict, filename: str) -> dt.datetime:
    fm_date = parse_date(meta.get("date"))
    if fm_date:
        return normalize_datetime(fm_date)

    prefix_match = re.match(r"(\d{4}-\d{2}-\d{2})", os.path.basename(filename))
    if prefix_match:
        parsed = parse_date(prefix_match.group(1))
        if parsed:
            return normalize_datetime(parsed)

    print(f"[WARN] 未解析到有效日期，使用默认 1970-01-01: {filename}", file=sys.stderr)
    return dt.datetime(1970, 1, 1)


def extract_title(meta: Dict, filename: str) -> str:
    if meta.get("title"):
        return str(meta["title"]).strip()
    stem = os.path.splitext(os.path.basename(filename))[0]
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
    return stem or filename


def detect_image_label(body: str) -> Tuple[str, List[str]]:
    sources: List[str] = []
    for pattern in IMAGE_PATTERNS:
        for match in pattern.finditer(body):
            src = match.group("src").strip()
            sources.append(src)
    if not sources:
        return "➖", []

    categories = set()
    for src in sources:
        lowered = src.lower()
        if lowered.startswith("http://") or lowered.startswith("https://"):
            categories.add("external")
        elif "images/" in lowered or "attachments/" in lowered:
            categories.add("local")
        else:
            categories.add("other")

    if categories == {"local"}:
        label = "🖼️"
    elif categories == {"external"}:
        label = "🌐"
    elif categories == {"other"}:
        label = "❓"
    else:
        label = "🔀"
    return label, sorted(categories)


def detect_type(path: str) -> str:
    normalized = path.replace("\\", "/").rstrip("/")
    if "/_posts/" in normalized or normalized.endswith("/_posts"):
        return "post"
    return "draft"


def resolve_published(meta: Dict, path: str) -> bool:
    """对 _posts 缺省视为发布；显式 published: false 才视为未发布。草稿始终未发布。"""
    content_type = detect_type(path)
    if content_type == "draft":
        return False
    published_meta = meta.get("published")
    if published_meta is False:
        return False
    return True


def resolve_permalink(meta: Dict) -> Optional[str]:
    """构造已发布 post 的站点链接，仅在 front matter 提供 permalink 时使用。"""
    raw = meta.get("permalink")
    if not raw:
        return None
    slug = str(raw).strip()
    slug = "/" + slug.lstrip("/")
    encoded = quote(slug, safe="/%._-~")
    return SITE_BASE.rstrip("/") + encoded


def build_record(path: str) -> Record:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    meta, body = split_front_matter(content)
    date_value = derive_date(meta, path)
    title = extract_title(meta, path)
    published = resolve_published(meta, path)
    content_type = detect_type(path.replace("\\", "/"))
    image_label, _ = detect_image_label(body)

    has_permalink = isinstance(meta, dict) and "permalink" in meta
    permalink_url: Optional[str] = None
    if content_type == "post" and published and has_permalink:
        permalink_url = resolve_permalink(meta)

    fmt = os.path.splitext(path)[1].lstrip(".").lower()

    remark_parts: List[str] = []
    if image_label in {"🌐", "🔀"}:
        remark_parts.append("含外链图片")
    if image_label == "❓":
        remark_parts.append("图片路径需确认")
    if date_value.year == 1970:
        remark_parts.append("日期需补充")
    if content_type == "post" and published and not has_permalink:
        remark_parts.append("缺permalink")

    rel_path = os.path.relpath(path, ROOT_DIR)

    return Record(
        path=path,
        rel_path=rel_path,
        date=date_value,
        year=date_value.year,
        title=title,
        published=published,
        content_type=content_type,
        image_label=image_label,
        remark="；".join(remark_parts),
        permalink_url=permalink_url,
        fmt=fmt,
    )


def group_by_year(records: Iterable[Record]) -> Dict[int, List[Record]]:
    grouped: Dict[int, List[Record]] = {}
    for rec in records:
        grouped.setdefault(rec.year, []).append(rec)
    for recs in grouped.values():
        recs.sort(key=lambda r: (r.date, r.title), reverse=True)
    return dict(sorted(grouped.items(), key=lambda item: item[0], reverse=True))


def render_markdown(grouped: Dict[int, List[Record]]) -> str:
    lines: List[str] = []
    lines.append("# 内容目录")
    lines.append(f"- Generated at: {dt.datetime.now().isoformat(timespec='seconds')}")
    lines.append("- 功能：快速浏览文章/草稿状态（按年分组，日期降序）")
    lines.append("- 生成：python scripts/generate_content_index.py")
    lines.append("")

    header = "| 日期 | 标题 | 是否发布 | 类型 | 有图片 | 格式 | 相对路径 | 备注 |"
    separator = "| --- | --- | --- | --- | --- | --- | --- | --- |"

    for year, recs in grouped.items():
        publish_count = sum(1 for r in recs if r.content_type == "post" and r.published)
        pending_count = sum(1 for r in recs if r.content_type == "post" and not r.published)
        draft_count = sum(1 for r in recs if r.content_type == "draft")
        lines.append(f"## {year}（发布: {publish_count}, 待发布: {pending_count}, 草稿: {draft_count}）")
        lines.append(header)
        lines.append(separator)
        for rec in recs:
            date_str = rec.date.strftime("%Y-%m-%d")
            safe_title = rec.title.replace("|", "\\|")
            if rec.permalink_url:
                title_md = f"[{safe_title}]({rec.permalink_url})"
            else:
                title_md = safe_title
            path_md = f"[{rec.rel_path}]({rec.rel_path})"
            published = "✅" if rec.published else "❌"
            lines.append(
                f"| {date_str} | {title_md} | {published} | {rec.content_type} | {rec.image_label} | {rec.fmt} | {path_md} | {rec.remark} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_output(content: str) -> None:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[INFO] 已生成 {OUTPUT_FILE}")


def main() -> None:
    files = list_markdown_files()
    if not files:
        print("[WARN] 未找到 Markdown 文件", file=sys.stderr)
        return

    records = [build_record(path) for path in files]
    grouped = group_by_year(records)
    markdown = render_markdown(grouped)
    write_output(markdown)


if __name__ == "__main__":
    main()
