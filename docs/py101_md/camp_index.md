# The Two-Day Python Crash Course

```motto
You already know some Python. This is where you learn what it was doing all along.
```

## Introduction

This section is a self-contained **two-day crash course**, written for incoming graduate students who arrive already able to write Python — a loop here, a `pandas` call there — but who have never been shown *why* the language behaves the way it does. It has been taught live several times; the pages below are the course notes, kept at their original chapter and example numbering so that they still line up with the lecture recordings.

It is deliberately a different animal from Chapters 1–3 of this site. Those chapters build Python from nothing, slowly, for someone meeting a `list` for the first time. This one assumes you have already written working code and goes after the layer underneath it: what a name really is, what happens to a stack frame when you call a function, why `@property` is a special case of something more general, and where the time goes when your estimation script takes forty minutes.

## What to expect

The original opening slide set four expectations, and they still hold:

- **A memory refresh, not a firehose.** Most of what follows will be familiar in outline. The value is in the corners you skipped.
- **Coding philosophy over pragmatics.** You will not leave with a cookbook. You will leave able to *read* the documentation and other people's code.
- **Reading errors and writing bugs.** Time spent understanding a traceback now is time you do not spend guessing later.
- **A complement, not a replacement.** If you missed a class in the main course, or took Python somewhere else, this fills gaps rather than repeating the main sequence.

Nothing here requires a Python on your own machine: as everywhere on this site, the code cells run in your browser. A few examples are about things a browser genuinely cannot do — compiling a C extension, timing a long computation, connecting to WRDS — and those are shown as plain, non-runnable code with instructions for your own machine.

## The seven chapters

The course runs over two days, four chapters then three. The second day is heavier per chapter, which is why it is shorter.

| | Chapter | What it is really about |
|---|---------|-------------------------|
| **Day 1** | [1. Style and Error Messages](camp_ch1_style.md) | PEP 8, and how to read a traceback instead of fearing it |
| | [2. Environments and Tooling](camp_ch2_environments.md) | `venv`, `conda`, and where your code should live |
| | [3. Names, Expressions, Statements](camp_ch3_names.md) | Names are not variables; namespaces, LEGB, and the grammar underneath |
| | [4. Functions](camp_ch4_functions.md) | Frames, `yield`, higher-order functions, decorators, recursion |
| **Day 2** | [5. Object-Oriented Python](camp_ch5_oop.md) | Members, `__call__`, descriptors behind `@property`, inheritance and the MRO |
| | [6. Data Manipulation with pandas](camp_ch6_pandas.md) | Reshaping, pipelines, and the alignment rule that silently ruins results |
| | [7. Making Python Fast](camp_ch7_performance.md) | Containers, laziness, Cython, Numba — and measuring before you optimise |

!!! tip "How this fits the main course"
    Several topics appear on both sides of the site, at different depths. Where that
    happens, the crash-course page links across, so you can drop into the slower
    treatment when you want it:

    | Crash course | Main course |
    |--------------|-------------|
    | 2. Environments and Tooling | [A1 Setting Up Your Python Environment](appendix_a1_environment.md), [A2 The Command Line and Paths](appendix_a2_shell.md) |
    | 3. Names, Expressions, Statements | [1.1 Objects and Types](ch1_1_objects.md), [2.2 Namespaces and Scope](ch2_2_namespaces_scope.md) |
    | 4. Functions | [2.1 Defining Functions](ch2_1_defining_functions.md), [2.3 First-Class Objects](ch2_3_first_class.md), [2.4 Use Cases](ch2_4_use_cases.md) |
    | 6. Data Manipulation with pandas | [3.1 NumPy](ch3_1_numpy.md) |

## A note on the numbering

Sections here are numbered by chapter — `3.1`, `3.2.1`, `Example 5.7` — rather than restarting on each page as they do elsewhere on this site. That is on purpose: each page *is* a chapter of the two-day course, and the recordings refer to these numbers. Where the original notes reused a number for two different examples, both keep the number and are told apart by their titles.

## Where the drawing happens

The live course was punctuated by moments marked 🎨 **Time to draw!** — the point where the lecturer stopped and drew boxes and arrows on the board, because the idea only lands as a picture. Those markers are kept. Where the picture is now on the page as a diagram, it says so; where it is not, treat it as an instruction: stop, get paper, and draw it yourself before reading on. That habit is most of what separates people who can debug from people who guess.
