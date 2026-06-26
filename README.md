# AI Programming in Python — Course Site

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

## Preview locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open http://127.0.0.1:8000 — the EN site is at `/`, the Chinese site at `/zh/`.

## Deploy to GitHub Pages

1. Create a new GitHub repo (e.g. `py101`) and push this folder to the `main` branch.
2. In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Open `mkdocs.yml` and set `site_url` to your real URL, e.g.
   `https://YOURNAME.github.io/py101/`.
4. Push. The included workflow (`.github/workflows/deploy.yml`) builds and
   publishes the site on every push. You only ever edit Markdown.

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
