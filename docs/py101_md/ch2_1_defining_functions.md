# Defining Functions

```motto
A function is an object that knows how to do something.
```

## Introduction

So far your programs have been straight-line scripts: a list here, a loop there, a condition to decide what runs. That works until you notice yourself writing the *same* few lines again and again — convert this temperature, clean up that string, score another student. A **function** lets you write such a piece of behavior **once**, give it a name, and then *use* it wherever you need it, as many times as you like.

This is the same idea of **abstraction** we met in 1.1, taken one step further. There, a *name* stood in for a value so you could talk about "the number `x`" without committing to which number. A function lets a name stand in for a *computation* — "square this", "greet that person" — without rewriting the steps each time. And in keeping with our chapter motto, a function is itself just another **object**: it has a type and an identity, it can be passed around and stored, exactly like a number or a list. We lean on that fact heavily by the end of the chapter; for now, we start simple.

Along the way we meet a second idea that quietly powers everything functions do: when a function runs, Python gives it a private workspace called a **frame**. We introduce frames informally as soon as we need them — they are what makes `return` make sense — and then reuse them whenever they help, all the way through recursion later in the chapter.

As before, most code here is **runnable** — press *Run* (or Ctrl/Cmd+Enter), change it, run it again.

## 1. Defining and calling a function

You create a function with the `def` keyword: a name, a parenthesised list of **parameters**, a colon, and an indented **body**. Writing `def` does *not* run the body — it just creates the function object and binds the name to it. The body runs only when you **call** the function, by writing its name followed by parentheses.

A function **definition** always has the same shape — a *header* line, then an indented *body*. In the template below, the parts in <span class="syn-k">red</span> are fixed Python syntax you must type **exactly** as shown; the parts in <span class="syn-p">blue italic</span> are placeholders you replace with your own:

<pre class="func-syntax"><span class="syn-k">def</span> <span class="syn-p">name</span><span class="syn-k">(</span><span class="syn-p">parameters</span><span class="syn-k">):</span>
    <span class="syn-p">body</span>
    <span class="syn-k">return</span> <span class="syn-p">value</span></pre>

Reading the header left to right: the keyword **`def`**, the function's **name**, a pair of **parentheses** holding the **parameters** (the list may be empty), and a **colon** to end the line. Everything indented beneath is the **body**. The red parts — `def`, `(`, `)`, `:`, and `return` — are not yours to change: misspell `def`, drop the colon, or forget the parentheses, and Python stops with a `SyntaxError`.

To **call** the function afterwards, you write its name followed by a pair of **parentheses**, with any **arguments** inside:

<pre class="func-syntax"><span class="syn-p">name</span><span class="syn-k">(</span><span class="syn-p">arguments</span><span class="syn-k">)</span></pre>

The parentheses are **not optional**: a call is *always* `name(...)`. They are required even when the function takes no arguments — you still write the empty `()`, as in `greet()`. The bare name `greet`, with no parentheses, is just the function object itself; it runs nothing until you add `()`.

???+ note "Key concept: function, parameter, argument"
    A **function** is a reusable, named piece of behavior. The names listed in its
    definition are its **parameters**; the actual values you pass when you call it
    are its **arguments**. A **`return`** statement hands a result back to the
    caller and ends the call.

### Defining vs. calling: two new verbs

These two words — *define* and *call* — are new, and they are worth slowing down on, because everything else in this chapter depends on telling them apart.

**Defining** a function is really just a kind of variable creation. In Chapter 1, `x = 5` created a name `x` bound to an object — the number `5`. Writing `def square(n): ...` does the very same thing: it creates a name, `square`, bound to an object. The only thing that changes is *what kind* of object. Instead of a number or a list, `square` is bound to a **function object** — an object that stores a *recipe*: "given some `n`, multiply it by itself." So defining is nothing more than writing a recipe down and pinning a name to it. Nothing is computed yet; no square is taken. You have only prepared the recipe for later.

That is what makes a function such a powerful kind of "variable." A number just sits there holding a value; a function holds *behavior* — a computation you can run on demand.

**Calling** is how you actually *use* that behavior. Think back to how you used ordinary variables in Chapter 1: mostly you *read* them (printed their value) or *modified* them. A function is used differently. You do not print a function to make it work — printing `square` just shows `<function ...>`, the recipe itself. Instead you **call** it: you ask the function to carry out its recipe and hand back a result. The parentheses are the signal — `square(3)` means "run the squaring recipe with `n` equal to `3`, and give me the answer."

Here is why the distinction earns its keep. Suppose `a = 1` and `b = 2`, and you want each of their squares. *Without* a function you would write the recipe out by hand every single time — `a * a`, then `b * b` — repeating yourself and risking a fresh typo at each turn. *Defining* `square` writes that recipe down just once; *calling* it — `square(a)`, then `square(b)` — runs the same recipe wherever you need it. **Define once, call as often as you like.** That split — write the recipe, then run it on demand — is the whole reason functions exist.

???+ warning "Pitfall: the parentheses are what *call* the function"
    `square` and `square(3)` are not the same thing. `square` is the function
    object itself — the recipe; `square(3)` *calls* it and evaluates to `9`. Write
    `square` with no parentheses and you have run nothing: `print(square)` just
    displays `<function square at 0x...>`. To actually *use* a function, you must
    call it, with parentheses.

The example below defines a one-line function and calls it twice. Notice the definition runs once; each *call* runs the body afresh with whatever argument it was given.

???+ example "Example: defining and calling"
    ```python
    def square(n):
        return n * n

    print(square(3))    # 9
    print(square(10))   # 100

    print(type(square)) # <class 'function'> — a function is an object
    ```

That last line is worth pausing on: `square` is an ordinary object with a type, just like `3` or `"hi"`. We will come back to this idea in force in 2.3.

```recall
Names point to objects: `def square(...)` binds the name `square` to a function object — the same kind of name-to-object binding as `x = 3`, except the object happens to be callable.
```

???+ question "In-class exercise: your first functions"
    1. Write a function `double(x)` that returns `x * 2`, and print `double(21)`.
    2. Write a function `greet(name)` that returns the string `"Hello, " + name + "!"`, and print the result for two different names.
    3. Predict what `square` returns for `square(2.5)`, then run it. Why does it work even though we never mentioned floats?

## 2. Parameters are local assignments

Here is the mental model that makes everything else click: **calling a function assigns its arguments to its parameters**. Writing `square(3)` is, in effect, doing `n = 3` *inside* the function, and then running the body. Parameters are just **local names** — names that exist only during the call.

The example below gives a parameter and a helper name. Both `n` and `result` are local: they are created when the call starts and disappear when it ends.

???+ example "Example: parameters and a local helper name"
    ```python
    def square(n):
        result = n * n     # 'result' is a new local name
        return result

    print(square(4))       # 16
    # print(result)        # NameError: 'result' is not defined out here
    ```

Uncomment the last line and run it: outside the function, `result` does not exist. That is not a bug — it is the whole point. Each call gets its own private set of names so calls cannot accidentally clobber one another. But *where* do those private names live while the call runs? That question leads us straight to the call stack.

Not every function needs input. A function may have **no parameters** at all — its parentheses are simply left empty. You still *define* it with `()` and still *call* it with `()`; there is just nothing to pass.

???+ example "Example: a function with no parameters"
    ```python
    def greet():
        return "Hello, class!"

    print(greet())   # Hello, class! — the () runs the function
    print(greet)     # <function greet at 0x...> — no parentheses, nothing runs
    ```

This is the clearest case of the rule from §1: the empty `()` is still required. `greet()` calls the function and gives you the string; `greet` on its own is just the function object, sitting there unused.

## 3. How a call runs: frames on the call stack

When you call a function, Python does three things, in order:

1. It creates a fresh **frame** for this call — a private namespace that holds the call's local names — and places it on top of the **call stack**.
2. It **binds the parameters to the arguments** inside that new frame (the local assignments from §2).
3. It runs the **body** in that frame. When the body finishes (or hits a `return`), the frame is discarded and control returns to whoever made the call.

So at any instant, the call stack is just the pile of frames for the calls that are currently *in progress*. The bottom frame is the module itself (the global names you define at the top level); each call you make stacks another frame on top, and each `return` pops one off.

???+ note "Key concept: frame, call stack, heap"
    A **frame** is the private namespace of one running call; it holds that call's
    local names. Frames are stacked on the **call stack** — one per in-progress
    call. The names in a frame still behave exactly as in Chapter 1: each is a
    label pointing at an **object**, and those objects live in the **heap**,
    shared by everyone. Names live in frames; objects live in the heap.

The picture below shows the call `square(4)` while it is running, started from the top level by `number = 4` then `answer = square(number)`. It has three parts, side by side. In the **middle** is the heap, holding the actual objects — the function, and the integers `4` and `16`. On the **left** is the global namespace (the module's own names); on the **right**, the call stack holds a dashed **frame** for the running call to `square`. Every name, wherever it lives, is just a label pointing at an object in the middle. Notice that `number` and `n` point at the **same** `4`: passing an argument bound a new local name to the very same object — nothing was copied. And `answer` points at nothing yet: the call has not returned.

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
  answer
frame: square(n)
  n -> i4
  result -> i16
```

```recall
Names point to objects: a frame is just a namespace — a set of names — and those names point into the shared heap exactly as in Chapter 1. The global namespace is nothing special; it is simply the namespace of the bottom frame, the module itself.
```

The `square` frame is drawn with a **dashed** border on purpose: it is *temporary*. It exists only while the call runs, and the next step — `return` — is what makes it disappear.

??? info "Deep dive: the heap — and a few genuinely *static* objects"
    The shared object area is the **heap**: memory the interpreter hands out as
    objects are created, and reclaims (through reference counting and garbage
    collection) once nothing points at them. Almost everything lives here — lists,
    strings, functions, your `16`. The exceptions are a handful of objects CPython
    pre-creates once at start-up and never frees: `None`, `True`, `False`, and the
    small integers from −5 to 256. *Those* genuinely sit in static storage, which
    is exactly why `id(4)` never changes and `4 is 4` is always `True` — the
    behavior we met in 1.1. For everything else, think **heap**.

??? note "Further reading: how CPython manages the heap"
    Optional, well past this course — if you want to see the heap for real:

    - [Memory Management — Python/C API](https://docs.python.org/3/c-api/memory.html) — the official overview: *"a private heap containing all Python objects and data structures."*
    - [`Objects/obmalloc.c`](https://github.com/python/cpython/blob/main/Objects/obmalloc.c) — CPython's actual object allocator (*pymalloc*): arenas, pools, and blocks.
    - [Python memory management (video)](https://www.youtube.com/watch?v=XGF3Qu4dUqk) — a visual walkthrough.

???+ info "A quick way to see the stack"
    Python can show you the live stack of frames. You will rarely need this, but it
    makes the idea concrete — run it and read the function names from the call
    that is currently running outward to the module:

    ```python
    import inspect

    def inner():
        for frame in inspect.stack():
            print("frame:", frame.function)

    def outer():
        inner()

    outer()
    ```

We will not dwell on the machinery — no pushing and popping by hand. The one idea to carry forward is simply this: **a running call has its own frame of local names, and those names point at objects in shared memory.** That is all we need to understand `return`.

## 4. The `return` statement

Now we can say precisely what `return` does, because it is the one place where the two halves of our picture — the **call stack** and the **heap** — meet.

When a call runs `return result`, the object that `result` points to is handed back to the caller, and then the call's frame is discarded. The caller binds one of *its own* names to that same object. So `return` neither moves nor copies the object — it stays put in the heap — it simply lets a name in the caller's frame point at it.

The picture below freezes the instant `answer = square(number)` returns. The **green arrow** is the return: `answer`, in the global namespace, is now bound to the very same `16` that `result` points to. A heartbeat later the `square` frame — `n`, `result` and all — is discarded; but the `16` lives on in the heap, because `answer` still points at it.

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

This is why a result computed inside a function can "escape" even though its frame is destroyed: `return` hands back not the name but the **object** (more precisely, a reference to it in the heap), and the caller keeps that reference. The frame was temporary scaffolding; the object it produced outlives it. That is exactly the interaction the diagram makes visible — the **call stack** holds the names that do the work, the **heap** holds the lasting objects, and `return` is what lets a name in the surviving caller reach an object first built inside the vanishing frame.

```recall
The motto at work: the `16` was never trapped inside `square` — it is an object in the heap. `return` simply let `answer`, a name in another frame, point at it.
```

A function can return **any** object, including a tuple — which is the idiomatic way to hand back **several** values at once (recall tuple packing from 1.2).

???+ example "Example: returning several values"
    ```python
    def min_max(numbers):
        return min(numbers), max(numbers)   # packs a tuple

    low, high = min_max([4, 9, 1, 7])       # unpacks it
    print(low, high)                        # 1 9
    ```

And what if a function never says `return`? It still returns something: the object `None` (the lone "no value" scalar from 1.1). A function that only *does* something — prints, modifies a list — hands back `None`.

???+ warning "Pitfall: printing is not returning"
    A function that `print`s a value has *not* returned it — the value went to the
    screen and the call still handed back `None`. If the caller needs the result
    (to store it, add it, pass it on), the function must `return` it. Beginners
    routinely `print` inside a function and then wonder why `total = compute()`
    leaves `total` as `None`. In our frame picture: `print` put characters on the
    screen but bound no object to carry back across the boundary, so `None` came
    back instead.

???+ question "In-class exercise: return"
    1. Write `add(a, b)` that returns `a + b`. Then write a second function that *prints* `a + b` instead. Call each, store the result in a variable, and print that variable. Explain the difference.
    2. Write `divmod2(a, b)` that returns both `a // b` and `a % b` as a tuple, and unpack the result at the call site.
    3. After a call returns, its frame is discarded. Explain in one sentence how the returned object nonetheless survives.

## 5. A worked function: Newton's method

We now have everything a real function needs — parameters, a body, and `return` — so let us write one that actually earns its keep. The problem is mathematical, and it is one of the most useful procedures in all of computing: **given a function, where does it cross zero?**

Suppose you want $\sqrt{2}$ but have no square-root button. That is the same as asking for the root of

$$f(x) = x^2 - 2,$$

because $f(x) = 0$ exactly when $x = \sqrt{2}$. **Newton's method** finds such a root by repeated improvement. Start with any guess $x$, and notice that the tangent line at that point crosses zero at

$$x_{\text{new}} = x - \frac{f(x)}{f'(x)}.$$

That crossing is a better guess than the one you started with. Repeat, and the guesses close in on the true root remarkably fast. For $f(x) = x^2 - a$ we have $f'(x) = 2x$, so each step is just $x - (x^2 - a) / (2x)$.

The only remaining question is when to stop. We stop once the guess is good enough — when $|x^2 - a|$ falls below a **tolerance** we choose. That tolerance is a parameter like any other, so the caller supplies it:

???+ example "Example: Newton's method for a square root"
    ```python
    def sqrt_newton(a, tolerance):
        x = a / 2                              # any starting guess will do
        while abs(x * x - a) > tolerance:
            x = x - (x * x - a) / (2 * x)      # step to the tangent's root
        return x

    print(sqrt_newton(2, 1e-10))    # 1.4142135623746899
    print(sqrt_newton(9, 1e-10))    # 3.0
    ```

Read that against §3 and §4. Each call gets its own frame holding `a`, `tolerance` and `x`; the loop rebinds the local `x` again and again inside that frame; and `return x` hands the final object back to the caller just before the frame is discarded. Nothing new is happening — this is the same machinery, doing something worth doing.

```recall
Names point to objects: `x` is not a box that gets edited. Each `x = x - ...` builds a *new* float in the heap and re-points the local name `x` at it. The old value is simply left behind.
```

???+ question "In-class exercise: Newton's method"
    1. Add a `print(x)` inside the loop and run `sqrt_newton(2, 1e-10)`. How many steps does it take? Roughly how many correct digits does each step buy you?
    2. What happens if you call `sqrt_newton(2, 0)`? Explain, in terms of floating-point values, why the loop may never end.
    3. Write `cbrt_newton(a, tolerance)` for the cube root, where $f(x) = x^3 - a$ and $f'(x) = 3x^2$.

We will meet this function twice more. In 2.2 it will show how a name inside a function is resolved, and in 2.4 we will rewrite it **recursively** — because "improve the guess, then do the same thing again" is exactly what recursion expresses.

## 6. Default parameter values

Newton's method leaves us with a small annoyance. The `tolerance` argument has to be typed on *every* call, even though we almost always want the same value — and for comparable results across runs we usually *should* keep it the same. Only occasionally do we want to change it. What we want is to preallocate a sensible value, and override it when we need to.

A parameter can carry a **default**: a value used when the caller omits that argument. This is perfect for a setting you usually want fixed but occasionally want to change — an error tolerance, a separator, a base.

???+ example "Example: Newton's method with a default tolerance"
    ```python
    def sqrt_newton(a, tolerance=1e-10):       # the usual value, preallocated
        x = a / 2
        while abs(x * x - a) > tolerance:
            x = x - (x * x - a) / (2 * x)
        return x

    print(sqrt_newton(2))            # 1.4142135623746899 — the default is used
    print(sqrt_newton(2, 1e-2))      # 1.4166666666666667 — cruder, and faster
    ```

The same idea reads just as naturally away from mathematics — a greeting that is usually `"Hello"`, but need not be:

???+ example "Example: a default parameter"
    ```python
    def greet(name, greeting="Hello"):
        return greeting + ", " + name + "!"

    print(greet("Ada"))                 # Hello, Ada!
    print(greet("Bob", "Welcome"))      # Welcome, Bob!
    ```

One rule follows from the syntax: **parameters with defaults must come after parameters without them.** `def f(a, b=2)` is fine; `def f(a=1, b)` is a `SyntaxError`, because Python would have no way to tell which argument you meant to omit.

But defaults hold a famous surprise, and it follows directly from our memory picture. **A default value is evaluated once, when the `def` runs — not on each call** — and the resulting object is stored *with the function object* in the heap. Every call that uses the default therefore shares that **one** object. If the default is *immutable* (like the string `"Hello"`), you never notice. If it is *mutable* (like a list), every call mutates the same shared object, and the changes pile up.

???+ example "Example: the shared mutable default"
    ```python
    def append_to(element, to=[]):     # the [] is created ONCE, at def time
        to.append(element)
        return to

    print(append_to(12))   # [12]
    print(append_to(42))   # [12, 42]  — same list, still there!
    print(append_to(7))    # [12, 42, 7]
    ```

You probably expected a fresh `[]` each call. But there is only one list object — born when `def` ran, stored on the function, and reused every time the default is taken. Each call appends to that same object in the heap.

???+ warning "Pitfall: never use a mutable default; use `None` as a sentinel"
    Because a mutable default is created once and shared, using `[]`, `{}`, or
    `set()` as a default is almost always a bug. The standard fix is to default to
    `None` and build a fresh object inside the body — so a new object is created
    *per call*, not once at definition:

    ```python
    def append_to(element, to=None):
        if to is None:
            to = []            # fresh list every call
        to.append(element)
        return to

    print(append_to(12))   # [12]
    print(append_to(42))   # [42]  — independent, as expected
    ```

???+ question "In-class exercise: defaults"
    1. Write `power(base, exponent=2)` so `power(5)` returns `25` and `power(5, 3)` returns `125`.
    2. Run the buggy `append_to` and explain, in terms of *where the default list lives*, why the second call shows two elements.
    3. Rewrite it with the `None`-sentinel pattern and confirm the calls are now independent.

??? info "Deep dive: docstrings and type hints"
    Two habits make functions self-explanatory and are standard in modern Python.
    A **docstring** — a string literal as the very first line of the body —
    documents what the function does; `help()` and editors read it. **Type hints**
    annotate the parameters and result; they do not change how the code runs, but
    they document intent and let tools catch mistakes:

    ```python
    def square(n: int) -> int:
        """Return the square of n."""
        return n * n

    print(square.__doc__)   # 'Return the square of n.'
    ```

    Hints are *not* enforced at runtime — `square(2.5)` still works and returns
    `6.25`. Treat them as precise documentation, not as guarantees.

## 7. A function factory, and a name that surprises you

Here is a second special case, and it is a genuine puzzle. Because a function is an object, we can build several of them in a loop and keep them in a dictionary — a small **function factory**. Each one is supposed to remember its own number.

Read the code, predict what `ff[3]()` prints, and only then run it.

???+ example "Example: five functions from a loop"
    ```python
    ff = {}

    for i in range(5):
        def f():
            return i          # which i is this?
        ff[i] = f

    print(ff[3]())            # not 3
    print(ff[0]())            # not 0 either
    ```

Every one of the five functions returns `4`. The factory did build five distinct function objects — `ff[0]` and `ff[3]` really are different objects — but they all agree on the answer, and the answer is wrong.

The reason is the single most important thing to understand about names inside functions. **`f` has no `i` of its own.** Nothing in `f`'s body assigns to `i`, so `i` is not one of `f`'s local names. When `f` *runs*, Python has to go looking for `i` elsewhere — and it finds the `i` left over from the loop, out in the global namespace. By the time you call `ff[3]()`, that loop has long finished and `i` is sitting at `4`.

So the lookup does not happen when the function is **defined**; it happens when the function is **called**. The name `i` inside `f` and the name `i` in the loop are the *same* name, resolved late — not a private copy taken at definition time.

???+ warning "Pitfall: a name inside a function is looked up when the function runs"
    This bites whenever a function is defined in one place and called in another —
    in a loop, in a list of callbacks, in a dictionary of handlers. The function
    does not photograph the values around it at `def` time. It keeps only the
    *name*, and resolves it later, against whatever the world looks like then.

    A first fix, using what §6 just taught you, is to give `f` a local `i` by
    making it a parameter with a default — and defaults *are* evaluated at `def`
    time, once per loop iteration:

    ```python
    ff = {}
    for i in range(5):
        def f(i=i):           # the local i captures this iteration's value now
            return i
        ff[i] = f

    print(ff[3]())            # 3
    ```

    Note what changed: `f` now has a parameter named `i`, so `i` *is* local, and
    there is nothing to look up outside.

That fix works, but it is a trick — it abuses the parameter list to smuggle in a value. The honest repair needs a piece of vocabulary we do not have yet: a way to say *which* namespace a name belongs to, and a way for an inner function to keep hold of an outer function's variable. That is precisely the subject of the next page.

```recall
Names refer to objects — and a name is only meaningful inside a namespace. `i` inside `f` and `i` in the loop look identical, and that is the whole problem: they *are* identical, because `f` never made one of its own.
```

## Summary

A **function** packages a named, reusable piece of behavior, created with `def` and run by **calling** it. Each call gets a private **frame** on the **call stack**: Python pushes the frame, binds the **arguments** to the **parameters** as local names, and runs the body — then discards the frame. Names live in frames; the **objects** they point to live in the shared **heap**. That split is exactly what **`return`** bridges: it carries an *object* back across the frame boundary so a name in the caller refers to it, after which the callee's frame vanishes but the object lives on.

**Newton's method** (§5) put all of that to work on a real problem, and its tolerance argument motivated **default parameters** (§6) — with the warning that a *mutable* default is created once and shared, so default to **`None`** and build fresh inside. The **function factory** of §7 then left us with an unfinished puzzle: five functions built in a loop that all return the same number, because a name inside a function is resolved when the function *runs*, not when it is defined.

Two threads therefore run out of this page. **2.2 Namespaces and Scope** picks up the puzzle directly: how Python organizes names into namespaces (local, enclosing, global, built-in), the rule it uses to decide which `i` you mean, and the proper repair for the factory. And a function is itself an ordinary **object** — a fact 2.3 exploits fully, where we also look closely at how arguments reach parameters (positional, keyword, and the unpacking operators `*` and `**`). Newton's method returns in **2.4**, rewritten as recursion.
