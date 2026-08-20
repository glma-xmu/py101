# How to put this course site online

The course has **one address you give to students**:

> **https://www.maguoliang.com/teaching/py101/**

and one behind it that always works as a fallback and is where the site is
actually built:

> **https://glma-xmu.github.io/py101/**

Steps 1–3 set up the GitHub Pages build; **Step 7** is what puts it under
`maguoliang.com`. You only do each **once**. After that, updating the site is just
"commit and push" (Step 5) — both addresses refresh on their own.

Everything technical is already prepared for you:
- the build recipe (`.github/workflows/deploy.yml`) — GitHub will build the site
  automatically; you never run any build command yourself;
- the address (`site_url` in `mkdocs.yml`) is already set to the `maguoliang.com`
  URL above.

> ⚠️ **Name the repository exactly `py101`.** Both addresses have `py101` baked in
> — the GitHub Pages one because that is how project sites work, and the
> `maguoliang.com` one because the personal site's workflow checks this repo out
> by name. If you want a different name, tell me first and I'll change the three
> places it appears, otherwise the page will load without its styling.

---

## Step 1 — Create the repository on GitHub

1. Go to <https://github.com> and sign in as **glma-xmu**.
2. Top-right **+** → **New repository**.
3. Fill in:
   - **Repository name:** `py101`
   - **Public** (leave it Public — Pages is free and simplest for public repos)
   - **Do NOT** check "Add a README", ".gitignore", or "license" (we already have files).
4. Click **Create repository**.

You'll land on a page that says "…quick setup". Leave it open; you'll need it.

---

## Step 2 — Upload the files

Pick **one** of the two methods. **Method A (GitHub Desktop) is the easiest** and
handles the login for you.

### Method A — GitHub Desktop (recommended)

1. Install **GitHub Desktop** from <https://desktop.github.com> and open it.
2. Sign in: **File → Options → Accounts → Sign in** (use your glma-xmu account).
3. **File → Add local repository…**
4. Browse to this folder and choose it:
   `D:\Dropbox\other\AI赋能\py101-main\py101-clean`
5. It will say *"This directory does not appear to be a Git repository — would you
   like to create one here?"* → click **create a repository** (keep branch = `main`).
6. GitHub Desktop now lists hundreds of files as changes. At the bottom-left, type a
   summary like `Initial course site`, then click **Commit to main**.
7. Click **Publish repository** at the top. In the dialog:
   - **Name:** `py101`
   - **Uncheck** "Keep this code private"
   - Click **Publish repository**.

This creates the repo on GitHub and uploads everything. (If you already created the
repo in Step 1, Desktop may say the name exists — just delete the empty one on
github.com, or skip Step 1 entirely and let "Publish" create it.)

### Method B — Command line (if you prefer typing)

1. Make sure **Git** is installed (<https://git-scm.com>).
2. Open **Git Bash** (or PowerShell) and run, line by line:

   ```bash
   cd "D:/Dropbox/other/AI赋能/py101-main/py101-clean"
   git init
   git add .
   git commit -m "Initial course site"
   git branch -M main
   git remote add origin https://github.com/glma-xmu/py101.git
   git push -u origin main
   ```

3. When it asks you to log in: a browser window usually opens — sign in and approve.
   If instead it asks for a **username/password** in the terminal:
   - username = `glma-xmu`
   - password = a **Personal Access Token** (NOT your GitHub password). Make one at
     github.com → **Settings → Developer settings → Personal access tokens → Tokens
     (classic) → Generate new token**, tick the **repo** scope, copy the token, and
     paste it as the password.

---

## Step 3 — Turn on GitHub Pages

1. Go to your repo: <https://github.com/glma-xmu/py101>
2. Click **Settings** (top menu of the repo).
3. In the left sidebar, click **Pages**.
4. Under **Build and deployment → Source**, choose **GitHub Actions**.
   - That's all — no branch to pick. (The build recipe is already in your repo.)

---

## Step 4 — Watch it build, then open your site

1. Click the **Actions** tab (top menu of the repo).
2. You'll see a run called **"Deploy course site to GitHub Pages"**.
   - 🟡 yellow dot = building (takes about 2–4 minutes)
   - ✅ green check = done
   - ❌ red cross = something failed — see *Troubleshooting* below.
   - *If the very first run failed because Pages wasn't on yet:* after Step 3, open
     the latest run and click **Re-run all jobs**.
3. When it's green, go back to **Settings → Pages**. It will show:
   *"Your site is live at https://glma-xmu.github.io/py101/"* → click **Visit site**.

Quick checks on the live site:
- the homepage and a chapter page load;
- press **Run** on a code cell (the first run downloads Python, ~15 MB — give it a
  moment), and it prints output;
- the **language switch** in the top bar flips between English and 中文.

---

## Step 5 — Updating the site later (you'll do this often)

You never touch the build. To publish changes:

- **GitHub Desktop:** make your edits → it shows the changes → type a summary →
  **Commit to main** → **Push origin**. The site rebuilds automatically in ~2 min.
- **Command line:**
  ```bash
  git add .
  git commit -m "describe what you changed"
  git push
  ```

Every push triggers a fresh build and deploy. Refresh the site after a couple of minutes.

---

## Step 6 (optional but recommended) — a fast mirror for students in China

`github.io` can be slow or intermittently blocked on the mainland. GitHub Pages is
perfect as your master copy, but for reliable student access, also serve the **same
built files** from a domestic machine (your course Linux server, or campus hosting):

1. Build the static site once (on any computer with Python):
   `pip install -r requirements.txt && mkdocs build` → this creates a `site/` folder.
2. Copy the contents of `site/` into your server's web root (e.g. nginx's
   `/var/www/html/py101/`).

The result is a plain folder of HTML — no Python needed on the server. The exact
server steps are in `SERVER_DEPLOY.md`, and the CI already rsyncs each build there
once the `SERVER_*` secrets are set (see `CI_MIRROR_SETUP.md`).

---

## Step 7 — Serve it under www.maguoliang.com/teaching/py101/

This is what makes the course live on your own domain instead of a github.io
address. You do it **once**.

> ⚠️ **Push this repo first.** The personal site builds the course by downloading
> `glma-xmu/py101` **from GitHub**, not from your computer. So commit and push your
> local changes (Step 5) *before* doing 7a — otherwise it will build whatever
> version is currently on GitHub, which still has the old address baked in and
> would give you a broken 中文 switch at the new URL.

### Why it works the way it does

`maguoliang.com` is already GitHub Pages: the apex resolves to GitHub's Pages IPs
and redirects to `www`, which is served by your **`glma-xmu/personal-website`**
repo. That repo publishes with GitHub Actions, uploading its `my-new-website/`
folder as the Pages artifact.

GitHub Pages gives any one repository either a domain root or exactly **one** path
segment — `<domain>/<reponame>`. There is no setting that puts this repo at
`/teaching/py101/`. The only way to that URL is for the files to be *inside* the
personal site's published folder.

They must not be *committed* there, though: one build is about **58 MB** (the
Pyodide runtime plus the vendored numpy and pandas wheels), so committing it on
every push would grow that repo's history without limit. Instead the personal
site's workflow **builds this repo at deploy time** and nests the result. Both
repositories stay exactly as small as their sources.

### 7a — Give the personal site a new build recipe

Your personal site already has a build recipe: a file in the
`glma-xmu/personal-website` repository at `.github/workflows/static.yml`. It says
"publish the `my-new-website` folder."

We need it to say "…and before you do, build the course and put it in
`my-new-website/teaching/py101/`." I have written that new recipe for you. It sits
in **this** project folder at `.github/personal-website-static.yml`.

"Copying one file over the other" just means: **take the text out of my file, and
paste it into GitHub's file, replacing what was there.** You do it in a web
browser — nothing to install, nothing to clone.

**Part 1 — copy my text**

1. In this project folder, open `.github/personal-website-static.yml`. Any text
   editor will do — VS Code, or right-click → *Open with* → *Notepad*.
2. Click once inside the text, press **Ctrl+A** (selects everything), then
   **Ctrl+C** (copies it).
3. Close the file without saving.

**Part 2 — paste it into GitHub**

4. In your browser, go to:
   <https://github.com/glma-xmu/personal-website/blob/main/.github/workflows/static.yml>
5. Above the file's text, on the right, there is a row of small icons. Click the
   **pencil ✏️** (its tooltip says *Edit this file*).
6. Click once inside the text, press **Ctrl+A**, then **Ctrl+V**. All the old text
   is replaced by mine. (Don't worry — GitHub keeps the old version in the
   repository's history, so nothing is lost.)
7. Top right, click the green **Commit changes…** button.
8. A box appears. Leave everything as it is — in particular leave
   *Commit directly to the `main` branch* selected — and click the green
   **Commit changes** button.

**Part 3 — watch it publish**

9. Click the **Actions** tab at the top of the `personal-website` repository.
10. A run named *Deploy static content to Pages* appears with a 🟡 yellow dot.
    Wait for it to turn into a green ✅ — about 2–3 minutes, because it is now
    building the course too.
11. Open <https://www.maguoliang.com/teaching/py101/>.

Check three things on the live page: a chapter page opens, a code cell prints
output when you press **Run**, and the **中文** switch in the top bar works from
the front page.

> If the run shows a red ❌, click it, then click the failing step to see the red
> lines, and send them to me.

### 7b (optional) — make course updates publish themselves

After 7a the course is live. This step only changes **how quickly a course update
shows up** on `maguoliang.com`.

You have three ways to publish a course update, and you can stop at whichever you
like:

| | What you do | How fast |
|---|---|---|
| **Do nothing** | Just push to `py101` as usual (Step 5) | Within a day — the recipe rebuilds itself every night |
| **Press a button** | `personal-website` → **Actions** tab → *Deploy static content to Pages* → **Run workflow** → **Run workflow** | ~2 minutes, whenever you want |
| **Set up a token** | The steps below, **once** | Automatic, ~2 minutes after every push |

`glma-xmu.github.io/py101/` always updates within ~2 minutes regardless, so you
are never without a current copy to show students.

#### What a PAT is, and why one is needed

**PAT** stands for **Personal Access Token**. It is a long password-like string —
it looks like `github_pat_11ABC...` — that stands in for your GitHub password when
a *program* rather than a person needs to do something on your behalf.

Here is why one is needed. When GitHub runs the recipe in your `py101` repository,
it hands that recipe a temporary automatic password. But that password only works
on **`py101` itself**. Our recipe needs to reach *out* and tap `personal-website`
on the shoulder — "the course changed, please rebuild" — and it has no permission
to do that. A PAT is how you grant exactly that one permission, and nothing more.

#### Creating the token

1. Go to <https://github.com/settings/personal-access-tokens> and sign in.
   (The long way round: click your **profile picture**, top right → **Settings** →
   scroll to the very bottom of the left sidebar → **Developer settings** →
   **Personal access tokens** → **Fine-grained tokens**.)
2. Click **Generate new token**. You may be asked for your password or a 2FA code.
3. **Token name:** type `py101 to personal-website` — this is just a label for you.
4. **Expiration:** pick **90 days**, or **Custom** and a date about a year out.
   Whatever you choose, the day it expires nothing breaks — updates simply fall
   back to the nightly rebuild in the table above.
5. **Resource owner:** leave it as your own account, **glma-xmu**.
6. **Repository access:** choose **Only select repositories**. A box appears —
   click it and pick **personal-website**. ⚠️ *Not* `py101`. The token is for
   reaching the personal site.
7. **Permissions** → find the **Repository permissions** section and expand it.
   Scroll down the list to **Contents** and change its dropdown from *No access*
   to **Read and write**.
   - *Metadata* will tick itself as *Read-only* and grey out. That is normal —
     GitHub requires it. Leave everything else on *No access*.
8. Scroll to the bottom and click **Generate token**.
9. GitHub now shows the token once, in a box with a copy icon. **Click the copy
   icon.** You cannot see it again after leaving this page — if you lose it, just
   delete the token and make another.

#### Storing it in the course repository

10. Go to <https://github.com/glma-xmu/py101/settings/secrets/actions>.
    (The long way round: the `py101` repo → **Settings** tab → in the left
    sidebar, **Secrets and variables** → **Actions**.)
11. Click the green **New repository secret** button.
12. **Name:** type `PERSONAL_SITE_TOKEN` — exactly this, capitals and underscores
    included. The recipe looks for it by this name.
13. **Secret:** paste the token (**Ctrl+V**).
14. Click **Add secret**.

Done. GitHub now hides the value from everyone, including you — it can be replaced
but never read back. From here on, every push to `py101` builds the site, publishes
it to GitHub Pages, and asks the personal site to rebuild.

> **When the token expires,** the only symptom is that `maguoliang.com` stops
> picking up course updates while `github.io` keeps working — the step is
> deliberately non-blocking, so your build still goes green rather than failing.
> If the personal site ever looks out of date, look at the **Rebuild the personal
> site** step in the latest `py101` Actions run: it will say what happened. Make a
> fresh token and update the secret the same way.

### What each address is for

| Address | Role |
|---|---|
| `www.maguoliang.com/teaching/py101/` | **Give this to students.** Canonical; what search engines index. |
| `glma-xmu.github.io/py101/` | Always-on fallback, and where the build actually happens. |
| `maguoliang.cn` | The in-China mirror from Step 6. |

All three serve the identical build. `docs/javascripts/lang-switch-fix.js` fixes
the one thing that would otherwise differ between them — the homepage language
switcher, whose links MkDocs writes as absolute paths derived from `site_url`.

---

## Troubleshooting — what to send me

If anything goes wrong, copy the details and send them over:

- **The Actions run shows a red ❌:** click the run → click the **build** job →
  scroll to the red lines → copy them here.
- **Site loads but looks plain / pictures and styling missing, or assets 404:**
  usually the repo name doesn't match `py101`. Tell me the exact repo name and I'll
  fix `site_url`.
- **A page is blank or 404:** send me the page's URL.
- **Code cells won't run:** press **F12** in the browser, open the **Console** tab,
  and send any red error text.

Don't worry about breaking anything — every deploy is just a rebuild, and we can
always push a fix.
