# Loose Ends and Style

## Introduction

A short closing page for the smaller — but real — topics that did not fit the four big themes: how to **document** a function so others (and future-you) can use it, two finer points about **parameter lists**, and the shared **style conventions** that keep everyone's Python readable. None of these change what your functions *do*; they change how easy your functions are to read, call, and trust.

As always, the code is runnable.

## 1. Documenting a function: docstrings and type hints

We previewed these in 2.1; here is the fuller picture, because a function nobody can understand is only half finished.

A **docstring** is a string literal written as the very first line of a function's body. It is not a comment — Python stores it on the function as `__doc__`, and `help()`, editors, and documentation tools all read it. A one-line docstring states what the function does; a longer one adds detail about arguments and the return value.

???+ example "Example: a docstring"
    ```python
    def clamp(value, low, high):
        """Return value limited to the range [low, high]."""
        return max(low, min(value, high))

    print(clamp(15, 0, 10))    # 10
    print(clamp.__doc__)       # Return value limited to the range [low, high].
    help(clamp)                # shows the signature and the docstring
    ```

**Type hints** annotate what kinds of object a function expects and returns. They do **not** change how the code runs — Python does not enforce them — but they document your intent precisely and let editors and checkers catch mistakes before you run anything.

???+ example "Example: type hints"
    ```python
    def repeat(text: str, times: int = 2) -> str:
        """Return text joined to itself, separated by spaces."""
        return " ".join([text] * times)

    print(repeat("hi", 3))     # hi hi hi
    print(repeat("ok"))        # ok ok
    ```

```recall
A name is just a label: a type hint like `text: str` does not make `text` a string — it only *says* it should be one. As in 1.1, the object decides its own type; the hint is a note to humans and tools.
```

???+ note "Key concept: docstrings and hints document, they don't enforce"
    A **docstring** (first line of the body, in triple quotes) says *what* a
    function does and is read by `help()`. **Type hints** say *what kinds* of value
    it works with. Neither is checked at runtime — both exist to make a function
    self-explanatory.

## 2. Finer parameter lists: keyword-only and positional-only

By default, every parameter can be filled either positionally or by keyword (2.3 §3.1). Occasionally you want to *restrict* that, to make call sites clearer or an API more stable. Two markers in the parameter list do this.

A bare **`*`** in the signature means "every parameter after me must be passed **by keyword**." This is great for options that would be meaningless as bare positional values.

???+ example "Example: keyword-only parameters"
    ```python
    def connect(host, *, timeout=30, secure=True):
        return f"{host} (timeout={timeout}, secure={secure})"

    print(connect("server", timeout=5))     # fine — keywords
    # print(connect("server", 5))           # TypeError: timeout is keyword-only
    ```

A **`/`** does the opposite: every parameter *before* it must be passed **positionally**. You meet this mostly in built-in functions, where it stops callers from depending on internal parameter names.

???+ example "Example: positional-only parameters"
    ```python
    def power(base, exp, /):
        return base ** exp

    print(power(2, 10))          # 1024 — positional
    # print(power(base=2, exp=10))  # TypeError: positional-only
    ```

???+ note "Key concept: `*` and `/` in a signature"
    A lone **`*`** forces the parameters after it to be **keyword-only**; a **`/`**
    forces the parameters before it to be **positional-only**. Both are optional
    tools for designing clearer, more deliberate function signatures.

## 3. PEP 8: the shared style guide

Python has a stream of design documents called **PEPs** — Python Enhancement Proposals. One of them, **PEP 8**, is the community **style guide**: a set of conventions for laying out code. It is *not* enforced by the language — your code runs the same either way — but following it makes your code instantly familiar to every other Python programmer, which is most of the point of style.

The conventions you will use constantly, many of them about functions:

- **Names:** functions and variables in `snake_case` (`read_file`, not `ReadFile` or `readfile`); constants in `UPPER_CASE`; classes in `CapWords`. A function name should usually be a verb phrase: `compute_total`, `is_valid`.
- **Indentation:** 4 spaces per level, never tabs.
- **Spacing:** a space after each comma and around operators (`a + b`, `f(x, y)`), but *not* just inside brackets or before a call's parenthesis (`f(x)`, not `f ( x )`).
- **Blank lines:** two blank lines between top-level functions, to let the eye separate them.
- **Line length:** keep lines reasonably short (PEP 8 says 79 characters; many projects use 88 or so).

The same function, before and after:

???+ example "Example: messy vs. PEP 8"
    ```python
    # not PEP 8
    def Add (X,Y):return X+Y

    # PEP 8
    def add(x, y):
        return x + y

    print(add(2, 3))   # 5
    ```

???+ note "Key concept: PEP 8 is recommended, not required"
    **PEP 8** is the standard style guide for Python. It is a convention, not a
    rule the interpreter enforces — but following it makes your code readable to
    everyone. Tools can apply it for you: **formatters** like `black` rewrite your
    code to a consistent style, and **linters** like `ruff` or `flake8` flag
    violations.

??? info "Deep dive: fixing some arguments with functools.partial"
    One more first-class trick worth knowing. `functools.partial` takes a function
    and *some* of its arguments, and returns a new function with those filled in —
    a tidy alternative to a tiny `lambda` or closure:

    ```python
    from functools import partial

    def power(base, exp):
        return base ** exp

    square = partial(power, exp=2)   # a new function: power with exp fixed at 2
    print(square(5))                 # 25
    ```

    It is the same first-class idea from 2.3 — functions are values you can build
    new functions from — packaged as a standard tool.

???+ question "In-class exercise: style and signatures"
    1. Rewrite this to follow PEP 8: `def Mul(A ,B):return A*B`.
    2. Add a one-line docstring and type hints to your `add` function from §3.
    3. Define `make_user(name, *, admin=False)` and show that `make_user("Ada", True)` fails while `make_user("Ada", admin=True)` works. Explain why.

## Summary

These are the finishing touches that turn working functions into *good* functions:

| Tool | What it adds |
|------|--------------|
| **Docstring** | a human-readable description, read by `help()` |
| **Type hints** | a note about the kinds of value involved (not enforced) |
| **`*` / `/` in signatures** | keyword-only and positional-only parameters |
| **PEP 8** | shared style conventions that keep code readable |

That closes **Chapter 2**. You can now define functions and call them; reason about frames, the heap, namespaces, and scope; pass, return, and build functions as first-class values; and apply them through decorators, recursion, `map`/`filter`/`reduce`, generators, and error handling — all written in clean, documented, conventional Python.
