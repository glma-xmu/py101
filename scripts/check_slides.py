#!/usr/bin/env python3
"""Bounded renderer and built-site checks for the static slides pilot.

Usage: python scripts/check_slides.py path/to/built/site
Run after a normal MkDocs build; no browser, network, or source writes are used.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from types import SimpleNamespace
from urllib.parse import parse_qs, urljoin, urlsplit

from mkdocs.structure.files import Files, InclusionLevel
from material.plugins.search.plugin import Parser as SearchParser

from build_slides import (
    ASSET_VERSION, DeckSection, HeadingIndex, TextbookTopic, incoming_sections,
    inject_textbook_links, on_files, parse_deck, parse_registry, parse_sections,
    read_decks, read_registry, render_deck, split_slides, textbook_to_deck_url, validate_links,
)
from check_navigation import Document


EXPECTED_SLIDES = {"lecture-1-1": 23}
REVEAL_SHA256 = {
    "reveal.js": "3fb84c30d2e610dd598843d75a123ef2c4dbc588847cda86cd8c7a61e18ddb6b",
    "reveal.css": "64e6203ee2048665c9f49c368f345fb3d7f936c404934162c70369a7682f388f",
    "LICENSE": "b2883e4b610bfa1b4d8fff84c4d4b825cc7d553cbd9fec4777c04068a2859dc0",
}
PREFIXES = ("/", "/py101/", "/teaching/py101/")
BASE = "https://slides-check.invalid"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def expect_invalid(function, *args):
    try:
        function(*args)
    except ValueError:
        return
    raise ValueError("Malformed slide source was accepted")


def check_renderer(root: Path, site: Path) -> None:
    source = '''---
title: Test deck
description: A renderer check
lang: en
source: test.pptx
---
<!-- slide: title-slide dense -->
# Hello
---
```text
---
```
'''
    deck = parse_deck(source, "lecture-test")
    require(len(deck.slides) == 2, "A code-block separator incorrectly split a slide")
    require(deck.slides[0][0] == "title-slide dense", "Multiple controlled CSS classes were lost")
    markup = render_deck(deck)
    require('class="title-slide dense"' in markup, "Slide class not rendered")
    require('class="highlight"' in markup, "Programming examples must be syntax-highlighted")
    escaped = render_deck(replace(deck, title='<Title & "quotes">'))
    require('<title>&lt;Title &amp; &quot;quotes&quot;&gt;' in escaped, "Title was not HTML-escaped")
    require('data-deck-title="&lt;Title &amp; &quot;quotes&quot;&gt;"' in escaped, "Attribute context was not escaped")
    expect_invalid(parse_deck, source, "../escape")
    expect_invalid(parse_deck, source.replace("title-slide dense", 'x" onclick="bad'), "lecture-test")
    expect_invalid(parse_deck, source.replace("title: Test deck", "title: []"), "lecture-test")
    expect_invalid(split_slides, "# One\n---\n")
    expect_invalid(split_slides, "# One\n```python\nprint(1)")

    config = SimpleNamespace(
        config_file_path=str(root / "mkdocs.yml"), site_dir=str(site),
        use_directory_urls=True, plugins=SimpleNamespace(_current_plugin=None),
    )
    # Match the personal-site workflow: config is inside course-src while cwd
    # is outside it. The hook must not depend on the invoking shell directory.
    previous = Path.cwd()
    try:
        os.chdir(root.parent)
        files = on_files(Files([]), config)
        files = on_files(files, config)  # repeated hooks must not duplicate routes
    finally:
        os.chdir(previous)
    require(len(files) == len(read_decks(root)), "Generated routes were duplicated")
    require(all(not f.is_documentation_page() and f.is_static_page() for f in files),
            "Decks must remain static HTML, outside Markdown navigation/search")
    require(all(f.inclusion == InclusionLevel.NOT_IN_NAV for f in files),
            "Deck navigation exclusion was lost")
    check_mapping_contract(root, deck)


def check_mapping_contract(root: Path, sample_deck) -> None:
    topics = read_registry(root)
    require(bool(topics), "The mapped slides pilot requires a textbook registry")
    sample_topic = next(iter(topics.values()))
    first = {"id": "intro", "title": "Intro", "start": 1, "level": 1, "textbook": sample_topic.id}
    second = {"id": "details", "title": "Details", "start": 2, "level": 2, "textbook": sample_topic.id}
    sections = parse_sections([first, second], 3)
    require(len(sections) == 2, "Valid section hierarchy rejected")
    for invalid in (None, [], {}, [dict(first, start=2)], [dict(first, start=True)],
                    [dict(first, id="slide-1")], [dict(first, id="../bad")],
                    [dict(first, level=2)], [dict(first, level=True)],
                    [dict(first, related="false")], [dict(first, unknown=True)],
                    [first, dict(second, start=1)], [first, dict(second, start=4)],
                    [first, dict(second, level=3)], [first, dict(second, id="intro")]):
        expect_invalid(parse_sections, invalid, 3)
    mapped = replace(sample_deck, sections=sections)
    validate_links([mapped], topics)
    expect_invalid(validate_links, [replace(mapped, sections=(replace(sections[0], textbook="unknown-topic"),))], topics)
    registry = {"topics": {sample_topic.id: {"page": sample_topic.page, "headings": dict(sample_topic.headings)}}}
    require(len(parse_registry(registry, root)) == 1, "Valid registry rejected")
    expect_invalid(parse_registry, {"topics": {"bad/id": registry["topics"][sample_topic.id]}}, root)
    expect_invalid(parse_registry, {"topics": {"test": {"page": "../escape.md", "headings": {"en": "a", "zh": "b"}}}}, root)
    expect_invalid(parse_registry, {"topics": {"test": {"page": "missing-page.md", "headings": {"en": "a", "zh": "b"}}}}, root)
    expect_invalid(parse_registry, {"topics": {"test": {"page": sample_topic.page, "headings": {"en": "a"}}}}, root)
    fake = TextbookTopic(sample_topic.id, sample_topic.page, {"en": "original-heading", "zh": "original-heading"})
    content = '<h2 id="original-heading">Original <code>text</code><a href="#original-heading">¶</a></h2><p>Unchanged body.</p>'
    def inject(value, decks=None):
        return inject_textbook_links(value, page_source=fake.page,
            page_url=fake.url("en").split("#")[0], language="en", decks=decks or [mapped], topics={fake.id: fake})
    linked = inject(content)
    require(linked.count('class="textbook-slides-link"') == 1, "Repeated topics created duplicate incoming links")
    require('<h2 id="original-heading">' in linked and '<code>text</code>' in linked,
            "Heading identity or original markup was changed")
    require('<p>Unchanged body.</p>' in linked, "Unrelated HTML was changed")
    require(inject(linked) == linked, "Heading-link injection is not idempotent")
    def search_titles(value):
        parser = SearchParser()
        parser.feed(value)
        parser.close()
        return ["".join(section.title).strip() for section in parser.data]
    require(search_titles(linked) == search_titles(content),
            "Generated heading chips changed Material search titles")
    require('data-search-exclude=""' in linked and 'aria-label="Slides:' in linked,
            "Search exclusion must preserve the chip's accessible link name")
    expect_invalid(inject, content.replace("original-heading", "missing-heading"))
    expect_invalid(inject, content + content)
    expect_invalid(inject, '<span id="' + fake.alias + '"></span>' + content)
    related = replace(mapped, sections=(replace(sections[0], related=True),))
    related_output = inject(content, [related])
    require(fake.alias in related_output and 'class="textbook-slides-link"' not in related_output,
            "Related-only topic should retain its alias without an incoming deck link")
    changed = replace(mapped, slides=mapped.slides + (("", "# Extra"),),
                      sections=(sections[0], replace(sections[1], start=3)))
    require('id="details"' in render_deck(mapped, topics) and 'id="details"' in render_deck(changed, topics),
            "Semantic section ids must survive a start-number change")


def resolved_local_path(page: str, href: str, prefix: str = "/") -> str:
    result = urlsplit(urljoin(BASE + prefix + page, href))
    require(result.netloc == "slides-check.invalid", f"Unexpected external runtime URL: {href}")
    require(result.path.startswith(prefix), f"Link escapes deployed site prefix: {href}")
    return result.path[len(prefix):]


def check_built_mapping(site: Path, decks, topics) -> None:
    """Check both directions against actual built targets, not just URL shapes."""
    documents = {}
    search_entries = []
    for index_path in site.rglob("search_index.json"):
        base = index_path.parent.parent.relative_to(site).as_posix()
        prefix = "" if base == "." else base + "/"
        for entry in json.loads(index_path.read_text(encoding="utf-8")).get("docs", []):
            location = entry.get("location", "")
            if prefix and not location.startswith(prefix):
                location = prefix + location
            search_entries.append((location, entry.get("title", "")))

    def load(page):
        if page not in documents:
            path = site / (page + "index.html" if page.endswith("/") else page)
            require(path.is_file(), f"Missing mapped destination: {page}")
            html = path.read_text(encoding="utf-8")
            documents[page] = (list(Document(html).root.walk()), HeadingIndex(html))
        return documents[page]

    for deck in decks:
        nodes, _ = load(deck.route)
        slides = [n for n in nodes if n.tag == "section" and n.parent and n.parent.has_class("slides")]
        ids = [n.attrs["id"] for n in nodes if n.attrs.get("id")]
        require(len(ids) == len(set(ids)), f"{deck.slug}: duplicate rendered HTML ids")
        outline = next((n for n in nodes if n.attrs.get("id") == "slides-outline"), None)
        if not deck.sections:
            require(outline is None, "Unmapped decks must not acquire a fake outline")
            continue
        require(outline is not None and outline.tag == "ol", "Mapped deck is missing its outline")
        entries = [n for n in outline.children if n.tag == "li"]
        require(len(entries) == len(deck.sections), "Outline section count differs from metadata")
        for entry, section in zip(entries, deck.sections):
            links = [n for n in entry.walk() if n.tag == "a"]
            require(len(links) == 1, "Outline entry must contain exactly one section link")
            require(entry.attrs.get("data-level") == str(section.level), "Outline hierarchy level changed")
            require(links[0].attrs.get("data-start") == str(section.start)
                    and links[0].attrs.get("href") == "#/" + section.id
                    and links[0].attrs.get("target") == "_self", "Outline entry has an incorrect section target")
        toolbar = next((n for n in nodes if n.attrs.get("id") == "slides-textbook"), None)
        require(toolbar is not None and toolbar.tag == "a" and toolbar.attrs.get("target") == "_self",
                "Textbook toolbar link is missing or cannot navigate natively")
        require(toolbar.attrs.get("href") == slides[0].attrs.get("data-textbook-en"),
                "Initial textbook control is not mapped to the first slide")
        for number, slide in enumerate(slides, start=1):
            section = deck.topic_for_slide(number)
            topic = topics[section.textbook]
            require(slide.attrs.get("data-slide-number") == str(number), "Legacy slide numbering changed")
            require(slide.attrs.get("id") == (section.id if number == section.start else f"slide-{number}"),
                    "Semantic/legacy slide anchor is incorrect")
            require(slide.attrs.get("data-topic-id") == section.id
                    and slide.attrs.get("data-topic-title") == section.title,
                    "Slide topic metadata does not follow section ranges")
            require(slide.attrs.get("data-textbook-related") == str(section.related).lower(),
                    "Related-only textbook mapping was lost")
            for language in ("en", "zh"):
                href = slide.attrs.get("data-textbook-" + language) or ""
                require(href == "../../../" + topic.url(language), "Outgoing textbook URL differs from registry")
                for prefix in PREFIXES:
                    target = urlsplit(urljoin(BASE + prefix + deck.route, href))
                    target_path = resolved_local_path(deck.route, href, prefix)
                    _, book_index = load(target_path)
                    require(target.fragment == topic.alias and len(book_index.ids.get(target.fragment, [])) == 1,
                            f"Slide {number}: missing {language} textbook anchor {target.fragment}")

    expected_links = sum(2 * len(list(incoming_sections(decks, topic.id))) for topic in topics.values())
    actual_links = 0
    for topic in topics.values():
        for language in ("en", "zh"):
            book_page = topic.url(language).split("#")[0]
            nodes, index = load(book_page)
            originals = index.headings.get(topic.headings[language], [])
            require(len(originals) == 1, f"Original textbook heading was lost: {topic.id}/{language}")
            heading = originals[0]
            heading_html = index.content[heading.start:heading.close_start + len(heading.tag) + 3]
            # Remove only our known plain-text chips to derive the pre-injection
            # title. The actual search JSON must match, not merely omit a word.
            original_heading_html = re.sub(r' <a class="textbook-slides-link"[^>]*>[^<]*</a>', "", heading_html)
            search_parser = SearchParser()
            search_parser.feed(original_heading_html)
            search_parser.close()
            title_section = next(s for s in search_parser.data if s.el.tag == heading.tag)
            original_title = "".join(title_section.title).strip()
            location = book_page + ("#" + heading.id if heading.tag != "h1" else "")
            indexed_titles = [title.replace("\u200b", "") for path, title in search_entries if path == location]
            require(bool(indexed_titles) and all(title == original_title for title in indexed_titles),
                    f"Search title changed after link injection: {topic.id}/{language}")
            aliases = index.ids.get(topic.alias, [])
            require(len(aliases) == 1 and aliases[0][0] == "span" and aliases[0][2] is originals[0]
                    and aliases[0][1].get("aria-hidden") == "true", "Book alias must stay inside its original heading")
            links = [(attrs, parent) for attrs, parent in index.generated_links
                     if attrs.get("data-slide-topic") == topic.id]
            expected = list(incoming_sections(decks, topic.id))
            require(len(links) == len(expected), f"Duplicate or missing inbound links for {topic.id}/{language}")
            actual_links += len(links)
            for deck, section in expected:
                matches = [(attrs, parent) for attrs, parent in links if attrs.get("data-slide-deck") == deck.slug]
                require(len(matches) == 1 and matches[0][1] is originals[0], "Incoming link left the mapped heading")
                attrs = matches[0][0]
                require("data-search-exclude" in attrs and bool(attrs.get("aria-label")),
                        "Heading chip must be excluded from search, not from accessibility")
                require(attrs.get("href") == textbook_to_deck_url(book_page, deck, section, language)
                        and attrs.get("target") == "_self", "Textbook link did not choose the earliest direct section")
                for prefix in PREFIXES:
                    target = urlsplit(urljoin(BASE + prefix + book_page, attrs["href"]))
                    target_path = resolved_local_path(book_page, attrs["href"], prefix)
                    require(target_path == deck.route.removesuffix("index.html"), "Textbook link leaves its deck")
                    target_nodes, _ = load(target_path)
                    require(parse_qs(target.query) == {"lang": [language]} and target.fragment == "/" + section.id,
                            "Textbook link lost locale or semantic section anchor")
                    require(sum(n.attrs.get("id") == section.id for n in target_nodes) == 1,
                            "Textbook link points to a missing slide section")
            for nav in (n for n in nodes if n.has_class("md-nav--secondary")):
                require(not any(n.has_class("textbook-slides-link") for n in nav.walk()),
                        "Generated heading link leaked into the table of contents")
                require(not any(n.tag == "a" and urlsplit(n.attrs.get("href") or "").fragment == topic.alias
                                for n in nav.walk()), "Book alias replaced an original ToC anchor")
    require(actual_links == expected_links, "Incoming textbook link total is inconsistent")


def check_built(root: Path, site: Path) -> tuple[int, int]:
    decks = read_decks(root)
    topics = read_registry(root)
    validate_links(decks, topics)
    for deck in decks:
        built_path = site / deck.route
        require(built_path.is_file(), f"Missing generated deck: {deck.route}")
        html = built_path.read_text(encoding="utf-8")
        require(html == render_deck(deck, topics), f"{deck.slug}: built deck is stale; rebuild from current source")
        document = Document(html)
        nodes = list(document.root.walk())
        slides = [n for n in nodes if n.tag == "section" and n.parent and n.parent.has_class("slides")]
        require(len(slides) == len(deck.slides), f"{deck.slug}: source/build slide count differs")
        if deck.slug in EXPECTED_SLIDES:
            require(len(slides) == EXPECTED_SLIDES[deck.slug], f"{deck.slug}: expected 23 pilot slides")
        require(not any(n.has_class("md-nav") for n in nodes), "Standalone deck contains textbook navigation")
        require(not (root / "docs" / deck.route).exists(), "Generated HTML must not be written into docs/")
        require(not (site / "zh" / deck.route).exists(), "English deck was incorrectly duplicated under zh/")
        require(not any(n.tag == "base" for n in nodes), "Base URL must not override deployment-relative links")

        runtime = []
        for node in nodes:
            if node.tag in ("script", "img") and node.attrs.get("src"):
                runtime.append(node.attrs["src"])
            if node.tag == "link" and node.attrs.get("rel") == "stylesheet":
                runtime.append(node.attrs.get("href") or "")
            if node.tag == "script":
                require(bool(node.attrs.get("src")), "Unexpected inline runtime script")
        scripts = [n.attrs.get("src") for n in nodes if n.tag == "script"]
        require(scripts == ["../../assets/reveal/reveal.js", f"../../assets/course-slides.js?v={ASSET_VERSION}"],
                "Reveal must load locally before the course player")
        styles = [n.attrs.get("href") for n in nodes if n.tag == "link" and n.attrs.get("rel") == "stylesheet"]
        require(styles == ["../../assets/reveal/reveal.css", f"../../assets/course-slides.css?v={ASSET_VERSION}"],
                "Reveal base CSS must load before local course styles")
        for prefix in PREFIXES:
            for href in runtime:
                require(not href.startswith(("/", "http:", "https:", "//")), f"Runtime URL is not relative: {href}")
                asset = resolved_local_path(deck.route, href, prefix)
                require((site / asset).is_file(), f"Missing local deck asset: {asset}")
            back = next((n for n in nodes if n.has_class("slides-back")), None)
            require(back is not None, "Slides-library return link is missing")
            require(resolved_local_path(deck.route, back.attrs.get("href") or "", prefix) == "slides/",
                    "Return link leaves the slides library")
        for control in ("slides-overview", "slides-fullscreen", "slides-reading"):
            require(sum(n.attrs.get("id") == control for n in nodes) == 1, f"Missing or duplicate control: {control}")

    for language in ("", "zh/"):
        library_page = language + "slides/index.html"
        library_path = site / library_page
        require(library_path.is_file(), f"Missing slides library: {library_page}")
        nodes = list(Document(library_path.read_text(encoding="utf-8")).root.walk())
        cards = [n for n in nodes if n.tag == "a" and n.has_class("slides-library__card")]
        require(len(cards) >= len(decks), f"Library is missing a deck card: {library_page}")
        for prefix in PREFIXES:
            targets = {resolved_local_path(library_page, n.attrs.get("href") or "", prefix) for n in cards}
            for deck in decks:
                require(deck.route.removesuffix("index.html") in targets, f"Library card misses {deck.slug}: {library_page}")
        home = site / language / "index.html"
        home_nodes = list(Document(home.read_text(encoding="utf-8")).root.walk())
        for nav in (n for n in home_nodes if n.has_class("md-nav--primary")):
            for link in (n for n in nav.walk() if n.tag == "a"):
                target = urlsplit(urljoin(BASE + "/" + language + "index.html", link.attrs.get("href") or ""))
                if target.netloc == "slides-check.invalid":
                    path = target.path.lstrip("/")
                    require(not path.startswith(("slides/", "zh/slides/")),
                            "Slides library/deck leaked into textbook chapter navigation")

    for index_path in site.rglob("search_index.json"):
        index = json.loads(index_path.read_text(encoding="utf-8"))
        for entry in index.get("docs", []):
            require("slides/" not in entry.get("location", ""), "Slides library/deck leaked into textbook search")
    for name, expected in REVEAL_SHA256.items():
        source = root / "docs/slides/assets/reveal" / name
        require(hashlib.sha256(source.read_bytes()).hexdigest() == expected, f"Vendored Reveal file changed: {name}")
        require((site / "slides/assets/reveal" / name).read_bytes() == source.read_bytes(), f"Built Reveal file differs: {name}")
    require(not (site / "slides/assets/reveal/README/index.html").exists(), "Vendor notes became a MkDocs page")
    check_built_mapping(site, decks, topics)
    return len(decks), sum(len(d.slides) for d in decks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, help="Built MkDocs site directory")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    try:
        check_renderer(root, args.site.resolve())
        count, slides = check_built(root, args.site.resolve())
    except (ValueError, OSError, KeyError) as error:
        print(f"Slide check failed: {error}", file=sys.stderr)
        return 1
    print(f"Slides OK: {count} deck, {slides} slides; EN/ZH links, local assets, three site prefixes, renderer and navigation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
