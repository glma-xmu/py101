# How to put this course site online (GitHub Pages)

This guide takes you from the folder on your computer to a live website at:

> **https://glma-xmu.github.io/py101/**

You only do Steps 1–3 **once**. After that, updating the site is just "commit and
push" (Step 5).

Everything technical is already prepared for you:
- the build recipe (`.github/workflows/deploy.yml`) — GitHub will build the site
  automatically; you never run any build command yourself;
- the address (`site_url` in `mkdocs.yml`) is already set to the URL above.

> ⚠️ **Name the repository exactly `py101`.** The site address has `py101` baked in.
> If you want a different name, tell me first and I'll change one line, otherwise
> the page will load without its styling.

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

The result is a plain folder of HTML — no Python needed on the server. Tell me when
you're ready and I'll write the exact server steps (and a one-command sync script).

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
