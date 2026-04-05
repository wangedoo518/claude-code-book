#!/usr/bin/env python3
from __future__ import annotations

import mimetypes
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


def normalize_fragment(article_html: str, html_path: Path, *, for_epub: bool = False):
    soup = BeautifulSoup(article_html, "lxml")

    for el in soup.select(".headerlink,.md-content__button,.mobile-share-strip"):
        el.decompose()

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
        if not html_path.exists():
            raise FileNotFoundError(f"Missing built page: {html_path}")
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


def build_combined_html(config: dict, pages: list[dict]) -> Path:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    stylesheets = []
    for pattern in ("assets/stylesheets/main*.css", "assets/stylesheets/palette*.css", "assets/css/custom.css"):
        for file in sorted(SITE_DIR.glob(pattern)):
            stylesheets.append(file.as_uri())

    body_sections = []
    for idx, page in enumerate(pages, start=1):
        fragment = normalize_fragment(page["article_html"], page["html_path"])
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

    cover_path = ROOT / "docs" / "assets" / "images" / "warwolf-book-icon.png"
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
        soup = normalize_fragment(page["article_html"], page["html_path"], for_epub=True)
        for img in soup.find_all("img"):
            src = img.get("src")
            if not src:
                continue
            img_path = Path(src)
            if not img_path.exists():
                continue
            file_name = image_items.get(src)
            if file_name is None:
                file_name = f"images/{img_path.name}"
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
    combined_html = build_combined_html(config, pages)
    pdf_path = build_pdf(config, combined_html)
    epub_path = build_epub(config, pages)
    print(f"Generated PDF: {pdf_path}")
    print(f"Generated EPUB: {epub_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
