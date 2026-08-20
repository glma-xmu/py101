# 3. Names, Expressions, and Statements

```motto
Python has no variables. It has names, and names refer to objects.
```

## Introduction

This is the chapter the rest of the course leans on. Almost every Python surprise a competent programmer runs into — the list that changed when you never touched it, the `UnboundLocalError` in a function that clearly defines the variable, the `+=` that behaves one way for integers and another for lists — comes from one misconception: that a Python "variable" is a box that holds a value.

It is not. A Python name is a **label**, and it is attached to an object that lives somewhere else. Once you see it that way, the surprises stop being surprises and become predictions.

We build that up in three passes. §3.1 is the object model: names, values, and the namespaces that hold names. §3.2 works through the grammar of **expressions** — the things that produce a value — with the comparison rules that reliably catch people out. §3.3 does the same for **statements**, the things that *do* something. The main course covers the same territory more slowly in [1.1 Objects and Types](ch1_1_objects.md) and [2.2 Namespaces and Scope](ch2_2_namespaces_scope.md); read those if a section here moves too fast.

## 3.1 Basic elements: names and values

### 3.1.1 Names are bound to values

Python "variables" are special, and the fastest way to see it is to watch an object's **identity** — the number `id()` returns, which in CPython is its address in memory. Increment an integer and look again.

???+ example "Example 3.1: the object moves, not the value"
    ```python
    n = 1
    print(id(n))
    n += 1
    print(id(n))
    ```

The two numbers differ. If `n` were a box holding `1`, adding one would leave the box where it is and change its contents. Instead, `n += 1` computed a *new* object, `2`, and re-pointed the label `n` at it. The original `1` is untouched — it is still there, still `1`, and other names may still be using it. This is worth [drawing on paper](https://david.goodger.org/projects/pycon/2007/idiomatic/handout.html#other-languages-have-variables) (🎨 **Time to draw!**) until it feels obvious.

Three terms make this precise, and the official documentation is worth reading on each:

- **[Names](https://docs.python.org/3/reference/expressions.html#atom-identifiers) and [values](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types).** An identifier occurring as an atom *is* a name; the value is the object it refers to.
- **Assignment, [binding](https://docs.python.org/3/reference/executionmodel.html#naming), and reference.** Assignment **binds** a name to an object. It never copies the object.
- **[Mutability](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types) ([see also](https://docs.python.org/3/library/stdtypes.html#immutable-sequence-types)).** Whether the object itself can be changed after it exists. This is the property that decides everything below.

The next example is the whole lesson in three movements: a plain binding, a *mutation* seen through two names, and a *rebinding* that leaves the second name behind. Run it, then press **Show memory** to see which names share an object.

???+ example "Example 3.2: binding, mutating, rebinding"
    ```python
    # 1. binding: the name 'x' refers to the value 5
    x = 5

    # 2. mutation: two names, one list — changes are visible through both
    a = [1, 2, 3]
    b = a                  # no copy happens here
    b[0] = 4               # mutate the object itself
    print(a, b)            # [4, 2, 3] [4, 2, 3]  — a "changed" without being touched

    # 3. rebinding: strings are immutable, so + must build a new object
    s = 'hello'
    t = s
    print(id(s) == id(t))  # True  — same object
    s = s + 'there'        # rebind s; t is unaffected
    print(id(s) == id(t))  # False — different objects now
    print(s, '|', t)
    ```

Step 2 is where the mental model earns its keep. `b = a` did not copy the list; it attached a second label to the same object. Mutating through either label is visible through both:

```memory
memory: Heap
namespace: Global namespace
objects:
  l1: list [4, 2, 3] @ 0x7f0a12
names:
  a -> l1
  b -> l1
```

Step 3 is the contrast. A string cannot be mutated, so `s + 'there'` has no choice but to build a new object; binding it to `s` moves that one label and leaves `t` pointing where it was.

```recall
Names refer to objects: `a` and `b` are two labels on one list, so changing it through either name changes it for both.
```

??? info "Deep dive: try `x, y = 257, 257`, then `x, y = 256, 256`"
    Compare `x is y` in each case. Small integers (−5 to 256) and short strings are
    **cached** by CPython — the interpreter keeps one shared object and hands it out
    repeatedly — so `x is y` is `True` for 256 and often `False` for 257. This is an
    implementation detail, not a language rule, and it is exactly why you must never
    use `is` to compare values. It also explains an inconsistency people report as a
    bug: in a single compiled block the two `257` literals may be folded into one
    constant, so the same comparison can answer differently at the REPL and in a
    script.

The clearest summary of all of this remains [Ned Batchelder's *Facts and Myths about Python names and values*](https://nedbatchelder.com/text/names.html). His list, in his order — the marked ones are the load-bearing ones:

- **Names refer to values.**
- Many names can refer to one value.
- Names are reassigned independently of other names.
- Values live until nothing references them.
- **Assignment never copies data.**
- Changes in a value are visible through all of its names.
- References can be more than just names.
- Lots of things are assignment.
- **Python passes function arguments by assigning to them.**
- Any name can refer to any value at any time.
- **Names have no type, values have no scope.**
- Values can't be deleted, only names can.

The eighth is worth expanding, because it is where the abstraction pays off: `for` loop targets, `import` statements, `def`, `class`, function parameters, `with ... as`, and `except ... as` are *all* forms of assignment. Learn the rule once and it applies to every one of them. We list them explicitly in [Example 3.9](#332-assignment-statements).

???+ note "Key concept: the takehome"
    1. **Python names are "pointers"** — labels attached to objects, not containers.
    2. **Names bound to mutable objects do not change** when the object is mutated; the object changes underneath every name that refers to it.
    3. **Names bound to immutable objects switch** — the object cannot change, so the name must move to a new one.

### 3.1.2 Namespaces

Names have to live somewhere, and that somewhere has a name of its own. Two related concepts are worth separating carefully, because people use them interchangeably and they are not the same thing:

> [A **namespace** is a mapping from names to objects.](https://docs.python.org/3/tutorial/classes.html) [A **scope** is a textual region of a Python program where a namespace is directly accessible.](https://docs.python.org/3/tutorial/classes.html)

A namespace is a *runtime* object — literally a dictionary, most of the time. A scope is a *lexical* fact about your source code, decided by the compiler from where you wrote things. The example below, taken from the official tutorial, changes the same name in three scopes and prints the result each time.

???+ example "Example 3.3: `local`, `nonlocal`, and `global`"
    ```python
    def scope_test():
        def do_local():
            spam = "local spam"

        def do_nonlocal():
            nonlocal spam
            spam = "nonlocal spam"

        def do_global():
            global spam
            spam = "global spam"

        spam = "test spam"
        do_local()
        print("After local assignment:", spam)
        do_nonlocal()
        print("After nonlocal assignment:", spam)
        do_global()
        print("After global assignment:", spam)

    scope_test()
    print("In global scope:", spam)
    ```

`do_local` binds a fresh local and throws it away. `do_nonlocal` reaches one level out, into `scope_test`'s namespace. `do_global` reaches all the way to the module. Only the last leaves anything visible after `scope_test()` returns.

Namespaces are what let Python decide the [resolution of names](https://docs.python.org/3/reference/executionmodel.html#resolution-of-names). The rule has an acronym — **LEGB** — and it names the four namespaces searched, innermost first:

**L**ocal → **E**nclosing → **G**lobal → **B**uilt-in

[2.2 §4 of the main course](ch2_2_namespaces_scope.md#4-scope-and-the-legb-rule) has a diagram of the four nested scopes and a worked example; it is the best two minutes you can spend if the rule is new. To see the third of them for yourself, print it — the global namespace really is just a dictionary:

???+ example "Example 3.4: the global namespace, printed"
    ```python
    for k, v in list(globals().items()):
        print(k, ':', v)
    ```

???+ warning "Pitfall: iterating `globals()` directly"
    Write `for k, v in globals().items():` without the `list(...)` and you get
    `RuntimeError: dictionary changed size during iteration` — because binding the loop
    targets `k` and `v` *adds two names to the very dictionary you are iterating*. It is
    a small joke at your expense, and a neat demonstration that loop variables are
    ordinary assignments into an ordinary namespace.

Now the gotcha this section exists for. A **class body** executes like a function body — it runs top to bottom in its own namespace, which becomes the class's attributes — but its name resolution does *not* work like a function's. A function that assigns to a name makes that name local everywhere in the function, so reading it before assignment raises `UnboundLocalError`. A class body instead falls back to the enclosing module. Watch what `+=` does with that.

???+ example "Example 3.5: names in a class body jump to the global namespace"
    ```python
    a = [5]
    d = 1

    class A:
        a += [3]        # reads the GLOBAL a, mutates it in place, rebinds A.a
        a = a + [4]     # builds a new list; only A.a moves
        d += 1          # reads the GLOBAL d = 1, binds A.d = 2

    print("A.a       =", A.a)      # [5, 3, 4]
    print("global a  =", a)        # [5, 3]   <- mutated from inside the class!
    print("A.d       =", A.d)      # 2
    print("global d  =", d)        # 1        <- untouched
    ```

Read the two pairs against each other, because the asymmetry is the point. `a` is a **list**, so `a += [3]` is an in-place mutation: the global list is extended, and the global name still points at the same, now longer, object. `d` is an **int**, so `d += 1` cannot mutate anything; it computes a new object and binds it inside the class only. Same syntax, opposite consequences, decided entirely by mutability. Put the identical code inside a function instead and neither line runs at all — you get `UnboundLocalError`, because in a function, assignment makes the name local.

???+ note "Key concept: the takehome"
    1. **Python searches from smaller namespaces outward** — Local, Enclosing, Global, Built-in ([diagram in 2.2](ch2_2_namespaces_scope.md#4-scope-and-the-legb-rule)).
    2. **The exception is an unbound name in a class body**, which skips the enclosing function scope and jumps straight to the global namespace.
    3. **There is one global namespace per module.** Your script runs in `__main__`; every `.py` file you import has its own. "Global" has never meant "program-wide".

## 3.2 Expressions

An **expression** is a piece of code that produces a value. The [reference grammar](https://docs.python.org/3/reference/expressions.html#grammar-token-python-grammar-enclosure) defines them in layers, each built from the one below, and skimming that structure once is what lets you read the documentation for anything else afterwards.

### 3.2.1 Atom

At the bottom is the **atom**: something with no internal structure worth parsing. The grammar, in the BNF the documentation uses — `::=` reads "is defined as" and `|` reads "or":

```text
atom          ::=  identifier | literal | enclosure
literal       ::=  stringliteral | bytesliteral | integer | floatnumber | imagnumber
stringliteral ::=  [stringprefix](shortstring | longstring)
stringprefix  ::=  "r" | "u" | "R" | "U" | "f" | "F"
                   | "fr" | "Fr" | "fR" | "FR" | "rf" | "rF" | "Rf" | "RF"
```

Read the last production and something practical falls out: `f` and `r` are *prefixes on a literal*, not operators or functions. That is why `rf"C:\Users\{name}"` is legal and why the prefix must touch the opening quote with nothing in between.

### 3.2.2 Primaries

A **primary** is the most tightly binding kind of expression — an atom, or an atom with something applied to it. There are five forms, and every piece of Python you write is made of them.

???+ example "Example 3.6: the five primaries"
    ```python
    lst = [10, 20, 30, 40]
    a = 1

    def f():
        pass

    print(a)            # 1. identifier      — an atom, the simplest primary
    print(f.__name__)   # 2. attribute reference    obj.name
    print(lst[1])       # 3. subscription           obj[key]
    print(lst[1:3])     # 4. slicing                obj[start:stop]
    print(range(5))     # 5. call                   obj(args)
    ```

The reason to know the list is that the layer *above* primaries — arithmetic, comparisons, boolean operators — binds more loosely than all five. That is why `-x[0]` negates the element rather than subscripting a negated `x`, and why `a.b(c)` needs no parentheses to mean what you want.

### 3.2.3 [Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)

The six familiar comparison operators are `<`, `>`, `==`, `>=`, `<=`, and `!=`. Python adds two more that are comparisons in the grammar even though they do not look like it: **`is`** / `is not`, which compares *identity*, and **`in`** / `not in`, which tests *membership*.

Comparisons in Python also **chain**, which is unusual and occasionally load-bearing. `a < b > c` does not compare `a < b` and then compare the resulting boolean to `c`, as C would; it means `(a < b) and (b > c)`, with `b` evaluated only once.

???+ example "Example 3.7: chained comparison"
    ```python
    a, b, c = 1, 2, 1
    print(a < b > c)          # True  — means (a < b) and (b > c)
    print(1 < 2 < 3 < 4)      # True  — chains as far as you like
    print((a < b) > c)        # False — forcing the C reading: True > 1 is False
    ```

The second gotcha is that `==` is a method call and `is` is not. `==` invokes the left operand's `__eq__`, which any class may define to mean whatever it likes; `is` compares `id()` and cannot be overridden. A class whose `__eq__` returns `True` unconditionally will therefore claim to equal `None`.

???+ example "Example 3.8: `==` can lie; `is` cannot"
    ```python
    class Foo:
        def __eq__(self, other):
            return True

    f = Foo()
    print(f == None)     # True  — Foo.__eq__ said so
    print(f is None)     # False — identity is not negotiable
    ```

???+ note "Key concept: the takehome"
    1. **Every comparison involving `NaN` is false**, including `NaN == NaN`; the sole exception is `NaN != NaN`, which is `True`. Test with `math.isnan(x)`, never `x == float("nan")`.
    2. **`None` is a singleton** — exactly one instance exists. Always write `x is None` / `x is not None`.
    3. **`x is y` should imply `x == y`.** If you define `__eq__` so that an object is unequal to itself, everything downstream — `in`, `dict`, `set`, `sort` — misbehaves.
    4. **What each one actually calls:** `==` invokes `__eq__`; `is` compares `id()`; `in` invokes `__contains__` if the class defines it, and otherwise falls back to iterating.

### 3.2.4 Operator precedence

The layering of the grammar *is* the precedence table. From tightest to loosest: enclosures and atoms, then primaries, then arithmetic, then bitwise operators, then comparisons, then `not`/`and`/`or`, and finally the conditional expression and `lambda`. The [full table](https://docs.python.org/3/reference/expressions.html#operator-precedence) is worth a bookmark rather than memorisation.

One row of it does bite in practice. Bitwise `&` and `|` bind **tighter** than comparisons, which is why a pandas filter written the obvious way is a `TypeError`:

```python
df[df.year > 2000 & df.gdp < 100]      # parses as df.year > (2000 & df.gdp) < 100
df[(df.year > 2000) & (df.gdp < 100)]  # what you meant
```

## 3.3 Statements

If an expression produces a value, a **statement** does something. The distinction is not pedantic: it is why `x = 5` cannot appear inside a function call, and why the walrus operator `:=` had to be added to get an assignment that *is* an expression.

### 3.3.1 Expression statements

An expression on a line by itself is a statement — evaluated, and the result discarded. Except at the REPL:

> *In interactive mode, if the value is not None, it is converted to a string using the built-in `repr()` function and the resulting string is written to standard output on a line by itself (except if the result is None, so that procedure calls do not cause any output).*

That parenthesis explains a daily experience: typing `x` at the prompt shows you `x`, while typing `my_list.append(4)` prints nothing — `append` returns `None`, and returning `None` is how Python signals "I did this by side effect." It is also why `lst = lst.append(4)` is a classic bug that silently sets `lst` to `None`.

### 3.3.2 Assignment statements

**1. Name-binding constructs.** Assignment wears many costumes. Every one of the following binds a name in the current namespace, and all obey the rules from §3.1:

???+ example "Example 3.9: eight ways to bind a name"
    ```python
    x = 1                       # 1. plain assignment

    for x in range(5):          # 2. a for-loop target
        pass

    class X:                    # 3. a class definition
        pass

    def func(x):                # 4. a def, and 5. its parameters
        pass

    import math                 # 6. import binds the module name
    from math import sqrt       # 7. ... or a name from inside it

    import io
    with io.StringIO("data") as fh:   # 8. the 'as' of a with statement
        pass

    print(x, X, func, math.pi, sqrt(9), fh.closed)
    ```

**2. Augmented assignment** evaluates, then assigns — and the two halves are not what they look like.

???+ example "Example 3.10: `x += 1` is not `x = x + 1` (🎨 **Time to draw!**)"
    ```python
    x, y = 1, 2
    x += 2
    x += y
    print(x + y)
    print(x.__radd__(y))   # int is immutable: a new object comes back
    print(x)

    # now the same operator on a mutable object
    nums = [1, 2]
    other = nums
    nums += [3]            # calls list.__iadd__ -> mutates in place
    print(nums, other)     # [1, 2, 3] [1, 2, 3]  — both names see it

    nums = nums + [4]      # no __iadd__ here: builds a NEW list
    print(nums, other)     # [1, 2, 3, 4] [1, 2, 3]  — they have parted ways
    ```

`x += 1` first looks for `__iadd__`, the in-place version. Mutable types define it and mutate themselves; immutable types do not, so Python falls back to `__add__` and rebinds the name. That single dispatch decision is the whole explanation for Example 3.5, and for every "my function modified my caller's list" bug you will ever file.

**3. Attributes.** An [attribute target](https://docs.python.org/3/reference/simple_stmts.html#attr-target-note) appearing on the left of an assignment always sets the *instance* attribute, even when the name currently resolves to a class attribute. `self.count += 1` inside a method therefore reads the class attribute and writes an instance one — which is how a "shared counter" quietly becomes per-instance. We return to this in [5.1](camp_ch5_oop.md#51-members).

### 3.3.3 The [`assert`](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) statement

`assert None is None` raises nothing; `assert 1 == 2, "message"` raises `AssertionError: message`. The optional second operand is the message, which is why `assert (x, "boom")` — with parentheses — is a bug that always passes: a non-empty tuple is truthy.

Use `assert` for invariants you believe cannot be violated, never for validating input, because `python -O` removes every assert from the compiled code.

### 3.3.4 The [`raise`](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement) statement

`raise SomeError("what went wrong")` throws an exception. Inside an `except` block, `raise` on its own re-raises the current one with its traceback intact, and `raise NewError(...) from err` records the original as the cause — which is what produces the *"The above exception was the direct cause of the following exception"* chain in a traceback.

### 3.3.5 The `yield` statement

`yield` turns a function into a generator, and it belongs with the call stack rather than here. See [4.2.2](camp_ch4_functions.md#422-the-yield-statement).

### 3.3.6 The [`try`](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement) statement

Three details, now that we have the vocabulary for them.

**1. The lifetime of `except ... as e`.** The name `e` is **deleted** at the end of the except block — Python does this deliberately, because the exception holds a reference to the traceback, which holds a reference to every frame, which would keep your entire call stack alive. If you need the exception afterwards, copy what you need out first:

```python
try:
    risky()
except ValueError as e:
    message = str(e)     # keep this, not e
print(message)           # fine; print(e) would be a NameError
```

**2. `finally` always runs — even after `return`.** If the `try` block returns and the `finally` block also returns, the `finally`'s value wins and the original return value is discarded. That is occasionally useful and much more often a bug; never `return` from a `finally`.

**3. The order of `except` clauses.** This is [Example 1.1](camp_ch1_style.md#12-reading-and-handling-error-messages) from the first chapter: clauses are tried top to bottom and the first match wins, so a broad handler placed first makes everything below it unreachable.

## Summary

| | |
|---|---|
| **Names, not variables** | Assignment binds a label to an object and never copies. `id()` shows the object. |
| **Mutability decides everything** | Mutating is visible through every name; rebinding moves one name only. |
| **LEGB** | Local → Enclosing → Global → Built-in. Class bodies skip Enclosing and jump to Global. |
| **One global per module** | `__main__` has its own; so does every module you import. |
| **Comparisons chain** | `a < b > c` means `(a < b) and (b > c)`, with `b` evaluated once. |
| **`==` vs `is`** | `==` calls `__eq__` and can be redefined; `is` compares identity and cannot. Use `is` only for `None`. |
| **`+=` is dispatched** | `__iadd__` if the type has it (mutate in place), otherwise `__add__` and rebind. |
| **`except ... as e`** | `e` is deleted when the block ends; `finally` runs even after `return`. |
