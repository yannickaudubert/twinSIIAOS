#!/usr/bin/env python3
"""Static human-UX audit for the versioned Radar V4 shell.

This does not pretend to replace visual review. It protects basic usability and
publication invariants between screenshot reviews: navigability, human help,
construction-slop absence, renderer/markup contracts and Free/Expert data
boundaries in the demo dataset.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "fixtures" / "radar-public.demo.json"

CRITICAL_PAGES = [
    "index.html",
    "start.html",
    "guide.html",
    "lexique.html",
    "resource.html",
]

CONSTRUCTION_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"lorem ipsum",
    r"à compléter",
    r"coming soon",
    r"work in progress",
]

FORBIDDEN_PUBLIC_FIELDS = {
    "fit",
    "competitive_position",
    "benchmark_summary",
    "blast_radius",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang: str | None = None
        self.title = ""
        self._in_title = False
        self.has_viewport = False
        self.links: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "html":
            self.lang = attrs_dict.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and attrs_dict.get("name") == "viewport":
            self.has_viewport = bool(attrs_dict.get("content"))
        elif tag == "a" and attrs_dict.get("href"):
            self.links.append(str(attrs_dict["href"]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()
        if data.strip():
            self.text.append(data.strip())


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def local_target_exists(page: Path, href: str) -> bool:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith(("#", "mailto:", "tel:")):
        return True
    raw_path = parsed.path
    if not raw_path:
        return True
    target = (page.parent / raw_path).resolve()
    try:
        target.relative_to(ROOT.parent.resolve())
    except ValueError:
        return False
    if raw_path.endswith("/"):
        target = target / "index.html"
    return target.exists()


def audit_pages() -> list[str]:
    errors: list[str] = []
    pages = sorted(ROOT.glob("*.html"))
    names = {page.name for page in pages}

    for required in CRITICAL_PAGES:
        if required not in names:
            errors.append(f"missing critical page: {required}")

    for page in pages:
        parser = parse_page(page)
        text = " ".join(parser.text)
        if parser.lang != "fr":
            errors.append(f"{page.name}: html lang must be fr")
        if not parser.has_viewport:
            errors.append(f"{page.name}: missing viewport meta")
        if not parser.title or "Resource Radar" not in parser.title:
            errors.append(f"{page.name}: title must identify Resource Radar")

        for pattern in CONSTRUCTION_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                errors.append(f"{page.name}: construction text matched {pattern!r}")

        for href in parser.links:
            if not local_target_exists(page, href):
                errors.append(f"{page.name}: broken local href {href!r}")

    start = (ROOT / "start.html").read_text(encoding="utf-8")
    guide = (ROOT / "guide.html").read_text(encoding="utf-8")
    glossary = (ROOT / "lexique.html").read_text(encoding="utf-8")
    resource = (ROOT / "resource.html").read_text(encoding="utf-8")
    resource_js = (ROOT / "resource.js").read_text(encoding="utf-8")
    app = (ROOT / "app.js").read_text(encoding="utf-8")

    expectations = {
        "start.html": (start, ["guide.html", "lexique.html", "#free-expert"]),
        "guide.html": (guide, ["start.html", "lexique.html", "resource-detail-v2.html"]),
        "lexique.html": (glossary, ["start.html", "guide.html", "resource-detail-v2.html"]),
        "resource.html": (resource, ["guide.html", "lexique.html", "#expert", 'id="resource-explanation"', 'href="#resource-explanation"']),
        "resource.js": (resource_js, ["getElementById('resource-explanation')", "public_explanation", "renderPublicExplanation"]),
        "app.js": (app, ["start.html", "guide.html", "lexique.html", "resource.html", "humanizeStaticShell"]),
    }
    for name, (content, markers) in expectations.items():
        for marker in markers:
            if marker not in content:
                errors.append(f"{name}: missing human-navigation/rendering marker {marker!r}")

    # Renderer contract: ids referenced by JS must exist on the dynamic resource page.
    resource_ids = set(re.findall(r'id="([A-Za-z0-9_-]+)"', resource))
    required_resource_ids = {
        "resource-content",
        "resource-title",
        "resource-summary",
        "resource-primary-role",
        "resource-explanation",
        "resource-proof",
        "resource-gaps",
        "resource-relations",
        "resource-provenance",
        "resource-trend",
        "resource-fit-public",
    }
    missing_ids = required_resource_ids - resource_ids
    if missing_ids:
        errors.append(f"resource.html: missing ids required by renderer: {sorted(missing_ids)}")

    return errors


def audit_fixture() -> list[str]:
    errors: list[str] = []
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if data.get("schema") != "siiaos.radar-public.v1":
        errors.append("fixture: incompatible radar-public schema")
    if data.get("fixture") is not True:
        errors.append("fixture: must be explicitly marked fixture=true")

    items = data.get("items")
    if not isinstance(items, list) or not items:
        errors.append("fixture: items must be a non-empty list")
        return errors

    explained = 0
    for item in items:
        if not isinstance(item, dict):
            errors.append("fixture: every item must be an object")
            continue
        leaked = FORBIDDEN_PUBLIC_FIELDS.intersection(item)
        if leaked:
            errors.append(f"fixture {item.get('id')}: protected fields leaked: {sorted(leaked)}")
        explanation = item.get("public_explanation")
        if explanation:
            explained += 1
            if not isinstance(explanation, dict):
                errors.append(f"fixture {item.get('id')}: public_explanation must be an object")
            else:
                for key in ("plain_language", "primary_role", "use_when", "avoid_when", "tradeoffs", "questions_to_ask"):
                    if not explanation.get(key):
                        errors.append(f"fixture {item.get('id')}: explained record missing {key}")

    if explained < 1:
        errors.append("fixture: at least one record must exercise structured public explainability")
    return errors


def main() -> int:
    errors = audit_pages() + audit_fixture()
    if errors:
        print("Human UX audit FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Human UX audit OK")
    print(f"- critical pages: {', '.join(CRITICAL_PAGES)}")
    print("- local navigation: resolved")
    print("- dynamic resource renderer contract: aligned")
    print("- construction slop: none detected")
    print("- public fixture: no protected Expert top-level fields")
    print("- structured Free explainability: exercised")
    return 0


if __name__ == "__main__":
    sys.exit(main())
