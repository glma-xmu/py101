# 7. Making Python Fast

```motto
Measure, then choose a better data structure. Only then reach for a compiler.
```

## Introduction

Python is slow, and everyone knows it. What is less widely known is that most slow Python is not slow *because of Python* — it is slow because of a quadratic membership test, a list that should have been a `set`, or ten million intermediate objects built to be thrown away. Those cost you a factor of a thousand and are fixed by changing three lines. Rewriting in C buys you a factor of a hundred and costs you a week.

So the order of operations in this chapter is deliberate, and it is the order you should follow in your own work. §7.1 is about **choosing the right container**, which is where the largest and cheapest wins live. §7.2 is about **not computing things you do not need**, which is what iterators and generators are for. Only then, in §7.3 and §7.4, do we compile: **Cython**, which type-annotates Python into C, and **Numba**, which JIT-compiles numeric functions with a single decorator.

Before any of it: **measure**. `time.perf_counter()` around a block, `timeit` for small snippets, and `cProfile` for a whole script will tell you where the time actually goes, which is almost never where you guessed. Optimising an unprofiled program is a way of spending effort at random.

!!! warning "About running these cells"
    §7.1 and §7.2 run in the browser as usual, and the timings are real — measured on
    your own machine, through WebAssembly, so absolute numbers run slower than native
    Python while the *ratios* remain the lesson. §7.3 and §7.4 need a C compiler and a
    JIT respectively, so their code is shown as plain listings for you to run on your
    own machine.

## 7.1 High-performance Python containers

Every container answers a different question quickly, and the same question slowly. Getting this right is the difference between a script that finishes and one you kill after an hour.

The starkest case is **membership**. `x in some_list` walks the list element by element — O(n). `x in some_set` hashes `x` and looks in one place — O(1), independent of size. On a hundred-thousand-element collection this is not a small constant factor:

???+ example "Example: `in` on a list versus a set"
    ```python
    import time

    n = 100_000
    lst = list(range(n))
    st = set(lst)
    target = n - 1              # the worst case for the list: it must scan all of it

    start = time.perf_counter()
    for _ in range(50):
        target in lst
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(50):
        target in st
    set_time = time.perf_counter() - start

    print(f"list: {list_time:.4f}s")
    print(f"set:  {set_time:.6f}s")
    print(f"the set is roughly {list_time / set_time:,.0f}x faster")
    ```

Be honest about what that measures: `target` is the *last* element, so the list does its maximum work. But that is the case you meet in practice — the misses are the expensive ones, and a filtering loop is full of misses. If your inner loop asks "have I seen this before?", the answer belongs in a `set` or a `dict`.

The second case is **insertion at the front**. A `list` stores its elements contiguously, so `insert(0, x)` has to shift every existing element one place right. `collections.deque` is a doubly-linked structure of blocks, and appending at either end is O(1).

???+ example "Example: `list.insert(0, …)` versus `deque.appendleft`"
    ```python
    import time
    from collections import deque

    n = 20_000

    lst = []
    start = time.perf_counter()
    for i in range(n):
        lst.insert(0, i)          # O(n) each time -> O(n^2) overall
    list_time = time.perf_counter() - start

    dq = deque()
    start = time.perf_counter()
    for i in range(n):
        dq.appendleft(i)          # O(1) each time
    deque_time = time.perf_counter() - start

    print(f"list.insert(0): {list_time:.4f}s")
    print(f"deque.appendleft: {deque_time:.4f}s")
    print(f"ratio: {list_time / deque_time:,.0f}x")
    ```

Then there is **memory**. A Python `list` of integers is a list of *pointers* to full `int` objects, each carrying a type pointer, a reference count, and a variable-length digit array. `array.array` stores raw machine values instead, and NumPy does the same with more capability on top.

???+ example "Example: what a container actually costs"
    ```python
    import sys
    from array import array

    n = 10_000
    py_list = list(range(n))
    c_array = array('q', range(n))       # 'q' = signed 64-bit integer

    list_bytes = sys.getsizeof(py_list) + sum(sys.getsizeof(x) for x in py_list)
    print(f"list  : {sys.getsizeof(py_list):>8,} bytes of pointers")
    print(f"        {list_bytes:>8,} bytes including the int objects")
    print(f"array : {sys.getsizeof(c_array):>8,} bytes, values stored directly")
    print(f"ratio : {list_bytes / sys.getsizeof(c_array):.1f}x")
    ```

The rest of `collections` is worth twenty minutes of your life. `defaultdict` removes the "check whether the key exists" branch from every grouping loop you will ever write; `Counter` does frequency counting in one call; `namedtuple` gives you a tuple whose fields have names, at tuple cost.

???+ example "Example: three from `collections`"
    ```python
    from collections import defaultdict, Counter, namedtuple

    words = "the quick brown fox jumps over the lazy dog the fox".split()

    groups = defaultdict(list)               # no key-existence check needed
    for w in words:
        groups[len(w)].append(w)
    print(dict(groups))

    print(Counter(words).most_common(3))     # frequency counting, one call

    Obs = namedtuple("Obs", "firm year revenue")
    row = Obs("ACME", 2024, 1_250_000)
    print(row.firm, row.year, row.revenue, "| as a tuple:", tuple(row))
    ```

???+ note "Key concept: pick the container from the question"
    | You need to… | Use |
    |---|---|
    | ask "is it in here?" repeatedly | `set` / `dict` — O(1) |
    | add or remove at both ends | `collections.deque` |
    | group items by a key | `collections.defaultdict` |
    | count occurrences | `collections.Counter` |
    | store many numbers of one type | `array.array`, or `numpy.ndarray` |
    | keep an ordered sequence you index | `list` — it is genuinely the right answer often |

## 7.2 Lazy evaluation and iterators

The second free win is not computing things. **Lazy** evaluation produces values only when they are asked for, so a pipeline over ten million rows never holds ten million rows in memory — it holds one.

You already use this. `range(10**9)` is instant and occupies a few dozen bytes, because it computes nothing until iterated. The same choice is available to you everywhere: a list comprehension `[f(x) for x in data]` builds the whole result; a generator expression `(f(x) for x in data)` builds a recipe.

???+ example "Example: a list comprehension versus a generator expression"
    ```python
    import sys, time

    n = 1_000_000

    start = time.perf_counter()
    squares_list = [x * x for x in range(n)]         # builds all n values
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    squares_gen = (x * x for x in range(n))          # builds nothing yet
    gen_time = time.perf_counter() - start

    print(f"list comp : {list_time:.4f}s, {sys.getsizeof(squares_list):>9,} bytes")
    print(f"generator : {gen_time:.6f}s, {sys.getsizeof(squares_gen):>9,} bytes")
    print("sum from the generator:", sum(squares_gen))   # one value at a time
    ```

The generator was effectively free to create because it did nothing. `sum()` then drives it, one value at a time, and the peak memory is a single integer instead of a million. This is the whole reason [§4.2.2](camp_ch4_functions.md#422-the-yield-statement) spent time on suspended frames: a generator *is* a frame that is allowed to pause, and that is what makes streaming possible.

The catch, and it catches everyone once: **a generator is consumed**. Iterate it twice and the second pass is empty.

???+ warning "Pitfall: generators are single-use"
    ```python
    g = (x for x in range(3))
    print(sum(g))   # 3
    print(sum(g))   # 0 -- exhausted, and no error to tell you
    ```

    If you need the values twice, materialise once with `list(g)`. If you need to
    stream *and* re-run, make a function that returns a fresh generator each call.

`itertools` is the standard library's toolbox for composing lazy pipelines without ever materialising an intermediate. Each of these returns an iterator, so they chain at constant memory.

???+ example "Example: composing with `itertools`"
    ```python
    import itertools

    data = range(1, 1_000_000)

    pipeline = itertools.islice(                  # take only what you need
        filter(lambda x: x % 3 == 0,             # ... of the multiples of 3
               map(lambda x: x * x, data)),      # ... of the squares
        5,
    )
    print(list(pipeline))                        # nothing above ran until now

    print(list(itertools.chain([1, 2], (3, 4))))            # concatenate lazily
    print(list(itertools.accumulate([1, 2, 3, 4])))          # running totals
    rows = [("a", 1), ("a", 2), ("b", 3)]
    print({k: [v for _, v in g]                              # groupby needs sorted input
           for k, g in itertools.groupby(rows, key=lambda r: r[0])})
    ```

Read the first pipeline carefully: `map` over a million values, `filter` over the result, and `islice` taking five. Because everything is lazy, roughly fifteen values were ever computed. Written with list comprehensions, the same code allocates two million-element lists to throw away.

??? info "Deep dive: what the bytecode says about `yield`"
    Python compiles to **bytecode** — an intermediate instruction set executed by a
    virtual machine — and `dis` shows it. Compare an ordinary function with a
    generator and the difference is structural, decided at compile time:

    ```python
    import dis

    def simple_gen():
        yield 1
        yield 2

    dis.dis(simple_gen)
    ```

    You will see `RETURN_GENERATOR` and `YIELD_VALUE` where a normal function would
    just compute and return. This is why a `yield` buried inside a branch that never
    executes still turns the whole function into a generator: the compiler decided
    before your code ever ran.

## 7.3 Cython

When the algorithm and the data structures are right and it is still too slow, the remaining cost is the interpreter itself: every `a + b` on Python objects is a type lookup, a method dispatch, an allocation for the result, and reference-count bookkeeping. **Cython** removes that by compiling your Python to C, and it goes fastest when you tell it the types so it can use machine integers instead of Python objects.

Start with the pure-Python version. Note the `timer` decorator — an entirely ordinary decorator of the kind we built in [§4.4](camp_ch4_functions.md#44-decorators), here doing real work:

???+ example "Example: the pure-Python baseline"
    ```python
    import time

    def timer(func):
        def wrapper(*args, **kwargs):
            stime = time.perf_counter()
            res = func(*args, **kwargs)
            etime = time.perf_counter()
            print(f"time elapsed: {etime - stime:.6f}s")
            return res
        return wrapper

    @timer
    def p_fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    print(p_fibonacci(70))
    ```

Now the Cython version. It is the *same algorithm* — the only additions are type declarations. `cpdef` creates a function callable from both C and Python; `cdef unsigned long long int` makes `a`, `b`, and the loop counter machine integers rather than Python objects.

```cython
# c_fibonacci.pyx
import time

def timer(func):
    def wrapper(*args, **kwargs):
        stime = time.perf_counter()
        res = func(*args, **kwargs)
        etime = time.perf_counter()
        print(f"time elapsed: {etime - stime}")
        return res
    return wrapper

cpdef unsigned long long int fibonacci(int n):
    cdef unsigned long long int a = 0, b = 1, i
    for i in range(n):
        a, b = b, a + b
    return a

fibonacci = timer(fibonacci)
```

Cython source is compiled ahead of time, which means a build step. `setup.py` describes it:

```python
# setup.py
from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension

extensions = [
    Extension(
        "c_fibonacci",                 # name of the resulting extension module
        sources=["c_fibonacci.pyx"],   # the Cython source
    )
]

setup(
    name="fibonacci",
    ext_modules=cythonize(extensions),
)
```

Build it in place, then import the result like any other module:

```powershell
pip install cython setuptools
python setup.py build_ext --inplace
```

```python
import c_fibonacci
print(c_fibonacci.fibonacci(70))
```

The build produces a `.c` file (worth opening once — it is a few thousand lines of C implementing what your twelve lines said) and a platform-specific binary such as `c_fibonacci.cp312-win_amd64.pyd`. The name encodes the Python version and architecture, which is the first practical cost of this approach: the artefact is tied to the interpreter that built it, so a co-author on a different platform must rebuild rather than copy.

Measure both with `%timeit` in IPython — `%timeit p_fibonacci(50)` against `%timeit c_fibonacci.fibonacci(50)` — and expect the typed version to land one to two orders of magnitude ahead on a tight numeric loop like this one. Run it yourself rather than trusting a number from these notes: the ratio depends on your compiler, your flags, and how much of the loop stayed in C.

???+ warning "Pitfall: `cdef` types are C types, with C behaviour"
    Python integers grow without limit; `unsigned long long int` does not. This
    `fibonacci` is exact up to n = 93 and silently wrong after it, where the pure-Python
    version stays exact forever. That trade — speed for machine-width arithmetic — is
    the actual decision you are making when you add `cdef`, and it deserves a comment
    in the code and a bounds check at the entry point.

Cython earns its keep when the hot spot is a loop over scalars that you cannot vectorise, and when you are willing to own a build step. If you can express the work as array operations, NumPy is already calling compiled code and will get you most of the way with none of this.

## 7.4 Numba

**Numba** takes the other route: instead of compiling ahead of time, it compiles **just in time**, the first time the function is called, using the actual argument types it sees. There is no build step and no separate source file — you add a decorator.

```python
from numba import njit
import numpy as np

@njit                       # compiled on the first call, cached after
def moving_average(x, window):
    n = x.shape[0]
    out = np.empty(n - window + 1)
    for i in range(n - window + 1):
        total = 0.0
        for j in range(window):
            total += x[i + j]
        out[i] = total / window
    return out

data = np.random.rand(1_000_000)
moving_average(data, 50)    # first call: compiles, so it is slow
moving_average(data, 50)    # subsequent calls: full speed
```

Two things to keep in mind. **Time the second call**, not the first — the first includes compilation, and timing it is the most common way people conclude Numba did nothing. And `@njit` means *nopython mode*: Numba compiles the whole function or raises. That restriction is the point, because the alternative — falling back to interpreted execution and quietly giving you no speedup — is worse. It also means Numba works on numbers, NumPy arrays, and loops, and does **not** work on `pandas` objects, dictionaries of mixed types, or arbitrary Python classes. Pull the numeric kernel out into its own function, `@njit` that, and leave the DataFrame handling outside.

Numba is usually the right first attempt: one decorator, no build system, and if it refuses the function it tells you why. Reach for Cython when you need to link against existing C, ship a compiled artefact, or you have hit something Numba will not accept.

???+ note "Key concept: the escalation ladder"
    1. **Profile** — `cProfile`, or `time.perf_counter()` around the suspect block.
    2. **Fix the data structure** — the `set`/`dict`/`deque` wins from §7.1, usually the biggest.
    3. **Stop materialising** — generators and `itertools` from §7.2.
    4. **Vectorise** — push the loop into NumPy or pandas, which are already compiled.
    5. **JIT the kernel** — `@njit` on the numeric inner function.
    6. **Compile it** — Cython, when you need the control or the artefact.

    Each rung costs more effort and more complexity than the one above. Most problems
    are solved by rung 2 or 3, and going straight to rung 6 is how a one-day speedup
    becomes a one-week rewrite of code nobody can maintain.

## Summary

| | |
|---|---|
| **Measure first** | `cProfile` and `perf_counter`. The bottleneck is almost never where you guessed. |
| **`in` on a list is O(n)** | Use a `set` or `dict` for membership; it is the single largest common win. |
| **`deque` for both ends** | `list.insert(0, x)` shifts everything; `appendleft` does not. |
| **Lazy beats materialised** | Generators and `itertools` compute one value at a time — but a generator is single-use. |
| **Cython = types + a build step** | `cdef` gives C speed and C overflow. The artefact is tied to one interpreter and platform. |
| **Numba = one decorator** | JIT, no build step; numbers and NumPy only, and you must time the *second* call. |
