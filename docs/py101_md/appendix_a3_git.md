# A3. Version Control with Git

```motto
Nothing is lost once it is committed.
```

## Introduction

You have a Python of your own (A1) and you can find your way around your files (A2). This last appendix adds the habit that protects both: **version control**, the practice of recording your project's history so that you can see what changed, when, and why — and go back if you need to.

Almost everything written about Git assumes a team: branches, pull requests, merge conflicts, code review. That is not what this page is for. Here you are one person working on your own project, and in that setting Git does three things that matter immediately. It replaces the folder full of `analysis_v2_final_REALLY.py` with one file that has a history. It lets you experiment recklessly, because a bad afternoon is one command away from being undone. And it lets you say exactly which version of your code produced a given number — which, in economics, is the difference between a result someone can check and a result they have to take on faith.

Everything below is the small subset you will actually use alone. The commands are identical on Windows and macOS. §8 names what has been left out and when you would go looking for it.

One honest warning: this is the appendix whose value is invisible until the day it saves you. The habit takes a week to build and pays for itself the first time you delete the wrong thing.

## 1. Installing Git and telling it who you are

On Windows, install **Git for Windows** from [git-scm.com](https://git-scm.com/download/win) and accept the defaults; it also gives you Git Bash, the POSIX shell mentioned in A2 §8. On macOS, running `git --version` will offer to install the Xcode command line tools, which is the easiest route.

Confirm it worked, in a new terminal:

```bash
git --version
```

Now identify yourself. Every commit is stamped with a name and an email address, so Git refuses to record anything until it knows them:

```bash
git config --global user.name "Your Name"
```

```bash
git config --global user.email "you@university.edu"
```

While you are here, make new repositories start on a branch called `main`, which is the modern default and what GitHub expects:

```bash
git config --global init.defaultBranch main
```

`--global` means "for every project on this machine", so this is a once-per-computer setup.

???+ warning "Pitfall: this is not a login"
    `user.name` and `user.email` are not an account, a password, or a GitHub sign-in.
    They are just text that Git writes into each commit to record authorship — you
    could put anything there, and Git would believe you. Signing in to GitHub is a
    separate thing, and it only matters in §7 when you push. Use the email you would
    want attached to your work.

## 2. What Git actually tracks: three places

Nearly every confusion about Git comes from not knowing which of three places a file is in. Learn this once and the commands stop feeling arbitrary.

```text
   working tree            staging area              repository
   (your folder)             (the index)           (committed history)

   you edit files   --->   git add   --->   git commit   --->   permanent
                                                                 snapshots
```

The **working tree** is your project folder as you see it in Explorer or Finder — the current state of your files, including edits you have not recorded. The **staging area**, also called the index, is a waiting room: files you have marked as belonging in the *next* snapshot. The **repository** is the permanent history, a chain of snapshots called **commits**, stored in the hidden `.git` folder.

So `git add` moves a change from the working tree to the staging area, and `git commit` turns everything in the staging area into a permanent snapshot. The staging area is what lets you commit *some* of your changes and not others — you fixed a bug and adjusted a chart, and you would rather record them separately.

???+ note "Key concept: working tree, staging area, repository"
    A file's changes live in one of three places. The **working tree** is your folder
    as it is right now, edits included. The **staging area** (or *index*) holds the
    changes you have marked for the next snapshot. The **repository** is the recorded
    history. `git add` moves a change one step right; `git commit` moves it the last
    step. Almost every Git command — and every row of the undo table in §6 — is
    named by which of these three it acts on.

???+ note "Key concept: commit"
    A **commit** is a permanent, complete snapshot of your project at one moment,
    together with a message saying what changed and who made it. Each commit has a
    unique identifier (a **hash**, like `a3f9c21`) and points back to the one before
    it, so the commits form a history you can read and return to. Committing never
    overwrites an earlier commit; it adds to the chain.

## 3. Starting a repository

Move into your project folder — the one A1 had you create — and turn it into a repository:

```bash
cd C:\dev\py101
```

```bash
git init
```

That creates a hidden `.git` folder holding the entire history. Deleting it deletes your history, so leave it alone; everything you need is done through commands, never by editing files in there.

The single most useful command in Git is:

```bash
git status
```

Run it constantly. It tells you which branch you are on, what has changed, what is staged, and — helpfully — what command to run next. When you are confused, `git status` is the answer.

???+ warning "Pitfall: don't `git init` in the wrong place"
    Run `git init` in your *project* folder, not in your home folder or your Desktop.
    A repository created at `C:\Users\yourname` will try to track every file you own,
    which is slow and unmanageable. And never create a repository inside another
    repository — if `git status` mentions files you have never heard of, you are
    probably nested inside one. Check with `git status` before you `git init`, and
    if you make a mistake, delete the `.git` folder and start again.

## 4. Decide what *not* to track, before your first commit

Not everything in a project folder belongs in its history. A file listed in **`.gitignore`** is invisible to Git — never staged, never committed, never mentioned by `git status`.

Four kinds of thing belong there. **Virtual environments** (`.venv/`) are large and machine-specific, and A1 already gave you the better way to record them: `requirements.txt`. **Generated files** like `__pycache__/` are rebuilt automatically. **Large data files** bloat a repository permanently. And **secrets** — API keys, passwords, tokens — must never be committed at all.

Create a file called `.gitignore` in your project root:

```text
# Environments
.venv/
venv/

# Python bytecode
__pycache__/
*.pyc

# Notebook checkpoints
.ipynb_checkpoints/

# Secrets — never commit these
.env
*.key

# Data (keep raw data out; adjust to taste)
data/raw/

# OS clutter
.DS_Store
Thumbs.db
```

???+ warning "Pitfall: a committed secret is committed forever"
    In Part 3 of this course you will be given an API key. If you commit it, removing
    it later does **not** help: the key remains readable in the earlier commit, and on
    a public repository it will be found by automated scanners within minutes. The
    only real fix is to revoke the key and issue a new one.

    So write `.gitignore` *before* your first commit, keep keys in a `.env` file that
    is ignored, and never paste a key directly into a `.py` file.

???+ warning "Pitfall: `.gitignore` does not untrack what Git already tracks"
    `.gitignore` only stops Git noticing files it is not *already* tracking. Adding a
    file to `.gitignore` after committing it changes nothing — Git keeps tracking it.
    To stop tracking a file while keeping it on disk:

    ```bash
    git rm --cached secrets.env
    ```

    Then commit that change. This is a common surprise, and it is the reason
    `.gitignore` is written early rather than late.

## 5. The everyday loop

With a `.gitignore` in place, the whole of solo Git is four commands in a cycle. You will run this loop several times a day.

**See what changed.** `git status` lists which files differ; `git diff` shows the actual lines, additions marked `+` and removals `-`:

```bash
git status
```

```bash
git diff
```

**Stage what belongs together.** Name specific files, or use `.` for everything that is not ignored:

```bash
git add analysis.py requirements.txt
```

**Record the snapshot**, with a message:

```bash
git commit -m "Add GDP per capita cleaning step"
```

**Read the history back:**

```bash
git log --oneline
```

which prints one line per commit, newest first:

```text
a3f9c21 Add GDP per capita cleaning step
7b21e04 Load prices.csv and print summary statistics
e10f8aa Initial commit: project skeleton and .gitignore
```

A note on messages, because future-you is the one who reads them. Write what the commit *does*, in the imperative — "Add rolling volatility", "Fix off-by-one in resample" — not "changes" or "update" or "asdf". A good rule: the message should complete the sentence "If applied, this commit will…". Explaining *why* matters more than *what*, since the diff already shows what.

How often? Commit whenever you reach a point you would be annoyed to lose, and whenever the change has a name. A commit that touches one idea is easy to understand and easy to undo; a commit containing a whole day's work is neither.

```recall
Nothing is lost once it is committed: everything in §6 is possible only for work
that reached the repository. Uncommitted edits have no history to return to.
```

??? info "Deep dive: seeing more of the history"
    Four variations on `git log` earn their keep once a project has some history:

    ```bash
    git log --oneline --stat      # which files changed, and by how many lines
    git log -p analysis.py        # every change ever made to one file, with diffs
    git show a3f9c21              # one commit in full
    git diff --staged             # what is staged but not yet committed
    ```

    The last one closes a gap in §5: plain `git diff` shows working tree versus
    staging area, so once you have run `git add`, your changes seem to vanish from
    `git diff`. They are in the staging area, and `git diff --staged` is where to
    look for them.

## 6. Undoing things

This is the section you will come back to, so it is written as a lookup table. The right command depends entirely on how far along the change is — which is the practical reason §2 was worth learning.

| What you want | Command | Notes |
|---|---|---|
| Discard edits to a file, not yet staged | `git restore analysis.py` | Permanent — the edits are gone |
| Unstage a file, keep the edits | `git restore --staged analysis.py` | The reverse of `git add` |
| Fix the last commit's message | `git commit --amend -m "Better message"` | Replaces the last commit |
| Add a forgotten file to the last commit | `git add forgotten.py` then `git commit --amend --no-edit` | Same idea |
| Undo an old commit, safely | `git revert a3f9c21` | Makes a *new* commit that reverses it |
| Move history back, keep the files | `git reset --mixed a3f9c21` | Commits after this one are undone, edits stay |
| Move history back, discard everything | `git reset --hard a3f9c21` | Dangerous — see below |
| Recover from a mistake | `git reflog` | Your safety net |

Two of these deserve more than a table row.

**`git revert` is the safe way to undo an old commit.** It does not delete anything; it writes a new commit that applies the opposite changes. Your history keeps a record that the mistake happened and was reversed, which is exactly what you want in work that has to be reproducible.

**`git reflog` is the safety net almost nobody knows about.** Git records every position your branch has occupied, even ones no longer reachable through `git log`. So when you reset too far and your commits appear to have vanished, `git reflog` lists where you have been, and `git reset --hard` back to that entry restores them. Commits are essentially never destroyed until weeks later, which is the deepest reason to commit often: committed work can almost always be recovered, and uncommitted work cannot.

???+ warning "Pitfall: `git reset --hard` discards uncommitted work with no warning"
    `--hard` throws away every uncommitted change in your working tree, silently and
    permanently. `git reflog` can rescue lost *commits*, but nothing can rescue edits
    that were never committed. Before any `--hard`, run `git status` and read it.
    If in doubt, commit first — a commit you no longer want is easy to undo, and
    an hour of lost work is not.

## 7. Marking versions, and keeping a copy elsewhere

Two finishing touches make the history useful beyond your own laptop.

A **tag** is a permanent, readable name for one commit — far easier to find later than a hash:

```bash
git tag -a midterm -m "Version submitted for the midterm"
```

Now `git show midterm` retrieves exactly the code that produced your submitted results, however much the project has moved on. For coursework, tagging what you hand in costs one command and settles any later question about what you actually submitted.

Everything so far lives in one folder on one computer, so a dead laptop still loses the lot. Pushing to **GitHub** fixes that, and it stays a single-person workflow: a backup that happens to live on someone else's server.

Create an empty repository on GitHub, then connect and upload:

```bash
git remote add origin https://github.com/yourname/py101.git
```

```bash
git push -u origin main
```

After that first push, `git push` alone sends new commits, and `git pull` brings down commits you made elsewhere — which is all you need to work on a laptop and a lab machine without emailing yourself zip files.

For signing in, the least painful route is the GitHub CLI: install it from [cli.github.com](https://cli.github.com/), run `gh auth login` once, and Git will stop asking. Note that your GitHub *password* will not work for pushing; GitHub requires a token or an SSH key, and `gh auth login` handles that for you.

???+ warning "Pitfall: public means public"
    A public repository is readable by anyone, and by every automated scanner on the
    internet. Before your first push, check `git status` and your `.gitignore`, and
    make sure no key, password, dataset you lack the rights to share, or file with
    personal data is included. Choose *private* when creating the repository if you
    are unsure — you can always make it public later, but you cannot un-publish
    something that has already been fetched.

## 8. What this page left out

The subset above is genuinely enough to work alone for a long time. Four things were left out on purpose; here is what they are, so you recognise the names and know when to go looking.

**Branches** let you develop several versions of a project side by side — an experiment kept separate from working code. Alone you can go a long way without them, though they are pleasant for a risky change you might abandon: `git switch -c experiment` starts one, `git switch main` returns.

**Merging** combines a branch back into another, and **merge conflicts** are what happens when two versions changed the same lines and Git needs you to decide. Unavoidable in a team, rare on your own.

**Pull requests** are a GitHub feature for proposing and reviewing changes before they are merged. They are about collaboration, not Git itself.

**Rebasing** rewrites history to make it tidier. It is genuinely useful and genuinely easy to misuse; leave it until you have a reason.

When you do need these, [Learn Git Branching](https://learngitbranching.js.org/) is the best introduction there is — it draws the commit graph as you type, which is exactly the part that is hard to picture.

???+ question "In-class exercise: break something, then get it back"
    Do this in a scratch folder, not in work you care about. The point is to make
    recovery feel routine before you need it.

    1. Create a folder, `git init` it, and write a `.gitignore` that ignores `.venv/`
       and `.env`. Commit it. Why is this the right first commit?
    2. Create `analysis.py` with one `print`. Commit it with a message written in the
       imperative mood.
    3. Change the file, then run `git status` and `git diff`. Now `git add` it and run
       `git diff` again. Explain why the output changed, using §2's three places.
    4. Commit, then make another edit and discard it with `git restore`. Confirm with
       `git status` that it is gone.
    5. Make and commit a change you decide you do not want. Undo it with `git revert`,
       then run `git log --oneline`. How many commits are there, and why is that the
       desired behaviour rather than a flaw?
    6. Create a `.env` file containing `API_KEY=secret123`. Run `git status`. Explain
       why it does not appear — and what you would have had to do if you had committed
       it before writing `.gitignore`.
    7. Tag your last commit `v1`, then run `git show v1`.

## Summary

Solo Git is a small loop plus a way back.

| Task | Command |
|---|---|
| Set up, once per machine | `git config --global user.name` / `user.email` |
| Start a repository | `git init` |
| See where you stand | `git status` |
| See what changed | `git diff`, `git diff --staged` |
| Stage a change | `git add file` |
| Record a snapshot | `git commit -m "message"` |
| Read the history | `git log --oneline` |
| Discard an edit | `git restore file` |
| Unstage | `git restore --staged file` |
| Fix the last commit | `git commit --amend` |
| Undo an old commit safely | `git revert hash` |
| Find lost commits | `git reflog` |
| Name a version | `git tag -a name -m "why"` |
| Back it up | `git push` |

The habits that matter more than the commands: write `.gitignore` first, commit small and often with messages that say why, run `git status` whenever you are unsure, and never let a secret near a repository.

That closes the appendix. With A1 you have an environment, with A2 you can navigate it, and with A3 your work has a history you can trust — which is the foundation the data chapters build on, and the difference between an analysis someone can reproduce and one they simply have to believe.
