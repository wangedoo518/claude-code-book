#!/usr/bin/env python3
from __future__ import annotations

import json
import mimetypes
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

import yaml
from bs4 import BeautifulSoup
from ebooklib import epub


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "mkdocs.yml"
SITE_DIR = ROOT / "site"
BUILD_DIR = ROOT / "build" / "downloads"
DOWNLOADS_DIR = ROOT / "docs" / "assets" / "downloads"
DOCS_DIR = ROOT / "docs"
MERMAID_VERSION = "11.12.0"
MERMAID_CONFIG = {
    "theme": "neutral",
    "securityLevel": "loose",
    "flowchart": {"htmlLabels": True, "useMaxWidth": True},
    "sequence": {"useMaxWidth": True},
}
MERMAID_FENCE_RE = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)


def source_md_path(md_path: str) -> Path:
    return DOCS_DIR / md_path


def quote_mermaid_label(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith('"') and stripped.endswith('"'):
        return stripped
    return f'"{stripped.replace("\"", "\\\"")}"'


def normalize_quadrant_block(block: str) -> str:
    lines = block.splitlines()
    if not lines or lines[0].strip() != "quadrantChart":
        return block

    normalized: list[str] = [lines[0]]
    for line in lines[1:]:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]

        if stripped.startswith("x-axis "):
            left, right = stripped[len("x-axis ") :].split("-->", 1)
            normalized.append(f"{indent}x-axis {quote_mermaid_label(left)} --> {quote_mermaid_label(right)}")
            continue

        if stripped.startswith("y-axis "):
            left, right = stripped[len("y-axis ") :].split("-->", 1)
            normalized.append(f"{indent}y-axis {quote_mermaid_label(left)} --> {quote_mermaid_label(right)}")
            continue

        if stripped.startswith("quadrant-"):
            key, value = stripped.split(None, 1)
            normalized.append(f"{indent}{key} {quote_mermaid_label(value)}")
            continue

        normalized.append(line)

    return "\n".join(normalized)


def normalize_mermaid_source(source_text: str) -> str:
    def replace_block(match: re.Match[str]) -> str:
        block = match.group(1)
        return f"```mermaid\n{normalize_quadrant_block(block)}\n```"

    return MERMAID_FENCE_RE.sub(replace_block, source_text)


def load_config() -> dict:
    return yaml.load(CONFIG_PATH.read_text(encoding="utf-8"), Loader=yaml.UnsafeLoader)


def iter_nav_entries(items: Iterable) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for item in items:
        if isinstance(item, dict):
            for label, value in item.items():
                if isinstance(value, str):
                    entries.append((label, value))
                elif isinstance(value, list):
                    entries.extend(iter_nav_entries(value))
        elif isinstance(item, str):
            entries.append((Path(item).stem, item))
    return entries


def md_to_html_path(md_path: str) -> Path:
    path = Path(md_path)
    if path.name == "index.md":
        if path.parent == Path("."):
            return SITE_DIR / "index.html"
        return SITE_DIR / path.parent / "index.html"
    return SITE_DIR / path.with_suffix("") / "index.html"


def clean_heading_text(tag) -> str:
    clone = BeautifulSoup(str(tag), "lxml")
    for el in clone.select(".headerlink,.md-content__button"):
        el.decompose()
    return clone.get_text(" ", strip=True).replace(" ¶", "").replace("¶", "")


def replace_mermaid_blocks(soup: BeautifulSoup, svg_paths: list[Path]) -> None:
    mermaid_blocks = soup.select("pre.mermaid")
    if not mermaid_blocks:
        return

    if len(mermaid_blocks) != len(svg_paths):
        raise RuntimeError(
            f"Mermaid count mismatch: HTML has {len(mermaid_blocks)} blocks, "
            f"but renderer produced {len(svg_paths)} SVGs."
        )

    for idx, (block, svg_path) in enumerate(zip(mermaid_blocks, svg_paths, strict=True), start=1):
        svg_text = svg_path.read_text(encoding="utf-8")
        width_match = re.search(r"max-width:\s*([0-9.]+)px", svg_text)
        viewbox_match = re.search(r'viewBox="[^"]*?\s([0-9.]+)\s([0-9.]+)"', svg_text)
        width_hint = None
        if width_match:
            width_hint = int(float(width_match.group(1)))
        elif viewbox_match:
            width_hint = int(float(viewbox_match.group(1)))

        figure = soup.new_tag("figure", attrs={"class": "mermaid-export"})
        img_attrs = {
            "class": "mermaid-export__image",
            "src": str(svg_path),
            "alt": f"Mermaid diagram {idx}",
            "loading": "lazy",
        }
        if width_hint:
            img_attrs["width"] = str(width_hint)
        img = soup.new_tag("img", attrs=img_attrs)
        figure.append(img)
        block.replace_with(figure)


def normalize_fragment(page: dict, *, for_epub: bool = False):
    soup = BeautifulSoup(page["article_html"], "lxml")

    for el in soup.select(".headerlink,.md-content__button,.mobile-share-strip"):
        el.decompose()

    replace_mermaid_blocks(soup, page.get("mermaid_svgs", []))

    html_path = page["html_path"]
    for tag in soup.find_all(src=True):
        src = tag.get("src", "")
        if not src or src.startswith(("http://", "https://", "data:", "file://")):
            continue
        resolved = (html_path.parent / src).resolve()
        if for_epub:
            tag["src"] = resolved.as_posix()
        else:
            tag["src"] = resolved.as_uri()

    for tag in soup.find_all(href=True):
        href = tag.get("href", "")
        if not href or href.startswith(("#", "http://", "https://", "mailto:", "javascript:")):
            continue
        resolved = (html_path.parent / href).resolve()
        if for_epub:
            tag["href"] = "#"
        else:
            tag["href"] = resolved.as_uri()

    return soup


def extract_pages(nav_entries: list[tuple[str, str]]):
    pages = []
    for nav_label, md_path in nav_entries:
        html_path = md_to_html_path(md_path)
        source_path = source_md_path(md_path)
        if not html_path.exists():
            raise FileNotFoundError(f"Missing built page: {html_path}")
        if not source_path.exists():
            raise FileNotFoundError(f"Missing source page: {source_path}")
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "lxml")
        article = soup.select_one("article.md-content__inner")
        if article is None:
            raise RuntimeError(f"Missing article content in {html_path}")
        title_tag = article.find(["h1", "h2"])
        title = clean_heading_text(title_tag) if title_tag else nav_label
        pages.append(
            {
                "nav_label": nav_label,
                "md_path": md_path,
                "source_path": source_path,
                "html_path": html_path,
                "title": title,
                "article_html": article.decode_contents(),
            }
        )
    return pages


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "google-chrome",
        "chromium-browser",
        "chromium",
        "chrome",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return str(path)
        result = subprocess.run(
            ["bash", "-lc", f"command -v {candidate} >/dev/null 2>&1 && command -v {candidate}"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    raise RuntimeError("Chrome/Chromium not found. Please install Google Chrome or Chromium.")


def find_npx() -> str:
    result = subprocess.run(
        ["bash", "-lc", "command -v npx >/dev/null 2>&1 && command -v npx"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    raise RuntimeError("npx not found. Please install Node.js to render Mermaid diagrams for PDF/EPUB exports.")


def render_mermaid_svgs(pages: list[dict], chrome: str) -> None:
    npx = find_npx()
    config_path = BUILD_DIR / "mermaid-config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(MERMAID_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")

    for page in pages:
        source_text = page["source_path"].read_text(encoding="utf-8")
        normalized_source = normalize_mermaid_source(source_text)
        mermaid_count = len(re.findall(r"^```mermaid\s*$", source_text, re.MULTILINE))
        if mermaid_count == 0:
            page["mermaid_svgs"] = []
            continue

        cache_dir = BUILD_DIR / "mermaid" / Path(page["md_path"]).with_suffix("")
        artefact_dir = cache_dir / "artifacts"
        prepared_source = cache_dir / "source.md"
        rendered_md = cache_dir / "rendered.md"
        cache_dir.mkdir(parents=True, exist_ok=True)

        needs_render = True
        if rendered_md.exists():
            existing_svgs = sorted(artefact_dir.glob("*.svg"))
            prepared_matches = prepared_source.exists() and prepared_source.read_text(encoding="utf-8") == normalized_source
            if (
                len(existing_svgs) == mermaid_count
                and rendered_md.stat().st_mtime >= page["source_path"].stat().st_mtime
                and prepared_matches
            ):
                needs_render = False

        if needs_render:
            artefact_dir.mkdir(parents=True, exist_ok=True)
            prepared_source.write_text(normalized_source, encoding="utf-8")
            for old_svg in artefact_dir.glob("*.svg"):
                old_svg.unlink()
            if rendered_md.exists():
                rendered_md.unlink()
            env = os.environ.copy()
            env["PUPPETEER_SKIP_DOWNLOAD"] = "1"
            env["PUPPETEER_EXECUTABLE_PATH"] = chrome
            subprocess.run(
                [
                    npx,
                    "-y",
                    f"@mermaid-js/mermaid-cli@{MERMAID_VERSION}",
                    "-i",
                    str(prepared_source),
                    "-o",
                    str(rendered_md),
                    "-e",
                    "svg",
                    "-a",
                    str(artefact_dir),
                    "-c",
                    str(config_path),
                    "-q",
                ],
                check=True,
                env=env,
            )

        svg_paths = sorted(artefact_dir.glob("*.svg"))
        if len(svg_paths) != mermaid_count:
            raise RuntimeError(
                f"Expected {mermaid_count} Mermaid SVGs for {page['md_path']}, got {len(svg_paths)}."
            )
        page["mermaid_svgs"] = svg_paths


def build_combined_html(config: dict, pages: list[dict]) -> Path:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    stylesheets = []
    for pattern in ("assets/stylesheets/main*.css", "assets/stylesheets/palette*.css", "assets/css/custom.css"):
        for file in sorted(SITE_DIR.glob(pattern)):
            stylesheets.append(file.as_uri())

    body_sections = []
    for idx, page in enumerate(pages, start=1):
        fragment = normalize_fragment(page)
        section_class = "book-page book-page--cover" if page["md_path"] == "index.md" else "book-page"
        body_sections.append(
            f'<section class="{section_class}" data-page="{idx}">'
            f'<div class="book-page__meta">{idx:02d}</div>'
            f"{str(fragment)}"
            f"</section>"
        )

    extra_css = """
    @page { size: A4; margin: 16mm 14mm 18mm 14mm; }
    body { background: #f3eee6; }
    .book-root { max-width: 1000px; margin: 0 auto; }
    .book-page { break-after: page; margin: 0 0 12mm; padding: 16px 18px; background: #fffdfa; border: 1px solid rgba(124,20,27,.08); border-radius: 18px; box-shadow: 0 8px 30px rgba(0,0,0,.05); }
    .book-page:last-child { break-after: auto; }
    .book-page__meta { margin-bottom: 10px; color: #8e1d24; font-weight: 700; letter-spacing: .08em; font-size: 12px; }
    .book-page .cover-page, .book-page .community-page { margin: 0 0 14px; }
    .book-page .md-typeset h1 { page-break-after: avoid; }
    .book-page pre { white-space: pre-wrap; word-break: break-word; }
    .book-page table { display: table !important; width: 100%; }
    .book-page img { max-width: 100%; height: auto; }
    .book-page .mermaid-export { margin: 1.2rem 0; text-align: center; page-break-inside: avoid; }
    .book-page .mermaid-export__image { display: inline-block; width: auto; max-width: 100%; height: auto; }
    .md-header, .md-sidebar, .md-footer, .md-tabs, .mobile-share-strip { display: none !important; }
    """

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{config['site_name']}</title>
  {''.join(f'<link rel="stylesheet" href="{href}">' for href in stylesheets)}
  <style>{extra_css}</style>
</head>
<body>
  <main class="book-root">
    {''.join(body_sections)}
  </main>
</body>
</html>
"""
    output = BUILD_DIR / "book.html"
    output.write_text(html, encoding="utf-8")
    return output


def build_pdf(config: dict, combined_html: Path) -> Path:
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = DOWNLOADS_DIR / "claude-code-book.pdf"
    chrome = find_chrome()
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--allow-file-access-from-files",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}",
            combined_html.as_uri(),
        ],
        check=True,
    )
    return pdf_path


def build_epub(config: dict, pages: list[dict]) -> Path:
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    output = DOWNLOADS_DIR / "claude-code-book.epub"

    book = epub.EpubBook()
    book.set_identifier("warwolf-claude-code-book")
    book.set_title(config["site_name"])
    book.set_language("zh-CN")
    book.add_author(config.get("site_author", "Warwolf Team"))

    cover_path = ROOT / "docs" / "assets" / "images" / "claude-code-source-cover.png"
    if cover_path.exists():
        book.set_cover("cover.png", cover_path.read_bytes())

    css = epub.EpubItem(
        uid="style",
        file_name="style/book.css",
        media_type="text/css",
        content="""
        body { font-family: "PingFang SC", "Noto Sans SC", sans-serif; line-height: 1.8; }
        h1, h2, h3 { color: #7c141b; }
        pre, code { font-family: Menlo, monospace; white-space: pre-wrap; }
        img { max-width: 100%; height: auto; }
        blockquote { border-left: 3px solid #b1242a; padding-left: 1em; color: #666; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 6px; }
        """.encode("utf-8"),
    )
    book.add_item(css)

    image_items: dict[str, str] = {}
    chapters = []
    for idx, page in enumerate(pages, start=1):
        soup = normalize_fragment(page, for_epub=True)
        for img in soup.find_all("img"):
            src = img.get("src")
            if not src:
                continue
            img_path = Path(src)
            if not img_path.exists():
                continue
            file_name = image_items.get(src)
            if file_name is None:
                file_name = f"images/{len(image_items) + 1:04d}-{img_path.name}"
                image_items[src] = file_name
                mime_type = mimetypes.guess_type(img_path.name)[0] or "image/png"
                book.add_item(
                    epub.EpubItem(
                        uid=f"img-{len(image_items)}",
                        file_name=file_name,
                        media_type=mime_type,
                        content=img_path.read_bytes(),
                    )
                )
            img["src"] = file_name

        chapter = epub.EpubHtml(
            title=page["title"],
            file_name=f"chapter-{idx:02d}.xhtml",
            lang="zh-CN",
        )
        chapter.content = f"""
        <html>
          <head><link rel="stylesheet" href="style/book.css" /></head>
          <body>{str(soup)}</body>
        </html>
        """
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = tuple(chapters)
    book.spine = ["nav", *chapters]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(str(output), book, {})
    return output


def main() -> int:
    config = load_config()
    nav_entries = iter_nav_entries(config["nav"])
    pages = extract_pages(nav_entries)
    chrome = find_chrome()
    render_mermaid_svgs(pages, chrome)
    combined_html = build_combined_html(config, pages)
    pdf_path = build_pdf(config, combined_html)
    epub_path = build_epub(config, pages)
    print(f"Generated PDF: {pdf_path}")
    print(f"Generated EPUB: {epub_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
