# Python and Big Data in Economics — Course Site

Clean, static, bilingual (English / 中文) course website built with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/). It deploys to
GitHub Pages automatically and requires **no backend servers**.

## Edit content

All course content lives in `docs/`:

- `docs/index.md` / `docs/index.zh.md` — the homepage (English / Chinese)
- `docs/py101_md/` — chapter pages. Each page has three files:
  - `slide_1_1.md`  → English (default)
  - `slide_1_1.zh.md` → Chinese translation
- Navigation and chapter titles are defined in `mkdocs.yml` under `nav:`

To add or rename a chapter, edit the Markdown file and update `nav:` in `mkdocs.yml`.

### Left navigation

Chapter/group titles open their first section; the separate arrow expands or
collapses the section list. On desktop, Chapters 1–3 start expanded. Exercises, Appendix, and
Two-Day Crash Course start collapsed unless they contain the current page.
This works in English and Chinese. The mobile menu retains Material's nested
drawer navigation, with the same separate title links and arrow controls.

`overrides/partials/nav.html` customizes only the top-level groups and delegates
page entries to Material's standard template. The collapsed groups are listed
in `extra.course_navigation.collapsed_first_pages` in `mkdocs.yml`, using their
first page's filename without `.md` or a language suffix. No page URLs change.
After building, run `python scripts/check_navigation.py site` to check the links
and initial expansion states in both languages.

## Lecture slides

The header's slideshow icon (tooltip: **Browse lecture slides / 浏览课堂课件**) opens a separate slide library. Slides
do not appear in the textbook sidebar or search results. The first pilot is
Lecture 1.1, converted from `resource/deck1_1_AoL.pptx` into 23 editable HTML
slides, with the original diagrams and exercises.

- Edit `slides-src/lecture-1-1.md`; a line containing only `---` starts the next
  slide. The initial YAML block provides the title, description, and language.
  Additional decks use `lecture-*.md` filenames and need a card in both slide
  library pages; supporting notes in this folder are not turned into slides.
- Each deck's optional `sections` list provides stable named destinations and
  a Contents outline. A section has `id`, `title`, `start` (one-based slide
  number), `level` (1–3), and a `textbook` topic key. Keep IDs stable when adding
  slides, and update the start numbers. No divider slides are added.
- `slides-src/textbook-links.yml` maps shared topic keys to an English source
  page and its existing EN/ZH heading IDs. The build adds stable
  `textbook-<topic-key>` aliases without changing old heading URLs or ToC entries.
  Matching textbook headings get a Slides link to the first matching section
  in each deck. In the player, Textbook follows the current slide or reading
  position and preserves the textbook language through `?lang=zh`.
- Use `related: true` for broader reading when there is no exact counterpart.
  This labels the player link Related reading and does not advertise an exact
  slide match on the textbook heading. The pilot uses it for array/deque.
- `scripts/build_slides.py` runs as a MkDocs hook. Normal `mkdocs build` and
  `mkdocs serve` generate the deck; no PowerPoint, Node, or online conversion
  service is needed for deployment.
- The deck is at `slides/decks/lecture-1-1/` under whichever site prefix serves
  the course. The player and its fonts/assets require no external CDN.
- Use arrow keys / Space to advance, Esc for the overview, and F for full screen
  where the browser permits it. Reading mode works well in a narrow VS Code
  browser panel. Code blocks can be copied into your adjacent `.ipynb` notebook;
  these slides do not execute code or save classroom notes.
- Keep saving the notebook in VS Code as before. Nothing in this pilot changes
  notebook storage or publishes your in-class notes automatically.
- Original PPTX/PDF files remain in the ignored `resource/` folder. See
  `slides-src/conversion-notes.md` for the small source corrections in this pilot.

After building, run `python scripts/check_slides.py site` and
`python scripts/check_navigation.py site`. Commit the Markdown, hook, library,
player assets, and images; do not commit generated `site/` files. Existing
deployment builds pick up the slides with the rest of the site.

## Student project gallery

The gallery icon beside the slideshow icon opens `/projects/` (or
`/zh/projects/`). Cards show the original cover, project title, cohort and slide
count. Cohort filters and a keyboard-accessible dialog let visitors browse slides
with Previous/Next, arrow keys, Home/End and Escape. The interface follows the
site language; student presentations retain their original language and layouts.

Only compressed WebP previews and `docs/projects/manifest.json` are published.
The source PPTX/PDF files stay in ignored `resource/projects/`; no original deck
URLs or download controls are included. This prevents access to the originals
through the site, but is not DRM: visitors can still save preview images or take
screenshots. Previews are static and do not play embedded video or animations.

To regenerate locally, run `powershell -File scripts/export_project_slides.ps1`
with Microsoft PowerPoint and Poppler (`pdftoppm`) available, then run
`python scripts/build_project_previews.py` with Pillow installed. Intermediate
PNGs and source metadata stay under `resource/projects/.previews/`. Review titles
in `scripts/project_titles.json` and `scripts/build_project_previews.py`, inspect
the private contact sheet, and commit the gallery assets. Normal CI builds only
copy the prepared previews; PowerPoint is not required on the deployment server.
Run `python scripts/check_projects.py site` after building to check gallery
coverage, preview assets, both languages, and the absence of original decks.
If replacing a source, delete its cached preview folder before rendering again.
Keep existing source filenames stable when updating the library.

The initial import contains 25 readable presentations (2025/2026 spring).
`resource/projects/26S/Group 8.pptx` has an invalid all-zero header and PowerPoint
cannot open it; replace it with a working file before adding its preview. The
presentation advice and grading criteria at the projects folder root are not
student submissions and are not included in the gallery.

## Preview locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open http://127.0.0.1:8000 — the EN site is at `/`, the Chinese site at `/zh/`.

## Deploy

The live site: **<https://www.maguoliang.com/teaching/py101/>**

1. Create a new GitHub repo (e.g. `py101`) and push this folder to the `main` branch.
2. In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Open `mkdocs.yml` and set `site_url` to the address students will use.
4. Push. The included workflow (`.github/workflows/deploy.yml`) builds and
   publishes the site on every push. You only ever edit Markdown.

The same build is served from three places — the personal site (canonical),
GitHub Pages (fallback and where it is built), and an Aliyun mirror. Full
instructions are in `DEPLOY.md`; the server side is in `SERVER_DEPLOY.md`.

## What was intentionally left out

The original project shipped with three features that need live backend servers
and therefore **cannot run on GitHub Pages** as-is:

- **AI chat tutor** (`chat.js` + a Flask/Gemini backend)
- **Auto-grading** (`grading.js`)
- **Real-time translation** (`translation-button.js` + a Node server — its engine
  files were already missing from the source repo)

These were removed so the static site is clean and reliable. They can be re-added
later by hosting the backend on a serverless function and pointing the frontend at it.

## Live lecture translation (recommended approach)

For helping students follow English lectures in real time, use a dedicated
classroom translation service (e.g. Wordly, Microsoft Translator for Education,
or Zoom translated captions) rather than building it into this site. Students
join on their phones and read live captions in their chosen language. Just put
the join link on the site.

## Offline / GFW-safe assets

To avoid depending on foreign CDNs (which can be slow or blocked in some
networks), the front-end libraries are vendored into `docs/vendor/` and served
from the site itself:

- `docs/vendor/codemirror/` — the code editor (loaded by `runnable.js`)
- `docs/vendor/katex/` — math rendering, including `fonts/`
- `docs/vendor/pyodide/` — the Pyodide **core** runtime (~14 MB: `pyodide.js`,
  `pyodide.asm.wasm`, `pyodide.asm.js`, `python_stdlib.zip`, `pyodide-lock.json`)

With these in place, plain-Python runnable cells work entirely from your own
domain — no external requests.

### On-demand packages (numpy / pandas / matplotlib)

The Pyodide *core* runs pure Python. Importing a third-party package downloads
its wheel from `PYODIDE_BASE` (set in `docs/javascripts/runnable.js`). The wheels
are **not** vendored by default (they are large). You have two options when a
chapter's runnable cell needs one:

1. **Vendor the wheel:** download the matching wheel for Pyodide 0.27.x (e.g.
   `numpy-*.whl`) into `docs/vendor/pyodide/` — it is listed in
   `pyodide-lock.json`. Then it loads locally like the core.
2. **Point `PYODIDE_BASE` at a server you control** (e.g. the course Linux
   server) that hosts the full Pyodide distribution including wheels. Change the
   one constant in `runnable.js`; serve with CORS enabled if it is a different
   origin from the site.

To update versions, re-fetch with `npm install pyodide@<v> codemirror@5 katex@<v>`
and copy the files into `docs/vendor/` (see the project history for the exact
file list).
