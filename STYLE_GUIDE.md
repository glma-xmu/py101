# Course Textbook — Style & Structure Guide

This guide defines how every chapter page is written and formatted. The goal is a
**textbook**: a student-friendly surface that a beginner can read top to bottom,
with real depth available for the curious. It is a reference for authors; it is
not published on the site (it lives outside `docs/`).

## Guiding principles

1. **Teach Python as it is used today.** Prefer current, idiomatic practice over
   dated tricks. Use f-strings, not `%` or `.format()`; iterate directly
   (`for item in items:`) or with `enumerate()`/`zip()`, never
   `for i in range(len(items))`; prefer comprehensions and built-ins
   (`sum`, `any`, `sorted`, `set`, `dict`) over hand-rolled loops; reach for the
   standard library (`pathlib`, `dataclasses`, `collections`) where a beginner
   would otherwise reinvent it. If a technique survives only in old textbooks,
   leave it out — or, if it is still worth recognising, flag it in a Deep dive as
   historical.

2. **Earn the "university" edge with depth, placed where it won't slow beginners.**
   Students should leave understanding *how Python actually works* — a real feel
   for the object model and CPython's memory (identity, references, what `id()`
   and `sys.getsizeof()` reveal). Put this rigour in **Deep dive** blocks: it
   gives motivated students an edge over self-taught and high-school learners
   without burdening a first-timer reading the main thread.

3. **Every Example states its purpose first.** Precede each Example block with a
   one-sentence lead-in saying what it demonstrates and why it matters, so the
   student knows what to look for before reading the code.

## Voice

- Write in complete sentences and connected paragraphs, not slide fragments.
- Explain *why*, not just *what*. Lead with intuition, then make it precise.
- Address the student directly ("you"), warmly but not chatty.
- Define a term the first time it appears; thereafter use it confidently.
- Prose carries the main thread. Lists are only for genuine enumerations, and
  each item is a complete clause.
- **Bridge every section.** Open each section (and subsection) with a short
  passage that says what it covers and how it connects to what came before and
  what follows. Never jump straight from a heading into a subheading, a list, or
  a code block — orient the reader first. Err on the side of *more* connective
  prose; generous, flowing exposition is preferred over terse coverage.

## Depth without clutter

Keep the main narrative readable by a beginner. Push implementation detail,
edge cases, and honest nuance into **Deep dive** blocks (collapsed by default),
so the surface stays smooth while the depth is one click away.

## The five blocks (the only special blocks we use)

Prose is the default. Use a block only when the reader should treat the content
differently from the main line. Do not introduce other admonition types.

| Block | Markdown | Use it for |
|-------|----------|------------|
| **Key concept** | `!!! note "Key concept: …"` | A formal definition of a new term. One per genuinely new concept. |
| **Example** | `!!! example "Example: …"` | A self-contained, referenceable worked demonstration, **preceded by a one-sentence lead-in** stating its purpose. (Code that is part of an explanation stays **inline**, not boxed.) |
| **Exercise** | `!!! question "Exercise: …"` | A task for the student. |
| **Pitfall** | `!!! warning "Pitfall: …"` | A common beginner mistake or gotcha. |
| **Deep dive** | `??? info "Deep dive: …"` | Optional depth: implementation details, honest nuance, advanced asides. Collapsed by default. |

Notes:

- Indent block content by 4 spaces. Always leave a blank line before any list,
  table, or code block (MkDocs swallows them otherwise).
- **`Example` blocks are automatically runnable.** `runnable.js` turns every
  Example admonition into an editable, in-browser Python cell (Pyodide) with a
  Run button — no per-block marking needed. So any snippet a student should run
  and tinker with belongs in an Example block; illustrative code that should
  *not* be run (deliberate errors, fragments) stays in a plain fenced block.

## Section numbering

- The page `# Title` (H1) is unnumbered.
- **Introduction** and **Summary/Review** are unnumbered.
- All other sections are numbered per page, restarting at 1 on each page:
  `## 1.`, `## 2.` for H2; `### 1.1`, `### 1.2` for H3; `#### 1.1.1` for H4.

## Page skeleton

```
# Page Title

## Introduction        (unnumbered: what this page covers, why it matters)

## 1. First topic
   ... prose, inline code, blocks ...

## 2. Second topic
   ...

## Summary             (unnumbered: recap + a table where useful)
```

## Organizing type material — the two axes

Type content is organized around two questions, introduced early and reused:

1. **What does it hold?** — scalar/atomic (numbers, `None`) vs. container
   (sequences, sets, mappings).
2. **Can it change?** — mutable vs. immutable.

Every built-in type is a point in that 2×2 grid. Cover all built-ins
(`int`, `float`, `complex`, `bool`, `None`, `str`, `bytes`, `bytearray`,
`list`, `tuple`, `range`, `set`, `frozenset`, `dict`), and treat **mutability**
as a first-class concept (it ties together identity, aliasing, and hashability),
with the "is the line really fundamental?" discussion in a Deep dive.

## Bilingual rule

Every page exists as `name.en.md` (English, default) and `name.zh.md` (中文),
kept structurally parallel: same sections, same numbering, same blocks. The
duplicate `name.md` mirrors the English file.

## Memory diagrams

To visualise how names refer to objects, use a `memory` fenced block. It is
**object-centric**: the framed box is *memory* and holds objects shown as
value · address · type; names live outside (a namespace) and arrow *into* the
object they refer to. Multiple names pointing at one object key share it (use
this to show aliasing). This reinforces Ch1's motto, *everything is an object*.

```
​```memory
memory: Heap                 # title of the memory box (optional)
namespace: namespace         # label above the names (optional)
objects:
  o1: int 1 @ 0x123456       # <type> <value> [@ <address>]; address optional
names:
  a -> o1
  b -> o1
​```
```

Use these wherever the *name → object* relationship is the teaching point —
especially first binding, `b = a` aliasing, rebinding, and mutate-in-place vs.
new-object. Keep diagrams small (a handful of names/objects); for full
step-through execution of larger programs, a self-hosted Python Tutor embed is
the future option.

## Chapter motto (epigraph) and callbacks

Each chapter opens with a **motto** — a short, memorable thesis the chapter
revolves around — placed right under the title with a `motto` block. When the
text later *demonstrates* that motto, mark the moment with a `recall` block that
restates it in one sentence. This anchors students and pays the idea off
repeatedly. Mottos should be the ones the material already turns on (Ch1:
*everything in Python is an object* leads, with *names refer to objects*
introduced in §1; Ch2: *functions are first-class objects*). These are
structural devices, not admonitions, so the five-block rule still holds.

```
​```motto
Everything in Python is an object.
​```

​```recall
Names refer to objects: a and b are two labels on one list, so changing it
through either name changes it for both.
​```
```

Rule of thumb: **one motto per chapter**, and a `recall` only where the concept
visibly shows itself (an example, a diagram, a surprising result) — not on every
paragraph, or it loses force.

## Collapsible blocks, reading mode, and live memory

- All five blocks are authored collapsible and **open by default** using `???+`
  (e.g. `???+ note "Key concept: …"`). Deep dives stay `???` (collapsed).
- A page-level **"Fold all blocks"** toggle (reading-mode.js) lets a student
  collapse every block to read the prose straight through, then unfold to dig in.
- **Live memory:** every Example cell has a **Show memory** button. It re-runs the
  cell in a fresh namespace and draws the object-centric memory diagram from the
  *real* run — actual types and addresses, with names that share an object
  converging on it (aliasing shown automatically). This complements the
  hand-authored `memory` diagrams: curated diagram to introduce a concept, live
  diagram to explore.

Note for authors: collapsible admonitions render as `<details class="example">`
(etc.) — the runnable-cell script matches both `.admonition.example` and
`details.example`, so Examples stay runnable whether or not they are collapsible.
