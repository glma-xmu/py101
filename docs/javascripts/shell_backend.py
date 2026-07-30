"""
A tiny teaching shell, running on Pyodide's in-memory filesystem.

This is NOT bash. It is a deliberately small emulator covering the commands
Appendix A2 teaches, implemented on top of a real POSIX-like filesystem (the
Emscripten MEMFS that Pyodide already provides), so that path resolution,
globbing, redirection and pipes behave the way they really do.

What it does not have, on purpose: permissions, users, processes, job control,
package managers, editors, or a network. Anything missing reports itself as
missing rather than pretending.

The JavaScript side (shell.js) calls three functions:
    shell_run(line)  -> JSON {"out": str, "clear": bool, "prompt": str}
    shell_reset()    -> rebuilds the practice filesystem, returns the prompt
    shell_prompt()   -> the current prompt string
"""

import glob as _glob
import json
import os
import shutil
import time

HOME = "/home/student"
CWD = HOME


class ShellError(Exception):
    """A message to show the student instead of a Python traceback."""


# --------------------------------------------------------------------------
# The practice filesystem
# --------------------------------------------------------------------------

_PRICES = """date,ticker,close,volume
2024-01-02,AAPL,185.64,52455980
2024-01-03,AAPL,184.25,58414460
2024-01-04,AAPL,181.91,71983570
2024-01-02,MSFT,370.87,25258600
2024-01-03,MSFT,370.60,23083500
2024-01-04,MSFT,367.94,20901500
"""

_GDP = """country,year,gdp_per_capita
USA,2022,76329
USA,2023,81695
JPN,2022,34017
JPN,2023,33834
DEU,2022,48718
DEU,2023,52746
"""

_SEED_DIRS = [
    "downloads",
    "py101",
    "py101/data",
    "py101/data/raw",
    "py101/notebooks",
]

_SEED_FILES = {
    "notes.txt": (
        "Week 1: objects and types\n"
        "Week 2: functions\n"
        "Week 3: numpy\n"
        "Week 4: pandas\n"
    ),
    "README.md": "# My coursework\n\nEverything for the Python course lives here.\n",
    "py101/analysis.py": (
        "import pandas as pd\n"
        "\n"
        "prices = pd.read_csv('data/prices.csv')\n"
        "print(prices.head())\n"
    ),
    "py101/requirements.txt": "numpy\npandas\nmatplotlib\n",
    "py101/.gitignore": ".venv/\n__pycache__/\ndata/raw/\n",
    "py101/data/prices.csv": _PRICES,
    "py101/data/gdp.csv": _GDP,
    "py101/data/raw/prices_2023.csv": "date,ticker,close\n2023-12-29,AAPL,192.53\n",
    "py101/notebooks/explore.ipynb": '{"cells": [], "nbformat": 4}\n',
    "downloads/lecture_slides.pdf": "%PDF-1.7 (not a real PDF)\n",
    "downloads/survey_data.zip": "PK (not a real zip)\n",
}


def shell_reset():
    """Delete and rebuild the practice filesystem, and go home."""
    global CWD
    if os.path.isdir(HOME):
        shutil.rmtree(HOME)
    os.makedirs(HOME, exist_ok=True)
    for d in _SEED_DIRS:
        os.makedirs(os.path.join(HOME, d), exist_ok=True)
    for path, text in _SEED_FILES.items():
        full = os.path.join(HOME, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    CWD = HOME
    return shell_prompt()


def shell_prompt():
    shown = CWD
    if CWD == HOME:
        shown = "~"
    elif CWD.startswith(HOME + "/"):
        shown = "~" + CWD[len(HOME):]
    return "student@py101:" + shown + "$"


# --------------------------------------------------------------------------
# Parsing: tokens that remember whether they were quoted
# --------------------------------------------------------------------------


def _tokenize(line):
    """Split a command line into [text, was_quoted] pairs."""
    toks, cur, quoted, started = [], "", False, False
    inq, qch = False, ""
    for ch in line:
        if inq:
            if ch == qch:
                inq = False
            else:
                cur += ch
        elif ch in "\"'":
            inq, qch, quoted, started = True, ch, True, True
        elif ch.isspace():
            if started:
                toks.append([cur, quoted])
                cur, quoted, started = "", False, False
        else:
            cur += ch
            started = True
    if inq:
        raise ShellError("unmatched quote — every \" or ' needs a partner")
    if started:
        toks.append([cur, quoted])
    return toks


def _resolve(p):
    """Turn a path the student typed into an absolute, normalised path."""
    if p == "~":
        p = HOME
    elif p.startswith("~/"):
        p = HOME + p[1:]
    if not p.startswith("/"):
        p = CWD.rstrip("/") + "/" + p
    return os.path.normpath(p)


def _expand(tok, quoted):
    """Glob an unquoted token containing wildcards; quoted tokens stay literal."""
    if quoted or not any(c in tok for c in "*?["):
        return [tok]
    matches = sorted(_glob.glob(_resolve(tok)))
    if not matches:
        return [tok]
    if tok.startswith("/") or tok.startswith("~"):
        return matches
    base = CWD.rstrip("/") + "/"
    return [m[len(base):] if m.startswith(base) else m for m in matches]


def _split_flags(args):
    """Separate -abc style flags from operands, and pull out -n VALUE."""
    flags, operands, values = set(), [], {}
    i = 0
    while i < len(args):
        a = args[i]
        if len(a) > 1 and a.startswith("-") and not a[1].isdigit():
            if a.startswith("--"):
                flags.add(a[2:])
            else:
                for ch in a[1:]:
                    flags.add(ch)
                if "n" in a[1:] and i + 1 < len(args) and args[i + 1].lstrip("-").isdigit():
                    values["n"] = int(args[i + 1])
                    i += 1
        elif a.startswith("-") and a[1:].isdigit():
            values["n"] = int(a[1:])
        else:
            operands.append(a)
        i += 1
    return flags, operands, values


# --------------------------------------------------------------------------
# Commands. Each takes (args, stdin) and returns text.
# --------------------------------------------------------------------------


def _need(path, what="file or folder"):
    full = _resolve(path)
    if not os.path.exists(full):
        raise ShellError("%s: no such %s" % (path, what))
    return full


def _listing_name(full, name):
    return name + "/" if os.path.isdir(full) else name


def cmd_pwd(args, stdin):
    return CWD


def _ls_row(full, shown, flags):
    if "l" not in flags:
        return _listing_name(full, shown)
    st = os.stat(full)
    when = time.strftime("%b %d %H:%M", time.localtime(st.st_mtime))
    size = "-" if os.path.isdir(full) else str(st.st_size)
    return "%8s  %s  %s" % (size, when, _listing_name(full, shown))


def _ls_join(rows, flags):
    return "\n".join(rows) if "l" in flags else "  ".join(rows)


def cmd_ls(args, stdin):
    flags, operands, _ = _split_flags(args)
    targets = operands or ["."]
    files, dirs = [], []
    for t in targets:
        full = _need(t)
        (dirs if os.path.isdir(full) else files).append((t, full))

    chunks = []
    # Plain file arguments are listed together, with no heading — like real ls.
    if files:
        chunks.append(_ls_join([_ls_row(f, t, flags) for t, f in files], flags))
    # Each directory argument gets its contents, headed by name only if there
    # is more than one target to tell apart.
    for t, full in dirs:
        names = sorted(os.listdir(full))
        if "a" not in flags:
            names = [n for n in names if not n.startswith(".")]
        body = _ls_join(
            [_ls_row(os.path.join(full, n), n, flags) for n in names], flags
        )
        chunks.append(t + ":\n" + body if len(targets) > 1 else body)
    return "\n\n".join(c for c in chunks if c)


def cmd_cd(args, stdin):
    global CWD
    target = args[0] if args else "~"
    full = _resolve(target)
    if not os.path.exists(full):
        raise ShellError("cd: %s: no such folder" % target)
    if not os.path.isdir(full):
        raise ShellError("cd: %s: not a folder (it is a file)" % target)
    CWD = full
    return ""


def cmd_cat(args, stdin):
    if not args:
        return stdin
    out = []
    for a in args:
        full = _need(a)
        if os.path.isdir(full):
            raise ShellError("cat: %s: that is a folder, not a file" % a)
        with open(full) as fh:
            out.append(fh.read())
    return "".join(out).rstrip("\n")


def _lines_of(args, stdin):
    if args:
        text = []
        for a in args:
            with open(_need(a)) as fh:
                text.append(fh.read())
        return "".join(text).splitlines()
    return stdin.splitlines()


def cmd_head(args, stdin):
    flags, operands, values = _split_flags(args)
    n = values.get("n", 10)
    return "\n".join(_lines_of(operands, stdin)[:n])


def cmd_tail(args, stdin):
    flags, operands, values = _split_flags(args)
    n = values.get("n", 10)
    return "\n".join(_lines_of(operands, stdin)[-n:])


def cmd_wc(args, stdin):
    flags, operands, _ = _split_flags(args)
    if operands:
        text = ""
        for a in operands:
            with open(_need(a)) as fh:
                text += fh.read()
    else:
        text = stdin
    lines, words, chars = len(text.splitlines()), len(text.split()), len(text)
    if flags & {"l", "w", "c"}:
        parts = []
        if "l" in flags:
            parts.append(str(lines))
        if "w" in flags:
            parts.append(str(words))
        if "c" in flags:
            parts.append(str(chars))
    else:
        parts = [str(lines), str(words), str(chars)]
    if operands:
        parts.append(" ".join(operands))
    return " ".join(parts)


def cmd_echo(args, stdin):
    return " ".join(args)


def cmd_mkdir(args, stdin):
    flags, operands, _ = _split_flags(args)
    if not operands:
        raise ShellError("mkdir: needs a folder name")
    for a in operands:
        full = _resolve(a)
        if "p" in flags:
            os.makedirs(full, exist_ok=True)
        else:
            if os.path.exists(full):
                raise ShellError("mkdir: %s: already exists" % a)
            parent = os.path.dirname(full)
            if not os.path.isdir(parent):
                raise ShellError(
                    "mkdir: %s: the parent folder does not exist (try mkdir -p)" % a
                )
            os.mkdir(full)
    return ""


def cmd_touch(args, stdin):
    if not args:
        raise ShellError("touch: needs a file name")
    for a in args:
        full = _resolve(a)
        parent = os.path.dirname(full)
        if not os.path.isdir(parent):
            raise ShellError("touch: %s: the folder does not exist" % a)
        if os.path.exists(full):
            os.utime(full, None)
        else:
            open(full, "w").close()
    return ""


def _dest_path(dest, src_full):
    full = _resolve(dest)
    if os.path.isdir(full):
        return os.path.join(full, os.path.basename(src_full))
    return full


def cmd_cp(args, stdin):
    flags, operands, _ = _split_flags(args)
    if len(operands) < 2:
        raise ShellError("cp: needs a source and a destination")
    *sources, dest = operands
    if len(sources) > 1 and not os.path.isdir(_resolve(dest)):
        raise ShellError("cp: with several sources, the destination must be a folder")
    for s in sources:
        src = _need(s)
        target = _dest_path(dest, src)
        if os.path.isdir(src):
            if "r" not in flags and "R" not in flags:
                raise ShellError("cp: %s is a folder — use cp -r to copy it" % s)
            shutil.copytree(src, target, dirs_exist_ok=True)
        else:
            shutil.copyfile(src, target)
    return ""


def cmd_mv(args, stdin):
    flags, operands, _ = _split_flags(args)
    if len(operands) < 2:
        raise ShellError("mv: needs a source and a destination")
    *sources, dest = operands
    if len(sources) > 1 and not os.path.isdir(_resolve(dest)):
        raise ShellError("mv: with several sources, the destination must be a folder")
    for s in sources:
        src = _need(s)
        shutil.move(src, _dest_path(dest, src))
    return ""


def cmd_rm(args, stdin):
    flags, operands, _ = _split_flags(args)
    if not operands:
        raise ShellError("rm: needs something to remove")
    recursive = bool(flags & {"r", "R"})
    for a in operands:
        full = _resolve(a)
        if not os.path.exists(full):
            if "f" in flags:
                continue
            raise ShellError("rm: %s: no such file or folder" % a)
        if os.path.isdir(full):
            if not recursive:
                raise ShellError("rm: %s is a folder — use rm -r to remove it" % a)
            shutil.rmtree(full)
        else:
            os.remove(full)
    return ""


def cmd_tree(args, stdin):
    root = _need(args[0]) if args else _resolve(".")
    lines = [args[0] if args else "."]
    ndirs, nfiles = 0, 0

    def walk(path, prefix):
        nonlocal ndirs, nfiles
        names = sorted(n for n in os.listdir(path) if not n.startswith("."))
        for i, n in enumerate(names):
            child = os.path.join(path, n)
            last = i == len(names) - 1
            lines.append(prefix + ("└── " if last else "├── ") + _listing_name(child, n))
            if os.path.isdir(child):
                ndirs += 1
                walk(child, prefix + ("    " if last else "│   "))
            else:
                nfiles += 1

    walk(root, "")
    lines.append("")
    lines.append("%d folders, %d files" % (ndirs, nfiles))
    return "\n".join(lines)


def cmd_find(args, stdin):
    flags, operands, _ = _split_flags(args)
    start, pattern, kind = ".", None, None
    rest = list(args)
    if rest and not rest[0].startswith("-"):
        start = rest.pop(0)
    i = 0
    while i < len(rest):
        if rest[i] == "-name" and i + 1 < len(rest):
            pattern = rest[i + 1]
            i += 2
        elif rest[i] == "-type" and i + 1 < len(rest):
            kind = rest[i + 1]
            i += 2
        else:
            raise ShellError("find: this shell understands only -name and -type")
    root = _need(start, "folder")
    import fnmatch

    base = start.rstrip("/") if start != "/" else ""

    def matches(name, t):
        if kind and t != kind:
            return False
        return not pattern or fnmatch.fnmatch(name, pattern)

    hits = []
    # Depth-first, pre-order — the order real find reports, starting with the
    # folder you asked about.
    if matches(os.path.basename(root) or "/", "d"):
        hits.append(start)

    def walk(path, shown):
        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            here = shown + "/" + name
            if os.path.isdir(full):
                if matches(name, "d"):
                    hits.append(here)
                walk(full, here)
            elif matches(name, "f"):
                hits.append(here)

    walk(root, base)
    return "\n".join(hits)


def cmd_grep(args, stdin):
    flags, operands, _ = _split_flags(args)
    if not operands:
        raise ShellError("grep: needs a pattern")
    pattern, files = operands[0], operands[1:]
    ignore = "i" in flags
    needle = pattern.lower() if ignore else pattern
    out, count = [], 0
    if files:
        for f in files:
            with open(_need(f)) as fh:
                for num, line in enumerate(fh.read().splitlines(), 1):
                    hay = line.lower() if ignore else line
                    if needle in hay:
                        count += 1
                        prefix = (f + ":") if len(files) > 1 else ""
                        if "n" in flags:
                            prefix += "%d:" % num
                        out.append(prefix + line)
    else:
        for num, line in enumerate(stdin.splitlines(), 1):
            hay = line.lower() if ignore else line
            if needle in hay:
                count += 1
                out.append(("%d:" % num if "n" in flags else "") + line)
    if "c" in flags:
        return str(count)
    return "\n".join(out)


def cmd_help(args, stdin):
    return (
        "This is a small teaching shell, not bash. It knows:\n"
        "\n"
        "  moving around   pwd   ls [-a -l]   cd\n"
        "  reading         cat   head [-n N]   tail [-n N]   wc [-l -w -c]\n"
        "  structure       tree\n"
        "  changing        mkdir [-p]   touch   cp [-r]   mv   rm [-r]\n"
        "  searching       find [-name PAT] [-type f|d]   grep [-i -n -c]\n"
        "  other           echo   clear   help\n"
        "\n"
        "It also understands wildcards (*, ?), redirection (>, >>) and one pipe (|).\n"
        "Press the Reset button to put the practice files back as they were."
    )


def cmd_clear(args, stdin):
    return "\x00CLEAR\x00"


_NOT_HERE = {
    "git": "git is real, but it is not in this emulator — see Appendix A3.",
    "python": "this shell cannot start Python; use the runnable cells on the page instead.",
    "python3": "this shell cannot start Python; use the runnable cells on the page instead.",
    "pip": "there is no package installer here — see Appendix A1 for pip on your own machine.",
    "sudo": "there are no users or permissions in this emulator, so nothing to sudo.",
    "apt": "there is no package manager here.",
    "vim": "there is no text editor here. Use echo with > to write a file.",
    "nano": "there is no text editor here. Use echo with > to write a file.",
    "man": "no manual pages here — type help for the command list.",
    "ssh": "there is no network in this emulator.",
    "curl": "there is no network in this emulator.",
}

COMMANDS = {
    "pwd": cmd_pwd,
    "ls": cmd_ls,
    "cd": cmd_cd,
    "cat": cmd_cat,
    "head": cmd_head,
    "tail": cmd_tail,
    "wc": cmd_wc,
    "echo": cmd_echo,
    "mkdir": cmd_mkdir,
    "touch": cmd_touch,
    "cp": cmd_cp,
    "mv": cmd_mv,
    "rm": cmd_rm,
    "tree": cmd_tree,
    "find": cmd_find,
    "grep": cmd_grep,
    "help": cmd_help,
    "clear": cmd_clear,
}


# --------------------------------------------------------------------------
# Running a line: pipes, then redirection, then the command itself
# --------------------------------------------------------------------------


def _run_segment(toks, stdin):
    """Run one pipeline segment. toks is a list of [text, quoted]."""
    redirect, mode = None, "w"
    clean = []
    i = 0
    while i < len(toks):
        text, quoted = toks[i]
        if not quoted and text in (">", ">>"):
            if i + 1 >= len(toks):
                raise ShellError("%s needs a file name after it" % text)
            mode = "w" if text == ">" else "a"
            redirect = toks[i + 1][0]
            i += 2
            continue
        clean.append(toks[i])
        i += 1
    if not clean:
        raise ShellError("nothing to run before the >")

    name = clean[0][0]
    args = []
    for text, quoted in clean[1:]:
        args.extend(_expand(text, quoted))

    if name in _NOT_HERE:
        raise ShellError("%s: %s" % (name, _NOT_HERE[name]))
    if name not in COMMANDS:
        raise ShellError(
            "%s: unknown command. This is a small teaching shell — type help "
            "to see what it knows." % name
        )

    out = COMMANDS[name](args, stdin)
    if redirect is not None:
        full = _resolve(redirect)
        parent = os.path.dirname(full)
        if not os.path.isdir(parent):
            raise ShellError("%s: the folder does not exist" % redirect)
        with open(full, mode) as fh:
            fh.write(out if out.endswith("\n") or not out else out + "\n")
        return ""
    return out


def shell_run(line):
    result = {"out": "", "clear": False, "prompt": shell_prompt()}
    line = line.strip()
    if not line:
        return json.dumps(result)
    try:
        toks = _tokenize(line)
        segments, cur = [], []
        for t in toks:
            if t[0] == "|" and not t[1]:
                segments.append(cur)
                cur = []
            else:
                cur.append(t)
        segments.append(cur)
        if any(not s for s in segments):
            raise ShellError("a | needs a command on both sides")
        data = ""
        for seg in segments:
            data = _run_segment(seg, data)
        if data == "\x00CLEAR\x00":
            result["clear"] = True
        else:
            result["out"] = data
    except ShellError as exc:
        result["out"] = str(exc)
        result["error"] = True
    except OSError as exc:
        result["out"] = getattr(exc, "strerror", None) or str(exc)
        result["error"] = True
    result["prompt"] = shell_prompt()
    return json.dumps(result)


shell_reset()
