#!/usr/bin/env python3
"""Check built EN/ZH navigation without browser or third-party dependencies.

Usage: python scripts/check_navigation.py path/to/built/site

The expected page lists intentionally mirror the course's top-level navigation.
Update them when deliberately adding, removing, or reordering course pages.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urljoin, urlsplit


@dataclass(frozen=True)
class Section:
    pages: tuple[str, ...]
    collapsed: bool = False

    @property
    def slug(self) -> str:
        return self.pages[0]


SECTIONS = (
    Section(("ch1_1_objects", "ch1_2_collections", "ch1_3_control_flow", "ch1_4_iterators")),
    Section(("ch2_1_defining_functions", "ch2_2_namespaces_scope", "ch2_3_first_class",
             "ch2_4_use_cases", "ch2_5_loose_ends")),
    Section(("ch3_1_numpy", "ch3_2_pandas", "ch3_3_reshape_group", "ch3_4_merge")),
    Section(("exercises_ch1", "exercises_ch2", "exercises_ch3"), collapsed=True),
    Section(("appendix_a1_environment", "appendix_a2_shell", "appendix_a3_git"), collapsed=True),
    Section(("camp_index", "camp_ch1_style", "camp_ch2_environments", "camp_ch3_names",
             "camp_ch4_functions", "camp_ch5_oop", "camp_ch6_pandas", "camp_ch7_performance"),
            collapsed=True),
)
LANGUAGES = ("", "zh/")
VOID_TAGS = frozenset(("area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "param", "source", "track", "wbr"))
BASE = "https://navigation-check.invalid/"


@dataclass
class Element:
    tag: str
    attrs: dict[str, str | None] = field(default_factory=dict)
    children: list[Element] = field(default_factory=list)
    parent: Element | None = field(default=None, repr=False)

    def has_class(self, name: str) -> bool:
        return name in (self.attrs.get("class") or "").split()

    def walk(self):
        for child in self.children:
            yield child
            yield from child.walk()

    def closest(self, tag: str) -> Element | None:
        node = self.parent
        while node is not None:
            if node.tag == tag:
                return node
            node = node.parent
        return None


class Document(HTMLParser):
    def __init__(self, html: str):
        super().__init__(convert_charrefs=True)
        self.root = Element("document")
        self.stack = [self.root]
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Element(tag, dict(attrs), parent=self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return


def page_path(language: str, slug: str) -> str:
    return f"{language}py101_md/{slug}/"


def link_target(page: str, href: str | None) -> str | None:
    if not href:
        return None
    target = urlsplit(urljoin(BASE + page, href))
    if target.scheme != "https" or target.netloc != "navigation-check.invalid":
        return None
    # An on-page fragment is not a section's direct navigation link.
    if target.fragment or target.query:
        return None
    path = target.path.lstrip("/")
    if path.endswith("index.html"):
        path = path[:-len("index.html")]
    return path


def check_page(site: Path, page: str, language: str, errors: list[str]) -> None:
    name = page + "index.html"

    def require(condition, message):
        if not condition:
            errors.append(f"{name}: {message}")
        return condition

    html_path = site / name
    if not require(html_path.is_file(), "built page is missing"):
        return
    document = Document(html_path.read_text(encoding="utf-8"))
    primary = [node for node in document.root.walk()
               if node.tag == "nav" and node.has_class("md-nav--primary")]
    if not require(len(primary) == 1, "expected one primary navigation"):
        return
    marked = [node for node in primary[0].walk() if "data-course-section" in node.attrs]
    require(len(marked) == len(SECTIONS), "expected exactly six marked course sections")

    for section in SECTIONS:
        matches = [node for node in marked if node.attrs["data-course-section"] == section.slug]
        prefix = section.slug + ": "
        if not require(len(matches) == 1, prefix + "expected one section marker"):
            continue
        group = matches[0]
        require(group.tag == "li" and group.parent is not None
                and group.parent.tag == "ul" and group.parent.parent is primary[0],
                prefix + "section must be a top-level primary-navigation item")
        toggles = [node for node in group.children
                   if node.tag == "input" and node.attrs.get("type") == "checkbox"]
        containers = [node for node in group.children
                      if node.tag == "div" and node.has_class("md-nav__container")]
        if not require(len(toggles) == 1 and len(containers) == 1,
                       prefix + "expected separate checkbox and header container"):
            continue
        toggle, header = toggles[0], containers[0]
        require(toggle.has_class("md-nav__toggle") and toggle.has_class("md-toggle"),
                prefix + "checkbox must retain Material's native toggle classes")
        anchors = [node for node in header.children if node.tag == "a"]
        labels = [node for node in header.children if node.tag == "label"]
        if require(len(anchors) == 1 and len(labels) == 1,
                   prefix + "header must have a sibling anchor and arrow label"):
            require(link_target(page, anchors[0].attrs.get("href"))
                    == page_path(language, section.slug),
                    prefix + "header link must resolve to the first subsection")
            toggle_id = toggle.attrs.get("id")
            require(bool(toggle_id) and labels[0].attrs.get("for") == toggle_id,
                    prefix + "arrow label must control this section's checkbox")
            require(labels[0].attrs.get("tabindex") == "0"
                    and bool((labels[0].attrs.get("aria-label") or "").strip()),
                    prefix + "arrow must be keyboard-focusable and have an accessible name")
            require(any(node.has_class("md-nav__icon") for node in labels[0].walk()),
                    prefix + "arrow label must contain the native navigation icon")
            require(not any(node.tag == "a" for node in labels[0].walk()),
                    prefix + "arrow must not wrap or replace the header link")

        expected = [page_path(language, slug) for slug in section.pages]
        active = page in expected
        require(("checked" in toggle.attrs) == active,
                prefix + "checked state must follow the active section")
        require(toggle.has_class("md-toggle--indeterminate") == (not active and not section.collapsed),
                prefix + "inactive chapters must expand natively; supplemental groups must collapse")

        subnavs = [node for node in group.children if node.tag == "nav" and node.has_class("md-nav")]
        if not require(len(subnavs) == 1, prefix + "expected one subsection navigation"):
            continue
        if len(labels) == 1:
            label_id = labels[0].attrs.get("id")
            nav_id = subnavs[0].attrs.get("id")
            require(bool(label_id) and subnavs[0].attrs.get("aria-labelledby") == label_id,
                    prefix + "subnavigation must be labelled by its arrow for Material keyboard behavior")
            require(bool(nav_id) and labels[0].attrs.get("aria-controls") == nav_id,
                    prefix + "arrow aria-controls must identify its subsection navigation")
        lists = [node for node in subnavs[0].children if node.tag == "ul"]
        if not require(len(lists) == 1, prefix + "expected one subsection list"):
            continue
        items = [node for node in lists[0].children if node.tag == "li"]
        actual = []
        for item in items:
            links = [node for node in item.walk()
                     if node.tag == "a" and node.has_class("md-nav__link")
                     and node.closest("li") is item]
            require(len(links) == 1, prefix + "each subsection must retain its own link")
            if len(links) == 1:
                actual.append(link_target(page, links[0].attrs.get("href")))
        require(actual == expected, prefix + "all subsection links must remain in course order")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, help="directory produced by mkdocs build")
    args = parser.parse_args(argv)
    site = args.site.resolve()
    if not site.is_dir():
        parser.error(f"built site directory does not exist: {site}")
    errors: list[str] = []
    count = 0
    for language in LANGUAGES:
        pages = [language] + [page_path(language, slug) for section in SECTIONS for slug in section.pages]
        for page in pages:
            check_page(site, page, language, errors)
            count += 1
    if errors:
        print(f"Navigation checks failed ({len(errors)} findings):", file=sys.stderr)
        for error in errors[:60]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 60:
            print(f"- ... and {len(errors) - 60} more", file=sys.stderr)
        return 1
    print(f"Navigation checks passed: {count} EN/ZH pages; all six sections and 27 subsection links preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
