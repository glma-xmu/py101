# Chapters 1–3 conversion notes

The library contains 11 decks and 265 slides. This expansion adds 10 decks and
242 slides to the existing 23-slide Lecture 1.1 pilot. Source PowerPoint files
remain unchanged under the ignored `resource/` directory.

| HTML source | Original PowerPoint | Slides |
| --- | --- | ---: |
| lecture-1-2.md | deck1_2_AoL.pptx | 31 |
| lecture-1-3.md | deck1_3_project.pptx | 6 |
| lecture-2-1.md | deck2_1_AoL.pptx | 25 |
| lecture-2-2.md | deck2_2_AoL.pptx | 13 |
| lecture-2-3.md | deck2_3_AoL.pptx | 35 |
| lecture-2-project.md | deck2_project_AoL.pptx | 10 |
| lecture-3-1.md | deck3_1.pptx | 33 |
| lecture-3-2.md | deck3_2_AoL.pptx | 36 |
| lecture-3-3.md | deck3_3_26S-AoL.pptx | 31 |
| lecture-3-4.md | deck3_4-26S_Aol.pptx | 22 |

## Adaptation

- Preserve the source sequence, exercise numbering, AoL labels, examples, and
  source attributions. Title slides name the particular lecture rather than
  repeating the same chapter title on every deck.
- Text and code are native HTML in editable Markdown sources. Tables remain
  HTML tables. Office equations become native MathML, including fractions,
  matrices, roots, subscripts, and superscripts. Inline wrappers keep Markdown
  from splitting equation paragraphs.
- Artwork is cropped from local PowerPoint renders to preserve source drawing
  appearance. These are supporting figures, not screenshots of whole slides.
  The LEGB drawing is expressed as a table with the same namespaces, scope
  contexts, and `global`/`nonlocal` labels.
- Contents sections follow the lecture topics. Text links use the matching
  textbook section; background-only links for project exercises are marked
  `related: true`. Chapter 3 uses the site's existing English content fallback
  under Chinese navigation; no missing Chinese translations are invented.
- Historical classroom announcements are labeled as historical. Dataset paths
  are retained as classroom examples; importing the slides does not publish
  data files or execute network/download examples.
- Explicitly invalid assignment exercises and incomplete syntax templates use
  plain-text fences. Valid examples remain Python fences with Copy controls.
  Runtime errors and unfinished logic used as questions remain questions.

## Source corrections

Smart quotes and non-breaking indentation in code are normalized. Adjacent
PowerPoint text runs are joined so that code is copyable without visual gaps.
Paragraphs and code are arranged into columns where necessary for readability.

| Deck / source slide | Correction in HTML |
| --- | --- |
| 1.2 / 3, 5 | Describe dictionary lookup by hashable keys, not only names/strings; distinguish `KeyError` from `get()` defaults. |
| 1.2 / 14 | `None` is a singleton that multiple names can refer to; use `is None`. Remove the incorrect claim about a sole name called Null. |
| 1.2 / 20, 23, 25, 28 | Clarify strings as immutable Unicode sequences, `{}` as an empty dictionary, Pythonic style as idiomatic rather than unique syntax, and conversion versus mutation. |
| 1.2 / 27 | State the required `time` import without supplying an exercise solution. |
| 2.1 / 2, 16, 19, 21 | Correct “first-order” to “first-class,” `f[3]()` to `ff[3]()`, and `dir(globals)` to `globals()`; preserve the function-factory puzzle. |
| 2.1 / 11–12 | Distinguish function signatures from calls and clarify required records. Make grade intervals non-overlapping and correct the supplied expected output to C/C/B for 60/70/80. |
| 2.2 / 8, 10, 12 | `args`/`kwargs` are conventional names, not keywords. `*args` collects a tuple; iterable unpacking is more general than lists. Clarify positional, keyword-only, and default parameter ordering. |
| 2.3 / 9–12 | Define recursion as self-calling rather than passing a function to itself. Match the Newton code's `x**2 - 3` to its equation. Remove a stray colon from the intentionally unfinished recursion example and label its missing update/stopping condition. |
| 2.3 / 23, 27, 30 | Add the missing `functools.reduce` import; clarify accumulator compatibility and generator resumption; replace undefined `i` in the single-image save example with `mnist1.png`. |
| 2 project / 9 | Correct the circular secant formula's previous-point index from n+1 to n−1. Retain the absolute-value root problem as an open exercise. |
| 3.1 / 2, 4, 10, 13, 17, 28 | Label the old announcement, distinguish notebook `%pip` from terminal installation, fix `arange`, use int64 in the squaring benchmark, clarify row broadcasting, and distinguish `np.vectorize` convenience from compiled ufunc performance. |
| 3.2 / 10, 11, 28 | Clarify Series dtype versus object contents; include NumPy/pandas imports; explain `.loc` as label-based and `.iloc` as position-based for both axes. |
| 3.3 / 10, 28 | Distinguish string conversion from `.str` methods; correct the stated column count; distinguish a market-value-weighted price level from a portfolio return. |
| 3.4 / 7–10, 12 | Restore missing string quotes and the source table's score of 75; distinguish inner/outer rules from left/right rosters; describe five common join modes rather than an exhaustive version-dependent count; organize the identifier-linking exercise without adding a solution. |

Technical references used for the corrections:
[Python function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions),
[NumPy vectorize](https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html),
[pandas indexing](https://pandas.pydata.org/docs/user_guide/indexing.html), and
[pandas merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html).

## Verification

`mkdocs build --strict` and `scripts/check_slides.py` check every source count,
all local assets, EN/ZH destinations, three deployment prefixes, and Python
syntax without executing exercises. The checker also covers untranslated
textbook fallback handling. Browser layout inspection measures the converted
slides at the player's 1280 × 720 design size, with visual review of code,
equations, figures, tables, Contents, reading mode, and mobile layout.

Edit the committed Markdown directly for future teaching changes. No Office
installation or conversion service is needed for normal builds or deployment.
