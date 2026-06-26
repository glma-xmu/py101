# Control Flow

## Introduction

A program is not just a list of statements run top to bottom. Real programs need to **repeat** work — do something for every student in a class — and to **choose** work — act only when a condition holds. The tools that decide *which* statements run, and *how many times*, are called **control flow**. This page covers the two everyday kinds: **loops**, which repeat, and **conditionals**, which choose. Along the way we lean constantly on 1.1–1.2: the things you loop over and test are the objects and containers you already met.

As before, the code here is live — press *Run* (or Ctrl/Cmd+Enter) to execute it, edit it, and run again.

## 1. The `for` loop

The most common thing you do with a container is visit its items one at a time. A `for` loop does exactly that: it takes each element of a container in turn and binds your loop variable to it, running the loop body once per element.

The example below walks a list, then a string, then a dictionary — every container you met in 1.1–1.2 can be looped over the same way.

???+ example "Example: looping over containers"
    ```python
    for n in [10, 20, 30]:
        print(n)

    for ch in "hi":
        print(ch)

    prices = {"apple": 3, "pear": 5}
    for key in prices:          # looping a dict yields its keys
        print(key, prices[key])
    ```

```recall
Names refer to objects: on each pass the loop variable is just a name being re-bound to the next object in the container — nothing is copied.
```

### 1.1 Counting with `range`

Sometimes you do not have a container to walk — you simply want to do something a fixed number of times, or generate a run of integers. That is what `range` is for, and it is most at home right here, as the thing a `for` loop counts over. Recall from 1.2 that `range` is a *lazy* sequence: `range(5)` stands for 0, 1, 2, 3, 4 without building a list.

???+ example "Example: range in a for loop"
    ```python
    for i in range(5):          # 0, 1, 2, 3, 4
        print(i)

    for i in range(2, 11, 2):   # start, stop (exclusive), step
        print(i)                # 2, 4, 6, 8, 10
    ```

### 1.2 Looping the Pythonic way: `enumerate` and `zip`

When you think you need the index *and* the item, reach for `enumerate` rather than counting by hand. And when you need to walk two sequences in lockstep, use `zip`. These read better and avoid a classic bug.

???+ example "Example: enumerate and zip"
    ```python
    colors = ["red", "green", "blue"]
    for i, color in enumerate(colors):
        print(i, color)

    names  = ["Ada", "Bob"]
    scores = [95, 88]
    for name, score in zip(names, scores):
        print(name, "scored", score)
    ```

`zip` is also the natural way to build a dictionary from two parallel lists: `dict(zip(names, scores))`. (`zip` stops at the shorter input.)

???+ warning "Pitfall: don't loop over `range(len(...))`"
    A common habit from other languages is `for i in range(len(colors)): color = colors[i]`. In Python this is clumsy and error-prone — iterate directly (`for color in colors`) when you need the items, or use `enumerate` when you genuinely need the index too.

???+ question "Exercise: for loops"
    1. Print every character of `"python"` on its own line.
    2. Use `range` to print the even numbers from 0 to 20.
    3. Given `names = ["Ada", "Bob", "Cleo"]`, print each as `"1. Ada"`, `"2. Bob"`, … using `enumerate` (start the count at 1).

## 2. The `while` loop

A `for` loop repeats *once per item*. Sometimes you instead want to repeat *as long as a condition holds*, without knowing in advance how many passes that will take — keep asking the user until they type a valid answer, keep halving a number until it is small enough. That is a **`while`** loop: it checks a condition, runs the body if it is true, and repeats.

The example below uses the classic *accumulator* pattern: a running total updated each pass.

???+ example "Example: a while loop with an accumulator"
    ```python
    total = 0
    n = 1
    while n <= 5:        # keep going while the condition is true
        total += n       # accumulate
        n += 1           # move toward the condition becoming false
    print(total)         # 15  (1+2+3+4+5)
    ```

Use a `for` loop when you are walking a known collection or a fixed count; reach for `while` when continuation depends on a condition you re-test each time.

???+ warning "Pitfall: the infinite loop"
    A `while` loop only ends when its condition becomes false, so the body must make progress toward that. Forgetting the `n += 1` above would loop forever. If you ever need to stop on a condition discovered *inside* the body, use `break` (next section).

???+ question "Exercise: while loops"
    1. Start from `n = 100` and keep halving it with integer division (`n //= 2`), printing each value, until it reaches 0.
    2. Sum the integers 1, 2, 3, … and stop as soon as the running total exceeds 50; print how many numbers you added.

## 3. `break`, `continue`, and the loop `else`

Inside any loop you sometimes need finer control. **`break`** exits the loop immediately. **`continue`** skips the rest of the current pass and moves to the next. And a loop may carry an **`else`** clause, which runs only if the loop finished *without* hitting a `break` — handy for "search" loops.

???+ example "Example: break, continue, and else"
    ```python
    for n in range(2, 10):
        if n % 2 == 0:
            continue          # skip even numbers
        print("odd:", n)

    target = 7
    for n in [3, 5, 7, 9]:
        if n == target:
            print("found", target)
            break             # stop searching
    else:
        print("not found")    # runs only if no break happened
    ```

## 4. Conditional execution: `if` / `elif` / `else`

Looping decides *how often* code runs; the **`if`** statement decides *whether* it runs. You give it a condition; the indented block runs only when that condition is true. Add `elif` ("else if") to test further conditions in turn, and a final `else` for the fallback.

The example below combines an `if`-chain with a `for` loop — the everyday pattern of acting differently on each item.

???+ example "Example: classifying numbers"
    ```python
    for n in range(-2, 3):
        if n > 0:
            print(n, "is positive")
        elif n < 0:
            print(n, "is negative")
        else:
            print(n, "is zero")
    ```

???+ question "Exercise: conditional filtering"
    Using `l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`:
    
    1. Print only the odd numbers.
    2. Print `"fizz"` for multiples of 3, `"buzz"` for multiples of 5, and the number otherwise.

## 5. Conditions: comparisons and booleans

Every `if` and `while` hinges on a condition — an expression that evaluates to `True` or `False`. This section is about writing those conditions well.

### 5.1 Comparing values vs. identity

To compare *values* Python offers the familiar operators `<`, `>`, `<=`, `>=`, `==` (equal), and `!=` (not equal). To ask the different question of whether two names point to the *same object* — identity, from 1.1 — use `is`.

???+ example "Example: == versus is"
    ```python
    a = [1, 2, 3]
    b = [1, 2, 3]
    print(a == b)   # True  — same contents
    print(a is b)   # False — two different objects

    c = a
    print(a is c)   # True  — same object (two names, one list)
    ```

```recall
Everything is an object: == compares the objects' values, while is compares their identities (id), the very thing we visualised in 1.1.
```

???+ warning "Pitfall: test for `None` with `is`"
    `None` is a single, unique object, so the idiomatic test is `x is None` (and `x is not None`), not `x == None`. Use `is` whenever you mean "the same object," and especially for `None`.

### 5.2 Boolean logic and truthiness

Conditions combine with **`and`**, **`or`**, and **`not`**. Two conveniences make Python conditions concise. First, every object is **truthy or falsy** on its own: `0`, `0.0`, `""`, empty containers (`[]`, `{}`, `set()`), and `None` count as false, and most everything else counts as true — so `if items:` means "if `items` is non-empty." Second, `and`/`or` **short-circuit**: they stop as soon as the result is known.

???+ example "Example: truthiness and boolean operators"
    ```python
    items = []
    if not items:
        print("the list is empty")

    name = ""
    print(name or "anonymous")   # "anonymous" — or returns the first truthy value

    x = 5
    print(0 < x < 10)            # True — chained comparison
    ```

Python also allows **chained comparisons** like `0 < x < 10`, which reads as `(0 < x) and (x < 10)` — closer to mathematical notation and a good example of writing conditions the Pythonic way.

???+ question "Exercise: conditions"
    1. Write a condition that is true when a string `s` is empty *or* contains only spaces. (Hint: `s.strip()`.)
    2. Given `age = 20`, use a single chained comparison to check that it lies between 13 and 64 inclusive.

## 6. Comprehensions: looping as an expression

Very often a loop exists only to *build a new collection* from an old one — square every number, keep the even ones, pair names with scores. Python has a compact, readable syntax for exactly this: the **comprehension**. It is control flow turned into a single expression, and it is one of the most recognisably Pythonic constructs.

The example below builds the same list two ways — the explicit loop, then the comprehension — so you can see the correspondence.

???+ example "Example: a list comprehension"
    ```python
    # explicit loop
    squares = []
    for x in range(6):
        squares.append(x * x)
    print(squares)

    # the same thing as a comprehension
    squares = [x * x for x in range(6)]
    print(squares)
    ```

A comprehension can **filter** with a trailing `if`, and it has **set** and **dict** forms that echo the collections from 1.2 — same braces, same idea.

???+ example "Example: filtering, set, and dict comprehensions"
    ```python
    evens = [x for x in range(10) if x % 2 == 0]
    print(evens)

    unique_lengths = {len(w) for w in ["hi", "bye", "ok"]}   # a set
    print(unique_lengths)

    squares_map = {x: x * x for x in range(5)}               # a dict
    print(squares_map)
    ```

???+ info "Deep dive: parentheses give a *generator*, not a tuple"
    Swapping the brackets for parentheses does **not** make a "tuple comprehension" — it makes a **generator expression**, which produces its values lazily, one at a time, instead of building the whole collection at once:

    ```python
    gen = (x * x for x in range(5))
    print(gen)            # <generator object ...>
    print(list(gen))      # [0, 1, 4, 9, 16]
    ```

    That laziness is the same idea behind `range`, and it is the subject of **1.4 Iterators**. For a tuple, just wrap a generator in `tuple(...)`.

???+ question "Exercise: comprehensions"
    1. Build a list of the squares of the odd numbers from 1 to 19.
    2. From `words = ["Ada", "bob", "CLEO"]`, build a list of their lowercased forms.
    3. Build a dict mapping each word in `words` to its length.

## Summary

Control flow is how a program decides what to do and how often. You now have the whole everyday toolkit:

| Construct | Use it to |
|-----------|-----------|
| `for ... in` | repeat once per item in a container (with `range`, `enumerate`, `zip`) |
| `while` | repeat as long as a condition holds |
| `break` / `continue` / loop `else` | exit early, skip a pass, or act when no `break` occurred |
| `if` / `elif` / `else` | run a block only when a condition is true |
| `==` / `is`, `and`/`or`/`not`, truthiness | write the conditions those choices depend on |
| comprehensions | build a new list, set, or dict in one expression |

Everything here operates on the objects and containers from 1.1–1.2 — loops walk them, conditions test them, comprehensions rebuild them. Next, **1.4 Iterators** opens up *how* iteration actually works, and why lazy sequences like `range` and generators matter.
