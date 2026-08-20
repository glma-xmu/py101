# 4. Functions

```motto
A function is an object. Calling it builds a frame; everything else follows from that.
```

## Introduction

You have written hundreds of functions. This chapter is about the two facts underneath them that nobody tells you: a `def` is an **assignment** — it builds a function object and binds a name to it — and a call is a **frame** pushed onto a stack. Hold those two, and generators, closures, decorators, and recursion stop being four separate topics and become four consequences of one mechanism.

§4.1 takes the definition apart. §4.2 takes the *call* apart, which is where `yield` belongs, because a generator is precisely a call whose frame is allowed to pause. §4.3 and §4.4 use the fact that functions are objects: passing them around, and wrapping them. §4.5 closes with recursion, which needs nothing new at all once you can see the stack.

The main course covers this ground at a gentler pace in [2.1 Defining Functions](ch2_1_defining_functions.md), [2.3 First-Class Objects](ch2_3_first_class.md), and [2.4 Use Cases](ch2_4_use_cases.md).

## 4.1 Simple functions

A function is defined and called with this shape:

```python
# function signature
def function_name([formal_parameters]):
    # function body
    pass | return expr | yield expr

function_name([arguments])
```

Behind that syntax, **defining** a function is a three-step procedure:[^cs61a]

1. Create a function with signature `function_name([formal_parameters])`.
2. Set the body of the function (the object lives in the heap[^heap]).
3. Bind `function_name` to that function object in the current frame.

[^cs61a]: The creation and call procedures follow John DeNero's presentation in CS 61A at UC Berkeley.
[^heap]: The heap stores objects; the stack stores frames, and frames hold references.

Step 3 is the one worth dwelling on, because it is ordinary assignment — the same binding rule as [§3.1](camp_ch3_names.md#311-names-are-bound-to-values). Which means a function name can be rebound like any other name, including on top of something you needed.

**1. The names of built-in functions are just names.** `max` is not a keyword. It is a name in the built-in namespace — the "B" of LEGB — and a global of the same name shadows it.

???+ example "Example 4.1: shadowing a built-in"
    ```python
    print(max(1, 2))
    max = min
    print(max(1, 2))
    ```

💡 **How to fix it?** Since `max = min` merely bound a *global* name that shadows the built-in, deleting the global uncovers the original again. Nothing was destroyed; it was hidden.

```python
del max                 # remove the global binding
print(max(1, 2))        # 2 — the built-in was there all along

import builtins
print(builtins.max(1, 2))   # or reach past the shadow without deleting anything
```

Every cell on a page shares one Python session, so the shadowing above really does persist until you reload — paste `del max` into the cell and run it again to undo it. This is the practical reason PEP 8 tells you to avoid built-in names, and the reason `ruff check` flags them ([§1.3](camp_ch1_style.md#13-let-a-tool-do-it-for-you)). Shadowing `list`, `dict`, `id`, `type`, `input`, or `sum` is one of the most common ways a beginner's script develops a mysterious `TypeError` four hundred lines later.

**2. Modifying values outside the function's scope.** 💡 *Why do we need functions at all?* A Python function does one of two things: it **returns** a value to the caller, or it has a **side effect**. In C the distinction is explicit, because you choose between them by choosing your types:

```c
/* side effect: the caller's own variables are changed, through pointers */
void swap(int *x, int *y)
{
    int tmp = *x;
    *x = *y;
    *y = tmp;
}

/* return value: a result is handed back */
int add(int x, int y)
{
    return x + y;
}
```

Python gives you no pointers and no `void`, so the distinction is easy to miss — and the place it bites is default arguments. A default value is evaluated **once**, when the `def` runs, and then belongs to the function object forever. Make it mutable and every call shares one object.

???+ example "Example 4.2: the mutable default argument ([a common gotcha](https://docs.python-guide.org/writing/gotchas/))"
    ```python
    def append_to(element, to=[]):
        to.append(element)
        return to

    my_list = append_to(12)
    print(my_list)          # [12]

    my_other_list = append_to(42)
    print(my_other_list)    # [12, 42]  — not a fresh list!

    print(append_to.__defaults__)   # the one shared list, living on the function object
    ```

The last line makes the mechanism visible: the default is stored on the function object itself, so mutating it mutates it for every future call. The fix is the standard idiom — default to `None` and build the real default inside:

```python
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
```

???+ warning "Pitfall: this applies to every mutable default"
    `{}`, `set()`, a `pd.DataFrame()`, an object you constructed — all evaluated once at
    definition time. `def f(x, cache={})` is the same bug wearing a useful-sounding name.
    `ruff check` catches this one (rule `B006`), which is a good argument for running it.

**3. Chained calls.** Because a call is just an expression, and expressions compose, calls nest as deeply as you like — the inner calls are evaluated first, and their return values become the outer call's arguments.

???+ example "Example 4.3: composing calls"
    ```python
    def f(x, y):
        return x + y

    def g(x, y):
        return x * y

    x1, x2, y1, y2 = 1, 2, 3, 4

    print(g(f(x1, x2), f(y1, y2)))   # g(3, 7) = 21
    ```

## 4.2 How a function is called: frames and namespaces

### 4.2.1 The call procedure

Calling a function is also a three-step procedure, and it is the mirror of the creation procedure:[^cs61a]

1. Add a local **frame**, forming a new environment.
2. **Bind the function's formal parameters to its arguments** in that frame.
3. Execute the body of the function in that new environment.

Step 2 is Batchelder's "Python passes function arguments by assigning to them" from [§3.1.1](camp_ch3_names.md#311-names-are-bound-to-values), stated as mechanism. Arguments are not copied into the function; the parameter is a *new name in a new namespace*, bound to the very same object the caller passed. That is the entire explanation of why a function can mutate your list but cannot rebind your variable.

🎨 **Time to draw!** Here is the picture for `square(4)`, mid-call. The module's names are on the left, the objects in the middle, and the call's own frame on the right — note that `n` and `number` are two names in two different namespaces pointing at *one* object:

```memory
memory: Heap
stack: Call Stack
objects:
  fn: a function
  i4: 4
  i16: 16
globals: Global Namespace
  square -> fn
  number -> i4
  answer -> i16 @return
frame: square(n)
  n -> i4
  result -> i16
```

To step through anything larger, [`pythontutor.com`](https://pythontutor.com/) animates the same picture for code you paste in. [2.1 §3](ch2_1_defining_functions.md) of the main course walks through the call stack in detail.

### 4.2.2 The `yield` statement

Generators are functions too. Writing `yield` anywhere in the body changes what `def` produces: calling it no longer runs the body, it builds a **generator-iterator** object. The difference that matters is what happens at `yield` — the frame is **suspended** rather than discarded, keeping every local name alive, and resumed where it left off when you ask for the next value.

The example below catches a generator in the act. `gi_running` reports whether the generator's frame is currently executing, so printing it from *inside* and *outside* the body shows the frame switching on and off.

???+ example "Example 4.4: a frame that pauses"
    ```python
    def g():
        print(f"inside the generator: gi_running = {g1.gi_running}")
        yield 1

    g1 = g()
    print("before first next():", g1.gi_running)   # False — body has not started
    next(g1)                                       # now the body runs
    print("after:", g1.gi_running)                 # False — suspended again
    print("frame:", g1.gi_frame)                   # the suspended frame itself
    ```

Notice that `g1 = g()` printed nothing. No line of the body ran until `next(g1)`, and after `yield 1` handed back its value the frame went back to sleep with all of its locals intact. That is the whole idea: a generator is a call you can pause.

??? info "Deep dive: what the bytecode says"
    `import dis; dis.dis(g)` shows a `RETURN_GENERATOR` at the top of the generator's
    code, where an ordinary function would begin its work directly. The compiler
    decides a function is a generator *at compile time*, purely from the presence of
    a `yield` in the body — which is why a `yield` inside an `if` that never runs
    still turns the whole function into a generator.

### 4.2.3 `yield` for coroutines

`yield` sends values *out*. It can also take values *in*: written as an expression, `term = yield`, it evaluates to whatever the caller passes to `.send(...)`. A generator used this way is a **coroutine** — a computation you feed incrementally rather than one you pull results from.

The example below (adapted from *Fluent Python*) averages numbers as they arrive, keeping the running total in its suspended frame, and returns a summary when told to stop. Three details make it work: `next(coro)` **primes** it, running up to the first `yield`; each `.send(value)` resumes the frame with that value; and the `return` inside a generator does not return normally at all — it raises `StopIteration`, carrying the value in `.value`.

???+ example "Example 4.5: a coroutine that accumulates"
    ```python
    from typing import NamedTuple

    class Result(NamedTuple):
        count: int
        average: float

    class Sentinel:
        def __repr__(self):
            return '<Sentinel>'

    STOP = Sentinel()

    def averager():
        total, count, average = 0.0, 0, 0.0
        while True:
            term = yield              # receives whatever .send() passes in
            print('received', term)
            if isinstance(term, Sentinel):
                break
            total += term
            count += 1
            average = total / count
        return Result(count, average)

    coro = averager()
    next(coro)                        # prime it: run up to the first yield
    for value in (10, 20, 30):
        coro.send(value)

    try:
        coro.send(STOP)
    except StopIteration as exc:      # 'return' in a generator arrives as this
        print('result:', exc.value)
    ```

The sentinel deserves a word. A plain `None` would be ambiguous — `.send(None)` is what `next()` does — so a private, one-of-a-kind object is used to mean "finish up", and `isinstance` recognises it without any chance of collision with real data.

Having to remember `next(coro)` before the first `send` is a genuine annoyance, and a decorator can remove it. That is [Example 4.10](#44-decorators), once we have decorators.

!!! tip "Where this leads"
    `yield from` delegates to a sub-coroutine and passes values through it, and this
    entire mechanism is what `async def` / `await` were built on top of. If you ever
    write asynchronous code — scraping, API calls, anything I/O-bound — you are using
    a polished version of what you just read.

## 4.3 Higher-order functions

In Python everything is an object, so when you call `f(x=1)` you pass an `int` object to `x`. Functions are objects too — which means a function can be passed to a function, and returned from one. That is what **higher-order** means, and it is how you abstract over a *process* rather than a value.

The concrete case: you are comparing three machine-learning algorithms. Keep the algorithms in their own module, and let `main.py` hold one function that runs whichever you hand it. Adding a fourth algorithm then changes nothing in `main.py`.

???+ example "Example 4.6: a function as an argument (first-class)"
    ```python
    # module.py -- several algorithms with a common signature
    def algo1(x):
        print("algorithm 1 computing")
        return 1.1 if x == 1 else 1.2

    def algo2(x):
        print("algorithm 2 computing")
        return 2.1 if x == 1 else 2.2

    def algo3(x):
        print("algorithm 3 computing")
        return 3.1 if x == 1 else 3.2

    # main.py -- one driver, any algorithm
    x = 0

    def ml(f):
        print(f"{f.__name__} invoked")     # the object carries its own name
        ans = f(x)
        print("answer is", ans)
        return ans

    for algo in (algo1, algo2, algo3):     # functions in a tuple, like any object
        ml(algo)
    ```

`f.__name__` is the giveaway that `f` really is an object with attributes, not a special syntactic thing. The other direction — returning a function — is where **closures** appear: `adder` outlives the call to `make_adder` that created it, and remembers `n`.

???+ example "Example 4.7: a function as a return value"
    ```python
    # example from CS 61A of UCB
    def make_adder(n):
        def adder(k):
            return k + n          # 'n' comes from the enclosing scope
        return adder

    add_three = make_adder(3)
    print(add_three(5))           # 8

    print(add_three.__closure__[0].cell_contents)   # 3 — n, kept alive
    ```

`make_adder(3)` has returned; its frame is gone. Yet `n` is still there, because the inner function holds a **cell** referring to it — the "E" of LEGB made concrete. That is Batchelder's "values live until nothing references them" doing its job. [2.3 §4](ch2_3_first_class.md) covers closures properly.

## 4.4 Decorators

A decorator is a higher-order function with syntax sugar. `@decor` above a `def` means exactly `func = decor(func)` — nothing more. Its most common use is *adding behaviour* to a function without editing the function.

Take the `fibonacci` we will define below. The reason `fibonacci(35)` takes so long is that it recomputes `fibonacci(1)` through `fibonacci(34)` an exponential number of times. If we could save results already computed instead of recursing again, the time would collapse. The question is how to implement that without touching `fibonacci` itself.

???+ example "Example 4.8: memoising with a decorator"
    ```python
    import time

    def memoize(func):
        cache = {}                        # lives in the closure, one per decoration
        def wrapper(n):
            if n not in cache:
                cache[n] = func(n)
            return cache[n]
        return wrapper

    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    start = time.perf_counter()
    print(fibonacci(28), f"plain:    {time.perf_counter() - start:.3f}s")

    fibonacci = memoize(fibonacci)        # <- exactly what @memoize would do
    start = time.perf_counter()
    print(fibonacci(28), f"memoised: {time.perf_counter() - start:.3f}s")
    ```

Read the rebinding line carefully, because it is the whole trick: `fibonacci` now names the *wrapper*, so the recursive calls inside the original body — which look up the global `fibonacci` — go through the cache too. Had we written `@memoize` above the `def`, the identical rebinding would have happened, just earlier and more legibly. In real code you would not write `memoize` at all; the standard library has it:

```python
import functools

@functools.cache               # or @functools.lru_cache(maxsize=None)
def fibonacci(n):
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)
```

**Remember: a decorator is applied at definition, not at run time.** Redefining `memoize` afterwards does nothing to a function that was already decorated — the wrapper it built is already bound.

The wrapper does cost you something, though: it is a *different* object, so it has the wrong name and the wrong docstring. `functools.wraps` copies that metadata across, and you should use it in every decorator you write.

???+ example "Example 4.9: `functools.wraps` keeps the identity"
    ```python
    import functools

    def shout(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs).upper()
        return wrapper

    def polite(func):
        @functools.wraps(func)              # the only difference
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs).upper()
        return wrapper

    @shout
    def greet_a(name):
        """Say hello."""
        return f"hello, {name}"

    @polite
    def greet_b(name):
        """Say hello."""
        return f"hello, {name}"

    print(greet_a("ana"), "|", greet_a.__name__, "|", greet_a.__doc__)
    print(greet_b("ana"), "|", greet_b.__name__, "|", greet_b.__doc__)
    print(greet_b.__wrapped__)              # wraps also keeps the original around
    ```

Without `@wraps`, `greet_a.__name__` is `'wrapper'` and its docstring is gone — which breaks `help()`, debuggers, and any code that dispatches on `__name__` (such as `ml` in [Example 4.6](#43-higher-order-functions)).

Now back to the annoyance from §4.2.3: a coroutine must be primed with `next()` before you can `send` to it. That is a behaviour to add to a function without editing it — a decorator.

???+ example "Example 4.10: a decorator that primes a coroutine"
    ```python
    import functools

    def coroutine(func):
        @functools.wraps(func)
        def start(*args, **kwargs):
            cr = func(*args, **kwargs)     # build the generator
            next(cr)                       # run it up to the first yield
            return cr                      # hand back a primed coroutine
        return start

    @coroutine
    def echo():
        while True:
            received = yield
            print("echo:", received)

    e = echo()          # already primed -- no next(e) needed
    e.send("first")
    e.send("second")
    ```

Compare this with Example 4.5, where the bare `next(coro)` had to be remembered by hand. The decorator moves that requirement from the caller to the definition, which is the general shape of the pattern: put the ceremony where it is written once, not where it is used many times.

[This primer on decorators](https://realpython.com/primer-on-python-decorators/#simple-decorators-in-python) is the best next thing to read, and if you want decorators that themselves take arguments — a third layer of nesting — [start here](https://realpython.com/primer-on-python-decorators/#creating-decorators-with-optional-arguments). We meet a more complicated example, a decorator defined *inside* a class, in [5.2.2](camp_ch5_oop.md#522-an-example).

## 4.5 Recursion

A function refers to itself inside its own body — which needs no new machinery at all, since by the time the body *runs*, the name has been bound and each call gets its own frame.

The first case is barely recursion in the usual sense; it is a function that returns *itself*, so that calling the result calls it again. It is the mechanism behind the chained `print_sum(1)(3)(5)` from [§1.2](camp_ch1_style.md#12-reading-and-handling-error-messages), and a compact demonstration that a function name is just a name.

???+ example "Example 4.11: recursion 1 — returning yourself"
    ```python
    def print_all(x):
        print(x)
        return print_all

    print_all(1)(2)(3)(4)     # each call prints, then hands back the function
    ```

The second is the familiar shape: a **base case** that stops, and a **recursive case** that moves toward it. Miss either and you get `RecursionError`.

???+ example "Example 4.12: recursion 2 — factorial"
    ```python
    def factorial(n):
        if n == 0 or n == 1:      # base case
            return 1
        else:
            return n * factorial(n - 1)   # recursive case

    number = 5
    print(f"Factorial of {number} is {factorial(number)}")

    import sys
    print("recursion limit:", sys.getrecursionlimit())   # ~1000 by default
    ```

That limit is not a formality. CPython does **not** optimise tail calls, so every recursive call really does occupy a frame on the stack, and a recursion a few thousand deep will stop your program. When the natural formulation is recursive but the depth is data-dependent — walking a large tree, or a long time series — write the loop instead.

Recursion is genuinely useful all the same: it is the natural way to express anything defined in terms of smaller copies of itself, which in this field means tree structures, dynamic programming, and automatic differentiation — the last of which we build in [5.3](camp_ch5_oop.md#53-inheritance).

## Summary

| | |
|---|---|
| **`def` is assignment** | It creates a function object and binds a name. Names can be shadowed — including built-ins. |
| **A call is a frame** | Parameters are new names in a new namespace, bound to the caller's objects. |
| **Defaults evaluate once** | At definition, and live on the function object. Never default to a mutable. |
| **A generator pauses a frame** | `yield` suspends with locals intact; `.send()` resumes with a value. |
| **`return` in a generator** | Arrives as `StopIteration.value`, not as a normal return. |
| **A decorator is `f = d(f)`** | Applied at definition time. Always use `functools.wraps`. |
| **Recursion costs frames** | No tail-call optimisation; `sys.getrecursionlimit()` is roughly 1000. |
