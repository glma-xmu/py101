# NumPy

```motto
Think in whole arrays, not one number at a time.
```

## Introduction

Chapters 1 and 2 gave you Python the language. Now we turn to what most people actually *use* Python for: working with data. Two libraries dominate that world — **NumPy** and **pandas** — and pandas is built directly on top of NumPy, so we start here.

NumPy gives you one new thing: the **array** (`ndarray`), a fixed-size sequence of numbers *of the same type*. That sounds like a list, but it behaves completely differently. You operate on a NumPy array **all at once** — square every element, add two arrays, multiply a matrix — with no loop in sight. This style is called **vectorization**, and because NumPy runs in C under the hood, it is dramatically faster than doing the same work with Python lists. Learning to *think in arrays* is the single biggest shift in this chapter.

We will use only a slice of NumPy — enough to be comfortable before pandas. As always, the code is **runnable**; the first Run downloads NumPy into your browser (a few MB, once), then it is cached.

## 1. The `ndarray`

You create an array from a list with `np.array`. Two rules make an array different from a list: it has a **fixed size**, and all elements share **one type** (its **`dtype`**). If you mix types, NumPy quietly promotes them all to one type that fits.

???+ example "Example: creating arrays and dtype"
    ```python
    import numpy as np

    a = np.array([1, 2, 3])
    print(a, "|", a.dtype)          # [1 2 3] | int64

    b = np.array([1, 2, "a"])       # mixing types -> everything becomes a string
    print(b, "|", b.dtype)          # ['1' '2' 'a'] | <U...

    c = np.array([1, 2, 3], dtype=float)   # ask for a specific type
    print(c, "|", c.dtype)          # [1. 2. 3.] | float64
    ```

???+ note "Key concept: ndarray"
    A NumPy **array** (`ndarray`) is a fixed-size grid of elements of a single
    **`dtype`** (`int64`, `float64`, …). One type + fixed size is exactly what lets
    NumPy store the data compactly and operate on it at C speed.

You rarely type arrays out by hand. NumPy builds them for you: **`np.arange`** (like `range`, but an array), **`np.linspace`** (evenly spaced points between two ends), and the **`np.random`** family for random data.

???+ example "Example: building arrays"
    ```python
    import numpy as np

    print(np.arange(0, 10, 2))       # [0 2 4 6 8]  — start, stop (exclusive), step
    print(np.linspace(0, 1, 5))      # [0.  0.25 0.5  0.75 1. ]  — 5 points, ends included

    np.random.seed(0)                # makes the "random" numbers reproducible
    print(np.random.randint(1, 10, size=5))     # 5 ints in [1, 10)
    print(np.random.normal(5, 3, size=4))       # 4 draws, mean 5, std 3
    ```

???+ question "In-class exercise: creating arrays"
    1. Create the array `[10, 20, 30, 40, 50]` two ways: from a list, and with `np.arange`.
    2. Make 11 evenly spaced points from 0 to 100 with `np.linspace`.
    3. Create a **3×3** array whose entries are drawn from a normal distribution with mean 5 and standard deviation 3. (Hint: `np.random.normal` takes a `size=`.)

## 2. Vectorization: operate on the whole array

Here is the shift. With a **list**, arithmetic does not do what a mathematician expects — `[1, 2, 3] + 4` is an error, and `[1, 2, 3] * 2` *repeats* the list. With a NumPy **array**, every operation applies **element by element**, and a scalar is applied to every element.

???+ example "Example: arithmetic on arrays"
    ```python
    import numpy as np
    a = np.array([1, 2, 3])

    print(a + 4)        # [5 6 7]   — 4 added to each element
    print(a * 2)        # [2 4 6]   — each element doubled (not repeated!)
    print(a * a)        # [1 4 9]   — element-wise multiply
    print(a ** 2)       # [1 4 9]
    ```

```recall
Recall from 1.2 that `list * 2` *duplicates* a list and `list + number` fails. NumPy arrays behave like math vectors instead — one reason we switch to arrays for data work.
```

This whole-array style is **vectorization**, and it is not just convenient — it is *fast*. NumPy pushes the loop down into compiled C code, so squaring a million numbers takes a blink compared to a Python loop.

???+ example "Example: how much faster?"
    ```python
    import numpy as np, time
    size = 1_000_000
    py_list = list(range(size))
    np_array = np.arange(size)

    t = time.perf_counter()
    _ = [x * x for x in py_list]        # the Python way
    print(f"list:  {time.perf_counter() - t:.4f} s")

    t = time.perf_counter()
    _ = np_array ** 2                   # the NumPy way
    print(f"numpy: {time.perf_counter() - t:.4f} s")
    ```

    The exact times depend on your machine, but NumPy is typically **tens of times
    faster** here — and the gap widens as the data grows.

???+ note "Key concept: vectorization"
    **Vectorization** means expressing a computation as operations on whole arrays
    rather than element-by-element loops. It is shorter to write *and* far faster,
    because NumPy runs the loop in C. The slogan is: *if you are writing a `for`
    loop over a NumPy array, there is usually a better way.*

## 3. Broadcasting

What happens when the two arrays are *different* shapes? NumPy tries to **broadcast** the smaller one across the larger — stretching it, without copying, so the shapes line up. The everyday case is adding a row vector to every row of a matrix.

???+ example "Example: broadcasting a vector across a matrix"
    ```python
    import numpy as np
    m = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    v = np.array([1, 1, 1])

    print(m + v)        # v is added to every row
    # [[ 2  3  4]
    #  [ 5  6  7]
    #  [ 8  9 10]]
    ```

The rule: NumPy compares shapes from the right; two dimensions are compatible when they are equal or one of them is 1. When they simply do not line up, you get a clear error rather than a silent wrong answer.

???+ warning "Pitfall: shapes must be compatible"
    ```python
    import numpy as np
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])   # 3×3
    v = np.array([1, 1])                              # length 2

    # m + v   ->  ValueError: operands could not be broadcast together
    ```

    A length-3 vector broadcasts across a 3-column matrix; a length-2 one does not.
    When broadcasting fails, check the shapes with `.shape`.

???+ note "Key concept: broadcasting"
    **Broadcasting** lets NumPy combine arrays of different but compatible shapes by
    stretching the smaller across the larger. A scalar (`a + 4`) is just the simplest
    case — it broadcasts to every element.

## 4. Shape: reshape and transpose

An array carries its dimensions in **`.shape`**. You can rearrange the same data into a new shape with **`.reshape`**, and flip rows and columns with **`.T`** (transpose).

???+ example "Example: reshape and transpose"
    ```python
    import numpy as np
    m = np.arange(12).reshape(3, 4)     # a 3×4 grid of 0..11
    print(m.shape)                      # (3, 4)

    print(m.T.shape)                    # (4, 3) — transposed
    print(m.reshape(2, 6).shape)        # (2, 6) — same 12 numbers, new shape
    print(m.reshape(-1).shape)          # (12,)  — -1 means "figure out this axis"
    ```

Reshaping never changes the numbers or their order in memory; it only changes how you *index* them. The total number of elements must stay the same (you cannot reshape 12 values into a 3×3 grid).

## 5. Universal functions and aggregations

NumPy comes with fast, element-wise math functions (**ufuncs**) like `np.sqrt`, `np.exp`, and `np.log`, plus **aggregations** that summarise an array: `sum`, `mean`, `min`, `max`, `std`. The important twist for 2-D data is the **`axis`** argument, which chooses the *direction* you collapse.

???+ example "Example: ufuncs, masks, and axis"
    ```python
    import numpy as np
    arr = np.array([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]])

    print(np.sqrt(arr[0]))        # [1. 1.414 1.732] — element-wise
    print(arr.sum())             # 45  — everything

    print(arr[arr > 3])          # [4 5 6 7 8 9] — a boolean MASK selects elements
    print(arr.min(axis=1))       # [1 4 7] — min of each ROW
    print(arr.mean(axis=0))      # [4. 5. 6.] — mean of each COLUMN
    ```

The `axis` numbers trip everyone up at first, so hold onto this: **`axis=0` runs down the rows and gives you one result per column; `axis=1` runs across the columns and gives you one result per row.**

???+ note "Key concept: axis"
    An **aggregation** collapses an array to a summary. On a 2-D array, `axis=0`
    collapses *down* (one number per column) and `axis=1` collapses *across* (one
    number per row). A **boolean mask** like `arr > 3` selects the elements where the
    condition is `True`.

??? info "Deep dive: loops vs. ufuncs, timed"
    Using a `for` loop over an array gives the *right* answer but throws away NumPy's
    speed. You can measure it with the timing decorator idea from 2.4:

    ```python
    import numpy as np, time

    def timed(func):
        def wrapper(x):
            t = time.perf_counter()
            out = func(x)
            print(f"{func.__name__}: {time.perf_counter() - t:.4f} s")
            return out
        return wrapper

    @timed
    def loop_reciprocal(x):
        out = np.empty(len(x))
        for i in range(len(x)):
            out[i] = 1.0 / x[i]
        return out

    @timed
    def ufunc_reciprocal(x):
        return 1.0 / x            # vectorized

    data = np.random.randint(1, 10, size=100_000)
    loop_reciprocal(data)
    ufunc_reciprocal(data)        # far faster, same result
    ```

## 6. View vs. copy

One behavior to know before pandas, because it causes real bugs. **Slicing a NumPy array gives you a *view* — a window onto the *same* data, not a fresh copy.** Change the view and you change the original; change the original and the view updates too.

???+ example "Example: a slice is a view"
    ```python
    import numpy as np
    x = np.arange(10)
    y = x[1:3]              # y is a VIEW into x
    print(y)               # [1 2]

    x[1:3] = [10, 11]      # change x...
    print(y)               # [10 11] — ...and y changed too!
    print(y.base is x)     # True — y is backed by x's data
    ```

When you want an independent piece of data that you can modify safely, ask for a **`.copy()`**.

???+ warning "Pitfall: change a view, change the original"
    ```python
    import numpy as np
    x = np.arange(10)

    view = x[1:3]          # shares x's data
    copy = x[1:3].copy()   # independent

    x[1:3] = [10, 11]
    print(view)            # [10 11]  — affected
    print(copy)            # [1 2]    — untouched
    ```

    This is the array-data version of the *aliasing* we saw with lists in 1.2: a
    slice can be a second window onto the same underlying values. If a later change
    surprises you, ask whether you were holding a view. Use `.copy()` when you need
    a piece you can edit without touching the original.

## Summary

NumPy's one big idea is the **array**: fixed size, single `dtype`, operated on **all at once**.

| Idea | What it gives you |
|------|-------------------|
| **`ndarray`** | a compact, same-type grid of numbers (`np.array`, `arange`, `linspace`, `random`) |
| **Vectorization** | element-wise math with no loops — short *and* C-fast |
| **Broadcasting** | combine compatible shapes (scalar + array, vector + matrix) |
| **`reshape` / `.T`** | rearrange the same data into a new shape |
| **ufuncs / `axis`** | fast element-wise functions and per-row/column aggregations |
| **view vs. copy** | a slice shares data; use `.copy()` for an independent piece |

You now have enough NumPy to be dangerous. Next, **3.2 pandas — Series and DataFrames** puts a *label* on every row and column of a 2-D array, turning these raw grids into the labelled data tables you will actually analyse.
