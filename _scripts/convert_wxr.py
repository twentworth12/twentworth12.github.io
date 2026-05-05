#!/usr/bin/env python3
"""One-shot WordPress WXR -> Jekyll markdown converter for tomwentworth.com.

Reads tomwentworth.WordPress.2026-05-05.xml in the project root and produces:
  _posts/YYYY-MM-DD-slug.md   for published posts
  _drafts/slug.md             for drafts
  assets/uploads/...           with all images downloaded locally
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WXR_PATH = ROOT / "tomwentworth.WordPress.2026-05-05.xml"
POSTS_DIR = ROOT / "_posts"
DRAFTS_DIR = ROOT / "_drafts"
ASSETS_DIR = ROOT / "assets" / "uploads"

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}

# Hosts whose images we want to download and serve locally.
LOCAL_IMAGE_HOSTS = {"tomwentworth.com", "tomwentworthcom.wordpress.com", "i1.wp.com", "i0.wp.com", "i2.wp.com"}


def text(el: ET.Element | None) -> str:
    return (el.text or "") if el is not None else ""


def expand_wp_embeds(html: str) -> str:
    """Expand WordPress oEmbed blocks (which store bare URLs) into real iframes."""
    # Match a wp:embed opening comment + the figure block. The figure block contains the bare URL.
    pattern = re.compile(
        r'<!--\s*wp:embed\s+(\{[^}]*\})\s*-->\s*'
        r'<figure[^>]*class="[^"]*wp-block-embed[^"]*"[^>]*>'
        r'\s*<div class="wp-block-embed__wrapper">\s*([^<\s]+)\s*</div>\s*'
        r'</figure>\s*'
        r'<!--\s*/wp:embed\s*-->',
        re.DOTALL,
    )

    def replace(m: re.Match) -> str:
        meta_json, url = m.group(1), m.group(2).strip()
        slug_match = re.search(r'"providerNameSlug":"([^"]+)"', meta_json)
        provider = slug_match.group(1) if slug_match else ""
        return embed_iframe(provider, url)

    return pattern.sub(replace, html)


def embed_iframe(provider: str, url: str) -> str:
    """Map a provider+URL to an embeddable iframe (or sensible fallback)."""
    if provider == "spotify":
        # https://open.spotify.com/show/X or /episode/X or /track/X -> /embed/...
        m = re.match(r"https?://open\.spotify\.com/(show|episode|track|playlist|album)/([A-Za-z0-9]+)", url)
        if m:
            kind, sid = m.group(1), m.group(2)
            return (
                f'<iframe style="border-radius:12px" '
                f'src="https://open.spotify.com/embed/{kind}/{sid}" '
                f'width="100%" height="232" frameborder="0" '
                f'allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" '
                f'loading="lazy"></iframe>'
            )

    if provider == "loom":
        m = re.match(r"https?://(?:www\.)?loom\.com/share/([A-Za-z0-9]+)", url)
        if m:
            lid = m.group(1)
            return (
                f'<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;">'
                f'<iframe src="https://www.loom.com/embed/{lid}" frameborder="0" allowfullscreen '
                f'style="position:absolute;top:0;left:0;width:100%;height:100%;"></iframe>'
                f'</div>'
            )

    if provider == "youtube":
        m = re.match(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]+)", url)
        if m:
            yid = m.group(1)
            return (
                f'<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;">'
                f'<iframe src="https://www.youtube.com/embed/{yid}" frameborder="0" '
                f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
                f'allowfullscreen '
                f'style="position:absolute;top:0;left:0;width:100%;height:100%;"></iframe>'
                f'</div>'
            )

    if provider == "twitter":
        # Use Twitter's official blockquote + widget.js. Note widget.js loaded once per page is fine
        # (idempotent), so we include the script tag with each tweet — the browser de-dupes.
        return (
            f'<blockquote class="twitter-tweet"><a href="{url}"></a></blockquote>'
            f'<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
        )

    # Fallback: leave URL as a hyperlink so the post still has the reference.
    return f'<p><a href="{url}">{url}</a></p>'


def strip_wp_block_comments(html: str) -> str:
    # Remove remaining WordPress Gutenberg block comments after embeds have been expanded.
    return re.sub(r"<!--\s*/?wp:[^>]*-->", "", html)


def normalize_image_url(url: str) -> str:
    # Strip query strings like ?w=600 from WordPress image URLs.
    parsed = urllib.parse.urlsplit(url)
    if parsed.netloc in LOCAL_IMAGE_HOSTS or parsed.netloc.endswith(".wordpress.com"):
        return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    return url


def local_asset_path_for(url: str) -> tuple[str, Path]:
    """Return (rewritten src, local file path) for a remote image URL.

    Example:
      https://tomwentworth.com/wp-content/uploads/2017/06/foo.png
        -> ('/assets/uploads/2017/06/foo.png', <ROOT>/assets/uploads/2017/06/foo.png)
    """
    parsed = urllib.parse.urlsplit(url)
    path = parsed.path  # /wp-content/uploads/YYYY/MM/file.ext
    # Trim leading /wp-content/uploads/ if present, otherwise use the basename hierarchy
    m = re.match(r"^/wp-content/uploads/(.+)$", path)
    sub = m.group(1) if m else os.path.basename(path)
    rel = f"/assets/uploads/{sub}"
    return rel, ROOT / "assets" / "uploads" / sub


def collect_and_rewrite_images(html: str, downloads: dict[str, Path]) -> str:
    """Find <img src=...> URLs we should localize, rewrite them, and queue downloads."""
    def repl(match: re.Match) -> str:
        full = match.group(0)
        attr = match.group(1)  # e.g., src="..." or srcset="..."
        url = match.group(2)
        normalized = normalize_image_url(url)
        parsed = urllib.parse.urlsplit(normalized)
        if parsed.netloc in LOCAL_IMAGE_HOSTS:
            new_src, local_path = local_asset_path_for(normalized)
            downloads[normalized] = local_path
            return f'{attr}="{new_src}"'
        return full

    # Match src="..." and src='...' (single-quote rare but safe)
    pattern = re.compile(r'\b(src)=["\']([^"\']+)["\']', re.IGNORECASE)
    html = pattern.sub(repl, html)

    # Drop srcset entirely — Jekyll will serve the single image; srcset would still point to WP.
    html = re.sub(r'\s+srcset=["\'][^"\']+["\']', "", html)
    return html


EMBED_TAG = "EMBEDPLACEHOLDER"


def stash_embeds(html: str) -> tuple[str, list[str]]:
    """Replace iframes and twitter blockquote+script blobs with placeholders.

    Pandoc 3.9's HTML reader fetches iframe src URLs and inlines their rendered HTML —
    which corrupts our preserved embeds. Stashing them as plain text avoids that.
    """
    stashed: list[str] = []

    def take(match: re.Match) -> str:
        idx = len(stashed)
        stashed.append(match.group(0))
        return f"<p>{EMBED_TAG}{idx}{EMBED_TAG}</p>"

    # Twitter blockquote + accompanying script tag (must come first so it doesn't get split)
    html = re.sub(
        r'<blockquote class="twitter-tweet">.*?</blockquote>\s*<script[^>]*></script>',
        take,
        html,
        flags=re.DOTALL,
    )
    # Iframes (and the optional position-relative wrapper div if present)
    html = re.sub(
        r'<div style="position:relative[^"]*"[^>]*>\s*<iframe[^>]*>\s*</iframe>\s*</div>',
        take,
        html,
        flags=re.DOTALL,
    )
    html = re.sub(r'<iframe[^>]*>\s*</iframe>', take, html, flags=re.DOTALL)
    return html, stashed


def restore_embeds(markdown: str, stashed: list[str]) -> str:
    def put(match: re.Match) -> str:
        return stashed[int(match.group(1))]
    return re.sub(rf"{EMBED_TAG}(\d+){EMBED_TAG}", put, markdown)


def html_to_markdown(html: str) -> str:
    """HTML -> GFM via pandoc, with iframes/embeds round-tripped through placeholders."""
    html, stashed = stash_embeds(html)
    proc = subprocess.run(
        [
            "pandoc",
            "--from", "html",
            "--to", "gfm+raw_html-smart",
            "--wrap=none",
        ],
        input=html,
        capture_output=True,
        text=True,
        check=True,
    )
    return restore_embeds(proc.stdout, stashed)


def yaml_escape(s: str) -> str:
    # Conservatively quote with double quotes and escape internal " and \.
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def front_matter(title: str, date: str, categories: list[str], tags: list[str], slug: str) -> str:
    lines = ["---", "layout: post", f"title: {yaml_escape(title)}", f"date: {date}"]
    if categories:
        lines.append("categories:")
        for c in categories:
            lines.append(f"  - {yaml_escape(c)}")
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f"  - {yaml_escape(t)}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def download_image(url: str, dest: Path) -> bool:
    if dest.exists():
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "wxr-migration/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"  ! failed to download {url}: {exc}", file=sys.stderr)
        return False


def main() -> int:
    if not WXR_PATH.exists():
        print(f"WXR file not found: {WXR_PATH}", file=sys.stderr)
        return 1

    POSTS_DIR.mkdir(exist_ok=True)
    DRAFTS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    tree = ET.parse(WXR_PATH)
    root = tree.getroot()
    channel = root.find("channel")
    assert channel is not None

    downloads: dict[str, Path] = {}
    counts = {"published": 0, "drafts": 0, "skipped": 0}

    for item in channel.findall("item"):
        post_type = text(item.find("wp:post_type", NS))
        if post_type != "post":
            continue

        status = text(item.find("wp:status", NS))
        if status not in ("publish", "draft"):
            counts["skipped"] += 1
            continue

        title = text(item.find("title")).strip()
        slug = text(item.find("wp:post_name", NS)).strip()
        if not slug:
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "untitled"

        post_date_str = text(item.find("wp:post_date", NS)).strip()  # YYYY-MM-DD HH:MM:SS (local)
        post_date_gmt_str = text(item.find("wp:post_date_gmt", NS)).strip()
        chosen = post_date_gmt_str if post_date_gmt_str and post_date_gmt_str != "0000-00-00 00:00:00" else post_date_str
        try:
            dt = datetime.strptime(chosen, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.now()
        date_iso = dt.strftime("%Y-%m-%d %H:%M:%S +0000")
        date_prefix = dt.strftime("%Y-%m-%d")

        categories: list[str] = []
        tags: list[str] = []
        for cat in item.findall("category"):
            domain = cat.attrib.get("domain", "")
            value = (cat.text or "").strip()
            if not value:
                continue
            if domain == "category":
                categories.append(value)
            elif domain == "post_tag":
                tags.append(value)

        content_html = text(item.find("content:encoded", NS))
        content_html = expand_wp_embeds(content_html)
        content_html = strip_wp_block_comments(content_html)
        content_html = collect_and_rewrite_images(content_html, downloads)

        try:
            markdown_body = html_to_markdown(content_html)
        except subprocess.CalledProcessError as exc:
            print(f"  ! pandoc failed for {slug}: {exc.stderr}", file=sys.stderr)
            markdown_body = content_html  # fall back: leave raw HTML

        fm = front_matter(title, date_iso, categories, tags, slug)
        body = fm + markdown_body.rstrip() + "\n"

        if status == "publish":
            out = POSTS_DIR / f"{date_prefix}-{slug}.md"
            counts["published"] += 1
        else:
            out = DRAFTS_DIR / f"{slug}.md"
            counts["drafts"] += 1
        out.write_text(body, encoding="utf-8")

    print(f"Wrote {counts['published']} posts, {counts['drafts']} drafts (skipped {counts['skipped']}).")
    print(f"Downloading {len(downloads)} unique images...")

    success = 0
    for url, dest in sorted(downloads.items()):
        if download_image(url, dest):
            success += 1
    print(f"Downloaded {success}/{len(downloads)} images.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
