# A1. Setting Up Your Python Environment

```motto
Every project gets its own Python.
```

## Introduction

Everything you have run so far has run **in this page**. That was deliberate: you got to spend your first weeks thinking about objects, names, and functions instead of fighting an installer. But the browser cells have real limits. They cannot open the files on your own disk, they forget everything when you reload, they cannot install whatever package you like, and they will not carry you through a serious dataset. To go further — and to do the data work in Chapter 3 — you need a Python of your own.

This page walks you from nothing to a working setup: an interpreter you installed, a project folder, an isolated environment for that project, the packages this course needs, and an editor that ties them together. It is written to be followed once, slowly, in front of your own computer, and then returned to when something breaks. The last section is a troubleshooting table; when you hit an error, go there first.

Two honest warnings before you start. First, this is the part of learning Python that feels least like programming — it is plumbing, and plumbing is dull. Second, **almost everyone hits at least one error here.** That is normal and it is not a sign that you are bad at this. Every error you are likely to meet is listed in §8 with its cause and its fix.

## 1. What "installing Python" actually means

It helps to be precise about what you are installing, because half of the confusion in this appendix comes from the word "Python" meaning three different things.

A `.py` file is just text. Something has to read that text and carry out what it says, and that something is a program called the **interpreter** — on Windows a file literally named `python.exe`. When you "install Python," you are installing that program, plus a large collection of modules that come with it (the **standard library**: `math`, `pathlib`, `json`, and the rest). "Python" also names the *language* the interpreter understands. So one word covers the language, the program that runs it, and the library that ships alongside — and when a tutorial says "use Python 3.13," it means the interpreter version.

You are already running an interpreter right now. This one was compiled to WebAssembly so it could run inside a web browser, but it is otherwise the real CPython. Run the cell below and look at what it reports about itself.

???+ example "Example: asking a Python about itself"
    ```python
    import sys

    print(sys.version)      # which version, and what it was built with
    print(sys.platform)     # which kind of machine it thinks it is on
    print(sys.prefix)       # the root folder of this Python installation
    ```

Look at what the last two lines report. `sys.platform` says `emscripten` — the toolchain that compiles C to WebAssembly — where the Python you are about to install will say `win32` on Windows or `darwin` on macOS. And `sys.prefix`, the folder an interpreter treats as its own home, is simply `/`: this browser Python owns the entire (imaginary) filesystem it lives in, because there is nothing else in there. On a real machine that value is the single most useful diagnostic you have, and you will meet it again in §5. You will run these same three lines on your own computer shortly, and the difference in output is the whole point of this page.

???+ note "Key concept: interpreter"
    The **interpreter** is the program that reads your Python source and executes it. A single computer can have several interpreters installed at once — different versions, in different folders, each with its own set of installed packages. Most environment problems are really the question *which interpreter am I actually running?*

## 2. Installing the interpreter

Download the official installer from [python.org/downloads](https://www.python.org/downloads/). Take the current stable release; anything from 3.11 up is fine for this course. Avoid installing Python from the Microsoft Store, and on macOS avoid using the `python3` that came with the system — both work in principle and cause avoidable trouble in practice.

### 2.1 Windows

Run the installer, and before clicking anything else, **tick the box at the bottom marked "Add python.exe to PATH."** This single checkbox is the most common cause of a broken setup. It tells Windows where to find the interpreter so that typing `python` in a terminal works from any folder. Then choose "Install Now."

One more thing is worth knowing if it applies to you. A Windows username containing non-ASCII characters — an accented letter, or anything from a non-Latin script — still breaks a surprising number of Python tools, which mishandle the resulting `C:\Users\...` path. You cannot easily rename an account, but you can sidestep the problem entirely by keeping your coursework somewhere with a plain-ASCII path, such as `C:\dev\`. This page assumes you do, and if you start that way you will never think about it again.

### 2.2 macOS

Run the `.pkg` installer from python.org and accept the defaults. It installs alongside the system Python rather than replacing it, and it gives you a `python3` command plus a matching `pip3`. When this page writes `python`, use `python3`; when it writes `\` in a path, use `/`.

???+ warning "Pitfall: the Microsoft Store stub"
    On a fresh Windows install, typing `python` may open the Microsoft Store instead
    of starting Python. That is a placeholder Microsoft ships to advertise its own
    Store build — it is not Python, and it appears when no real Python is on your
    PATH. If you see it, Python either is not installed or was installed without the
    PATH box ticked. Reinstall and tick the box, or disable the stub under
    *Settings → Apps → Advanced app settings → App execution aliases*.

## 3. Just enough terminal

To use Python you need a **terminal**: a window where you type commands and read text back. On Windows, press the Start button and open **Windows PowerShell** (or **Terminal**, which is the newer host for it). On macOS, open **Terminal** from Applications → Utilities.

A terminal is always sitting *in* some folder, called the **working directory**, and most commands act on that folder unless you say otherwise. That single idea is what makes commands like "run this file" unambiguous. Appendix A2 covers navigation and paths properly; for this page you only need four commands:

| Task | Windows (PowerShell) | macOS |
|------|----------------------|-------|
| Show the current folder | `pwd` | `pwd` |
| List what is in it | `ls` | `ls` |
| Move into a folder | `cd projects` | `cd projects` |
| Make a folder | `mkdir py101` | `mkdir py101` |

Now check that the installation worked. Open a **new** terminal — a terminal reads the PATH when it starts, so one that was already open will not see a freshly installed Python — and run:

```powershell
python --version
```

You should see something like `Python 3.13.1`. If you get an error, or the Microsoft Store opens, go to §8.

??? info "Deep dive: the `py` launcher, and having several Pythons"
    The Windows installer also gives you a small dispatcher called **`py`**. It finds the
    Pythons installed on the machine and runs the one you ask for, which is handy once
    there is more than one:

    ```powershell
    py --version         # the default (newest) Python
    py --list            # every Python py can find
    py -3.11 --version   # ask for a specific version
    py -3.11 -m venv .venv   # build an environment from that specific version
    ```

    `py` works even when PATH is misconfigured, which makes it a useful diagnostic: if
    `py --version` succeeds while `python --version` fails, Python is installed and the
    problem is purely PATH.

## 4. Why every project gets its own Python

Suppose you install `pandas` and use it all semester. Next year you join a research project whose code was written against an older pandas and breaks on the version you have. If both projects share one Python, you are stuck: upgrading serves one project and breaks the other. And with only one shared Python, the set of installed packages is a growing pile that nobody can reconstruct — so "it works on my machine" stops meaning anything.

The fix is to stop treating Python as one global thing. Instead, each project gets a **virtual environment**: a folder holding a link to an interpreter and, crucially, its *own* place to keep installed packages. Two projects on the same machine can then hold different versions of the same package without ever meeting.

???+ note "Key concept: virtual environment"
    A **virtual environment** is a folder containing a reference to a Python interpreter
    and a private `site-packages` directory for that project's installed packages.
    Creating one costs a second and a few megabytes. The convention is one environment
    per project, in a subfolder named `.venv`, never shared and never copied — it is
    disposable and rebuildable, which is exactly why it can be left out of version
    control (Appendix A3).

A project folder ends up looking like this, with the environment sitting quietly inside it:

```text
C:\dev\py101\
├── .venv\              <- the environment: interpreter link + this project's packages
├── data\               <- datasets you download
├── notebooks\          <- Jupyter notebooks
├── analysis.py         <- your code
└── requirements.txt    <- the list of packages this project needs
```

## 5. Creating and using an environment

Make a project folder and move into it. From your home directory:

```powershell
mkdir C:\dev\py101
cd C:\dev\py101
```

### 5.1 Creating it

The interpreter can build an environment for you, using the standard-library `venv` module. The `-m` flag means "run this module as a program":

```powershell
python -m venv .venv
```

That creates the `.venv` folder. Nothing is using it yet — creating an environment and *using* it are two separate steps, which is the next thing to get straight.

### 5.2 Activating it

**Activating** an environment tells the current terminal to reach for this project's Python instead of the global one. On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS:

```bash
source .venv/bin/activate
```

Your prompt gains a `(.venv)` prefix. That prefix is your at-a-glance confirmation that the environment is active — get in the habit of glancing at it before you install anything. When you are finished, `deactivate` returns the terminal to normal, and closing the terminal deactivates too. Activation lasts only for that one terminal window: open a second one and you must activate again.

Now run the same three lines from §1 in your own Python, and compare:

```powershell
python -c "import sys; print(sys.version); print(sys.platform); print(sys.prefix)"
```

`sys.platform` now reports `win32` or `darwin` rather than `emscripten`, and `sys.prefix` points at your project's `.venv` folder rather than a system directory. If you deactivate and run it again, `sys.prefix` jumps back to the global installation. That single value is the ground truth about which Python you are talking to.

```recall
Every project gets its own Python: `sys.prefix` changing when you activate is that
motto made visible — same command, same machine, a different interpreter answering.
```

???+ warning "Pitfall: PowerShell refuses to run the activation script"
    On Windows you may get `Activate.ps1 cannot be loaded because running scripts is
    disabled on this system`. Windows blocks script execution by default. Allow locally
    written and signed remote scripts **for your own user account only**:

    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
    ```

    Answer `Y`, then run the activation command again. The `-Scope CurrentUser` part
    matters: it changes the policy for you alone and needs no administrator rights.

???+ warning "Pitfall: installing into the wrong Python"
    The commonest environment bug of all: you install a package, then Python insists it
    is not installed. Almost always the environment was not active, so the package
    landed in the global Python while your code runs in `.venv` (or the reverse). Two
    habits prevent it — check for the `(.venv)` prefix in your prompt, and install with
    `python -m pip install ...` rather than bare `pip install ...`. The `python -m` form
    guarantees you get the pip belonging to the interpreter you are actually running.

### 5.3 A faster alternative: uv

Once you are comfortable with the above, it is worth knowing about **uv**, a modern replacement for `venv` and `pip` that does the same jobs far faster and skips the activation dance entirely:

```powershell
uv venv                          # create .venv
uv pip install pandas            # install into it, no activation needed
uv run python analysis.py        # run a script in it, no activation needed
```

Install it on Windows with `winget install --id=astral-sh.uv`, or into an existing Python with `python -m pip install uv`. I have put it second rather than first on purpose: `venv` and `pip` are what every textbook, every colleague, and every LLM will assume you are using, so learn those as your baseline and treat uv as a convenience once the concepts are solid.

## 6. Installing packages

**pip** is Python's package installer. It downloads packages from the **Python Package Index** (PyPI) and unpacks them into the active environment. With `.venv` active, install what this course needs:

```powershell
python -m pip install numpy pandas matplotlib jupyter
```

Expect it to take a minute or two — those are large packages, and pip prints a line per download. A few more pip commands earn their keep. `python -m pip list` shows what is installed in the active environment — a fast way to confirm you are where you think you are. `python -m pip show pandas` reports a package's version and, usefully, the folder it was installed into. `python -m pip uninstall pandas` removes it.

### 6.1 Recording what a project needs

An environment is disposable, so the list of what belongs in it must live somewhere durable. That is a plain text file, conventionally `requirements.txt`:

```text
numpy
pandas
matplotlib
jupyter
```

Anyone with that file — including you, on another computer, next year — can rebuild the environment in one command:

```powershell
python -m pip install -r requirements.txt
```

To capture exactly what you currently have, versions and all, use `python -m pip freeze > requirements.txt`. Pinned versions like `pandas==2.2.3` make a project reproducible, which is the same instinct that makes version control worth learning in Appendix A3: a result nobody can reproduce is a result nobody can check.

??? info "Deep dive: installing from a mirror (only if PyPI is slow for you)"
    Skip this unless you need it. pip downloads from PyPI, whose servers are fast from
    most of the world — but on a heavily throttled network, or from a region where PyPI
    is far away or unreliable, installs can crawl or time out. In that case point pip at
    a **mirror**: a server that carries a full copy of PyPI's packages.

    ```powershell
    python -m pip config set global.index-url <mirror-url>
    ```

    That is written to a pip config file, so it applies to every future install until
    you undo it with `python -m pip config unset global.index-url`. Which mirror to use
    depends on where you are — your university's IT pages or a regional mirror service
    will name one. Well-known public options include Tsinghua University's
    (`https://pypi.tuna.tsinghua.edu.cn/simple`) and Aliyun's, both widely used in China.

    A mirror only changes *where packages come from*, never which environment they land
    in — so it fixes slow downloads and nothing else.

??? info "Deep dive: where packages actually go, and how Python finds them"
    When you `import pandas`, Python searches a list of folders held in `sys.path`, in
    order, and uses the first match. With your environment active, ask it what that
    list is:

    ```powershell
    python -c "import sys; [print(p) for p in sys.path]"
    ```

    You will see a path ending in `.venv\Lib\site-packages`
    (Windows) or `.venv/lib/python3.13/site-packages` (macOS). That is the private
    package directory the environment gave you, and it is why activation changes what
    is importable.

    Note also what `sys.path` starts with: the folder of the script you are running.
    That is why a file of your own named `random.py` or `pandas.py` will shadow the real
    module and produce baffling errors — your folder is searched before the library.

## 7. An editor: VS Code

A terminal and a text editor are enough to write Python, but an editor built for it will catch typos as you type, complete names, and run code without leaving the window. **Visual Studio Code** is the standard choice: install it from [code.visualstudio.com](https://code.visualstudio.com/), then open the Extensions panel (`Ctrl+Shift+X`) and install the **Python** extension from Microsoft.

Now the step that trips up nearly everyone: **open your project folder, not your file.** Use *File → Open Folder* and choose `C:\dev\py101`. VS Code's Python support is built around having a project folder open — it looks inside it for `.venv`, resolves imports relative to it, and starts its terminal there. Open a lone `.py` file instead and half of that stops working, for reasons that are invisible from the outside.

With the folder open, tell VS Code which interpreter to use: press `Ctrl+Shift+P`, type `Python: Select Interpreter`, and choose the one whose path contains `.venv`. It will usually be recommended at the top of the list. The chosen interpreter appears in the status bar along the bottom, and every terminal VS Code opens from now on will have that environment already active. Create a file called `analysis.py`, put `print("hello from my own Python")` in it, and press the ▷ button. The output appears in a terminal panel at the bottom.

For Chapter 3 you will also want notebooks. With the Python extension installed, create a file ending in `.ipynb` and VS Code opens it as a notebook: cells of code you run one at a time, keeping results in memory between them — much closer to how the cells on this site behave, and the natural way to explore a dataset. The first time you run a cell it may ask to install `ipykernel`; say yes.

???+ question "Checkpoint: prove your setup works"
    Do this in your own terminal, not in the browser. You are finished when all five
    steps succeed:

    1. In a new terminal, `python --version` prints a version, not an error.
    2. `cd C:\dev\py101` then activate `.venv`, and your prompt shows `(.venv)`.
    3. `python -c "import sys; print(sys.prefix)"` prints a path inside your project.
    4. `python -c "import pandas; print(pandas.__version__)"` prints a version.
    5. In VS Code, with the *folder* open and the `.venv` interpreter selected, run a
       one-line `analysis.py` and see its output.

    If a step fails, find its symptom in §8 before trying anything else.

## 8. When it breaks

Read the error, then find it here. Symptoms are given as they appear on screen.

| Symptom | What it means | Fix |
|---------|---------------|-----|
| `python : The term 'python' is not recognized` | The terminal cannot find the interpreter — usually PATH | Open a *new* terminal. Still failing: reinstall with "Add python.exe to PATH" ticked, or use `py` instead |
| Typing `python` opens the Microsoft Store | The Store stub is answering; no real Python on PATH | Install from python.org with the PATH box ticked (§2.1) |
| `Activate.ps1 cannot be loaded ... running scripts is disabled` | PowerShell blocks scripts by default | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again |
| `ModuleNotFoundError: No module named 'pandas'` right after installing it | Installed into a different Python than the one running | Check for `(.venv)` in the prompt; reinstall with `python -m pip install pandas` |
| `pip` works but installs somewhere unexpected | Bare `pip` may belong to another interpreter | Always `python -m pip ...` |
| Downloads crawl or time out | Network trouble reaching PyPI | Retry; on a persistently slow network, use a mirror (§6.1) |
| `SyntaxError` on the very first line of a working example | Python 2 is running, or the file is not Python | Use `python3` on macOS; check the file extension |
| Imports fail only in VS Code, fine in the terminal | VS Code is pointed at another interpreter | `Python: Select Interpreter` → the `.venv` one; reopen the folder |
| Odd path or encoding errors mentioning your username | Non-ASCII characters in the path | Move the project under a plain-ASCII path such as `C:\dev\` |

When none of that fits, the fastest route to help is a well-formed question — and the same is true whether you are asking a classmate, a lecturer, or an LLM. Give five things: the exact command you ran, the **complete** error text pasted rather than paraphrased, your operating system, the output of `python --version`, and the output of `python -c "import sys; print(sys.prefix)"`. Those last two answer "which Python?", which is the first thing anyone will need to know and the thing beginners almost never think to include.

Finally, remember that an environment is disposable. If one gets into a state you cannot explain, do not spend an hour excavating it — delete the `.venv` folder, recreate it, and reinstall from `requirements.txt`. That is a thirty-second fix, and it is the reason we keep the package list in a file.

???+ question "In-class exercise: two environments, one machine"
    This exercise makes isolation concrete rather than theoretical.

    1. Create a second project folder with its own `.venv`.
    2. In the first, install `pandas`; in the second, install nothing.
    3. Activate each in turn and run `python -m pip list`. Explain the difference.
    4. In the second environment, run `python -c "import pandas"`. Which error do you
       get, and why is it the *correct* behaviour rather than a bug?
    5. Print `sys.prefix` in both. Relate what you see to this page's motto.

## Summary

You now have a Python of your own and a way of organising work in it. The pieces:

| Piece | What it is | The command that matters |
|-------|-----------|--------------------------|
| **Interpreter** | the program that runs your code | `python --version` |
| **Virtual environment** | one project's private interpreter + packages | `python -m venv .venv` |
| **Activation** | pointing this terminal at that environment | `.\.venv\Scripts\Activate.ps1` |
| **pip** | installs packages into the active environment | `python -m pip install numpy` |
| **requirements.txt** | the durable record of what a project needs | `python -m pip install -r requirements.txt` |
| **VS Code** | editor; open the *folder*, select the `.venv` interpreter | `Ctrl+Shift+P` → *Select Interpreter* |

The one diagnostic worth memorising is `python -c "import sys; print(sys.prefix)"`. Most setup problems reduce to running a different Python than you meant to, and that line tells you which one you have.

Two things follow from here. Appendix A2 takes the terminal seriously — paths, navigation, and the handful of commands that make a command line genuinely faster than a mouse. Appendix A3 adds version control, so that a working project stays working and every result you produce can be traced back to the code that made it.
