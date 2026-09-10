# Lecture 1.1 conversion notes

The HTML lecture retains the 23-slide sequence and exercises. The latest
`../course materials/deck1_1.pptx` removes the AoL labels and closing picture. The following corrections apply to the HTML adaptation; the source PPTX and PDF remain unchanged.

| Source slide | Correction |
| --- | --- |
| 3 | Tighten the two paragraphs for a readable web layout; retain the six mathematical expressions and original video. Describe binding a name to an object, including reuse of an existing object, without implying every assignment allocates a new object. |
| 4 | Replace the unrelated caption “Example 0.6.3 picture generation” with “Quick verification · names and object identity.” The code is unchanged. |
| 5 | Clarify that `id()` returns an object's identity, unique during its lifetime. Its value is the memory address in CPython; that is not a guarantee for every Python implementation. |
| 9 | Add `import sys` before the original `sys.getsizeof(a)` call. The earlier example supplies `a`. |
| 10 | Replace the typographic en dash in `c = 3.14 – 5j` with the executable ASCII minus: `c = 3.14 - 5j`. |
| 16 | Clarify that some list methods mutate the list, while other methods do not. Tuple methods do not mutate the tuple. |
| 18 | Replace typographic quotation marks with straight Python string delimiters. Mark tuple item assignment, including `t[2] = "tuple"`, as invalid. Correct `l.extend((5))` to `l.extend((5,))`, which supplies an iterable. Explain that a check mark means the expression or operation is valid, not that its result is `True`; for example, `2 in (4, 5, 6)` is valid and evaluates to `False`. |
| 20 | Distinguish constructing a slice with `slice(start, stop, step)` from subscription syntax such as `items[start:stop:step]`. Parentheses alone do not turn colon notation into a slice object. |
| 22 | Clarify that `array` elements share a declared type, rather than the same value. Replace the blanket speed claim with the narrower point that arrays store homogeneous values compactly and performance depends on the operation and workload. |
| 13, 23 | Use “values in a container” and “names refer to objects” to keep the distinction between a name and its object clear. |

Source assets are copied byte-for-byte from the PPTX. Slide 19's explanatory labels remain separate from its diagram image. Off-canvas and covered pictures from slide 23, and slide 3's alternate text-rendering fallback image, are not added as new lecture content.

Grammar, punctuation, and line breaks are lightly edited throughout for the web.
Exercise numbering and open questions are preserved; no exercise solutions are
added. Slide 18 retains its intentionally failing examples, with error comments
instead of ambiguous ticks. Run those statements individually in a notebook.

Accuracy references: Python's official documentation for
[`id`](https://docs.python.org/3/library/functions.html#id),
[`slice`](https://docs.python.org/3/library/functions.html#slice),
[lists and tuples](https://docs.python.org/3/tutorial/datastructures.html), and
[`array`](https://docs.python.org/3/library/array.html).
