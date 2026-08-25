# Functions Are First-Class Objects

## Introduction

We have said twice now that a function is just an **object** — once in 2.1's motto, and again whenever we drew `square` sitting in the heap like any other value. This page finally cashes that in. Because a function is an ordinary object, you can do with it everything you can do with a number or a list: bind it to a name, store it in a list or dict, **pass it to another function**, and **return it from one**. That freedom is what "first-class" means, and it unlocks a powerful idea — the **higher-order function** — that the whole of 2.4 is built on.

As always, the code is runnable.

## 1. A function is an object

In Chapter 1 we checked an object's identity and type with `id()` and `type()`. A function answers both, just like an integer does — and nothing stops you from giving it a second name, or tucking it inside a list or a dictionary.

???+ example "Example: functions are values you can move around"
    ```python
    def square(n):
        return n * n

    print(type(square))      # <class 'function'>

    sq = square              # a second name for the same function object
    print(sq(5))             # 25 — same function, new name

    ops = {"sq": square, "neg": lambda n: -n}   # functions stored in a dict
    print(ops["sq"](4))      # 16
    ```

```recall
Names point to objects: that function object lives in the **heap** like every value from 2.1, and `sq = square` is the very same aliasing from 1.2 — two names, one object. The object just happens to be callable, so both names can be called.
```

???+ note "Key concept: first-class object"
    An object is **first-class** when the language puts no restrictions on it: it
    can be named, stored in data structures, passed as an argument, and returned
    as a result. In Python, functions are first-class — which is exactly what the
    rest of this page exploits.

## 2. Higher-order functions

Because a function is a value, a function can take *another function* as one of its arguments. A function that **takes a function as an argument, or returns one**, is called a **higher-order function**. You have already used some: `sorted` accepts a `key` function, and `max` does too.

The example below writes a tiny higher-order function of our own, and also passes the built-in `len` as an argument to `sorted`.

???+ example "Example: passing a function as an argument"
    ```python
    def apply_twice(func, x):
        return func(func(x))        # call the passed-in function, twice

    def increment(n):
        return n + 1

    print(apply_twice(increment, 5))   # 7

    words = ["python", "is", "great"]
    print(sorted(words, key=len))      # ['is', 'great', 'python'] — sorted by length
    ```

???+ note "Key concept: higher-order function"
    A **higher-order function** is one that takes a function as an argument or
    returns a function as its result. Ordinary functions work on data; higher-order
    functions work on *behavior*.

Here is a more useful one, and it will stay with us for the rest of the page. Suppose we want to **count how many times a function is called** — a crude profiler. The counter has to survive between calls, and 2.2 gave us two ways to arrange that. There is also a third, which you can now recognise for what it is:

???+ example "Example: `call_count`, counting with a shared default"
    ```python
    def call_count(func, x=[0]):
        print(f"calling {x[0] + 1} times")
        x[0] += 1
        func()

    call_count(print)          # calling 1 times
    call_count(print)          # calling 2 times
    call_count(print)          # calling 3 times
    ```

That `x=[0]` is the *shared mutable default* from 2.1 §6 — the thing we called a bug — used here deliberately. Because the list is created once at `def` time and reused by every call, mutating `x[0]` is a way of remembering something between calls. It works, and you will meet it in real code, but it is a trick: the state is hidden in the signature, and any caller who passes their own `x` silently resets the tally.

The counter from [2.2 §6](ch2_2_namespaces_scope.md) does the same job honestly, with the tally bound to an enclosing frame instead of smuggled into a parameter. We return to that in §4, once closures have a name.

The more pressing limitation is different. Look at the last line of the body: `func()` — with empty parentheses. **`call_count` can only count functions that take no arguments.** `call_count(print)` prints a blank line, which is not much of a demonstration, and `call_count(max)` would fail outright. What we want is to hand `print` something to print.

The obvious repair is to accept one more parameter and pass it along:

???+ example "Example: passing one argument through"
    ```python
    def call_count(func, arg_to_call, x=[0]):
        print(f"calling {x[0] + 1} times")
        x[0] += 1
        func(arg_to_call)

    call_count(print, "hello")     # calling 1 times / hello
    call_count(print, "python")    # calling 2 times / python
    ```

Better — but only for functions taking *exactly one* argument. Two arguments and we are stuck again. We could add `arg2`, `arg3`, and give them defaults, but that is obviously the wrong road: we do not know in advance how many arguments the wrapped function needs, nor what they are called.

To solve this properly we need to look more carefully at how arguments reach parameters at all — and, first, at a piece of Python syntax that has nothing to do with functions.

## 3. How arguments reach parameters

### 3.1 Positional and keyword arguments

When a function has several parameters, you can supply the arguments two ways. **Positional** arguments match parameters by order. **Keyword** arguments name the parameter explicitly, so order stops mattering and the call reads clearly.

???+ example "Example: positional vs keyword arguments"
    ```python
    def power(base, exponent):
        return base ** exponent

    print(power(2, 10))                # 1024 — positional, matched by order
    print(power(exponent=10, base=2))  # 1024 — keyword, order-free
    print(power(2, exponent=10))       # 1024 — positional then keyword
    ```

???+ warning "Pitfall: positional arguments must come first"
    Once a keyword argument appears in a call, every argument after it must also be
    a keyword. `power(base=2, 10)` is a `SyntaxError`. Keep positionals first, then
    keywords.

### 3.2 The star: packing and unpacking

Before we can solve the `call_count` problem, meet the `*` operator on its own ground. It has nothing to do with functions to begin with — it is about **packing** several values into one object and **unpacking** one object back into several names. You have already done both without noticing.

Start with the plainest case. Writing several values on the right of `=` **packs** them into a tuple; writing several names on the left **unpacks** them again:

???+ example "Example: packing and unpacking, without any star"
    ```python
    a = 1, 2, 3           # packing: a is the tuple (1, 2, 3)
    print(a, type(a))

    a, b, c = 1, 2, 3     # unpacking: one name per value
    print(a, b, c)        # 1 2 3
    ```

The rule so far is strict — **as many names as values**. Give it the wrong count and Python refuses, because it has no way to guess which name you meant to leave out:

```python
a, b = 1, 2, 3            # ValueError: too many values to unpack (expected 2)
```

The star relaxes exactly that restriction. A name marked with `*` says *"however many are left over"*, and collects them into a **list**:

???+ example "Example: one star absorbs the remainder"
    ```python
    a, *b, c = 1, 2, 3, 4, 5
    print(a, b, c)        # 1 [2, 3, 4] 5   — b took the middle

    *a, b = 1, 2, 3, 4, 5
    print(a, b)           # [1, 2, 3, 4] 5

    a, *b = 1, 2, 3, 4, 5
    print(a, b)           # 1 [2, 3, 4, 5]

    *a, b = [1]
    print(a, b)           # [] 1           — 'however many' may be none
    ```

Two things follow from "however many are left." The starred name always ends up a **list**, even when it catches a single item or nothing at all. And there can be **at most one** star, since two would be ambiguous — `*a, *b = 1, 2, 3` is a `SyntaxError`, because nothing decides where the first run stops and the second begins.

One more boundary is worth probing. Unpacking needs something to iterate over, so `*a, b = [1]` works while `*a, b = 1` does not — a bare `1` is not a sequence, and Python says so: `TypeError: cannot unpack non-iterable int object`.

???+ question "In-class exercise: predict the unpacking"
    Work these out on paper *before* running them. For each, give the value and type of every name, or say why it fails.

    1. `a = 1, 2, 3`
    2. `a, b, c = 1, 2, 3`
    3. `a, b = 1, 2, 3`
    4. `a, *b, c = 1, 2, 3, 4, 5`
    5. `*a, b, c = 1, 2, 3, 4, 5`
    6. `*a, *b = 1, 2, 3, 4, 5`
    7. `*a, b = 1`

Now the direction that matters for calls. Used in front of an existing sequence, `*` does the **reverse**: it spreads that one object back out into separate values.

???+ example "Example: a star spreads a sequence"
    ```python
    nums = [3, 1, 4, 1, 5]
    print(nums)            # [3, 1, 4, 1, 5] — one argument, a list
    print(*nums)           # 3 1 4 1 5       — five separate arguments
    print(max(*nums))      # 5 — same as max(3, 1, 4, 1, 5)
    ```

Note how `print(nums)` and `print(*nums)` differ: the first hands `print` a single list object, the second hands it five separate arguments. So `*` on a *name* packs, and `*` on a *value* unpacks — one symbol, two opposite directions, and which one you get depends on which side of the `=` (or of the call) it sits.

The double star does the same for **dictionaries**. Where `*` spreads a sequence into positional values, `**` spreads a mapping into `key=value` pairs — most visibly when merging two dicts:

???+ example "Example: `**` unpacks a mapping"
    ```python
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"d": 4, "e": 5, "f": 6}

    combined = {**dict1, **dict2}       # both spread into one new dict
    print(combined)                     # {'a': 1, 'b': 2, ..., 'f': 6}
    ```

### 3.3 Variable-length parameters: `*args` and `**kwargs`

Everything in §3.2 was about ordinary values. Now point the same two operators at a **parameter list**, and the `call_count` problem dissolves.

Passing an unknown number of arguments to a function takes two steps, and they are precisely the two directions you just saw:

1. **Packing** — in the *definition*, `*args` collects however many positional arguments arrive into a tuple.
2. **Unpacking** — in the *call* inside the body, `*args` spreads that tuple back out into separate arguments for the function being wrapped.

???+ example "Example: collecting arguments with `*` and `**`"
    ```python
    def total(*args):
        print("args is", args)      # a tuple of everything passed
        return sum(args)

    print(total(1, 2, 3, 4))        # args is (1, 2, 3, 4) -> 10

    def show(**kwargs):
        for key, value in kwargs.items():
            print(key, "=", value)

    show(a=1, b=2)                  # a = 1 / b = 2  (kwargs is a dict)
    ```

The names `args` and `kwargs` are pure convention — the `*` and `**` do the work. And note what each *is*: `args` is a tuple, `kwargs` is a dict, so everything you know about tuples and dicts from Chapter 1 applies inside the body.

Now `call_count` can count anything at all. It packs whatever arrives into `args`, and unpacks it again on the way through:

???+ example "Example: `call_count`, finished"
    ```python
    def call_count(func, *args, x=[0]):
        print(f"calling {x[0] + 1} times")
        x[0] += 1
        func(*args, sep=", ")           # spread the tuple back out

    call_count(print, "hello", "python", "world")
    # calling 1 times
    # hello, python, world
    ```

The `sep=", "` is there to prove the point. If `args` were passed along as a single tuple, `print` would show it with parentheses and commas of its own; because the star *unpacked* it, `print` received three separate strings and joined them with the separator we asked for. Try deleting the star and compare.

???+ note "Key concept: `*args` and `**kwargs`"
    In a *definition*, `*args` gathers extra positional arguments into a tuple and
    `**kwargs` gathers extra keyword arguments into a dict. In a *call*, `*` and
    `**` spread a sequence or dict back into separate arguments. It is the same
    packing/unpacking from §3.2, applied to a parameter list.

    Two ordering rules apply, and both come from Python needing to tell arguments
    apart: **positional arguments must precede keyword arguments** in a call, and
    in a definition the order is ordinary parameters, then `*args`, then
    `**kwargs`, with defaulted parameters after non-defaulted ones.

A wrapper that accepts `*args, **kwargs` and forwards both can stand in front of *any* function whatsoever — which is exactly the shape of a decorator in 2.4.

???+ example "Example: a pass-through higher-order function"
    ```python
    def call_it(func, *args, **kwargs):
        print("calling", func.__name__)
        return func(*args, **kwargs)        # forward everything, untouched

    print(call_it(max, 3, 7, 2))            # calling max -> 7
    call_it(print, "a", "b", "c", sep=", ") # calling print -> a, b, c
    ```

???+ question "In-class exercise: variable-length arguments"
    1. Write `my_sum(*args)` that returns the sum of however many numbers it is given, and test it with two, then five numbers.
    2. `**kwargs` is a dict, so it has `.keys()`, `.values()` and `.items()`. Write `sum_of_kwargs` so that `sum_of_kwargs(Alice=5, Bob=3, Charlie=4)` returns `12`, and a version that also reports who contributed the most.
    3. Given `pair = (3, 4)`, call `power` from §3.1 as `power(*pair)` and confirm it returns `81`.
    4. Rewrite `call_count` so it no longer needs the `x=[0]` default, using the counter from 2.2 §6 instead. Which version would you rather hand to someone else, and why?

## 4. Functions as return values: closures

The other half of "higher-order" is **returning** a function. When a function defines an inner function and returns it, the inner one carries its **enclosing** scope with it — the local names of the function that built it (recall the enclosing scope from 2.2). An inner function bundled together with the enclosing names it still refers to is called a **closure**.

???+ example "Example: a function that builds functions"
    ```python
    def make_linear(a, b):
        def line(x):
            return a * x + b      # 'a' and 'b' come from the enclosing scope
        return line

    double_plus_one = make_linear(2, 1)
    triple = make_linear(3, 0)

    print(double_plus_one(5))     # 11
    print(triple(5))              # 15
    ```

The picture below freezes `make_linear(2, 1)` at the very instant it returns. Its frame holds `a → 2`, `b → 1`, and the freshly built inner function `line`; the green arrow hands that function back to the global name `double_plus_one`.

```memory
memory: Heap
stack: Call Stack
objects:
  ln: a function
  i2: 2
  i1: 1
globals: Global Namespace
  double_plus_one -> ln @return
frame: make_linear(a, b)
  a -> i2
  b -> i1
  line -> ln
```

Now look at what survives. The instant `make_linear` returns, the frame above is discarded — and yet by the time you call `double_plus_one(5)`, `a` and `b` are *still there*. This is the heap idea from 2.1 carried to its conclusion: the **frame** was temporary, but the objects `2` and `1` are **not** freed, because the returned closure still refers to them. A closure is exactly that — a function bundled with a private pocket of the heap that it keeps alive.

```recall
The motto at work: `make_linear`'s frame vanished, but `a` and `b` are objects in the heap, kept alive by the closure that points at them. Each call to `make_linear` makes a *new* closure with its own captured values.
```

The same idea repairs the function factory from 2.1 §7. `make_f(i)` in [2.2 §6.1](ch2_2_namespaces_scope.md) was a closure all along — each returned `f` kept its own captured `i` alive in exactly the way `double_plus_one` keeps `a` and `b`. Now the name for it is available.

To let the inner function *change* a captured name rather than only read it, use `nonlocal` — exactly the keyword from 2.2. That gives us the counter we built there, which we can finally call by its proper name:

???+ example "Example: a closure that counts"
    ```python
    def make_counter():
        calls = 0
        def step():
            nonlocal calls        # rebind the enclosing 'calls', not a new local
            calls += 1
            return calls
        return step

    c = make_counter()
    print(c(), c(), c())          # 1 2 3
    d = make_counter()
    print(d())                    # 1 — a fresh, independent counter
    ```

Set that beside the `x=[0]` version of `call_count` from §2. Both remember a tally between calls; the difference is *where the memory lives*. The closure keeps it in a captured enclosing name, private and per-counter. The default-argument trick keeps it in the function's signature, visible to every caller and resettable by any of them. Same behavior, and one of them is honest about it.

???+ note "Key concept: closure"
    A **closure** is an inner function together with the enclosing-scope names it
    still refers to. The closure keeps those objects alive after the outer call
    returns, giving the inner function a private, persistent memory.

Closures are more than a counter trick — they let you bundle **data together with the behavior that acts on it**, while keeping the data **private**. The example below builds simple game characters. Each `make_player` call captures its own `hp` and `damage` and returns a small bundle of functions that share them. Notice that `hp` is *not* one of the returned keys: the only way to change a character's health is through its own `take_damage` — nothing outside can reach in and set `hp` to a nonsense value.

???+ example "Example: closures with private state (game characters)"
    ```python
    def make_player(name, hp, damage):
        def attack(other):
            other["take_damage"](damage)      # spend my damage on someone else
        def take_damage(amount):
            nonlocal hp
            hp -= amount
        def status():
            print(f"{name}: {hp} hp")
        return {"attack": attack, "take_damage": take_damage, "status": status}

    bob = make_player("Bob", 100, 10)
    charlie = make_player("Charlie", 100, 5)

    bob["attack"](charlie)
    charlie["status"]()        # Charlie: 90 hp
    bob["status"]()            # Bob: 100 hp — untouched
    ```

All three inner functions close over the *same* `hp` and `damage` from one `make_player` call, so they cooperate: `attack` triggers the other player's `take_damage`, which updates the `hp` that `status` later reads. Two different players carry two independent sets of captured values. If that sounds like an **object** with private fields and methods — it is. Closures are one of the oldest ways to get encapsulation, and the seed of the classes you will meet in Chapter 3.

??? info "Deep dive: where captured variables actually live"
    A closure has to store its captured variables *somewhere*, and you can look
    right at them. Python keeps them in **cells** attached to the function object,
    reachable through `__closure__`:

    ```python
    print(charlie["take_damage"].__closure__)              # a tuple of cell objects
    print(charlie["take_damage"].__closure__[0].cell_contents)   # 90 — the live hp
    ```

    This is the heap idea made literal: the captured `hp` is an object held by a
    cell on the inner function, which is exactly why it outlives the `make_player`
    call that created it. And because `attack`, `take_damage`, and `status` came
    from the *same* call, they share the **same** cell for `hp` — change it through
    one and the others see the change at once. Sibling closures are tied together
    by the heap cells they hold in common.

??? info "Deep dive: three ways to remember, and how to choose"
    Chapter 2 has now shown three ways to make a value survive between calls, and
    they are worth laying side by side because the choice is a real one.

    A **global** (2.2 §6) is the bluntest: the tally is a module-level name that
    anything can read or overwrite, and the function only makes sense next to it.
    A **mutable default** — `call_count`'s `x=[0]` — hides the tally in the
    signature by exploiting the shared-default trap from 2.1 §6; it is compact,
    it appears in real code, and it leaks, because any caller may pass their own
    `x` and silently reset the count. A **closure** with `nonlocal` puts the tally
    in a captured enclosing frame: private, one per counter, and it says what it
    means.

    Reach for the closure. Recognise the other two so you can read other people's
    code — and so you can see that all three are the same idea about *where a name
    lives*, which is the thread running through 2.1, 2.2 and this page.

## 5. `lambda`: a function with no name

Often the function you want to pass somewhere is so small that giving it a `def` and a name feels heavy. A **`lambda`** builds a function *inline*, as an expression, with no name. Its body is a single expression whose value is returned automatically.

The syntax is `lambda parameters: expression`. These two definitions are equivalent:

???+ example "Example: lambda is just a compact function value"
    ```python
    def square_def(n):
        return n * n

    square_lambda = lambda n: n * n      # same behavior, written inline

    print(square_def(6), square_lambda(6))   # 36 36
    ```

Where `lambda` shines is passing a one-off function to a higher-order function, so you never have to name it.

???+ example "Example: lambda as a key function"
    ```python
    people = [("Ada", 36), ("Bob", 41), ("Cleo", 29)]

    print(sorted(people, key=lambda person: person[1]))   # sort by age
    print(max(people, key=lambda person: person[1]))      # oldest -> ('Bob', 41)
    ```

???+ warning "Pitfall: keep lambdas tiny"
    A `lambda` can hold only a *single expression* — no statements, no multiple
    lines. That is by design: if a function needs more than one short expression,
    give it a real `def` and a descriptive name. Reserve `lambda` for the little
    throwaway functions you pass to `sorted`, `max`, `map`, and friends.

## Summary

Functions in Python are **first-class objects**, so they can be named, stored, passed, and returned like any value:

| Idea | What it means |
|------|---------------|
| **First-class** | a function can be aliased, put in a list/dict, passed, and returned |
| **Higher-order function** | takes a function as an argument, or returns one |
| **`*args` / `**kwargs`** | collect extra arguments when defining; spread them when calling |
| **Closure** | an inner function plus the enclosing names it keeps alive |
| **`lambda`** | a small, anonymous function written inline as one expression |

These are not five separate tricks but one idea seen from different sides: *a function is a value*. Next, **2.4 Use Cases** puts that idea to work in the five patterns your course is built around — decorators, recursion, `map`/`filter`/`reduce`, generators, and error handling — every one of them a higher-order function in disguise.
