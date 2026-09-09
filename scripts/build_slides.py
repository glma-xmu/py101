"""Build trusted slide Markdown as standalone, local-only Reveal HTML.

Register this file under ``hooks`` in mkdocs.yml. The source stays outside docs/
so it is not rendered a second time as a course page or indexed as navigation.
No HTML is written into the source tree: MkDocs copies generated static files.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import posixpath
import re
from urllib.parse import quote

import markdown
import yaml
from mkdocs.exceptions import PluginError
from mkdocs.plugins import event_priority
from mkdocs.structure.files import File, InclusionLevel


GENERATOR = "scripts/build_slides.py"
ASSET_VERSION = "4"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LANG = re.compile(r"[a-zA-Z]{2,3}(?:-[a-zA-Z0-9]{2,8})*\Z")
CLASSES = re.compile(r"[a-z][a-z0-9-]*(?: +[a-z][a-z0-9-]*)*\Z")
SLIDE_MARKER = re.compile(r"<!--\s*slide:\s*(.*?)\s*-->\Z")
FENCE_START = re.compile(r" {0,3}(`{3,}|~{3,})[^\n]*\Z")


@dataclass(frozen=True)
class DeckSection:
    id: str
    title: str
    start: int
    level: int
    textbook: str
    related: bool = False


@dataclass(frozen=True)
class TextbookTopic:
    id: str
    page: str
    headings: dict[str, str]
    translated: bool = True

    @property
    def alias(self) -> str:
        return "textbook-" + self.id

    def source_page(self, language: str) -> str:
        return self.page if language == "en" or not self.translated else self.page[:-3] + ".zh.md"

    def url(self, language: str, directory_urls: bool = True) -> str:
        page = PurePosixPath(self.page)
        if directory_urls:
            path = str(page.parent) + "/" if page.stem in {"index", "README"} else str(page.with_suffix("")) + "/"
        else:
            path = str(page.with_suffix(".html"))
        if path.startswith("./"):
            path = path[2:]
        return ("zh/" if language == "zh" else "") + path + "#" + self.alias


@dataclass(frozen=True)
class Deck:
    slug: str
    title: str
    description: str
    lang: str
    source: str
    slides: tuple[tuple[str, str], ...]
    sections: tuple[DeckSection, ...] = ()

    @property
    def route(self) -> str:
        return f"slides/decks/{self.slug}/index.html"

    def topic_for_slide(self, number: int) -> DeckSection | None:
        return next((section for section in reversed(self.sections) if section.start <= number), None)


def parse_sections(value, slide_count: int) -> tuple[DeckSection, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError("sections must be a nonempty list when provided")
    sections = []
    ids = set()
    previous_start = 0
    previous_level = 0
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict) or set(item) - {"id", "title", "start", "level", "textbook", "related"}:
            raise ValueError(f"Section {index}: unexpected fields")
        for field in ("id", "title", "textbook"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"Section {index}: {field} must be nonempty text")
        if not SLUG.fullmatch(item["id"]) or re.fullmatch(r"slide-\d+", item["id"]):
            raise ValueError(f"Section {index}: invalid or reserved id")
        if item["id"] in ids:
            raise ValueError(f"Duplicate section id: {item['id']}")
        if not SLUG.fullmatch(item["textbook"]):
            raise ValueError(f"Section {index}: invalid textbook topic id")
        start, level = item.get("start"), item.get("level")
        if type(start) is not int or not previous_start < start <= slide_count:
            raise ValueError(f"Section {index}: starts must increase within the deck")
        if index == 1 and start != 1:
            raise ValueError("The first section must start on slide 1")
        if type(level) is not int or not 1 <= level <= 3 or level > previous_level + 1:
            raise ValueError(f"Section {index}: hierarchy must start at 1 and cannot skip a level")
        if "related" in item and type(item["related"]) is not bool:
            raise ValueError(f"Section {index}: related must be true or false")
        sections.append(DeckSection(**item))
        ids.add(item["id"])
        previous_start, previous_level = start, level
    return tuple(sections)


def parse_registry(value, root: Path) -> dict[str, TextbookTopic]:
    if not isinstance(value, dict) or set(value) != {"topics"} or not isinstance(value["topics"], dict):
        raise ValueError("Textbook link registry must contain one topics mapping")
    topics = {}
    docs = (root / "docs").resolve()
    for topic_id, item in value["topics"].items():
        if not isinstance(topic_id, str) or not SLUG.fullmatch(topic_id):
            raise ValueError("Textbook topic ids must be lowercase ASCII slugs")
        if not isinstance(item, dict) or set(item) != {"page", "headings"}:
            raise ValueError(f"Textbook topic {topic_id}: expected page and headings")
        page = item["page"]
        if (not isinstance(page, str) or "\\" in page or not page.endswith(".md")
                or page.endswith(".zh.md") or PurePosixPath(page).is_absolute()
                or ".." in PurePosixPath(page).parts or str(PurePosixPath(page)) != page):
            raise ValueError(f"Textbook topic {topic_id}: invalid canonical page")
        headings = item["headings"]
        if (not isinstance(headings, dict) or set(headings) != {"en", "zh"}
                or any(not isinstance(v, str) or not v.strip() or any(c.isspace() for c in v) for v in headings.values())):
            raise ValueError(f"Textbook topic {topic_id}: expected existing en/zh heading ids")
        translated = (docs / (page[:-3] + ".zh.md")).is_file()
        if not translated and headings["zh"] != headings["en"]:
            raise ValueError(f"Textbook topic {topic_id}: an untranslated page must use the English heading in both locales")
        topic = TextbookTopic(topic_id, page, headings, translated)
        for language in ("en", "zh"):
            source = (docs / topic.source_page(language)).resolve()
            if not source.is_relative_to(docs) or not source.is_file():
                raise ValueError(f"Textbook topic {topic_id}: missing {language} page {topic.source_page(language)}")
        topics[topic_id] = topic
    return topics


def read_registry(root: Path) -> dict[str, TextbookTopic]:
    path = root / "slides-src/textbook-links.yml"
    if not path.exists():
        return {}
    try:
        return parse_registry(yaml.safe_load(path.read_text(encoding="utf-8")), root)
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid textbook-links.yml: {error}") from error


def validate_links(decks: list[Deck], topics: dict[str, TextbookTopic]) -> None:
    for deck in decks:
        for section in deck.sections:
            if section.textbook not in topics:
                raise ValueError(f"{deck.slug}/{section.id}: unknown textbook topic {section.textbook}")


def split_slides(text: str) -> list[str]:
    """A --- line separates slides, except inside fenced programming examples."""
    parts: list[str] = []
    lines: list[str] = []
    fence_char = ""
    fence_length = 0
    for line in text.splitlines():
        if fence_char:
            if re.fullmatch(r" {0,3}" + re.escape(fence_char) + "{" + str(fence_length) + r",}\s*", line):
                fence_char = ""
            lines.append(line)
            continue
        fence = FENCE_START.fullmatch(line)
        if fence:
            fence_char, fence_length = fence[1][0], len(fence[1])
        if line.strip() == "---" and not fence_char:
            part = "\n".join(lines).strip()
            if not part:
                raise ValueError("Empty slide before a --- separator")
            parts.append(part)
            lines = []
        else:
            lines.append(line)
    if fence_char:
        raise ValueError("Unclosed fenced code block")
    last = "\n".join(lines).strip()
    if not last:
        raise ValueError("The deck must end with a nonempty slide")
    parts.append(last)
    return parts


def parse_deck(text: str, slug: str) -> Deck:
    if not SLUG.fullmatch(slug):
        raise ValueError("Deck filenames must use lowercase words/numbers separated by hyphens")
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Deck must start with YAML front matter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError("Unclosed YAML front matter") from None
    try:
        metadata = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML front matter: {error}") from error
    if not isinstance(metadata, dict):
        raise ValueError("Front matter must contain title, description, lang, and source")
    unknown = set(metadata) - {"title", "description", "lang", "source", "sections"}
    if unknown:
        raise ValueError(f"Unknown deck metadata: {', '.join(sorted(str(k) for k in unknown))}")
    for key in ("title", "description", "lang", "source"):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            raise ValueError(f"Front matter '{key}' must be nonempty text")
    if not LANG.fullmatch(metadata["lang"]):
        raise ValueError("Invalid deck language code")
    slides = []
    for index, chunk in enumerate(split_slides("\n".join(lines[end + 1:])), start=1):
        first, _, rest = chunk.partition("\n")
        classes = ""
        marker = SLIDE_MARKER.fullmatch(first)
        if marker:
            classes = marker[1].strip()
            if not CLASSES.fullmatch(classes):
                raise ValueError(f"Slide {index}: invalid CSS class marker")
            chunk = rest.strip()
            if not chunk:
                raise ValueError(f"Slide {index}: marker must be followed by slide content")
        elif first.startswith("<!-- slide:"):
            raise ValueError(f"Slide {index}: malformed slide marker")
        slides.append((classes, chunk))
    sections = parse_sections(metadata.pop("sections"), len(slides)) if "sections" in metadata else ()
    return Deck(slug=slug, slides=tuple(slides), sections=sections, **metadata)


def read_decks(root: Path) -> list[Deck]:
    # Supporting notes and READMEs may share this directory. Only lecture-*.md
    # is presentation source; a malformed lecture must still fail the build.
    sources = sorted((root / "slides-src").glob("lecture-*.md"))
    if not sources:
        raise ValueError(f"No slide sources found in {root / 'slides-src'}")
    decks = []
    for source in sources:
        try:
            decks.append(parse_deck(source.read_text(encoding="utf-8"), source.stem))
        except ValueError as error:
            raise ValueError(f"{source.name}: {error}") from error
    return decks


def render_deck(deck: Deck, topics: dict[str, TextbookTopic] | None = None,
                directory_urls: bool = True) -> str:
    """Repo-authored HTML is trusted; metadata is escaped for its HTML context."""
    topics = topics or {}
    validate_links([deck], topics)
    sections = []
    for number, (classes, text) in enumerate(deck.slides, start=1):
        content = markdown.markdown(
            text,
            extensions=["extra", "sane_lists", "codehilite"],
            extension_configs={"codehilite": {"css_class": "highlight", "guess_lang": False}},
            output_format="html",
        )
        section = deck.topic_for_slide(number)
        section_id = section.id if section and section.start == number else f"slide-{number}"
        attributes = {"id": section_id, "class": classes, "aria-label": f"Slide {number}",
                      "data-slide-number": str(number)}
        if section:
            topic = topics[section.textbook]
            attributes.update({
                "data-topic-id": section.id, "data-topic-title": section.title,
                "data-textbook-en": "../../../" + topic.url("en", directory_urls),
                "data-textbook-zh": "../../../" + topic.url("zh", directory_urls),
                "data-textbook-related": str(section.related).lower(),
            })
        else:
            attributes.update({"data-topic-id": "", "data-topic-title": "", "data-textbook-en": "",
                               "data-textbook-zh": "", "data-textbook-related": "false"})
        attrs = " ".join(f'{key}="{escape(value, quote=True)}"' for key, value in attributes.items())
        sections.append(f'<section {attrs}>\n{content}\n</section>')
    body = "\n".join(sections)
    textbook_control = '<a id="slides-textbook" href="../../../" target="_self">Text</a>'
    outline_control = ""
    if deck.sections:
        first = topics[deck.sections[0].textbook]
        textbook_control = (f'<a id="slides-textbook" href="../../../{escape(first.url("en", directory_urls), quote=True)}" '
                            'target="_self">Text</a>')
        entries = []
        for index, section in enumerate(deck.sections):
            end = deck.sections[index + 1].start - 1 if index + 1 < len(deck.sections) else len(deck.slides)
            numbers = str(section.start) if end == section.start else f"{section.start}–{end}"
            entries.append(f'<li data-level="{section.level}"><a href="#/{section.id}" data-start="{section.start}" '
                           f'target="_self">{escape(section.title)} <span class="slide-outline-range">{numbers}</span></a></li>')
        outline_control = ('<details class="slide-outline"><summary id="slides-contents">Contents</summary>'
                           '<nav aria-label="Lecture sections"><ol id="slides-outline">' + "".join(entries)
                           + '</ol></nav></details>')
    return f'''<!doctype html>
<html lang="{escape(deck.lang, quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(deck.description, quote=True)}">
  <meta name="referrer" content="no-referrer">
  <title>{escape(deck.title)} · Course slides</title>
  <link rel="stylesheet" href="../../assets/reveal/reveal.css">
  <link rel="stylesheet" href="../../assets/course-slides.css?v={ASSET_VERSION}">
</head>
<body data-deck-title="{escape(deck.title, quote=True)}" data-source="{escape(deck.source, quote=True)}">
  <nav class="slide-toolbar" aria-label="Slide controls">
    {textbook_control}
    <a class="slides-back" href="../../">Slides</a>
    {outline_control}
    <button type="button" id="slides-overview" title="Overview (O)">Overview</button>
    <button type="button" id="slides-fullscreen" title="Fullscreen (F)">Fullscreen</button>
    <button type="button" id="slides-reading" aria-pressed="false">Reading view</button>
  </nav>
  <div class="reveal"><div class="slides">
{body}
  </div></div>
  <script src="../../assets/reveal/reveal.js"></script>
  <script src="../../assets/course-slides.js?v={ASSET_VERSION}"></script>
</body>
</html>
'''


@event_priority(-200)
def on_files(files, config):
    # Run after mkdocs-static-i18n (-100). Its current File adapter cannot accept
    # abs_src_path=None, and English-only standalone decks should not be cloned
    # into locale folders. config.site_dir remains the common output root.
    root = Path(config.config_file_path).resolve().parent
    try:
        decks = read_decks(root)
        topics = read_registry(root)
        validate_links(decks, topics)
        for deck in decks:
            existing = files.get_file_from_path(deck.route)
            if existing:
                if existing.generated_by != GENERATOR:
                    raise ValueError(f"Generated slide route collides with {deck.route}")
                files.remove(existing)
            generated = File.generated(
                config, deck.route, content=render_deck(deck, topics, config.use_directory_urls),
                inclusion=InclusionLevel.NOT_IN_NAV,
            )
            generated.generated_by = GENERATOR
            files.append(generated)
    except ValueError as error:
        raise PluginError(f"Slide build failed: {error}") from error
    return files


@dataclass
class HeadingPosition:
    id: str
    tag: str
    start: int
    open_end: int
    close_start: int = -1


class HeadingIndex(HTMLParser):
    """Locate heading boundaries without reserializing or changing page HTML."""

    def __init__(self, content: str):
        super().__init__(convert_charrefs=False)
        self.content = content
        self.line_offsets = [0]
        for line in content.splitlines(keepends=True):
            self.line_offsets.append(self.line_offsets[-1] + len(line))
        self.headings: dict[str, list[HeadingPosition]] = {}
        self.ids: dict[str, list[tuple[str, dict, HeadingPosition | None]]] = {}
        self.generated_links: list[tuple[dict, HeadingPosition | None]] = []
        self.current: HeadingPosition | None = None
        self.feed(content)
        self.close()

    def position_in_content(self):
        line, column = self.getpos()
        return self.line_offsets[line - 1] + column

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if re.fullmatch(r"h[1-6]", tag):
            start = self.position_in_content()
            heading = HeadingPosition(attrs.get("id", ""), tag, start, start + len(self.get_starttag_text()))
            self.current = heading
            if heading.id:
                self.headings.setdefault(heading.id, []).append(heading)
        if attrs.get("id"):
            self.ids.setdefault(attrs["id"], []).append((tag, attrs, self.current))
        if tag == "a" and attrs.get("data-slides-generated") == "1":
            self.generated_links.append((attrs, self.current))

    def handle_endtag(self, tag):
        if self.current and tag == self.current.tag:
            self.current.close_start = self.position_in_content()
            self.current = None


def incoming_sections(decks: list[Deck], topic_id: str):
    """One incoming textbook link per deck/topic, at the earliest direct section."""
    for deck in decks:
        section = next((s for s in deck.sections if s.textbook == topic_id and not s.related), None)
        if section:
            yield deck, section


def textbook_to_deck_url(page_url: str, deck: Deck, section: DeckSection, language: str) -> str:
    target = deck.route.removesuffix("index.html").rstrip("/")
    start = posixpath.dirname(page_url) or "."
    relative = posixpath.relpath(target, start=start)
    return relative + "/?lang=" + quote(language) + "#/" + section.id


def inject_textbook_links(content: str, *, page_source: str, page_url: str,
                          language: str, decks: list[Deck], topics: dict[str, TextbookTopic]) -> str:
    selected = [topic for topic in topics.values() if topic.source_page(language) == page_source]
    if not selected:
        return content
    index = HeadingIndex(content)
    edits: dict[int, list[str]] = {}
    for topic in selected:
        original_id = topic.headings[language]
        matches = index.headings.get(original_id, [])
        if len(matches) != 1 or len(index.ids.get(original_id, [])) != 1:
            raise ValueError(f"{page_source}: expected one heading #{original_id} for {topic.id}")
        heading = matches[0]
        if heading.close_start < 0:
            raise ValueError(f"{page_source}: unclosed heading #{original_id}")
        existing_alias = index.ids.get(topic.alias, [])
        if existing_alias:
            if (len(existing_alias) != 1 or existing_alias[0][0] != "span"
                    or existing_alias[0][1].get("data-slides-generated") != "1"
                    or existing_alias[0][2] is not heading):
                raise ValueError(f"{page_source}: alias collision #{topic.alias}")
        else:
            alias = (f'<span id="{topic.alias}" class="textbook-topic-anchor" '
                     'aria-hidden="true" data-slides-generated="1"></span>')
            edits.setdefault(heading.open_end, []).append(alias)
        for deck, section in incoming_sections(decks, topic.id):
            href = textbook_to_deck_url(page_url, deck, section, language)
            existing_links = [(attrs, parent) for attrs, parent in index.generated_links
                              if attrs.get("data-slide-deck") == deck.slug and attrs.get("data-slide-topic") == topic.id]
            if existing_links:
                if (len(existing_links) != 1 or existing_links[0][1] is not heading
                        or existing_links[0][0].get("href") != href):
                    raise ValueError(f"{page_source}: conflicting generated slide link for {topic.id}")
                continue
            label = "课件" if language == "zh" else "Slides"
            title = deck.title + " · " + section.title
            link = (f' <a class="textbook-slides-link" href="{escape(href, quote=True)}" target="_self" data-search-exclude="" '
                    f'title="{escape(title, quote=True)}" aria-label="{escape(label + ": " + title, quote=True)}" '
                    f'data-slide-deck="{deck.slug}" data-slide-topic="{topic.id}" data-slides-generated="1">{label}</a>')
            edits.setdefault(heading.close_start, []).append(link)
    for position in sorted(edits, reverse=True):
        content = content[:position] + "".join(edits[position]) + content[position:]
    return content


def on_page_content(html, page, config, files):
    # ToC nodes and their existing heading ids have already been created. Insert
    # small sibling elements inside headings without changing that ToC model.
    root = Path(config.config_file_path).resolve().parent
    try:
        topics = read_registry(root)
        source = page.file.src_uri
        # i18n uses English source files for untranslated pages in the Chinese
        # build. Follow the build locale, not only the filename suffix.
        language = "zh" if source.endswith(".zh.md") or config.theme.get("language") == "zh" else "en"
        if not any(topic.source_page(language) == source for topic in topics.values()):
            return html
        decks = read_decks(root)
        validate_links(decks, topics)
        return inject_textbook_links(html, page_source=source, page_url=page.file.url,
                                     language=language, decks=decks, topics=topics)
    except ValueError as error:
        raise PluginError(f"Textbook slide links failed: {error}") from error


def on_serve(server, config, builder):
    # MkDocs already watches docs/ and mkdocs.yml; slide sources live beside them.
    server.watch(str(Path(config.config_file_path).resolve().parent / "slides-src"))
    return server
