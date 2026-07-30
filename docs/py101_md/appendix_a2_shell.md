# A2. The Command Line and Paths

```motto
Every command runs somewhere.
```

## Introduction

In Appendix A1 you typed commands into a terminal without much explanation of what you were doing. This page fills that gap. It is about two things that turn out to be the same thing: the **command line**, where you tell a computer what to do by typing instead of clicking, and **paths**, the way you name a file so that a program can find it.

You need both for ordinary work, and not because the command line is romantic. Many tools — `pip`, `git`, `python` itself — have no other interface. A command is text, which means it can be pasted into an email, put in a README, or handed to an LLM in a way that a sequence of mouse clicks never can. And when a program cannot find your data file, the fix is nearly always a path you got wrong, which you cannot diagnose without understanding what a path is.

The commands here are the **POSIX** ones — the family used on Linux and macOS, and the ones every tutorial, error message, and LLM answer will assume. Windows PowerShell reaches the same ideas by slightly different names, and §8 lines the two up. §9 then brings all of it back into Python, where you will spend most of your time.

This page has **live terminals** in it. Type into them and press Enter. They come pre-loaded with a small practice filesystem, they share one working directory from top to bottom of the page, and the *Reset files* button puts everything back if you break something. Be clear about what they are, though: a small teaching shell running on a genuine POSIX-style filesystem, so paths, wildcards, redirection and pipes behave exactly as they really do — but with no permissions, no users, no network, no text editors, and no package manager. `help` lists everything it knows. Anything it does not know says so rather than pretending.

## 1. The filesystem is a tree

Before any command makes sense you need a picture of what it acts on. Every file on your computer sits inside a **folder** (also called a **directory** — the words are interchangeable, and command-line tools tend to say "directory"). Folders sit inside other folders, and that nesting goes all the way up until it stops. The result is a tree.

### 1.1 One tree, or one per drive

On macOS and Linux there is exactly one tree, and its base is written `/`, pronounced "root". Everything on the machine hangs off it, including external disks, which get attached somewhere inside the single tree.

Windows instead gives each drive its own tree, labelled by a letter: `C:\` for your main disk, `D:\` for a USB stick. So Windows has several roots and POSIX has one. This is the deepest difference between the two, and it is why some paths cannot be translated from one to the other.

### 1.2 Absolute and relative paths

A **path** is a description of how to reach a file or folder. There are two kinds, and confusing them is the single most common cause of "file not found".

An **absolute path** starts at the root and leaves nothing to interpretation: `/home/student/py101/data/prices.csv`, or on Windows `C:\dev\py101\data\prices.csv`. You can hand it to any program, from anywhere, and it will find the same file. You can recognise one by its first character: a `/` on POSIX, a drive letter on Windows.

A **relative path** starts wherever you happen to be: `data/prices.csv` means "from here, go into `data`, then take `prices.csv`". It is shorter, and it keeps working if the whole project moves to another computer — which is why real code uses relative paths almost exclusively. But it only means something once you know where "here" is, and that is the subject of §2.

### 1.3 Three shorthands

Three symbols appear constantly inside paths, and they are worth learning as vocabulary rather than deciphering each time.

A single dot **`.`** means "the folder I am in". So `./analysis.py` and `analysis.py` name the same file; the explicit form shows up when a program needs to be told that a name is a path rather than a command.

Two dots **`..`** mean "the folder above this one" — the parent. It can be chained and combined: `../data` is a sibling folder, and `../../README.md` climbs two levels before descending. This is how you refer to something outside your current folder without spelling out an absolute path.

A tilde **`~`** means "my home folder" — `/home/student` in our practice terminal, `/Users/yourname` on macOS, `C:\Users\yourname` on Windows. So `~/py101` is your project folder no matter whose machine it is, which makes it the polite way to write instructions for someone else.

???+ note "Key concept: path"
    A **path** names a location in the filesystem tree. An **absolute** path starts at
    the root (`/` or `C:\`) and means the same thing from anywhere. A **relative** path
    starts at the current working directory, and means nothing until you know what that
    is. `.` is here, `..` is one level up, `~` is your home folder.

### 1.4 Writing paths down

Four details about the writing of paths cause more trouble than they should.

**Separators.** POSIX separates folder names with a forward slash `/`; Windows traditionally uses a backslash `\`. Nearly everything on Windows now accepts either, and Python accepts either, so prefer `/` — it works everywhere and, as §9 shows, it avoids a genuine trap in Python string literals.

**Case.** On Linux, `Data` and `data` are two different folders. On Windows and by default on macOS, they are the same one. Code written on a case-insensitive machine can therefore fail on Linux — which is where servers and CI run. Pick a convention, lowercase is the usual one, and stay consistent.

**Spaces.** A space normally separates one argument from the next, so a path containing a space must be quoted: `cd "My Documents"`, not `cd My Documents`. This is reason enough to keep spaces out of folder names for anything you will touch from a terminal; underscores and hyphens cost nothing.

**Extensions.** The `.csv` in `prices.csv` is just the last part of the name, and it is a convention rather than a rule — but tools rely on it heavily. Both Windows Explorer and macOS Finder hide extensions by default, which produces some memorable confusion.

???+ warning "Pitfall: hidden extensions"
    Explorer and Finder hide known extensions, so a file called `prices.csv` shows up as
    `prices`. Two consequences follow. First, if you "rename" it to `prices.csv` in the
    graphical view, you have really made `prices.csv.csv`, which is why your program
    cannot find it. Second, a file shown as `report.pdf` may really be
    `report.pdf.exe`, which is how a good deal of malware gets opened. Turn extensions
    on — on Windows, *View → Show → File name extensions*; on macOS, *Finder →
    Settings → Advanced → Show all filename extensions* — and leave them on.

## 2. Where am I? `pwd`, `ls`, `cd`

A terminal is always **inside** one folder. Every relative path you type is interpreted from there, so before running anything you should be able to answer "where am I?" without guessing. Three commands cover it: **`pwd`** prints the working directory, **`ls`** lists what is in it, and **`cd`** moves you somewhere else.

Try them below. You start in `/home/student`, and the prompt shows an abbreviated form of where you are — `~` for home, `~/py101` once you have moved down one level. Watch the prompt change as you `cd`.

```terminal
pwd
ls
cd py101
ls
cd data
pwd
cd ..
cd ~
```

Two things in that sequence are worth pausing on. `cd py101` used a relative path, so it worked only because you happened to be in `/home/student`; running it twice fails the second time. And `cd ..` then `cd ~` show the two ways back — one step up, or all the way home. `cd` with no argument at all also goes home, which is a useful reflex when you are lost.

The `ls` here marks folders with a trailing `/` so you can tell them from files at a glance. Adding **`-a`** also shows names beginning with a dot, which are hidden by convention — try `ls -a py101` and you will find a `.gitignore` that plain `ls` never mentioned. Adding **`-l`** gives one entry per line with its size and modification time.

???+ note "Key concept: working directory"
    The **working directory** (or *current directory*) is the folder a terminal is
    sitting in. It is what every relative path is measured from, and what a program
    means by "here" when it opens a file. `pwd` tells you what it is; `cd` changes it.
    Each terminal window has its own, and it changes nothing about the files themselves.

```recall
Every command runs somewhere: `ls` did not fail or succeed on its own merits — it
listed different things depending only on where you were standing when you ran it.
```

## 3. Reading files without opening them

Once you can move around, the next thing you want is to look inside a file — often just to check that it is the file you think it is, which is faster from a terminal than from an editor.

**`cat`** prints a whole file. It is named for "concatenate", because given several files it prints them one after another. For a short file that is exactly right; for a large one it floods the screen, which is what the next two commands are for.

**`head`** prints the first ten lines and **`tail`** the last ten, and both take `-n` to ask for a different number. On a data file this is the fastest way to see the column names, or to check that the last row is not junk. **`wc`** counts: `wc -l` gives lines, which on a CSV is the row count. And **`tree`** draws the folder structure below you, which is the quickest way to get your bearings in an unfamiliar project.

```terminal
cd py101/data
cat gdp.csv
head -n 3 prices.csv
tail -n 2 prices.csv
wc -l prices.csv
cd ~
tree
```

Notice that `wc -l prices.csv` reports 7 while the file holds six observations. The header row is a line too. That off-by-one is a habit worth acquiring now, because you will meet it again the moment you start counting rows in pandas.

## 4. Making, copying, moving, deleting

So far you have only looked. These five commands change things, and they are the ones to be careful with.

**`mkdir`** makes a folder. It fails if the parent does not exist, which is what `-p` is for: `mkdir -p a/b/c` creates the whole chain in one go and stays quiet if part of it is already there. **`touch`** creates an empty file (and, on an existing one, updates its modification time). **`cp`** copies and **`mv`** moves — and `mv` is also how you *rename*, since moving a file to a new name in the same folder is the same operation. Both take a destination that may be either a new name or an existing folder to drop the thing into. Copying a whole folder needs `-r`, for "recursive".

**`rm`** deletes, and removing a folder likewise needs `-r`. Note what this shell does when you forget: it refuses and tells you, rather than doing something surprising.

```terminal
mkdir practice
cd practice
touch first.txt
echo "some text" > first.txt
cp first.txt second.txt
mv second.txt renamed.txt
ls
cd ~
rm -r practice
```

???+ warning "Pitfall: `rm` is permanent"
    Deleting from a graphical file manager moves things to the Recycle Bin or Trash, so
    a mistake is recoverable. `rm` has no such safety net: it unlinks the file, and it is
    gone. There is no undo, and the shell does not ask for confirmation. The combination
    to be genuinely careful with is `rm -r` on a path built from a wildcard, because a
    stray space turns `rm -r ./old*` into something much worse. Before any `rm -r`, run
    the same path through `ls` first and read what comes back. This is also the strongest
    argument for Appendix A3: a file that is committed to version control can be
    recovered, and one that is not, cannot.

## 5. Wildcards

Typing out twenty file names is not the intended experience. The shell will expand patterns for you before the command ever runs — a feature called **globbing**.

A **`*`** stands for any run of characters, including none, so `*.csv` matches every name ending in `.csv` and `prices*` matches every name starting with `prices`. A **`?`** stands for exactly one character. The expansion happens in the shell, not in the command: by the time `ls` runs, it has been handed the actual list of matching names and has no idea a pattern was involved.

That last point explains a rule that otherwise looks arbitrary. `find` takes a pattern of its own and wants to receive it unexpanded, so you must **quote** it — `find . -name "*.csv"` — otherwise the shell helpfully expands `*.csv` against the current folder first and `find` gets the wrong thing entirely. Quoting is how you say "leave this one alone".

```terminal
cd py101/data
ls *.csv
ls -l *.csv
wc -l *.csv
cd ~
ls py101/*/
```

## 6. Redirection and pipes

Here is where the command line stops being a slower mouse and starts being something you cannot do by clicking.

Every command writes its result to what is conventionally called *standard output*, which normally means your screen. Two symbols redirect it into a file instead. **`>`** writes, replacing whatever the file held before; **`>>`** appends to the end. So `wc -l *.csv > counts.txt` puts the counts in a file rather than on screen, and the second form is how you accumulate a log across several commands.

**`|`**, the **pipe**, is the better idea: it connects one command's output directly to the next command's input, with no file in between. `cat prices.csv | grep MSFT` prints the file, hands that text to `grep`, and you see only the matching lines. Add another stage — `cat prices.csv | grep MSFT | wc -l` — and you have counted how many MSFT rows there are without writing anything down. Each command does one small job and knows nothing about the others; you get the useful behaviour by composing them. That design is most of why these forty-year-old tools are still in use.

```terminal
cd py101/data
cat prices.csv | grep MSFT
cat prices.csv | grep MSFT | wc -l
wc -l *.csv > counts.txt
cat counts.txt
echo "checked today" >> counts.txt
cat counts.txt
cd ~
```

???+ warning "Pitfall: `>` overwrites without asking"
    `>` truncates its target the moment the command starts — before it produces any
    output. Two consequences catch people. Writing `>` when you meant `>>` silently
    destroys the previous contents. And `sort data.csv > data.csv` does not sort a file
    in place; it empties it first and leaves you with nothing. Redirect to a new name,
    then rename.

## 7. Searching: `find` and `grep`

Two commands answer the two questions you actually have about a project you do not know well.

**`find`** searches by **name**, walking down through every subfolder. `find . -name "*.csv"` reports every CSV anywhere below you, which is how you locate a data file whose folder you have forgotten. `-type f` restricts results to files and `-type d` to directories, so `find . -type d` sketches the folder structure. Note that it lists the folder you started from as well.

**`grep`** searches by **content**, printing the lines that contain what you asked for. `grep AAPL prices.csv` pulls out just the Apple rows; `-i` ignores case, `-n` prefixes each hit with its line number, and `-c` reports a count instead of the lines. Given no file, it reads from a pipe, which is how it usually gets used.

Between them: `find` when you know roughly what the file is called, `grep` when you know something that is written inside it.

```terminal
find . -name "*.csv"
find . -type d
grep -n AAPL py101/data/prices.csv
grep -c MSFT py101/data/prices.csv
grep -i aapl py101/data/prices.csv
```

## 8. The same ideas on Windows

Nothing in §1 changes on Windows — the tree, absolute and relative paths, and the working directory are the same concepts. What changes is the vocabulary, and PowerShell has thoughtfully given itself two.

PowerShell's own commands are `Verb-Noun` pairs: `Get-Location`, `Get-ChildItem`, `Set-Location`. They are verbose but self-describing, and they are what you will see in Windows documentation. PowerShell also defines **aliases** with the familiar POSIX names, so `pwd`, `ls`, `cd`, `cat`, and `mkdir` all work as you would expect. Use the short names day to day; recognise the long ones when you read someone else's script.

| Task | POSIX | PowerShell alias | PowerShell's own name |
|------|-------|------------------|----------------------|
| Print working directory | `pwd` | `pwd` | `Get-Location` |
| List a folder | `ls` | `ls`, `dir` | `Get-ChildItem` |
| Change folder | `cd` | `cd` | `Set-Location` |
| Print a file | `cat` | `cat`, `type` | `Get-Content` |
| First / last lines | `head`, `tail` | — | `Get-Content -TotalCount 10`, `-Tail 10` |
| Count lines | `wc -l` | — | `(Get-Content f).Count` |
| Make a folder | `mkdir` | `mkdir`, `md` | `New-Item -ItemType Directory` |
| Copy | `cp` | `cp`, `copy` | `Copy-Item` |
| Move or rename | `mv` | `mv`, `move` | `Move-Item` |
| Delete | `rm` | `rm`, `del` | `Remove-Item` |
| Search contents | `grep` | — | `Select-String` |
| Find by name | `find` | — | `Get-ChildItem -Recurse -Filter` |

Three differences are worth holding on to. Because Windows gives every drive its own tree, changing disk means naming it: `cd D:\data`. Wildcards, redirection with `>` and `>>`, and the pipe `|` all work in PowerShell, though the pipe there carries structured objects rather than plain text, so `|` composes rather differently once you go beyond simple cases. And the flags mostly do not transfer: `-n`, `-l`, `-r` are POSIX conventions, while PowerShell spells its options out as `-Recurse`, `-Filter`, `-TotalCount`.

??? info "Deep dive: getting a real POSIX shell on Windows"
    The table above is a translation, and translations leak. If you would rather run the
    real commands, Windows offers two routes.

    **Git Bash** arrives with Git for Windows (Appendix A3) and gives you a genuine bash
    with the standard tools, operating on your normal Windows drives. It is the lighter
    option and it is enough for everything on this page.

    **WSL**, the Windows Subsystem for Linux, runs an actual Linux distribution
    alongside Windows: `wsl --install` from an administrator PowerShell, and you have a
    complete Ubuntu with its own package manager. It is the better environment if you
    later need Linux-only tooling, at the cost of a second filesystem to keep straight —
    your Windows files appear under `/mnt/c/`, and crossing that boundary is noticeably
    slower than staying on one side of it.

    Neither is required for this course. Both are worth knowing exist.

## 9. Paths in Python: `pathlib`

Everything so far has been about talking to a shell. But the reason paths matter to you is that your *programs* have to name files, and this is where the ideas above start paying rent. The tool for it is `pathlib` in the standard library, and it is the one part of this page you should expect to use every week.

The problem it solves is that a path written as a plain string is a path you have to do arithmetic on by hand. Joining `"data"` and `"prices.csv"` means worrying about whether either end already has a slash, and which slash; pulling the extension off a filename means finding the last dot. `pathlib` gives you a `Path` object that knows it is a path.

The headline feature is that `/` joins paths. It reads like the thing it produces, and it inserts exactly one separator of whichever kind the current system uses.

???+ example "Example: building paths with `/`"
    ```python
    from pathlib import Path

    data = Path("py101") / "data"
    prices = data / "prices.csv"

    print(prices)              # py101/data/prices.csv
    print(prices.name)         # prices.csv  — the final component
    print(prices.stem)         # prices      — the name without its extension
    print(prices.suffix)       # .csv        — the extension, dot included
    print(prices.parent)       # py101/data  — the folder holding it
    print(prices.parts)        # ('py101', 'data', 'prices.csv')
    ```

Those five attributes replace most of the string-slicing people write once and then get subtly wrong. `stem` and `suffix` in particular are how you build an output name from an input name — `prices.with_suffix(".parquet")` rather than chopping at the last dot yourself.

A `Path` can also answer questions about the actual disk, which is the other half of its job. `exists()`, `is_file()` and `is_dir()` check what is really there; `Path.cwd()` returns the working directory from §2, which is precisely what relative paths in your program are measured against; and `glob()` does §5's wildcard matching from inside Python.

???+ example "Example: asking about what is really there"
    ```python
    from pathlib import Path

    print(Path.cwd())                  # the working directory, from §2

    # Make a folder and two files, so there is something real to ask about.
    sandbox = Path("sandbox")
    sandbox.mkdir(exist_ok=True)
    (sandbox / "prices.csv").write_text("date,close\n2024-01-02,185.64\n")
    (sandbox / "gdp.csv").write_text("country,year\nUSA,2023\n")

    print(sandbox.is_dir())                       # True
    print((sandbox / "prices.csv").exists())      # True
    print((sandbox / "nope.csv").exists())        # False

    # The same wildcard idea as §5, returning Path objects:
    print(sorted(p.name for p in sandbox.glob("*.csv")))
    print((sandbox / "gdp.csv").read_text())
    ```

    `mkdir`, `write_text`, `read_text` and `glob` are the same four operations you ran
    as `mkdir`, `echo >`, `cat` and `ls *.csv` in the terminal — and in fact the
    terminals on this page and these Python cells share one in-browser filesystem, so a
    file you create in either is visible from the other.

Now the trap that catches every Windows beginner, and it is worth understanding rather than memorising. In a Python string, a backslash begins an **escape sequence**: `\n` means newline, `\t` means tab. So a Windows path pasted straight into quotes is not the text you think it is.

???+ warning "Pitfall: backslashes in Python strings"
    Consider a path copied out of Explorer:

    ```python
    path = "C:\data\notes.txt"   # broken, and quietly so
    ```

    Python reads `\n` as a newline character, so this string contains an actual line
    break where you meant `\n`. Sometimes you get a `SyntaxError` — `"C:\Users\new"`
    fails outright, because `\U` starts a Unicode escape — but the silent version is
    worse, because it produces a string that merely fails to name any real file.

    There are three fixes, and all three are fine:

    ```python
    path = r"C:\data\notes.txt"          # raw string: backslashes stay literal
    path = "C:/data/notes.txt"           # forward slashes: Windows accepts them
    path = Path("C:/data") / "notes.txt" # pathlib, which is what to reach for
    ```

    Use a raw string when you must paste a Windows path verbatim, and `pathlib`
    otherwise.

One further reason to prefer `pathlib`: it separates the *grammar* of paths from the machine you are on. `PurePosixPath` and `PureWindowsPath` parse each convention without touching any disk, so you can see the two systems side by side — including the drive letter that has no POSIX equivalent.

???+ example "Example: the two conventions, side by side"
    ```python
    from pathlib import PurePosixPath, PureWindowsPath

    posix = PurePosixPath("/home/student/py101/data/prices.csv")
    print(posix.parts)      # ('/', 'home', 'student', 'py101', 'data', 'prices.csv')
    print(posix.parent)     # /home/student/py101/data

    win = PureWindowsPath(r"C:\dev\py101\data\prices.csv")
    print(win.parts)        # ('C:\\', 'dev', 'py101', 'data', 'prices.csv')
    print(win.drive)        # C:      — POSIX paths have no drive at all
    print(win.as_posix())   # C:/dev/py101/data/prices.csv
    ```

Finally, the habit to take away. Write paths **relative** to your project and build them with `/`, so that `pd.read_csv(Path("data") / "prices.csv")` works on your laptop, on a classmate's, and on a server, with no line to edit. An absolute path like `C:\Users\yourname\Desktop\prices.csv` works exactly once, on one machine, until you tidy your Desktop. When you meet `pd.read_csv` in Chapter 3, that argument is a path, and everything on this page applies to it.

???+ question "In-class exercise: a small reorganisation"
    Use the terminal above; press *Reset files* first so everyone starts level.

    1. From your home folder, report the working directory, then list everything in
       `py101` **including** hidden names. What did the plain `ls` hide, and why is that
       file's name a reasonable thing to hide?
    2. How many data rows — not lines — are in `py101/data/prices.csv`? Show the command
       and explain the adjustment.
    3. Make a folder `py101/data/clean`, and copy into it only the CSVs directly inside
       `py101/data` (not the one in `raw/`). Verify with `tree py101/data`.
    4. Using one pipeline, write the AAPL rows of `prices.csv` into
       `py101/data/clean/aapl.csv`. Then check the result with `wc -l`.
    5. Find every `.csv` anywhere under your home folder. Run it once with the pattern
       quoted and once without, from inside `py101/data`. Explain the difference in terms
       of §5.
    6. In a runnable cell, use `pathlib` to print the stem and suffix of
       `py101/data/prices.csv`, then produce the name `prices.parquet` from it without
       writing the word "prices".

## Summary

Two halves of one idea: paths name locations, and commands act on them from wherever you happen to be standing.

| Task | Command | Note |
|------|---------|------|
| Where am I | `pwd` | every relative path is measured from here |
| What is here | `ls`, `ls -a`, `ls -l` | `-a` shows dotfiles, `-l` adds size and time |
| Move | `cd`, `cd ..`, `cd ~` | no argument also means home |
| Look inside | `cat`, `head -n N`, `tail -n N` | `head` for column names |
| Count | `wc -l` | remember the header row |
| Structure | `tree` | fastest orientation in a new project |
| Create | `mkdir -p`, `touch` | `-p` makes the whole chain |
| Copy, move, rename | `cp -r`, `mv` | `mv` renames; `-r` for folders |
| Delete | `rm`, `rm -r` | permanent — `ls` the path first |
| Match many names | `*`, `?` | expanded by the shell, before the command |
| Redirect, append | `>`, `>>` | `>` truncates immediately |
| Compose | `\|` | output of one becomes input of the next |
| Find by name | `find . -name "*.csv"` | quote the pattern |
| Find by content | `grep -n PATTERN file` | `-i` ignores case, `-c` counts |

And in Python: build paths with `Path("data") / "prices.csv"`, read them apart with `.name`, `.stem`, `.suffix`, `.parent`, keep them relative to the project, and never paste a Windows path into quotes without a leading `r`.

Appendix A3 takes the last step. You can now find, inspect and rearrange your files — but nothing so far records *what changed and why*, and `rm` has already shown how little it takes to lose work permanently. Version control fixes both.
