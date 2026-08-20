# 2. Environments and Tooling

```motto
Your code, your data, and your Python are three separate things. Keep them that way.
```

## Introduction

Every research project you start will need a slightly different Python from the last one: this one needs the `pandas` that the co-author's script assumes, that one needs a `torch` old enough for the cluster's CUDA driver, and the referee report you are answering was computed three years ago against versions you cannot name. A **virtual environment** is how Python lets all of those coexist on one machine without fighting.

This chapter is the practical one. §2.1 says why environments exist, §2.2 and §2.3 give you the two standard tools — `venv` and `conda` — §2.4 is about where your files should live, and §2.5 covers `uv`, which did not exist when this course was first taught and is now the fastest way to do all of it.

!!! tip "The slower version of this chapter"
    [A1 Setting Up Your Python Environment](appendix_a1_environment.md) walks through
    the same ground one click at a time, with a troubleshooting table for every error
    you are likely to hit, and [A2 The Command Line and Paths](appendix_a2_shell.md)
    teaches the terminal itself with a live shell you can practise in. This chapter
    assumes you have a terminal open and know what a path is.

## 2.1 Why Python virtual environments

You can run Python like any other program, but the *base* interpreter you install comes with limited functionality — only the standard library. It cannot import NumPy, because NumPy is not part of Python. Everything interesting is a package you add.

That is where the trouble starts, because packages have versions and versions have opinions about each other. Incompatibility shows up in a few recognisable ways:

- **The language moved.** `async` and `await` became reserved keywords in Python 3.7. Code from 3.6 that used `async` as a variable name is a syntax error now.
- **Packages disagree about each other.** A `matplotlib` built against an old NumPy will not import against a new one — try `matplotlib==2.2.2` with `numpy==1.20` and watch it fail. The same story replays with every NumPy major release; `numpy` 2.0 broke a long list of packages compiled against 1.x.
- **`DeprecationWarning`s become errors.** What a library merely grumbles about in one version, it removes in the next.

Sometimes you *want* the newest of everything. Sometimes you need to run the code you wrote four years ago exactly as it ran then. Both are reasonable, and neither is possible if your machine has one shared pile of packages. The fix is to give each project its own self-contained **environment**: its own interpreter, its own installed packages, its own version numbers.

<div style="text-align:center;margin:1.3rem 0;">
<svg viewBox="0 0 700 260" xmlns="http://www.w3.org/2000/svg" role="img" width="660" style="max-width:100%;height:auto;font-family:-apple-system,Segoe UI,Roboto,sans-serif;">
  <title>One machine, one base Python, three independent project environments</title>
  <desc>A box labelled "Your computer" contains a base Python interpreter at the top. Below it sit three separate environment boxes — thesis-env with pandas 2.2 and numpy 2.0, replication-env with pandas 1.3 and numpy 1.20, and torch-env with torch 2.1 — each drawn as its own sealed container, and each paired with a project folder holding code and data that lives outside the environment.</desc>
  <rect x="6" y="6" width="688" height="248" rx="14" fill="none" stroke="var(--md-default-fg-color--light, #666)" stroke-width="1.4" stroke-dasharray="6 5"/>
  <text x="20" y="28" fill="var(--md-default-fg-color--light, #666)" font-size="13" font-weight="700" letter-spacing="0.06em">YOUR COMPUTER</text>
  <rect x="260" y="44" width="180" height="38" rx="9" fill="#306998"/>
  <text x="350" y="68" fill="#ffffff" font-size="15" font-weight="700" text-anchor="middle">base Python 3.13</text>
  <g fill="none" stroke="var(--md-default-fg-color--light, #666)" stroke-width="1.6">
    <path d="M310,82 L130,112"/>
    <path d="M350,82 L350,112"/>
    <path d="M390,82 L570,112"/>
  </g>
  <g font-size="13">
    <rect x="30" y="112" width="200" height="86" rx="10" fill="none" stroke="#3a9d4f" stroke-width="2"/>
    <text x="130" y="134" fill="#3a9d4f" font-size="14" font-weight="700" text-anchor="middle">thesis-env</text>
    <text x="130" y="157" fill="var(--md-default-fg-color, #111)" text-anchor="middle">pandas 2.2</text>
    <text x="130" y="177" fill="var(--md-default-fg-color, #111)" text-anchor="middle">numpy 2.0</text>
    <rect x="250" y="112" width="200" height="86" rx="10" fill="none" stroke="#f0a500" stroke-width="2"/>
    <text x="350" y="134" fill="#b07800" font-size="14" font-weight="700" text-anchor="middle">replication-env</text>
    <text x="350" y="157" fill="var(--md-default-fg-color, #111)" text-anchor="middle">pandas 1.3</text>
    <text x="350" y="177" fill="var(--md-default-fg-color, #111)" text-anchor="middle">numpy 1.20</text>
    <rect x="470" y="112" width="200" height="86" rx="10" fill="none" stroke="#c8202a" stroke-width="2"/>
    <text x="570" y="134" fill="#c8202a" font-size="14" font-weight="700" text-anchor="middle">torch-env</text>
    <text x="570" y="157" fill="var(--md-default-fg-color, #111)" text-anchor="middle">torch 2.1</text>
    <text x="570" y="177" fill="var(--md-default-fg-color, #111)" text-anchor="middle">numpy 1.26</text>
  </g>
  <rect x="150" y="214" width="400" height="30" rx="8" fill="none" stroke="var(--md-default-fg-color--light, #666)" stroke-width="1.4"/>
  <text x="350" y="234" fill="var(--md-default-fg-color, #111)" font-size="13" text-anchor="middle">your code and data live out here, in project folders</text>
</svg>
</div>

The last box is the part people forget. The environment holds *Python's* things — the interpreter and the packages. Your `.py` files and your data belong somewhere else entirely, in a project folder you back up and put under version control. Environments are disposable; you should be able to delete one and rebuild it from a requirements file in a minute. Your code is not disposable.

???+ note "Key concept: virtual environment"
    A **virtual environment** is a directory containing its own Python interpreter
    (or a link to one) and its own `site-packages` folder. **Activating** it puts that
    interpreter first on your `PATH`, so `python` and `pip` mean *this* environment's
    Python and *this* environment's packages until you deactivate.

## 2.2 Using `venv` to manage environments

[`venv`](https://docs.python.org/3/library/venv.html) ships with Python itself — nothing to install. It creates an environment as a plain folder, which you conventionally put inside the project it belongs to and name `.venv`.

Here is the whole workflow. Run it from inside your project folder.

???+ example "Example 2.1: create and use an environment called `.venv`"
    | Purpose | Command |
    |---------|---------|
    | Create the environment | `python -m venv .venv` |
    | Activate it (PowerShell) | `.\.venv\Scripts\Activate.ps1` |
    | Activate it (macOS / Linux) | `source .venv/bin/activate` |
    | Upgrade `pip` inside it | `python -m pip install --upgrade pip` |
    | Install what you need | `python -m pip install pandas` |
    | Record what you installed | `python -m pip freeze > requirements.txt` |
    | Leave it | `deactivate` |

Once activated, your prompt gains a `(.venv)` prefix — that prefix is the whole user interface, and it is worth trusting more than your memory. To be certain which interpreter you are actually running, ask it:

```powershell
python -c "import sys; print(sys.prefix)"
```

If that prints a path ending in `.venv`, you are inside the environment. If it prints your system Python's folder, activation did not take, and anything you `pip install` next will land in the wrong place.

???+ warning "Pitfall: PowerShell refuses to run the activation script"
    A fresh Windows install blocks local scripts, so `Activate.ps1` fails with
    *"running scripts is disabled on this system"*. Allow signed and local scripts for
    your own account, once:

    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
    ```

    Then open a new terminal and activate again. The old `Activate.bat` still exists
    for `cmd.exe`, but `Activate.ps1` is the one you want in PowerShell.

## 2.3 Using `conda` to manage environments

`conda` solves the same problem from a different direction. `pip` installs Python packages; `conda` is a general package manager that also installs the non-Python things scientific packages depend on — compilers, BLAS libraries, CUDA runtimes — and can install a *different Python version* into an environment, which `venv` cannot. Anaconda's own write-up of [the difference between `venv`+`pip` and `conda`](https://www.anaconda.com/blog/understanding-conda-and-pip) is worth ten minutes.

The distribution question is separate from the tool question. **Anaconda** is a large download that arrives with 250+ packages preinstalled; **Miniconda** is the same `conda` with nothing but Python, at roughly a tenth the size. Unless you want the bundled GUI tools, prefer Miniconda and install what you actually need. (For a fully open-source stack with a faster solver, [Miniforge](https://github.com/conda-forge/miniforge) is the same idea again, defaulting to the community `conda-forge` channel.)

???+ example "Example 2.2: the same workflow in `conda`"
    | Purpose | Command |
    |---------|---------|
    | Create a *named* environment | `conda create --name newenv python=3.12` |
    | Create one *by location* | `conda create --prefix ./envs python=3.12` |
    | Activate it | `conda activate newenv` |
    | Install a package | `conda install numpy` |
    | Record the environment | `conda env export > environment.yml` |
    | Leave it | `conda deactivate` |

The two creation forms are worth distinguishing. A **named** environment lives in conda's own central folder, and you activate it from anywhere by name — convenient, and easy to lose track of. A **prefix** environment lives in a directory you choose, usually inside the project, which makes the link between project and environment obvious at the cost of typing the path.

💡 **What's your choice?** There is no universal answer, and the honest one depends on how much you value not thinking about where things are. If your work is pure Python plus the usual data stack, `venv` (or `uv`, in §2.5) is lighter and one less concept. If you need particular Python versions or packages with heavy compiled dependencies — and in economics that means `torch`, `geopandas`, or anything wrapping a Fortran solver — `conda` will save you a bad afternoon.

???+ note "Key concept: the takehome"
    1. **`venv` is part of the Python standard library** — always there, nothing to install.
    2. **Check the `pip` box** when you install Python, or you will have an interpreter you cannot add packages to.
    3. **`conda` is a chamberlain** taking care of your Python environments, including the non-Python parts that `pip` cannot reach.

??? info "Deep dive: `conda activate` on a Linux server"
    Older course notes tell you to use `source activate newenv` on Linux. That advice
    dates from before conda 4.4 (2017) and you should no longer need it: `conda
    activate` is the current form on every platform. It does require that conda's
    shell hook has been installed into your shell startup file, which `conda init
    bash` does once. If you are on a cluster where you cannot run `conda init`,
    source the hook yourself in your job script:

    ```bash
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate newenv
    ```

    This is the single most common reason a job that works interactively fails under
    a scheduler: the batch shell is not a login shell and never read your `.bashrc`.

## 2.4 Writing code

Choose whatever editor you like — PyCharm, Spyder, VS Code, or a modern editor such as Cursor or Zed. They differ far less than their partisans claim. Two things are worth knowing whichever you pick.

The first is that most of them understand the `#%%` marker. A comment of that exact form splits a script into **cells** that you can execute one at a time, giving you a notebook's interactivity in an ordinary `.py` file that diffs cleanly in git. You will see `#%%` at the top of several examples in these notes for that reason.

The second is that your editor must be pointed at the right interpreter — the one inside the environment from §2.2 or §2.3, not the system Python. In VS Code that is the *Python: Select Interpreter* command; every other editor has an equivalent buried in project settings. Nearly every "but I installed it!" problem is this setting.

Separate from the Python environment, organise the project itself. Something like this is enough, and the reason it works is that each top-level folder answers a different question — what came in, what I wrote, what came out:

???+ example "Example 2.3: a project layout that survives a co-author"
    ```text
    project/
    |--data/            <- raw inputs, read-only, never edited by hand
    |--literature/
    |--code/
    |  |--modules.py    <- the functions
    |  |--main.py       <- the script that calls them
    |--scripts/
    |  |--submitter.sh  <- how the cluster job is launched
    |--results/         <- everything regenerable; safe to delete
    |--.venv/           <- the environment: disposable, git-ignored
    |--requirements.txt <- how to rebuild .venv from nothing
    ```

The discipline that makes this pay off is that `results/` is *derived*. If you cannot delete it and regenerate everything by running `main.py`, you have state living somewhere it should not, and the version of the table in your paper is one you can no longer reproduce.

## 2.5 A faster alternative: `uv`

Since this course was first given, a third tool has taken over much of this territory. [**`uv`**](https://docs.astral.sh/uv/) — from the authors of Ruff — does what `venv` and `pip` do, one to two orders of magnitude faster, and adds the piece both of them lack: a **lockfile** that pins every transitive dependency, so a collaborator can reconstruct your environment exactly rather than approximately.

```powershell
pip install uv          # or: winget install astral-sh.uv

uv init myproject       # creates pyproject.toml and a git repo
cd myproject
uv add pandas numpy     # resolves, installs, and records in uv.lock
uv run main.py          # runs in the project's environment, no activation
```

Two things about that last command are the point. `uv run` creates the environment on demand if it does not exist and uses it without activation, so the entire class of "I installed it into the wrong Python" errors goes away. And `uv.lock`, committed alongside your code, means `uv sync` on another machine reproduces byte-identical package versions — which is what a replication package actually requires and what `requirements.txt` only approximates.

`uv` can also install interpreters (`uv python install 3.12`), which removes the last thing `venv` could not do. It does not replace `conda` for non-Python dependencies, so if you are in the `geopandas`-and-CUDA world, stay with conda.

!!! tip "What to do if you are starting today"
    Start a new project with `uv`. Keep `conda` for projects with heavy compiled
    dependencies. Learn the `venv` commands anyway, because you will meet them in
    every README written before 2024.

## Summary

| | |
|---|---|
| **Why environments** | Packages and language versions conflict; each project gets its own sealed set. |
| **`venv`** | Standard library, no install. `python -m venv .venv`, then activate. |
| **`conda`** | Also manages non-Python dependencies and Python versions. Prefer Miniconda over Anaconda. |
| **`uv`** | Fastest option, with a real lockfile. `uv add`, `uv run`, `uv sync`. |
| **Check which Python** | `python -c "import sys; print(sys.prefix)"` settles every argument. |
| **Project layout** | Code, data, and environment in separate folders; `results/` must be regenerable. |
