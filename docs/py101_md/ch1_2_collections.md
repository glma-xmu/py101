# Collections

## Introduction

Every type in **1.1 Objects and Types** held a single value. The real power of a programming language, though, comes from gathering many values together and treating the whole group as one thing — a roster of students, the pixels of an image, a table of measurements. The types that do this are the **containers**, and they are where most real Python programs spend their time.

This page walks the three container families, distinguished by the question *how are the items kept?* A **sequence** keeps its items in order, so each has a position you can index by. A **set** keeps its items unique, throwing away duplicates and forgetting order. A **mapping** pairs each item with a key, so you look things up by name rather than by position. Once all three are in hand, Section 4 returns to **mutability** — the second axis from 1.1 — because it quietly governs how they all behave, and Section 5 covers **slicing**, reading whole subsequences at once. The code here is live, so run and tweak it.

## 1. Sequences: lists, tuples, and ranges

The containers you will use most are ordered **sequences**. The two workhorses are the **list** and the **tuple**. Both hold an ordered collection of items; the headline difference is mutability. A list is written with square brackets `[]` and is mutable; a tuple is written with parentheses `()` and is immutable.

The example below builds one of each and prints them — notice both can mix items of different types.

???+ example "Example: a list and a tuple"
    ```python
    my_list  = [1, 2, 3, "hello", 4.5]   # mutable
    my_tuple = (1, 2, 3, "world", 6.7)   # immutable
    print(my_list)
    print(my_tuple)
    ```

A third sequence, `range`, represents an arithmetic progression of integers without storing them all — `range(1, 101)` stands for 1 through 100 but holds only its start, stop, and step. It is the idiomatic way to generate number sequences, often handed straight to `list()` or `tuple()`.

???+ example "Example: generating numbers with range"
    ```python
    numbers = list(range(1, 101))  # 1, 2, ..., 100
    print(numbers[:10], "...")     # show just the first ten
    print(len(numbers))            # 100
    ```

`range` takes up to three arguments — `range(stop)`, `range(start, stop)`, and `range(start, stop, step)` — and, exactly like a slice, the `stop` value is *excluded*. A negative step counts downward, and an empty range is perfectly legal.

???+ example "Example: the forms of range"
    ```python
    print(list(range(5)))          # [0, 1, 2, 3, 4]
    print(list(range(2, 8)))       # [2, 3, 4, 5, 6, 7]
    print(list(range(0, 10, 3)))   # [0, 3, 6, 9]
    print(list(range(5, 0, -1)))   # [5, 4, 3, 2, 1] — counting down
    print(list(range(1, 1)))       # [] — empty range
    ```

???+ question "Exercise: building sequences"
    1. Create a list of a few items of different types; print the whole list and one element by index (indexing starts at 0).
    2. Do the same with a tuple.
    3. Use `range()` to build a list, and then a tuple, of the numbers 1 to 100.

Sequences share a common toolkit — indexing, membership tests with `in`, length with `len()`, and slicing (Section 5). They also have **methods**, which are functions attached to an object and called with a dot.

???+ note "Key concept: method"
    A **method** is a function that belongs to an object and is called on it with
    dot notation, as in `my_list.append(4)`. Because lists are mutable, many list
    methods change the list *in place*; tuples, being immutable, have no such
    methods.

The most common list methods are `append()` (add one item to the end), `extend()` (add all items from another iterable), and `pop()` (remove and return the item at an index, last by default). The `+` operator concatenates two sequences into a new one.

## 2. Sets

Where a sequence carefully remembers the order of its items, a **set** deliberately forgets it. A set is an unordered collection of *distinct* items, mirroring the mathematical set: `{1, 2}` is the same set as `{2, 1, 1}`. Sets are mutable; their immutable counterpart is `frozenset`. They shine at two jobs: fast membership tests and removing duplicates.

The example below shows both jobs at once, and how to build a set from another collection.

???+ example "Example: creating sets and dropping duplicates"
    ```python
    seen = {1, 2, 2, 3}
    print(seen)                  # {1, 2, 3} — the duplicate 2 is gone
    print(2 in seen)             # True — membership tests are fast

    nums = set([1, 1, 2, 3, 3])  # build a set from a list
    print(nums)                  # {1, 2, 3}
    print(set())                 # set() — the empty set ({} is an empty dict!)
    ```

Because a set mirrors a mathematical set, it supports the familiar set operations, each available both as a method and as an operator.

???+ example "Example: set operations"
    ```python
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    print(a | b)        # union               {1, 2, 3, 4, 5, 6}
    print(a & b)        # intersection         {3, 4}
    print(a - b)        # difference           {1, 2}
    print(a ^ b)        # symmetric difference {1, 2, 5, 6}
    print({1, 2} <= a)  # subset test          True
    ```

A set's elements must be **hashable**, which is why a set can hold numbers, strings, and tuples but not lists. When you need an *immutable* set — say, to use as a dictionary key or as a member of another set — reach for `frozenset`.

??? info "Deep dive: what does 'hashable' mean?"
    An object is **hashable** if it has a hash value that never changes during its
    lifetime, which is what lets Python place it in the internal table that makes
    set membership and dict lookup fast. Immutable built-ins (numbers, strings,
    tuples of hashables) are hashable; mutable ones (lists, dicts, sets) are not —
    which is exactly why a `list` cannot be a set element or a dict key, but a
    `frozenset` can. This is the practical payoff of the mutable/immutable line
    from Section 4.

???+ question "Exercise: sets"
    1. From `numbers = [1, 2, 2, 3, 4, 4, 5]`, produce a list of just the unique values.
    2. With `a = {1, 2, 3, 4}` and `b = {3, 4, 5, 6}`, compute the values in `a` or `b` but not both.
    3. Try adding a list to a set and read the error; then add a tuple instead and watch it work.

## 3. Mappings: the dictionary

The last of the three families abandons positions altogether and instead pairs each value with a key of your choosing. A **dictionary** (`dict`) stores **key–value pairs** and is the most important container in everyday Python. It is mutable, and it lets you look a value up by its key rather than by position.

The example below creates a dictionary two ways, looks a value up, and both adds and updates a pair.

???+ example "Example: creating and using a dict"
    ```python
    scores = {"Ada": 95, "Bob": 88}   # braces with key: value pairs
    also   = dict(Ada=95, Bob=88)     # the dict() constructor
    print(scores["Ada"])              # 95 — found by key, not position
    scores["Cleo"] = 91               # add a new pair
    scores["Ada"] = 100               # update an existing one
    print(scores)
    ```

Looking up a missing key with `[]` raises a `KeyError`. When a key might be absent, `get()` returns `None` (or a default you supply) instead of crashing — and `update()` merges another dictionary in.

???+ example "Example: safe lookup and merging"
    ```python
    scores = {"Ada": 95}
    print(scores.get("Bob"))               # None — no crash
    print(scores.get("Bob", 0))            # 0 — your chosen default
    scores.update({"Bob": 88, "Ada": 100}) # merge: adds Bob, updates Ada
    print(scores)
    ```

To walk a dictionary you iterate its `keys()`, `values()`, or `items()` — the last hands you the key and value together, which you will use constantly once you reach the `for` loop in **1.3**.

???+ warning "Pitfall: dict keys must be hashable"
    A key must be hashable (see the set deep dive), so you may key by a number,
    string, or tuple — but never by a list. The *value*, by contrast, can be any
    object at all.

???+ question "Exercise: dictionaries"
    1. Build a dict mapping three names to ages, then print one person's age.
    2. Use `get()` to look up a name that is absent, returning `"unknown"` instead of crashing.
    3. Add a new person, then update an existing person's age.

## 4. Mutability and identity

We met mutability as one of the two axes in 1.1; now that we have the container types in hand, we can give it the attention it deserves, because it quietly governs how assignment, comparison, and even dictionary keys behave.

The defining difference between a list and a tuple shows up across several operations. The example below shows that you can read an element from either by index, but only a list lets you reassign or delete one. (The line that would fail on a tuple is left commented — uncomment it to see the error.)

???+ example "Example: only the list can be edited"
    ```python
    l = [1, 2, 3]
    t = (4, 5, 6)

    print(l[0], t[0])  # reading works for both
    l[0] = 100         # OK: lists are mutable
    del l[1]           # OK
    print(l)
    # t[0] = 100       # TypeError: tuples are immutable
    ```

Mutability also explains a subtle behaviour of `+=`. The example below shows that for a mutable list, `+=` changes the object in place so its identity is unchanged; for an immutable tuple, `+=` must build a brand-new object, so its identity changes.

???+ example "Example: += and object identity"
    ```python
    l = [1, 2, 3]; before = id(l); l += [4]; print(before == id(l))  # True  (same object)
    t = (1, 2, 3); before = id(t); t += (4,); print(before == id(t)) # False (new object)
    ```

???+ warning "Pitfall: two names, one mutable object"
    Because a name is only a label, binding `b = a` makes both names point to the
    *same* object. If that object is mutable, a change through one name is visible
    through the other:

    ```python
    a = [1, 2, 3]
    b = a
    b.append(4)
    print(a)   # [1, 2, 3, 4] — surprised?
    ```

    This *aliasing* is harmless for immutable objects (you can never change them)
    but a classic source of bugs for mutable ones.

Visually, the two names share one list, so a change made through `b` is seen through `a`:

```memory
memory: Heap
objects:
  o1: list [1, 2, 3, 4] @ 0x5f3a20
names:
  a -> o1
  b -> o1
```

```recall
Names refer to objects: a and b are two labels on one list, so changing it through either name changes it for both.
```

There is also a practical payoff: immutability is what makes an object usable as a dictionary key or a set member. Try to use a list as a key and Python refuses, because a key must not change underneath the dictionary.

??? info "Deep dive: is the mutable/immutable line really fundamental?"
    Partly. At the language level, mutability is a genuine, observable contract
    that every Python implementation honours, and it is *why* immutable objects
    can be hashed (and thus used as dict keys or set members). But the boundary
    has honest grey areas. A tuple is immutable, yet a tuple *containing a list*
    lets you mutate the inner list — the tuple's own references don't change, but
    what they point to can. And the *reason* a type is immutable is often a design
    and implementation choice (safety, sharing, optimisation, hashing) rather than
    a deep law. So: treat mutability as a real and useful concept, but understand
    that the line is drawn by Python's designers, with C-level mechanics
    underneath — not handed down by mathematics.

???+ question "Exercise: mutability in action"
    1. Set the second element of a list to `-1` and confirm it works; try the same on a tuple and read the error.
    2. Use `id()` to check a list before and after an in-place change — does its identity hold? Then explain, in one sentence, why a tuple "edit" needs a new object.

## 5. Slicing: reading subsequences

Indexing reads one element; **slicing** reads a whole subsequence. The notation is `sequence[start:stop:step]`, where `start` is the first index included (default 0), `stop` is the first index *excluded*, and `step` is the stride (default 1; a negative step walks backwards). The colons are required; the three numbers are each optional.

The example below slices a list a few different ways — change the numbers and rerun to build intuition.

???+ example "Example: slicing a list"
    ```python
    xs = list(range(10))  # [0, 1, ..., 9]
    print(xs[2:5])        # [2, 3, 4]
    print(xs[:3])         # [0, 1, 2]
    print(xs[::-1])       # [9, 8, ..., 0] — reversed
    ```

???+ question "Exercise: slice syntax"
    Decide whether each is a valid slice used as `seq[…]`, and say what it does:
    `1:2:1`, `9:1:-1`, `1.5:2.3:3.14`, `:-5:-1`, `::-1`.

??? info "Deep dive: a slice is itself an object"
    The notation `start:stop:step` builds a `slice` object, and you can make one
    explicitly and reuse it:

    ```python
    s = slice(1, 10, 2)
    print(list(range(20))[s])  # [1, 3, 5, 7, 9]
    ```

    So `slice` is a *type*, and `xs[1:10:2]` is sugar for `xs[slice(1, 10, 2)]`.

## Summary

The containers are where Python programs keep their data. Place any built-in collection on the two axes from 1.1 — *what it holds* and *whether it can change*:

| Category | Types | Mutable? |
|----------|-------|----------|
| Sequences | `list` / `tuple`, `range` | `list` mutable, `tuple`/`range` immutable |
| Sets | `set` / `frozenset` | `set` mutable, `frozenset` immutable |
| Mappings | `dict` | mutable |

Mutability is more than a label: it explains aliasing, the behaviour of `+=`, and why only immutable (hashable) objects can be dictionary keys or set members. With the types (1.1) and the containers (1.2) in hand, **1.3 Control Flow** puts them to work — looping over them and testing them.
