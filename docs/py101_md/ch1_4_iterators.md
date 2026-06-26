# Iterables and Iterators

## Introduction

In **1.3 Control Flow** the `for` loop simply *worked* — on lists, strings, dictionaries, and ranges alike. But how does it actually walk them? And why can it walk a `range`, or a generator expression, that never builds a full list in memory? The answer is a small, elegant contract called the **iterator protocol**. Understanding it explains the laziness behind `range` (from 1.2) and generator expressions (from 1.3), and it lets you build your own on-demand sequences. As always, the code here is live.

## 1. Iterables: what a `for` loop needs

An **iterable** is any object a `for` loop can walk. The loop's very first move is to call the built-in `iter()` on the object — and that only works if the object provides a special method called `__iter__`.

???+ note "Key concept: iterable"
    An **iterable** is an object that implements `__iter__`, so that `iter(obj)`
    succeeds and hands back an *iterator*. Lists, tuples, strings, dictionaries,
    sets, ranges, and file objects are all iterable.

The example below shows `iter()` succeeding on a list and failing on an integer — the difference is precisely whether the object carries `__iter__`.

???+ example "Example: what is iterable?"
    ```python
    a = [1, 2, 3]
    it = iter(a)                   # works: a list is iterable
    print(it)                      # <list_iterator object ...>

    print(hasattr(a, "__iter__")) # True
    print(hasattr(1, "__iter__")) # False — ints are not iterable
    # iter(1)                      # would raise: TypeError: 'int' object is not iterable
    ```

```recall
Everything is an object: being "iterable" is not a magic category — it just means the object carries an `__iter__` method, the same way every object carries a type and a value.
```

??? info "Deep dive: the legacy `__getitem__` route"
    Before `__iter__` existed, a `for` loop could walk any object that supported
    integer indexing via `__getitem__` (`obj[0]`, `obj[1]`, …), stopping when an
    `IndexError` was raised. Python still honours this fallback, so very old
    sequence types remain iterable. In modern code, define `__iter__` — it is the
    explicit, standard way to make an object iterable.

## 2. Iterators: producing one value at a time

Calling `iter()` returns an **iterator** — the object that actually produces the values. An iterator implements `__next__`, which the built-in `next()` calls to fetch the next item; when there are no items left, `__next__` raises `StopIteration`. A `for` loop is really just this dance: get an iterator with `iter()`, call `next()` over and over, and stop when `StopIteration` is raised.

???+ note "Key concept: iterator"
    An **iterator** produces values on demand. It implements `__next__` (returns
    the next value, or raises `StopIteration` when exhausted) and `__iter__`
    (which returns `self`). So every iterator is also iterable — but a plain
    iterable, like a list, is *not* itself an iterator until you call `iter()` on it.

The example below drives the protocol by hand, exactly as a `for` loop does under the hood.

???+ example "Example: iterating by hand with next()"
    ```python
    it = iter([10, 20, 30])
    print(next(it))   # 10
    print(next(it))   # 20
    print(next(it))   # 30
    # next(it)        # StopIteration — nothing left to hand back
    ```

???+ warning "Pitfall: an iterator is single-use"
    An iterator is exhausted once you walk it to the end — there is no rewind. A
    fresh `iter()` (or a new `for` loop over the original *iterable*) gives you a
    new iterator. This is why looping over the same `range` twice works (each loop
    calls `iter()` again), but looping over the same generator twice does not.

## 3. Why it matters: lazy evaluation

The whole point of separating iterators from iterables is **lazy evaluation**: an iterator does not compute or store all its values up front. It produces each value only when asked. That buys three things — the ability to handle data too big for memory (the lines of a multi-gigabyte file), to represent conceptually *infinite* sequences, and to skip work for items you never look at.

The example below makes the saving concrete: a real list of a million integers costs megabytes, while the lazy `range` that represents the same numbers stays tiny.

???+ example "Example: lazy range vs. a real list"
    ```python
    import sys
    big  = list(range(1_000_000))   # actually builds a million-element list
    lazy = range(1_000_000)         # stores only start, stop, step
    print(sys.getsizeof(big) > 1_000_000)  # True — megabytes
    print(sys.getsizeof(lazy))              # a few dozen bytes, constant
    ```

This is the same laziness you met with `range` in 1.2 and generator expressions in 1.3 — now you can see it is the iterator protocol underneath.

## 4. Generators: the easy way to make an iterator

Writing `__iter__` and `__next__` by hand is rare. The everyday way to create an iterator is a **generator function**: an ordinary `def` that uses `yield` instead of `return`. Each `yield` hands back a value and *pauses* the function, freezing its state; the next call to `next()` resumes right after the `yield`. The result is a lazy iterator you got almost for free — and the generator *expressions* from 1.3 are simply its compact cousin.

???+ note "Key concept: generator"
    A **generator** is an iterator produced by a function containing `yield` (or by
    a generator expression). It computes each value on demand and remembers where
    it left off between calls.

The example below defines a small generator and walks it with a `for` loop and with `list()`.

???+ example "Example: a generator function"
    ```python
    def countdown(n):
        while n > 0:
            yield n        # hand back n, then pause here
            n -= 1

    for x in countdown(3):
        print(x)           # 3, 2, 1

    print(list(countdown(5)))   # [5, 4, 3, 2, 1]
    ```

Because values come one at a time, a generator can even describe an *endless* sequence — you just stop taking values when you have enough.

???+ example "Example: an effectively infinite generator"
    ```python
    def squares():         # conceptually infinite
        n = 1
        while True:
            yield n * n
            n += 1

    g = squares()
    print(next(g), next(g), next(g))   # 1 4 9 — only what we asked for is computed
    ```

???+ question "Exercise: iterators and generators"
    1. Use `iter()` and `next()` to pull the first two items out of the string `"hi"` by hand.
    2. Write a generator `evens(limit)` that yields 0, 2, 4, … up to (not including) `limit`, and print `list(evens(10))`.
    3. Write a generator that yields the powers of two (1, 2, 4, 8, …) and use it to print the first five.

??? info "Deep dive: expression vs. function"
    A generator *expression* — `(x*x for x in range(5))` from 1.3 — and a generator
    *function* with `yield` produce the same kind of lazy iterator. Reach for the
    expression when the logic fits on one line; write a function with `yield` when
    you need loops, conditions, or state that a single expression cannot express.

## Summary

The iterator protocol is the quiet machinery beneath every loop:

| Term | Implements | Role |
|------|-----------|------|
| **Iterable** | `__iter__` | can be handed to `iter()` / a `for` loop (list, str, dict, `range`, …) |
| **Iterator** | `__iter__` (returns `self`) + `__next__` | produces values one at a time via `next()`, raising `StopIteration` when done |
| **Generator** | a `def` with `yield`, or a `(… for …)` expression | the easy, lazy way to build an iterator |

In practice you will almost never build your own iterable from scratch. The everyday workflow runs the other way: you take one of Python's built-in iterables and get an iterator from it — explicitly with `iter()`, or implicitly the moment a `for` loop, a comprehension, or `list()` walks it. And when you need to *produce* a sequence yourself, you reach for a **generator**, the easiest way to get something with the full power of an iterator. The three ideas nest inside one another — every generator is an iterator, and every iterator is an iterable:

<div style="text-align:center;margin:1.2rem 0;">
<svg viewBox="0 0 360 340" xmlns="http://www.w3.org/2000/svg" role="img" width="320" style="max-width:100%;height:auto;font-family:-apple-system,Segoe UI,Roboto,sans-serif;">
  <title>Iterables contain iterators, which contain generators</title>
  <desc>Three nested circles: the outer is Iterables, defined by __iter__; the middle is Iterators, which add __next__; the inner is Generators, a special iterator created by a yield function or a generator expression.</desc>
  <circle cx="180" cy="185" r="150" fill="none" stroke="var(--md-primary-fg-color, #3f6ec6)" stroke-width="1.6"/>
  <circle cx="180" cy="185" r="104" fill="none" stroke="var(--md-primary-fg-color, #3f6ec6)" stroke-width="1.6"/>
  <circle cx="180" cy="185" r="58" fill="none" stroke="var(--md-primary-fg-color, #3f6ec6)" stroke-width="1.6"/>
  <text x="180" y="56" text-anchor="middle" font-size="15" font-weight="700" fill="var(--md-default-fg-color, #222222)">Iterables</text>
  <text x="180" y="74" text-anchor="middle" font-size="12" font-family="monospace" fill="var(--md-default-fg-color--light, #666666)">__iter__</text>
  <text x="180" y="104" text-anchor="middle" font-size="15" font-weight="700" fill="var(--md-default-fg-color, #222222)">Iterators</text>
  <text x="180" y="122" text-anchor="middle" font-size="12" font-family="monospace" fill="var(--md-default-fg-color--light, #666666)">+ __next__</text>
  <text x="180" y="181" text-anchor="middle" font-size="14" font-weight="700" fill="var(--md-default-fg-color, #222222)">Generators</text>
  <text x="180" y="199" text-anchor="middle" font-size="11" font-family="monospace" fill="var(--md-default-fg-color--light, #666666)">yield / (… for …)</text>
</svg>
</div>

A `for` loop is just `iter()` followed by repeated `next()` until `StopIteration`. Separating the iterator from the iterable enables **lazy evaluation** — the reason `range`, generator expressions, and your own generators can stand in for sequences that would never fit in memory. With Chapter 1's foundations in place — objects and types, collections, control flow, and now iteration — you are ready to package logic into reusable units in **Chapter 2: Functions**.
