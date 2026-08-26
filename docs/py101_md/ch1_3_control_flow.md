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

???+ question "Exercise: looping over every container"
    1. Make a list and use a `for` loop to print its elements.
    2. Do the same with a tuple.
    3. Make a dictionary and use a `for` loop to print its **values**.
    4. Use a `for` loop to print its **keys**.
    5. Print the key–value pairs in a formatted way using an f-string, so the output reads `apple costs 3`.

    For 3 and 4, look up `.values()` and `.items()` — and note that looping a dict
    directly, as in the example above, gives you the keys.

???+ warning "Pitfall: never change a container while looping over it"
    A `for` loop keeps an internal position in the container. Add or remove items
    mid-loop and that position no longer means what the loop thinks it does. The
    two cases below fail in *different* ways, which is what makes this worth
    studying rather than just memorising.

    A dictionary refuses outright:

    ```python
    d = {'a': [1], 'b': [1, 2], 'c': [], 'd': []}
    for i in d:
        if not d[i]:          # empty list is falsy
            d.pop(i)          # RuntimeError: dictionary changed size during iteration
    ```

    A list does something worse — it stays silent:

    ```python
    d = [1, 2, 3, 0, 5]
    for i in range(4):
        if not d[i]:
            d.pop(i)
    print(d)                  # [1, 2, 3, 5] — correct!
    ```

    That looks like a success, and it is the reason this bug survives in real code.
    But it is luck, not correctness. The `0` happened to be the last index the loop
    visited, so nothing shifted underneath it. Change the data and the same code
    misbehaves in two different ways:

    ```python
    d = [1, 0, 0, 4, 5]
    for i in range(4):
        if not d[i]:
            d.pop(i)
    print(d)                  # [1, 0, 4, 5] — a zero SURVIVED

    d = [0, 0, 0, 0, 5]
    for i in range(4):
        if not d[i]:
            d.pop(i)          # IndexError: list index out of range
    ```

    Trace the middle case. Removing the `0` at index 1 shifts everything after it
    down a position, so the second `0` slides into index 1 — which the loop has
    already passed. It is stepped over and never tested. In the third case the list
    shrinks faster than the loop advances, until `d[3]` refers to an index that no
    longer exists.

    So the dictionary's `RuntimeError` is the *kind* behaviour: it tells you
    immediately. The list quietly returns a plausible answer that is sometimes
    wrong, which is far harder to catch.

    The fix for both is the same: **iterate over one thing and modify another.**
    Build the result you want instead of editing in place — a comprehension (§6) is
    usually the clearest way — or loop over a copy, `for i in list(d):`, so the
    thing being iterated and the thing being changed are two different objects.

    ```python
    d = {'a': [1], 'b': [1, 2], 'c': [], 'd': []}
    d = {k: v for k, v in d.items() if v}     # build a new dict; nothing mutated
    print(d)                                   # {'a': [1], 'b': [1, 2]}
    ```

    This is the same lesson as the aliasing pitfall in 1.2 §4, seen from another
    angle: mutating an object that something else is currently relying on.

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

The name is the picture: a zipper, pairing up two rows of teeth. `zip` is also the natural way to build a dictionary from two parallel lists — `dict(zip(names, scores))` — and it stops at the shorter input.

But `zip` does not hand you a list of pairs. Print it and you get something odd:

???+ example "Example: a `zip` is used up once"
    ```python
    account = ["622848", "600314", "500297"]
    balance = (1_000_000, 1_300_500, 500)

    z1 = zip(account, balance)
    print(z1)                 # <zip object at 0x...> — not a list!

    for k, v in z1:
        print(k, "has a balance of", v)

    print("second pass:")
    for k, v in z1:           # nothing at all happens
        print(k, "has a balance of", v)

    print(list(zip(account, balance)))   # a fresh zip, materialised
    ```

The second loop prints nothing, and no error is raised. A `zip` object does not *hold* the pairs; it **produces** them, one at a time, on demand — and once produced, they are gone. Walk it a second time and there is nothing left to give.

That behaviour is not a quirk of `zip`. It is the defining property of an **iterator**, and `enumerate`, `range`'s companions, generator expressions and file objects all share it. If you need the pairs more than once, capture them with `list(...)`. Chapter 1.4 takes this apart properly — for now, simply notice that Python often returns a thing that *will produce* values rather than a container that already holds them.

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
    Using the thirteen-element list
    `l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]`:

    1. Print the elements that are **odd**.
    2. Print the elements that are **perfect squares** (1, 4, 9, …).
    3. Print the elements that are **perfect cubes**.
    4. Print `"fizz"` for multiples of 3, `"buzz"` for multiples of 5, and the number otherwise.

    For 2 and 3, you need to decide whether a number *is* a square without a
    built-in that tells you. Two approaches: test whether `round(n ** 0.5) ** 2 == n`,
    or check membership in a set you build first, such as
    `{i * i for i in range(1, 4)}`. Which would you trust for very large numbers,
    and why?

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
    `None` is a single, unique object — there is exactly one of it in a running
    program, no matter how many names point at it. So after `a = None; b = None`,
    `a is b` is `True`, because both names label that same one object. That is why
    the idiomatic test is `x is None` (and `x is not None`) rather than
    `x == None`: you are asking about identity, and identity is the stronger and
    faster question. Use `is` whenever you mean "the same object," and always for
    `None`.

Every comparison is an **expression** — a piece of code that evaluates to a value — and comparisons evaluate to a `bool`. That is what lets you put one straight into an `if`.

Python also allows comparisons to be **chained**, and it means what mathematical notation means, not what most languages do. Writing `0 <= x < 10` really does test both halves, and reads exactly as it would on a blackboard.

???+ example "Example: chained comparisons"
    ```python
    a, b, c, d, e = 1, 4, 3, 3, 5

    print(a < b > c == d != e)   # True
    print(a < b and b > c and c == d and d != e)   # the same thing, spelled out

    x = 7
    print(0 <= x < 10)           # True — one clear test, not two
    ```

A chain is evaluated pairwise and joined with `and`, so `a < b > c` means `a < b and b > c`. One detail follows from that: each middle operand is evaluated only **once**, and the chain stops early if any link is false.

Chaining is genuinely useful for ranges like `0 <= x < 10`. Longer chains such as the first line above are legal, but they are a puzzle rather than good style — if you find yourself writing one, `and` says it more plainly.

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

## 7. What people mean by "Pythonic"

You have now met the word twice — §1.2 called `enumerate` and `zip` "the Pythonic way" — so it deserves a definition, even a loose one.

**Pythonic** is not a technical term. It describes code that uses the constructs Python actually gives you, rather than habits carried over from another language and transliterated. C-style code written in Python usually *works*; it just reads as though the author would rather have been writing C. The Pythonic version is normally shorter, and — more to the point — it says what it means, so a reader spends no effort reconstructing the intent.

The clearest test is the one from §1.2. Both of these produce the same output:

```python
for i in range(len(colors)):        # not Pythonic: indices as a means to an end
    print(i, colors[i])

for i, color in enumerate(colors):  # Pythonic: says "index and item"
    print(i, color)
```

The second is not merely tidier. It cannot go out of range, it does not repeat `colors`, and it states the actual intention — *number these items* — instead of leaving the reader to infer it from arithmetic.

Without labelling them, this chapter has already handed you most of the standard vocabulary:

| Feature | Where it appeared | What it replaces |
|---|---|---|
| **f-strings** | 1.1 | `+` concatenation, `%`, `.format()` |
| **`None`** and `is None` | 1.1, §5.1 | sentinel values like `-1` or `""` |
| **`with`** | 1.2 §3.1 | remembering to call `.close()` |
| **`zip`** | §1.2 | index arithmetic over two lists |
| **`enumerate`** | §1.2 | `range(len(...))` plus a counter |
| **`sorted`** with `key=` | 1.2 | hand-written sorting |
| **comprehensions** | §6 | a loop that only exists to fill a list |
| **truthiness** (`if not d[i]`) | §5.2 | `if len(x) == 0`, `if x == None` |

Two cautions, because "Pythonic" gets used as a bludgeon. It is not a synonym for *short* — a comprehension three lines wide with two conditions is worse than the loop it replaced, and §6's deep dive says so. And it is not a synonym for *clever*; the chained comparison in §5.1 is legal and compact and still harder to read than `and`. The goal is code whose meaning is obvious to the next reader, which is usually you.

???+ question "Exercise: make it Pythonic"
    Rewrite each of these, then say in one sentence what the rewrite makes clearer.

    1. `i = 0`, then a `while i < len(items):` loop that prints `items[i]` and increments `i`.
    2. `result = []` followed by a `for` loop that appends `n * n` when `n` is even.
    3. `if len(names) == 0: print("empty")`.
    4. `f = open("data.txt"); text = f.read(); f.close()`.
    5. `msg = "Total: " + str(total) + " items"`.
    6. Two lists `ks` and `vs` combined into a dict with a `range(len(ks))` loop.

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
