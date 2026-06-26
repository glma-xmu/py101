# Exercises — Chapter 1: Python Basics

A set of practice problems, grouped by the section they exercise. Try them on your own; where a problem shows code, treat it as the given data or a starting point. Each problem shows a **sample output** so you know what to aim for. Solutions are not provided here.

???+ note "A note on functions"
    A few problems define a small function with `def name(args): … return …`, and the iterator problems use generator functions with `yield`. The `yield` form is covered in 1.4; the general topic of functions arrives in **Chapter 2**, but the basic `def` shown here is all you need.

## 1. Objects and Types

???+ question "Exercise 1.1 — predict the type"
    Predict the `type()` of each value, then check. Which is a `set` and which is a `dict`? Which is a `tuple`?

    ```python
    for v in [1, 1.0, True, "1", [1], (1,), {1}, {1: "a"}, 3 - 2j, None]:
        print(v, "->", type(v))
    ```

    **Sample output**
    ```text
    1 -> <class 'int'>
    1.0 -> <class 'float'>
    True -> <class 'bool'>
    1 -> <class 'str'>
    [1] -> <class 'list'>
    (1,) -> <class 'tuple'>
    {1} -> <class 'set'>
    {1: 'a'} -> <class 'dict'>
    (3-2j) -> <class 'complex'>
    None -> <class 'NoneType'>
    ```

???+ question "Exercise 1.2 — Booleans behave like numbers"
    Explain each result. In what sense is `True` an integer, and why does summing a list of `True`/`False` count the `True`s?

    ```python
    print(True + True)
    print(sum([True, False, True, True]))
    print("yes" if 3 else "no")
    ```

    **Sample output**
    ```text
    2
    3
    yes
    ```

???+ question "Exercise 1.3 — but Booleans are *not* just numbers"
    Because `1 == True == 1.0` (and they hash the same), predict how many keys this dictionary ends up with, and which value wins. Then write a check `is_real_bool(x)` that returns `True` only for an actual Boolean. Where would insisting on a genuine `bool` — rather than any truthy value — actually matter? (Hint: `isinstance(x, bool)`.)

    ```python
    d = {1: "one", True: "true", 1.0: "float"}
    print(d)
    print(is_real_bool(1))      # should be False
    print(is_real_bool(True))   # should be True
    ```

    **Sample output**
    ```text
    {1: 'float'}
    False
    True
    ```

???+ question "Exercise 1.4 — when is it the *same* object?"
    Predict each comparison, then run it. Why is `==` the right tool for comparing values, while `is` asks a different question? (The 257 case is implementation-dependent — a typical run prints `False`.)

    ```python
    a = 256; b = 256
    print(a is b)
    c = 257; d = 257
    print(c is d)
    print(c == d)
    ```

    **Sample output**
    ```text
    True
    False
    True
    ```

???+ question "Exercise 1.5 — which numeric type?"
    For each expression, predict whether the result is `int`, `float`, or `complex`, then confirm with `type()`.

    ```python
    for e in [7 / 2, 7 // 2, 2 ** 0.5, 3 + 4.0, 1 + 2j]:
        print(type(e))
    ```

    **Sample output**
    ```text
    <class 'float'>
    <class 'int'>
    <class 'float'>
    <class 'float'>
    <class 'complex'>
    ```

???+ question "Exercise 1.6 — `None` is a value too"
    Predict the output, then explain what the *inner* and *outer* `print` each display, and what `print(...)` returns.

    ```python
    print(print("hello"))
    x = print("world")
    print(x is None)
    ```

    **Sample output**
    ```text
    hello
    None
    world
    True
    ```

???+ question "Exercise 1.7 — `type()` vs `isinstance()`"
    With `x = True`, compare the checks below. Which is `True`, and why? Which would you use to ask "is this a number?", and which to ask "is this exactly a Boolean?"

    ```python
    x = True
    print(type(x) is int)
    print(isinstance(x, int))
    print(isinstance(x, bool))
    ```

    **Sample output**
    ```text
    False
    True
    True
    ```

### Optional: types beyond the basics

These explore a few built-in types we did **not** cover formally — worth recognising when you meet them in real code. All optional.

???+ question "Exercise 1.8 — array (optional)"
    An `array.array` is like a list, but every element must share one numeric type. Create one, index it, and see what happens if you append the wrong type.

    ```python
    import array
    a = array.array('i', [1, 2, 3, 4, 5])   # 'i' = signed integer
    print(a)
    print(type(a))
    print(a[0], a[-1])
    # a.append(6.0)   # uncomment: what happens?
    ```

    **Sample output**
    ```text
    array('i', [1, 2, 3, 4, 5])
    <class 'array.array'>
    1 5
    # a.append(6.0)  ->  TypeError: 'float' object cannot be interpreted as an integer
    ```

???+ question "Exercise 1.9 — bytes and bytearray (optional)"
    `bytes` is an immutable sequence of raw bytes; `bytearray` is its mutable twin. Explore both, and convert text to bytes and back with an encoding.

    ```python
    b = b"hi"
    print(b, type(b))
    ba = bytearray(b"hi")
    ba[0] = 72            # the byte for 'H'
    print(ba)
    print("café".encode("utf-8"))
    print(b"caf\xc3\xa9".decode("utf-8"))
    ```

    **Sample output**
    ```text
    b'hi' <class 'bytes'>
    bytearray(b'Hi')
    b'caf\xc3\xa9'
    café
    ```

???+ question "Exercise 1.10 — exact arithmetic: Fraction and Decimal (optional)"
    Floats are approximate. Compare a float sum with the exact answers from `Fraction` and `Decimal`.

    ```python
    from fractions import Fraction
    from decimal import Decimal
    print(0.1 + 0.2)
    print(0.1 + 0.2 == 0.3)
    print(Fraction(1, 10) + Fraction(2, 10))
    print(Decimal("0.1") + Decimal("0.2"))
    ```

    **Sample output**
    ```text
    0.30000000000000004
    False
    3/10
    0.3
    ```

???+ question "Exercise 1.11 — a complex number's parts (optional)"
    `complex` is a built-in numeric type. Pull out its real and imaginary parts and its magnitude.

    ```python
    z = 3 + 4j
    print(z.real, z.imag)
    print(abs(z))
    print(type(z))
    ```

    **Sample output**
    ```text
    3.0 4.0
    5.0
    <class 'complex'>
    ```

???+ question "Exercise 1.12 — frozenset (optional)"
    A `frozenset` is an immutable set — so, unlike a `set`, it is hashable and can be a dictionary key or an element of another set.

    ```python
    fs = frozenset([1, 2, 2, 3])
    print(fs)
    # fs.add(4)              # uncomment: what happens?
    d = {fs: "ok"}           # a frozenset can be a key
    print(d[frozenset([3, 2, 1])])
    ```

    **Sample output**
    ```text
    frozenset({1, 2, 3})
    # fs.add(4)  ->  AttributeError: 'frozenset' object has no attribute 'add'
    ok
    ```

## 2. Collections

???+ question "Exercise 2.1 — using `set()` and `{}` correctly"
    Run each line and summarise the rule: when does `set(...)` succeed, and when does `{...}` build a *set* rather than something else? Finally, how do you create `{(1, 2, 3)}` — one element, a tuple — using the `set()` function?

    ```python
    print(set((1, 2, 3)))
    print(set((1,)))
    print({1, 2, 3})
    print({(1, 2, 3)})
    ```

    **Sample output**
    ```text
    {1, 2, 3}
    {1}
    {1, 2, 3}
    {(1, 2, 3)}
    ```

???+ question "Exercise 2.2 — `KeyError` vs `get()`"
    Show that indexing a missing key raises `KeyError`, while `get()` does not. Then look up `"key3"` so it returns `"missing"` instead of crashing.

    ```python
    d = {"key1": "value1", "key2": "value2"}
    print(d["key1"])
    print(d.get("key3", "missing"))
    ```

    **Sample output**
    ```text
    value1
    missing
    ```

???+ question "Exercise 2.3 — remove duplicates"
    From `nums`, produce a list of just the unique values in sorted order.

    ```python
    nums = [1, 2, 2, 3, 4, 4, 4, 5, 1]
    ```

    **Sample output**
    ```text
    [1, 2, 3, 4, 5]
    ```

???+ question "Exercise 2.4 — set algebra"
    With the two sets below, compute their union, intersection, the elements in `a` but not `b`, and the symmetric difference. Also check whether `{2, 3}` is a subset of `a`.

    ```python
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    ```

    **Sample output**
    ```text
    {1, 2, 3, 4, 5, 6}
    {3, 4}
    {1, 2}
    {1, 2, 5, 6}
    True
    ```

???+ question "Exercise 2.5 — build a dictionary from two lists"
    Pair the names with the scores into a dictionary (one call does it). Then add `"Dan"` with 88, update `"Bob"` to 90, and look up `"Eve"` returning `"unknown"` if absent.

    ```python
    names  = ["Ada", "Bob", "Cleo"]
    scores = [91, 85, 78]
    ```

    **Sample output**
    ```text
    {'Ada': 91, 'Bob': 90, 'Cleo': 78, 'Dan': 88}
    unknown
    ```

???+ question "Exercise 2.6 — lists change, tuples do not"
    Predict which edits succeed and which raise an error, and explain why in terms of mutability. Does `id(l)` change after the in-place edits?

    ```python
    l = [10, 20, 30]
    t = (10, 20, 30)
    l[0] = 99
    del l[1]
    print(l)
    # t[0] = 99   # uncomment: what happens?
    ```

    **Sample output**
    ```text
    [99, 30]
    # t[0] = 99  ->  TypeError: 'tuple' object does not support item assignment
    ```

???+ question "Exercise 2.7 — string surgery"
    From the messy title below, produce the slug `"data-science-101"` (trim, lowercase, spaces to hyphens). Then print how many words it has and the original string reversed.

    ```python
    title = "  Data Science 101  "
    ```

    **Sample output**
    ```text
    data-science-101
    3
      101 ecneicS ataD  
    ```

### Beginner list drills

Quick "finger exercises" for getting fluent with list **indexing**, **slicing**, **nesting**, and the way a name *refers to* a list — the Python counterpart of the classic pointer drills in C.

???+ question "Exercise 2.8 — index from both ends"
    Print the first element, the last element, the second element, and the second-to-last — using indexing (try negative indices for the ones near the end).

    ```python
    xs = [10, 20, 30, 40, 50]
    ```

    **Sample output**
    ```text
    10
    50
    20
    40
    ```

???+ question "Exercise 2.9 — slice predictions"
    Predict each slice before running it.

    ```python
    xs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(xs[2:5])
    print(xs[:3])
    print(xs[7:])
    print(xs[::2])
    print(xs[::-1])
    ```

    **Sample output**
    ```text
    [2, 3, 4]
    [0, 1, 2]
    [7, 8, 9]
    [0, 2, 4, 6, 8]
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ```

???+ question "Exercise 2.10 — edit in place"
    Apply these steps in order, printing `xs` after each: append `60`; insert `15` at index 1; `pop` the element at index 3; replace the slice `xs[0:2]` with `[1, 2, 3]`.

    ```python
    xs = [10, 20, 30, 40, 50]
    ```

    **Sample output**
    ```text
    [10, 20, 30, 40, 50, 60]
    [10, 15, 20, 30, 40, 50, 60]
    [10, 15, 20, 40, 50, 60]
    [1, 2, 3, 20, 40, 50, 60]
    ```

???+ question "Exercise 2.11 — a list of lists (matrix)"
    Print the element at row 1, column 2 (0-indexed); the whole middle row; and the middle column (the column needs a loop or comprehension).

    ```python
    m = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
    ```

    **Sample output**
    ```text
    6
    [4, 5, 6]
    [2, 5, 8]
    ```

???+ question "Exercise 2.12 — two names, one list (the 'pointer' trap)"
    Predict both prints. Why does changing `b` also change `a` in the first case but not the second? (Recall: a name refers to an object; `a[:]` makes a copy.)

    ```python
    a = [1, 2, 3]
    b = a
    b.append(4)
    print(a)

    a = [1, 2, 3]
    b = a[:]          # a copy
    b.append(4)
    print(a)
    ```

    **Sample output**
    ```text
    [1, 2, 3, 4]
    [1, 2, 3]
    ```

???+ question "Exercise 2.13 — by hand, no shortcuts"
    Without using `[::-1]`, `reversed()`, `max()`, or `sum()`, use a loop to print the list reversed, then its maximum, then its total.

    ```python
    xs = [4, 9, 2, 7, 5, 1]
    ```

    **Sample output**
    ```text
    [1, 5, 7, 2, 9, 4]
    9
    28
    ```

## 3. Control Flow

???+ question "Exercise 3.1 — a sequence with a fractional step"
    Print `0.0, 0.5, 1.0, …, 10.0`. You must use `range` (which yields only integers, so scale appropriately).

    **Sample output**
    ```text
    0.0
    0.5
    1.0
    ...
    9.5
    10.0
    ```

???+ question "Exercise 3.2 — trace the loop by hand"
    Without running it, write out the value of **every** variable at each step, then run to confirm.

    ```python
    def naive_by2(lst, by):
        n = len(lst) // by
        res = []
        for i in range(n):
            res.append([lst[2 * i], lst[2 * i + 1]])
        return res

    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(naive_by2(nums, 2))
    ```

    **Sample output**
    ```text
    [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
    ```

???+ question "Exercise 3.3 — regroup the list"
    Produce `[[1, 3, 5, 7, 9], [2, 4, 6, 8, 10]]` — odds first, then evens — without iterators or generators. (Hint: a slice with a step, `lst[start::step]`.)

    ```python
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ```

    **Sample output**
    ```text
    [[1, 3, 5, 7, 9], [2, 4, 6, 8, 10]]
    ```

???+ question "Exercise 3.4 — FizzBuzz"
    For the numbers 1 to 30, print `"fizz"` for multiples of 3, `"buzz"` for multiples of 5, `"fizzbuzz"` for multiples of both, otherwise the number.

    **Sample output**
    ```text
    1
    2
    fizz
    4
    buzz
    fizz
    7
    8
    fizz
    buzz
    11
    fizz
    13
    14
    fizzbuzz
    ...
    ```

???+ question "Exercise 3.5 — stop when you have enough"
    Add the integers 1, 2, 3, … and stop as soon as the running total first **exceeds 100**. Print the final total and how many numbers you added. (Use a `while` loop.)

    **Sample output**
    ```text
    105
    14
    ```

???+ question "Exercise 3.6 — primes below 50"
    Print every prime from 2 up to 50, using only loops and `if` (no imports).

    **Sample output**
    ```text
    2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
    ```

???+ question "Exercise 3.7 — least squares by loop"
    For the data below and the model $y = b x$, find the slope $b$ minimising $L(b)=\sum_{i=1}^{5}(y_i - b x_i)^2$. Search `b` over `0.50, 0.51, …, 1.50` with a loop, keeping the best `b` so far. Do **not** use `min` or `numpy.argmin`.

    ```python
    xs = [0, 1, 2, 3, 4]
    ys = [0, 0, 1, 3, 5]
    ```

    **Sample output**
    ```text
    best b = 1.03
    ```

## 4. Iterables and Iterators

???+ question "Exercise 4.1 — iterate by hand"
    Use `iter()` and `next()` to pull the values out of the list one at a time, and show what happens after the last one is taken.

    ```python
    data = [10, 20, 30]
    ```

    **Sample output**
    ```text
    10
    20
    30
    # next(it) once more -> StopIteration
    ```

???+ question "Exercise 4.2 — an iterator is single-use"
    Predict the two outputs, then explain why the second is empty.

    ```python
    it = iter([1, 2, 3])
    print(list(it))
    print(list(it))
    ```

    **Sample output**
    ```text
    [1, 2, 3]
    []
    ```

???+ question "Exercise 4.3 — a squares generator, two ways"
    Produce the squares `1, 4, 9, 16, …` (a) with a generator **function** using `yield`, and (b) with a generator **expression**. For the expression, stop at 100, and print the list of results.

    **Sample output**
    ```text
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    ```

???+ question "Exercise 4.4 — infinite Fibonacci"
    Write a generator that yields Fibonacci numbers indefinitely ($F_0=0$, $F_1=1$, $F_n=F_{n-1}+F_{n-2}$), then print the first 10.

    ```python
    def fibonacci():
        ...   # your code here
    ```

    **Sample output**
    ```text
    0 1 1 2 3 5 8 13 21 34
    ```

???+ question "Exercise 4.5 — a filtering generator expression"
    Write a **generator expression** that yields the *lengths* of the words that start with a consonant and end with a vowel (a, e, i, o, u). Print the list of results.

    ```python
    words = ["apple", "banana", "orange", "kiwi", "grape",
             "elephant", "tiger", "lion", "mouse"]
    vowels = "aeiou"
    ```

    **Sample output**
    ```text
    [6, 4, 5]
    ```

???+ question "Exercise 4.6 — perfect squares with a generator"
    Write a generator that yields the **perfect squares** not exceeding 100 (1, 4, 9, …), then print them on one line. (A perfect square is $n^2$ for a whole number $n$.)

    **Sample output**
    ```text
    1 4 9 16 25 36 49 64 81 100
    ```

???+ question "Exercise 4.7 — list vs generator, in memory"
    Compare the memory footprint of a list versus a generator for the same computation, and explain the difference. (Exact byte counts vary by platform.)

    ```python
    import sys
    print(sys.getsizeof([x * x for x in range(10000)]))
    print(sys.getsizeof((x * x for x in range(10000))))
    ```

    **Sample output**
    ```text
    85176
    200
    ```

???+ question "Exercise 4.8 — the two-argument `iter()` (optional)"
    `iter(f, sentinel)` calls the function `f` repeatedly until it returns `sentinel`. Using it (not a `while` loop), draw random integers from 0–9 until the first `0`, printing the numbers drawn before it (the `0` itself is not printed).

    ```python
    import random
    # Hint: define f() to return one random.choice(range(10)), then iter(f, 0).
    ```

    **Sample output** (varies each run)
    ```text
    2
    6
    4
    ```

???+ question "Exercise 4.9 — average run length (optional)"
    Building on the previous problem, repeat the experiment **50 times** and report the average count of numbers drawn before the first `0`. (Collect each run's length in a list, then take `sum(lengths) / 50`. The theoretical average is about 9.)

    **Sample output** (varies each run)
    ```text
    average length over 50 runs: 8.74
    ```
