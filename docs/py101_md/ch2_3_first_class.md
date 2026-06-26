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

So far so good — but `apply_twice` only works because `increment` takes exactly one argument. What if the function we want to hand off needs a different number of arguments? To pass arguments through cleanly, we first need to look more carefully at how arguments reach parameters at all.

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

### 3.2 Variable-length arguments: `*args` and `**kwargs`

Sometimes you do not know in advance how many arguments there will be. Two special markers handle that. In a **definition**, `*args` **collects** any extra positional arguments into a *tuple*, and `**kwargs` collects any extra keyword arguments into a *dict*. The names `args` and `kwargs` are just convention — the `*` and `**` do the work.

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

The same stars also work in the *other* direction. In a **call**, `*` **spreads** a sequence into positional arguments and `**` spreads a dict into keyword arguments. One symbol, two opposite jobs: *collect* when defining, *spread* when calling.

???+ example "Example: spreading arguments into a call"
    ```python
    nums = [3, 1, 4, 1, 5]
    print(max(*nums))               # same as max(3, 1, 4, 1, 5) -> 5

    settings = {"sep": "-", "end": "!\n"}
    print("a", "b", "c", **settings)   # a-b-c!
    ```

Now the higher-order puzzle from §2 solves itself. A wrapper can accept *any* arguments with `*args, **kwargs` and pass them straight through to the function it calls — this exact pattern is the heart of decorators in 2.4.

???+ example "Example: a pass-through higher-order function"
    ```python
    def call_it(func, *args, **kwargs):
        print("calling", func.__name__)
        return func(*args, **kwargs)        # forward everything, untouched

    print(call_it(max, 3, 7, 2))            # calling max -> 7
    call_it(print, "a", "b", "c", sep=", ") # calling print -> a, b, c
    ```

???+ note "Key concept: `*args` and `**kwargs`"
    In a *definition*, `*args` gathers extra positional arguments into a tuple and
    `**kwargs` gathers extra keyword arguments into a dict. In a *call*, `*` and
    `**` spread a sequence or dict back into separate arguments. The order in a
    definition is fixed: ordinary parameters, then `*args`, then `**kwargs`; and
    parameters with defaults must follow those without.

??? info "Deep dive: the same star unpacks assignments"
    That gathering `*` is not unique to functions — it also works when unpacking a
    sequence into names, which is handy on its own:

    ```python
    first, *rest = [10, 20, 30, 40]
    print(first)   # 10
    print(rest)    # [20, 30, 40] — '*rest' collects whatever is left
    ```

    One `*` may appear on the left-hand side, collecting the leftover items into a
    list. It is the same idea as `*args`: a star means "however many are left."

???+ question "In-class exercise: variable-length arguments"
    1. Write `my_sum(*args)` that returns the sum of however many numbers it is given, and test it with two, then five numbers.
    2. Write `greet_all(**people)` taking keyword arguments like `greet_all(Alice=9, Bob=7)` and printing `"Alice is 9"` for each. (Recall `kwargs` is a dict.)
    3. Given `pair = (3, 4)`, call `power` from §3.1 as `power(*pair)` and confirm it returns `81`.

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

To let the inner function *change* a captured name (not just read it), use `nonlocal` — exactly the keyword from 2.2. A classic use is a counter that remembers its tally between calls.

???+ example "Example: a closure that counts"
    ```python
    def make_counter():
        count = 0
        def step():
            nonlocal count        # rebind the enclosing 'count', not a new local
            count += 1
            return count
        return step

    c = make_counter()
    print(c(), c(), c())          # 1 2 3
    d = make_counter()
    print(d())                    # 1 — a fresh, independent counter
    ```

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

??? info "Deep dive: the `x=[0]` counter trick"
    Before closures click, people sometimes fake a persistent counter with a
    *mutable default* — `def step(_cache=[0]): _cache[0] += 1`. It works only by
    exploiting the very trap we warned about in 2.1: the default list is created
    once and shared across calls. It is clever but fragile and surprising. A
    closure with `nonlocal` says what you mean and is the right tool.

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
