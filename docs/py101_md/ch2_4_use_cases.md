# Functions in Practice: Five Use Cases

## Introduction

In 2.3 we learned that a function is a value: it can be passed, returned, and built on the fly. This page spends that capital. We work through five classic patterns that every Python programmer reaches for — **decorators**, **recursion**, **`map`/`filter`/`reduce`**, **generators**, and **error handling**. The first three are higher-order functions through and through; the last two round out the everyday toolkit for writing functions that are lazy where they should be and robust when things go wrong. Each builds directly on Chapters 1–2, so watch for the callbacks.

As always, every cell is runnable.

## 1. Decorators

Imagine you have written a dozen functions and now want every one of them to announce when it starts and finishes — for logging, timing, or debugging. You could paste the same two `print`s into all twelve bodies, but that is exactly the repetition functions were meant to kill. And if someone *else* wrote the functions, you may not be able to edit them at all.

The way out is a **decorator**: a higher-order function that takes a function, wraps it in some extra behavior, and returns the wrapped version. It is the pass-through wrapper from 2.3 §3.2, given a name and a purpose.

???+ example "Example: a logging decorator"
    ```python
    def announce(func):
        def wrapper(*args, **kwargs):
            print(f"{func.__name__} is being called.")
            result = func(*args, **kwargs)        # do the real work
            print(f"finished calling {func.__name__}.")
            return result
        return wrapper

    @announce
    def add(a, b):
        return a + b

    print(add(2, 3))
    ```

Two ideas from 2.3 are doing all the work here. `wrapper` is a **closure** — it remembers `func` from its enclosing scope — and it forwards `*args, **kwargs` so it works for *any* function, whatever its arguments. The `@announce` line is pure convenience: it means exactly `add = announce(add)`, rebinding the name `add` to the wrapped version.

???+ note "Key concept: decorator"
    A **decorator** is a higher-order function that takes a function and returns a
    new function wrapping it. Writing `@decorator` above a `def` is shorthand for
    `name = decorator(name)`. The wrapper uses a closure (to remember the original)
    and `*args`/`**kwargs` (to pass arguments through untouched).

A close cousin of decoration is the **`assert`** statement, which a wrapper often uses to guard a function's inputs. `assert condition, "message"` does nothing if the condition is true, but raises `AssertionError` with your message if it is false — a quick way to state an assumption and fail loudly when it is violated.

???+ example "Example: assert as a guard"
    ```python
    def mean(values):
        assert len(values) > 0, "mean() needs at least one value"
        assert None not in values, "values must not contain None"
        return sum(values) / len(values)

    print(mean([2, 4, 6]))     # 4.0
    # print(mean([]))          # AssertionError: mean() needs at least one value
    ```

???+ warning "Pitfall: a wrapper must forward and return"
    If your `wrapper` forgets to pass `*args, **kwargs` to `func`, or forgets to
    `return func(...)`'s result, the decorated function will silently lose its
    arguments or its return value. A wrapper that does not return becomes a
    function that returns `None` — the 2.1 trap, one level up.

??? info "Deep dive: memoization and `functools.wraps`"
    A decorator can do more than log — it can *remember*. A **memoizing** decorator
    caches results so repeated calls with the same arguments are instant:

    ```python
    def memoize(func):
        cache = {}                       # closure state
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        return wrapper
    ```

    One blemish: wrapping replaces the original, so `add.__name__` becomes
    `"wrapper"`. Decorating `wrapper` with `@functools.wraps(func)` copies the
    original's name and docstring across, keeping introspection honest.

???+ question "In-class exercise: decorators"
    1. Write a decorator `timed` that prints how long the wrapped function took (use `time.perf_counter()` before and after).
    2. Apply `announce` to a function that takes keyword arguments, and confirm they still arrive correctly.
    3. Explain in one sentence why `wrapper` needs `*args, **kwargs` rather than fixed parameters.

## 2. Recursion

A **recursive** function is one that calls itself. It is the natural shape for any problem that is defined in terms of a smaller copy of itself — and it leans directly on the **call stack** from 2.1, because each call gets its own frame.

Every recursion needs two parts: a **base case** that stops the descent, and a **recursive case** that moves one step toward it.

???+ example "Example: factorial"
    ```python
    def factorial(n):
        if n == 0:                 # base case: stop here
            return 1
        return n * factorial(n - 1)   # recursive case: a smaller problem

    print(factorial(4))            # 24
    ```

Why does this work without a loop? Because every call to `factorial` gets its *own* frame on the call stack, each with its own `n`. The picture below freezes `factorial(3)` at its deepest point, just as `factorial(0)` is about to return. Four frames are stacked, paused mid-multiplication, each waiting on the one above it.

```memory
memory: Heap
stack: Call Stack
objects:
  fn: a function
  i3: 3
  i2: 2
  i1: 1
  i0: 0
globals: Global Namespace
  factorial -> fn
frame: factorial(3)
  n -> i3
frame: factorial(2)
  n -> i2
frame: factorial(1)
  n -> i1
frame: factorial(0)
  n -> i0
```

As each call hits its base case or finishes, its frame returns a value and is discarded, and the frame beneath it resumes — `factorial(0)` returns `1`, then `factorial(1)` returns `1*1`, then `factorial(2)` returns `2*1`, and so on back down the stack.

```recall
The call stack at work: recursion is not magic — it is just many frames of the *same* function, each with its own locals, stacked exactly as in 2.1. The base case is what keeps the stack from growing forever.
```

The same shape solves many problems. Summing a list, for instance, is "the first element plus the sum of the rest."

???+ example "Example: recursive sum and Fibonacci"
    ```python
    def total(xs):
        if len(xs) == 0:           # base case
            return 0
        return xs[0] + total(xs[1:])

    def fib(n):
        if n < 2:                  # base cases: fib(0)=0, fib(1)=1
            return n
        return fib(n - 1) + fib(n - 2)

    print(total([1, 2, 3, 4]))     # 10
    print([fib(i) for i in range(8)])   # [0, 1, 1, 2, 3, 5, 8, 13]
    ```

???+ warning "Pitfall: forgetting the base case"
    A recursion with no reachable base case never stops calling itself. Python does
    not loop forever, though — each call consumes a frame, and when the stack gets
    too deep (about a thousand frames by default) it stops with a
    `RecursionError`. If you see that error, your base case is missing or never
    reached.

???+ question "In-class exercise: recursion"
    1. Write `count_down(n)` that prints `n, n-1, …, 1, "liftoff!"` using recursion, not a loop.
    2. Write a recursive `power(base, exp)` computing `base ** exp` (base case `exp == 0` returns `1`).
    3. `fib` above recomputes the same values many times. Decorate it with the `memoize` decorator from §1 and compare how far up you can compute.

## 3. `map`, `filter`, and `reduce`

Three built-in higher-order functions capture the most common things you do to a sequence: transform every element, keep some elements, or boil the whole thing down to one value. Each takes a **function** plus an **iterable** — the perfect home for the `lambda` from 2.3.

- **`map(func, iterable)`** applies `func` to every element.
- **`filter(func, iterable)`** keeps the elements for which `func` returns `True`.
- **`reduce(func, iterable)`** (from the `functools` module) combines elements pairwise, left to right, into a single result.

???+ example "Example: map, filter, reduce"
    ```python
    from functools import reduce

    nums = [1, 2, 3, 4, 5]

    print(list(map(lambda x: x * x, nums)))        # [1, 4, 9, 16, 25]
    print(list(filter(lambda x: x % 2 == 0, nums)))# [2, 4]
    print(reduce(lambda a, b: a + b, nums))        # 15  (((1+2)+3)+4)+5
    ```

Notice the `list(...)` around `map` and `filter`: like `range` in 1.2, they return **lazy iterators**, computing each value only as you ask for it (the iterator protocol from 1.4). `reduce` is different — it consumes the whole iterable to produce one value, so it needs no `list`.

???+ note "Key concept: map / filter / reduce"
    These are higher-order functions over an iterable: **`map`** transforms,
    **`filter`** selects, **`reduce`** aggregates. The first two are lazy iterators;
    `reduce` returns a single value and lives in `functools`.

???+ warning "Pitfall: often a comprehension is clearer"
    `map` and `filter` overlap with the comprehensions from 1.3. Many Pythonistas
    write `[x*x for x in nums]` rather than `list(map(lambda x: x*x, nums))`, and
    `[x for x in nums if x % 2 == 0]` rather than the `filter` version — they read
    better. Reach for `map`/`filter` when you already have a named function to pass
    (`map(str, nums)`), and keep `reduce` for genuine running aggregations.

???+ question "In-class exercise: map / filter / reduce"
    1. Use `map` to turn `["1", "2", "3"]` into `[1, 2, 3]`. (Hint: pass `int`.)
    2. Use `filter` to keep only the words longer than three letters from `["hi", "there", "ok", "world"]`.
    3. Use `reduce` to find the maximum of `[3, 9, 2, 7]` without calling `max`.

## 4. Generators

A **generator** is a function that produces a *stream* of values, one at a time, instead of computing them all up front. We met generators briefly in 1.4 as a way to make iterators; here is the mechanism. A function becomes a **generator function** the moment its body contains the keyword **`yield`**. Calling it does not run the body — it hands back a generator object, and each value is produced only when asked for.

The magic of `yield` is what it does to the **frame**. In 2.1, a normal `return` discarded the call's frame for good. `yield` does the opposite: it hands back a value but **suspends the frame instead of discarding it** — local variables, the current line, all of it — and keeps that frame alive, attached to the generator object out in the heap. When you ask for the next value, the very same frame is resumed exactly where it paused, on the line after the `yield`. A generator is, in effect, a function whose frame you can set down and pick back up.

???+ example "Example: a generator function"
    ```python
    def countdown(n):
        while n > 0:
            yield n          # hand back n, then pause here
            n -= 1           # resumes here on the next request

    for x in countdown(3):
        print(x)             # 3, 2, 1

    print(list(countdown(5)))   # [5, 4, 3, 2, 1]
    ```

```recall
The call stack at work: a normal `return` throws its frame away; `yield` keeps it. That preserved frame — held alive on the heap, much like a closure's captured scope in 2.3 — is exactly why the generator's local `n` remembers its value from one `next()` to the next.
```

Because values are produced on demand, a generator can describe a sequence too large — even *infinite* — to ever hold in memory. You simply stop asking when you have enough.

???+ example "Example: an endless stream of squares"
    ```python
    def squares():
        n = 1
        while True:          # never ends...
            yield n * n
            n += 1

    g = squares()
    print(next(g), next(g), next(g))   # 1 4 9 — computed one at a time
    ```

And the compact cousin from 1.3, the **generator expression**, is the same idea in one line — parentheses instead of the square brackets of a list comprehension:

???+ example "Example: a generator expression"
    ```python
    gen = (x * x for x in range(5))
    print(type(gen))         # <class 'generator'>
    print(list(gen))         # [0, 1, 4, 9, 16]
    ```

???+ note "Key concept: generator"
    A **generator** is an iterator produced either by a function containing `yield`
    or by a generator expression `(… for …)`. It computes values lazily, pausing at
    each `yield` and resuming on the next request, so it never needs to store the
    whole sequence.

???+ warning "Pitfall: a generator is single-use"
    Like every iterator (1.4), a generator runs once. After you have looped over it
    or exhausted it with `list()`, it is empty — looping again yields nothing. Call
    the generator function again to get a fresh one.

## 5. Handling errors with `try` / `except`

Even correct functions meet bad input: a missing file, a zero divisor, a `None` where a number should be. The `assert` from §1 is for catching *your own* mistaken assumptions during development; **`try` / `except`** is for gracefully handling errors you expect might happen at runtime, so one bad value does not crash the whole program.

The shape is: run the risky code in a `try` block; if it raises an exception, the matching `except` block handles it instead of the program stopping.

???+ example "Example: catching a specific error"
    ```python
    def safe_divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            print("can't divide by zero; returning None")
            return None

    print(safe_divide(10, 2))   # 5.0
    print(safe_divide(10, 0))   # message, then None
    ```

The full form has two more optional blocks. **`else`** runs only if the `try` block raised *nothing*; **`finally`** runs no matter what, and is the place for cleanup that must always happen.

???+ example "Example: else and finally"
    ```python
    def read_int(text):
        try:
            value = int(text)
        except ValueError:
            print(f"{text!r} is not a whole number")
            return None
        else:
            print("parsed successfully")
            return value
        finally:
            print("done trying")

    read_int("42")     # parsed successfully / done trying -> 42
    read_int("oops")   # not a whole number / done trying -> None
    ```

This is exactly what lets a batch job skip the few broken records and finish the rest: wrap the risky step per item in `try`/`except`, log the failure, and carry on.

???+ note "Key concept: try / except / else / finally"
    Put risky code in **`try`**; handle a named exception in **`except SomeError`**;
    use **`else`** for code that should run only when no error occurred; use
    **`finally`** for cleanup that must run either way.

???+ warning "Pitfall: don't catch everything blindly"
    A bare `except:` (or `except Exception`) swallows *every* error — including
    typos in your own code and the user pressing Ctrl-C — and hides real bugs.
    Catch the *specific* exceptions you actually expect (`ZeroDivisionError`,
    `ValueError`, `FileNotFoundError`), and let the unexpected ones surface.

???+ question "In-class exercise: error handling"
    1. Write `safe_index(seq, i)` that returns `seq[i]`, or `None` if the index is out of range (catch `IndexError`).
    2. Wrap `int(input(...))` in a `try`/`except` loop that keeps asking until the user types a valid number.
    3. Explain when you would use `assert` versus `try`/`except`.

## Summary

Five everyday patterns, all resting on the idea that a function is a value:

| Use case | What it is | Builds on |
|----------|-----------|-----------|
| **Decorator** | a higher-order wrapper that extends a function | closures, `*args`/`**kwargs` (2.3) |
| **Recursion** | a function that calls itself | the call stack (2.1) |
| **map / filter / reduce** | higher-order functions over an iterable | `lambda` (2.3), iterators (1.4) |
| **Generators** | functions that yield a lazy stream | iterators (1.4), comprehensions (1.3) |
| **try / except** | handling runtime errors gracefully | — |

Next, **2.5 Loose Ends and Style** steps back from features to the smaller finishing touches — documenting functions, finer parameter lists, and the shared style conventions (PEP 8) that make Python code, including everything you have just written, readable to everyone else.
