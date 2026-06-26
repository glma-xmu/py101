# Objects and Types

```motto
Everything in Python is an object.
```

## Introduction

Before you can write a useful Python program, you need a clear picture of the *stuff* a program manipulates. In Python that stuff has a single, unifying name: every piece of data — a number, a piece of text, a list of results, even a function — is an **object**. This page builds your mental model of objects, and then uses two simple questions to organise every built-in type Python gives you. By the end you should be able to look at any value and say what it is, what you can do with it, and whether it can change.

A helpful analogy: if a program is a building, objects are the materials and types are the *kinds* of material. Knowing your materials — which are rigid, which are flexible, which hold other things — is what lets you design something that stands up.

Most of the code on this page is **live**: edit it and press *Run* (or Ctrl/Cmd+Enter) to execute it right here in your browser, then change it and run again. The best way to learn these ideas is to poke at them.

## 1. Objects: identity, type, and value

Programming is, in large part, the art of putting mathematical ideas into practice, and the most important idea it borrows from mathematics is abstraction. The most elementary abstraction is the **variable**. You have met it before: in primary school you counted with concrete numbers like 1, 2, 3, and in middle school you used a symbol such as $x$ to stand for a generic number that might be 1, 2, or 100. That versatility is the whole point.

In Python we call such a symbol a **name**. When you write `x = 1`, Python sets aside a chunk of memory holding the value `1`, and then *binds* the name `x` to that object. The name is a label; the object is the thing the label points to.

???+ note "Key concept: object"
    An **object** is a piece of data living in memory with a well-defined structure. Every object carries three things at once:

    - its **identity** — a unique identifier (in CPython, its memory address), read with `id()`;
    - its **type** — what kind of thing it is, which fixes the values it can hold and the operations it allows, read with `type()`;
    - its **value** — the actual data it stores.

You have already met this chapter's motto — *everything in Python is an object*. Here in Section 1 we add its companion principle, the one that makes assignment make sense: **names refer to objects**. Binding a name never copies a value; it simply attaches another label to an object that already exists.

The example below demonstrates that assignment binds a name to an object rather than copying a value — run it and watch how two names end up sharing one identity.

???+ example "Example: a name points to an object"
    ```python
    a = 1
    print(id(a))   # the identity (address) of the object 1
    print(type(a)) # the type: <class 'int'>

    b = a
    print(id(b))   # same number as id(a): b points to the SAME object
    ```

    `a` and `b` are two labels on one object. We did not copy the value `1`; we
    added a second name for it.

The picture below captures what just happened: in the global namespace, the names `a` and `b` are two drawers, and both arrows point to the **same** object in memory.

```memory
memory: Heap
objects:
  o1: int 1 @ 0x123456
names:
  a -> o1
  b -> o1
```

*The address is illustrative — what matters is that every object has one (see the deep dive below).*

```recall
The motto in action: the value 1 is not tied to a name. It lives in memory as an object, and a and b are just labels pointing at it.
```

This example already uses three tools you will reach for constantly: `print()` displays whatever value you pass it, `id()` returns an object's identity, and `type()` returns its type. We also use **f-strings** for formatting — prefix a string with `f` and put an expression in `{}`, as in `f"{id(b):02X}"` to show an identity in hexadecimal.

???+ question "Exercise: names and values"
    1. Bind the name `person_name` to the string `"Alice"`, then print it.
    2. Re-bind `person_name` to `"Bob"`, and use an f-string to print *The current name is Bob.*
    3. Bind a second name to the same object and confirm with `id()` that both names share one object.

??? info "Deep dive: how big is an object, and where does it live?"
    The internal arrangement of an object's data is its **memory layout**. You can ask how many bytes an object occupies with the `sys` module:

    ```python
    import sys
    print(sys.getsizeof(10))           # a small int
    print(sys.getsizeof([1, 2, 3, 4])) # a list
    ```

    Identity (`id`) being the memory address is a *CPython* detail — other Python
    implementations only promise that `id()` is unique and constant for an
    object's lifetime. Rely on the guarantee, not on the address.

??? note "Further reading: how Python runs your code"
    Optional and well beyond this course — for the curious who want to peek at how
    the interpreter actually runs your program and stores your objects:

    - [Python Virtual Machine — concept](https://www.slideshare.net/slideshow/python-virtual-machine-concept-n-kavitha-pptx/272595248) (N. Kavitha, SlideShare) — a gentle picture of the interpreter that executes your code.
    - [*Inside the Python Virtual Machine*](https://leanpub.com/read/insidethepythonvirtualmachine/leanpub-auto-the-view-from-30000ft) (Obi Ike-Nwosu, Leanpub) — start with "The view from 30,000 ft" for the big picture.

## 2. Two questions that organise every type

Python ships with many built-in types, but you do not have to memorise them as a flat list. Almost every one is pinned down by answering two questions.

The first question is **what does it hold?** Some objects are *scalar* (or atomic): they represent one indivisible value, like the integer `7` or the constant `None`. Others are *containers*: they hold other objects, like a list of numbers or a dictionary of name–score pairs.

The second question is **can it change?** This is the property of **mutability**.

???+ note "Key concept: mutable vs. immutable"
    An object is **mutable** if its value can change after it is created, and
    **immutable** if it cannot. Lists, dictionaries, sets, and `bytearray` are
    mutable; numbers, strings, tuples, `frozenset`, and `bytes` are immutable.

Hold these two axes — *scalar vs. container* and *mutable vs. immutable* — in mind. This page covers the **scalar** types; the next page, **1.2 Collections**, takes up the containers and returns to mutability, which turns out to explain a surprising amount.

## 3. Scalar types

We begin with the simplest objects, the **scalars**. A scalar type represents a single, indivisible value: there is nothing "inside" it that you could take apart or iterate over. That makes scalars the natural place to start, before we meet the containers that are built to hold them. Python's scalars are the numbers — which most programs lean on constantly — and the solitary object `None`.

### 3.1 Numbers

Python has three numeric types — `int` (whole numbers), `float` (numbers with a decimal point), and `complex` (numbers with a real and imaginary part) — plus `bool`, the type of `True` and `False`. All four are immutable.

The example below creates one value of each numeric type and prints what Python thinks each one is.

???+ example "Example: the numeric types"
    ```python
    a = 1          # int
    b = 2.0        # float
    c = 3.14 - 5j  # complex
    flag = True    # bool

    print(a, b, c, flag)
    print(type(a), type(b), type(c), type(flag))
    ```

To check what type something is at runtime, use `isinstance()`, which asks whether an object is an instance of a given type. The next example checks a couple of values — including the surprising relationship between `bool` and `int`.

???+ example "Example: checking types with isinstance"
    ```python
    a = 1
    flag = True

    print(isinstance(a, int))     # True
    print(isinstance(flag, bool)) # True
    print(isinstance(flag, int))  # also True — see the pitfall below
    print(flag + 1)               # 2
    ```

???+ warning "Pitfall: `bool` is a kind of `int`"
    `bool` is a *subclass* of `int`, so `True` behaves like `1` and `False` like
    `0` in arithmetic, and `isinstance(True, int)` is `True`. This is usually
    convenient (`sum([True, False, True])` is `2`) but occasionally surprising,
    so remember that a Boolean *is* an integer as far as Python is concerned.

???+ question "Exercise: numbers and `isinstance`"
    1. For each of `a`, `b`, `c`, `flag` above, print its `type()`.
    2. Investigate `False`: what are `isinstance(False, int)` and `False + 1`?
    3. Read the official documentation for `isinstance()` and note what its second argument may be.

### 3.2 The `None` object

`None` is a special scalar that represents "no value." It is its own type (`NoneType`) and has exactly one instance, which you will see returned by functions that do work but have nothing meaningful to give back.

The example below shows a common way to meet `None` in the wild: `print()` itself returns it.

???+ example "Example: where None comes from"
    ```python
    result = print("hello")  # print() does its job, then returns None
    print(result)            # None
    print(type(result))      # <class 'NoneType'>
    ```

## 4. Text and binary data

Text occupies an interesting middle ground between scalars and containers, which is why we treat it here, in between the two. A string is built from smaller pieces — its characters — so in the strict sense it is a container, a sequence. Yet in practice we reach for a string as if it were a single value, and most beginners use text long before they ever think about sequences. So we introduce it now as a basic type, note its container nature in passing, and return to its sequence behaviour once we reach Section 5.

### 4.1 Strings

A **string** (`str`) is a piece of text, written in single or double quotes. Strings are immutable: operations on them produce *new* strings rather than changing the original. A string is technically a *sequence* of characters — so it is really a container — but it is so fundamental that we treat it as a basic type and revisit its sequence behaviour in Section 5.

The example below shows that a string method returns a new string and leaves the original untouched — the hallmark of an immutable type.

???+ example "Example: strings are immutable"
    ```python
    name = "Ada"
    print(name.upper())  # "ADA" — a brand-new string
    print(name)          # "Ada" — the original is unchanged
    ```

Because handling text is so common, `str` comes with a large toolkit of methods. A handful you will reach for constantly are changing case, trimming whitespace, splitting and joining, and searching or replacing. Every one returns a *new* string — the original is never touched.

The example below puts the most useful ones to work on a messy piece of text.

???+ example "Example: common string methods"
    ```python
    s = "  Hello, World  "
    print(s.strip())               # "Hello, World" — trim surrounding spaces
    print(s.strip().lower())       # "hello, world" — methods chain
    print("a,b,c".split(","))      # ['a', 'b', 'c'] — split into a list
    print("-".join(["x", "y", "z"]))  # "x-y-z" — join a list into a string
    print("hello".replace("l", "L"))  # "heLLo"
    print("hello".find("l"))       # 2 — index of first match (-1 if absent)
    ```

???+ question "Exercise: string methods"
    1. Reverse a string with slicing — `s[::-1]` (slicing is covered in **1.2 Collections**).
    2. Count the words in `"the quick brown fox"` using `split()`.
    3. Given `" 2024-01-02 "`, strip it and `split` on `"-"` to get `['2024', '01', '02']`.

### 4.2 Bytes

When you need raw binary data rather than text, Python offers `bytes` (immutable) and its mutable twin `bytearray`. You will not need them often early on, but they are the binary counterpart to `str`/`list`, and they round out the picture.

??? info "Deep dive: text is not bytes"
    A `str` is a sequence of Unicode *characters*; `bytes` is a sequence of raw
    8-bit *bytes*. Converting between them requires an **encoding** (usually
    UTF-8): `"café".encode("utf-8")` gives bytes, and `.decode("utf-8")` turns
    them back. Confusing the two is the source of most "mojibake" garbled-text
    bugs.

## Summary

Everything in Python is an **object**, and every object carries an **identity** (`id()`), a **type** (`type()`), and a **value**. To organise the many types, ask two questions — *what does it hold?* (scalar vs. container) and *can it change?* (mutable vs. immutable). This page covered the **scalars** — the numbers (`int`, `float`, `complex`, `bool`) and the lone `None` — and the **text** types (`str`, plus `bytes`/`bytearray`). The next page, **1.2 Collections**, takes up the containers — sequences, sets, and mappings — and returns to mutability, which ties them all together.
