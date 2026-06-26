# Namespaces and Scope

## Introduction

In 2.1 we saw that names live in **frames** while the objects they point to live in the **heap**. A running call keeps its own local names in its frame; the module keeps its names at the top level. Each such collection of names has a proper title: a **namespace**. This page answers the two questions that follow immediately. How many namespaces are in play at once? And when you write a bare name like `x`, which namespace does Python look in to find it? The answer to the second is a four-letter rule — **LEGB** — that you will use to reason about almost every function you read.

As always, the code here is runnable — press *Run*, change it, run it again.

## 1. A namespace is a dictionary of names

A **namespace** is exactly what 2.1's frames hinted at: a mapping from names to the objects they refer to — literally a Python dictionary underneath. Writing `x = 5` adds or updates the entry `"x" → <the object 5>` in whichever namespace you are currently in. Nothing more mysterious than that.

And Python keeps **several namespaces at once**. You have already met two of them: the **global** namespace (the module's top-level names, which `globals()` returns) and a **local** namespace (the names inside the function call that is running, which `locals()` returns).

The example below shows the two are genuinely separate dictionaries.

???+ example "Example: globals() and locals()"
    ```python
    title = "Chapter 2"            # a global name

    def show():
        note = "inside show"       # a local name
        print("locals:", list(locals()))            # ['note']
        print("title is global:", "title" in globals())  # True
        print("note is global:", "note" in globals())    # False

    show()
    ```

```recall
Names point to objects: a namespace is just the bookkeeping that records which name points to which object — the same arrows we have been drawing, now gathered into a labelled dictionary.
```

???+ note "Key concept: namespace"
    A **namespace** is a mapping from names to objects (a dictionary). Python
    maintains several at once — **built-in**, **global**, **enclosing**, and
    **local** — and every name you use is resolved by looking through them.

## 2. Functions can be defined inside functions

A function body is just ordinary code, and nothing stops that code from containing another `def`. A function defined inside another is a **nested function** — and it can do something new: it can *see* the names of the function that encloses it.

The example below defines `inner` inside `outer`. When `inner` runs, it reads `message` — a local name belonging to `outer` — even though `message` is not one of `inner`'s own locals.

???+ example "Example: an inner function sees the outer's names"
    ```python
    def outer():
        message = "hello from outer"
        def inner():
            print(message)      # inner reads outer's local 'message'
        inner()

    outer()                     # hello from outer
    ```

Two things to notice. First, writing `def inner` only *creates* `inner` each time `outer` runs; like any function it does nothing until it is **called**, which is why we then write `inner()`. Second, `inner` exists only while `outer` is running — it is just a local name of `outer`, born and discarded with that call.

The surrounding scope that `inner` can see — `outer`'s namespace — is called the **enclosing** scope. It is the "E" in the LEGB rule we are about to meet, and the whole reason `nonlocal` exists. That is all we need for now; in 2.3 we put nested functions to real work, passing them around and returning them.

```recall
Names point to objects: nothing magic is happening — `inner` simply has no `message` of its own, so when it needs that name Python looks in the scope around it and finds `outer`'s.
```

## 3. The four namespaces

At any moment, up to four kinds of namespace can be in scope:

- **Local** — the names inside the function call running right now: its frame. Created when the call starts, discarded when it returns.
- **Enclosing** — the local names of an outer function, as seen by a nested function defined inside it (the case we just met in §2). That outer namespace is the inner function's *enclosing* one. We put nested functions to real work in 2.3.
- **Global** — the names defined at the top level of your module. One per module, created when the module starts, alive for the whole program.
- **Built-in** — the names Python pre-defines and makes available everywhere: `print`, `len`, `range`, `max`, `True`, `None`, and so on. They live in the `builtins` module.

The example below confirms that the built-in names really do live in a module of their own.

???+ example "Example: the built-in namespace"
    ```python
    import builtins
    print("print" in dir(builtins))   # True
    print("len" in dir(builtins))     # True
    print(len(dir(builtins)) > 100)   # True — lots of built-in names
    ```

## 4. Scope and the LEGB rule

**Scope** is the region of a program where a name is reachable without any qualification. Each namespace has a scope. When you use a bare name, Python searches the namespaces in a fixed order and stops at the **first** match:

> **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in

This is the **LEGB rule**. If the name turns up in none of the four, Python raises a `NameError`.

The four scopes **nest**, one inside the next: a name search starts in the innermost (Local) and works its way out to the Builtins. The picture below is the map. On the left are the scope names; on the right, the code that lives in each. It also previews the two escape hatches from §6 — `global` lets the innermost function rebind a name all the way out in the module scope, and `nonlocal` lets it rebind a name in the enclosing function.

<div style="text-align:center;margin:1.3rem 0;">
<svg viewBox="0 0 660 290" xmlns="http://www.w3.org/2000/svg" role="img" width="640" style="max-width:100%;height:auto;font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-weight:700;">
  <title>The LEGB scopes nest: Built-in ⊃ Global ⊃ Enclosing ⊃ Local</title>
  <desc>Four nested boxes. Built-in (the interpreter) contains Global (the module), which contains Enclosing (nested functions), which contains Local (the running function). An arrow labelled "global" reaches from the local function out to the global/module scope; an arrow labelled "nonlocal" reaches from local out to the enclosing scope.</desc>
  <defs>
    <marker id="legb-fg" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--md-default-fg-color, #111111)"/></marker>
    <marker id="legb-red" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#e0303a"/></marker>
  </defs>
  <rect x="8" y="12" width="470" height="266" rx="12" fill="#2f6db5"/>
  <rect x="26" y="48" width="436" height="212" rx="11" fill="#3a9d4f"/>
  <rect x="44" y="92" width="404" height="150" rx="10" fill="#f0a500"/>
  <rect x="62" y="140" width="290" height="64" rx="9" fill="#c8202a"/>
  <line x1="243" y1="24" x2="243" y2="250" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.85"/>
  <text x="22" y="35" fill="#ffffff" font-size="17">Builtins</text>
  <text x="40" y="71" fill="#ffffff" font-size="17">Globals</text>
  <text x="58" y="116" fill="#1a1a1a" font-size="17">Enclosure</text>
  <text x="86" y="180" fill="#ffffff" font-size="17">Locals</text>
  <text x="300" y="35" fill="#ffffff" font-size="16">Interpreter</text>
  <text x="312" y="71" fill="#10331c" font-size="16">Modules</text>
  <text x="268" y="116" fill="#3a2600" font-size="16">Nested functions</text>
  <text x="252" y="180" fill="#ffffff" font-size="16">Function</text>
  <path d="M352,170 C600,168 602,44 468,62" fill="none" stroke="var(--md-default-fg-color, #111111)" stroke-width="2.3" marker-end="url(#legb-fg)"/>
  <text x="588" y="108" fill="var(--md-default-fg-color, #111111)" font-size="16">global</text>
  <path d="M352,186 C520,202 520,122 452,122" fill="none" stroke="#e0303a" stroke-width="2.3" marker-end="url(#legb-red)"/>
  <text x="498" y="170" fill="#e0303a" font-size="16">nonlocal</text>
</svg>
</div>

The example below puts three `x`'s in three different scopes; each `print(x)` finds the nearest one in the search order.

???+ example "Example: LEGB in action"
    ```python
    x = "global"

    def outer():
        x = "enclosing"
        def inner():
            x = "local"
            print(x)        # local
        inner()
        print(x)            # enclosing

    outer()
    print(x)                # global
    ```

The picture below freezes the moment `inner()` is running. There are three different names, all spelled `x`, each in its own namespace and each pointing at its own string in the heap. `inner`'s lookup finds the local `x` first and never consults the others. (The built-in namespace sits one step further out still, and is not drawn.)

```memory
memory: Heap
stack: Call Stack
objects:
  s1: 'global'
  s2: 'enclosing'
  s3: 'local'
globals: Global Namespace
  x -> s1
frame: outer()
  x -> s2
frame: inner()
  x -> s3
```

When a name is *not* found locally, the search simply continues outward — which is why a function can read a global without any ceremony.

???+ example "Example: lookup falls through to the global"
    ```python
    greeting = "hi"          # global

    def f():
        print(greeting)      # no local 'greeting' — found in the global scope

    f()
    ```

```recall
The motto at work: there is nothing special about "global" — it is simply the namespace the search reaches *after* the local and enclosing ones. Built-in names are just the ones it reaches last of all.
```

## 5. Shadowing: when one name hides another

Bind a name in an inner scope that also exists in an outer one, and the inner binding **shadows** — hides — the outer one for the rest of that scope. Usually this is harmless and even useful (every function is free to have its own `i` or `result`). Occasionally it is a trap, most painfully when you shadow a **built-in**.

???+ example "Example: shadowing the built-in `max`"
    ```python
    print(max(1, 2))   # 2  — the built-in max

    max = min          # bind the global name 'max' to the min function
    print(max(1, 2))   # 1  — 'max' now finds our global before the built-in!

    del max            # remove our global; the built-in becomes reachable again
    print(max(1, 2))   # 2
    ```

???+ warning "Pitfall: don't name things after built-ins"
    It is easy to reach for `list`, `dict`, `sum`, `max`, `id`, `type`, or `str` as
    variable names — and the moment you do, you lose the built-in for the rest of
    that scope. The symptom is baffling: `list(...)` suddenly raises
    `TypeError: 'list' object is not callable`, because `list` is now your data,
    not the type. Pick another name (`items`, `total`, `kind`, `text`).

## 6. Assigning inside a function: local by default

Here is the rule that explains most scope surprises: **assigning to a name anywhere in a function makes that name local to the whole function** — even if a global of the same name exists, and even on lines *before* the assignment. *Reading* a name is fine (LEGB walks outward and finds the global); but the moment you *assign*, you have declared a local.

So reading a global from inside a function just works.

???+ example "Example: reading a global"
    ```python
    counter = 0

    def show():
        print(counter)   # reads the global — prints 0

    show()
    ```

But *assigning* to that same name makes it local throughout the function — which produces a famous error if you also read it first.

???+ warning "Pitfall: `UnboundLocalError`"
    ```python
    counter = 0

    def bump():
        counter = counter + 1   # UnboundLocalError
        return counter

    # bump()
    ```

    Because `counter` is assigned inside `bump`, it is local for the *whole*
    function — so the right-hand side `counter + 1` reads a local that has no value
    yet. Python does not fall back to the global here. The fix is to be explicit
    about your intent, with `global` or `nonlocal`.

To rebind a **global** from inside a function, declare it with `global`. To rebind a name from an **enclosing** function, declare it with `nonlocal`.

???+ example "Example: global and nonlocal"
    ```python
    total = 0
    def add(n):
        global total            # 'total' refers to the module-level name
        total += n
    add(3); add(4)
    print(total)                # 7

    def outer():
        message = "before"
        def inner():
            nonlocal message    # 'message' refers to outer's local
            message = "after"
        inner()
        print(message)          # after
    outer()
    ```

???+ warning "Pitfall: reach for `return`, not `global`"
    `global` works, but a function that quietly rewrites module-level variables is
    hard to follow and easy to break. The clearer habit is to **pass values in as
    arguments and hand results back with `return`**, keeping each function
    self-contained. Save `global`/`nonlocal` for the few cases that genuinely need
    shared, mutable state.

## 7. Why have scopes at all?

??? info "Deep dive: what scopes buy you"
    Scopes are not red tape — they earn their keep. **Encapsulation:** because a
    function's locals are invisible outside it, you can reuse plain names like `i`,
    `x`, or `result` in every function without fear of collision. **Information
    hiding:** a function's internal names stay private, so callers depend only on
    what it returns, not on how it works. **Reclaiming memory:** because the local
    namespace vanishes when a call returns, the objects that only it referred to
    lose their last reference and can be freed immediately — the reference-counting
    cleanup we mentioned in 2.1. Small, well-scoped functions are easier to read,
    test, and reason about precisely because their names cannot leak.

## Summary

Python resolves every bare name through a stack of namespaces:

| Namespace | Where it applies | Inspect with | Lifetime |
|-----------|------------------|--------------|----------|
| **Local** | inside one running call | `locals()` | that call |
| **Enclosing** | inside a nested function | — | while the outer call runs |
| **Global** | the whole module | `globals()` | the whole program |
| **Built-in** | everywhere, unless shadowed | `dir(builtins)` | the whole program |

A name is looked up **L → E → G → B**, stopping at the first match (or a `NameError`). **Assigning** to a name makes it local for the entire function, so reach for `global` or `nonlocal` only when you truly mean to rebind an outer name — and prefer passing arguments and returning results instead. Shadowing is fine for your own names but dangerous for built-ins.

Next, **2.3 Functions Are First-Class Objects** takes the nested functions we just leaned on and makes them the main event: passing functions as arguments, returning them, and the closures that let an inner function remember its enclosing scope.
