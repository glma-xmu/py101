# Exercises — Chapter 2: Functions

A set of practice problems, grouped by the section they exercise. Try them on your own; where a problem shows code, treat it as the given data or a starting point. Each problem shows a **sample output** so you know what to aim for. Solutions are not provided here.

## 1. Defining and Calling Functions

???+ question "Exercise 1.1 — your first function"
    Write a function `double(x)` that returns `x * 2`, then call it on `21` and on `3.5`.

    **Sample output**
    ```text
    42
    7.0
    ```

???+ question "Exercise 1.2 — a function with no parameters"
    Write `greet()` that takes no arguments and returns `"Hello, class!"`. Call it. Then print `greet` *without* parentheses and explain the difference.

    **Sample output**
    ```text
    Hello, class!
    <function greet at 0x...>
    ```

???+ question "Exercise 1.3 — return vs print"
    Write two functions: `add_return(a, b)` that **returns** `a + b`, and `add_print(a, b)` that **prints** it. Store each call's result in a variable and print that variable. Why is one of them `None`?

    **Sample output**
    ```text
    7
    7
    None
    ```

???+ question "Exercise 1.4 — several return values"
    Write `min_max(numbers)` that returns both the smallest and largest value as a tuple, and unpack the result into `low, high`. Test it on `[4, 9, 1, 7]`.

    **Sample output**
    ```text
    1 9
    ```

???+ question "Exercise 1.5 — default parameter"
    Write `power(base, exponent=2)` so that `power(5)` squares and `power(5, 3)` cubes.

    **Sample output**
    ```text
    25
    125
    ```

???+ question "Exercise 1.6 — the shared mutable default"
    Predict the output, then run it. Explain *where* the default list lives that makes the second and third calls grow.

    ```python
    def append_to(element, to=[]):
        to.append(element)
        return to

    print(append_to(1))
    print(append_to(2))
    print(append_to(3))
    ```

    **Sample output**
    ```text
    [1]
    [1, 2]
    [1, 2, 3]
    ```

???+ question "Exercise 1.7 — fix the trap"
    Rewrite `append_to` using the `None`-sentinel pattern so each call without a list starts fresh. Confirm `append_to(1)` and `append_to(2)` each return a one-element list.

    **Sample output**
    ```text
    [1]
    [2]
    ```

???+ question "Exercise 1.8 — locals are private"
    Run the code below. Why does the last line raise `NameError`?

    ```python
    def square(n):
        result = n * n
        return result

    print(square(4))
    print(result)
    ```

    **Sample output**
    ```text
    16
    NameError: name 'result' is not defined
    ```

## 2. Namespaces and Scope

???+ question "Exercise 2.1 — LEGB by prediction"
    Predict all three lines of output, then run it.

    ```python
    x = "global"

    def outer():
        x = "enclosing"
        def inner():
            x = "local"
            print(x)
        inner()
        print(x)

    outer()
    print(x)
    ```

    **Sample output**
    ```text
    local
    enclosing
    global
    ```

???+ question "Exercise 2.2 — reading a global"
    Write a function `show()` that prints the value of a module-level variable `counter` (set to `0`) *without* taking it as an argument. Explain which scope the name is found in.

    **Sample output**
    ```text
    0
    ```

???+ question "Exercise 2.3 — shadowing a built-in"
    Predict each line. Then add a line that restores access to the built-in `max`.

    ```python
    print(max(1, 2))
    max = min
    print(max(1, 2))
    ```

    **Sample output**
    ```text
    2
    1
    ```

???+ question "Exercise 2.4 — UnboundLocalError"
    Explain why this raises an error, and fix it two ways: once with `global`, once by passing `counter` in and returning the new value.

    ```python
    counter = 0
    def bump():
        counter = counter + 1
        return counter
    bump()
    ```

    **Sample output**
    ```text
    UnboundLocalError: ...local variable 'counter'...
    ```

???+ question "Exercise 2.5 — the global keyword"
    Using `global`, write `add(n)` so that repeated calls accumulate into a module-level `total`. Call `add(3)` then `add(4)` and print `total`.

    **Sample output**
    ```text
    7
    ```

???+ question "Exercise 2.6 — nonlocal"
    Write `outer()` that defines `message = "before"`, then a nested `inner()` that uses `nonlocal` to set it to `"after"`. Call `inner()`, then print `message` from `outer`.

    **Sample output**
    ```text
    after
    ```

???+ question "Exercise 2.7 — why a swap function fails"
    Run the code. Why are `a` and `b` unchanged afterwards? Discuss it in terms of local names.

    ```python
    def swap(x, y):
        x, y = y, x

    a, b = 1, 2
    swap(a, b)
    print(a, b)
    ```

    **Sample output**
    ```text
    1 2
    ```

???+ question "Exercise 2.8 — inspect the namespaces"
    Write a function with one local variable that prints `list(locals())` and whether the name `"print"` is in `dir(__builtins__)`. Confirm the local appears and `print` is a built-in.

    **Sample output**
    ```text
    ['note']
    True
    ```

## 3. First-Class and Higher-Order Functions

???+ question "Exercise 3.1 — functions in a dict"
    Build a dictionary `ops` mapping `"sq"` to a squaring function and `"neg"` to a negating function, then call each through the dictionary on the value `4`.

    **Sample output**
    ```text
    16
    -4
    ```

???+ question "Exercise 3.2 — a higher-order function"
    Write `apply_twice(func, x)` that returns `func(func(x))`. Test it with a function that adds 3, starting from 10.

    **Sample output**
    ```text
    16
    ```

???+ question "Exercise 3.3 — sort with a key"
    Given `words = ["python", "is", "great"]`, sort them by length using `sorted` with a `key`.

    **Sample output**
    ```text
    ['is', 'great', 'python']
    ```

???+ question "Exercise 3.4 — positional vs keyword"
    Define `rect(width, height)` returning the area. Call it once positionally and once with both keywords in reverse order; confirm the same result. Then explain why `rect(height=3, 4)` is an error.

    **Sample output**
    ```text
    12
    12
    ```

???+ question "Exercise 3.5 — `*args`"
    Write `my_sum(*args)` that adds however many numbers it is given. Test it with two numbers and with five.

    **Sample output**
    ```text
    3
    15
    ```

???+ question "Exercise 3.6 — `**kwargs`"
    Write `scoreboard(**players)` taking calls like `scoreboard(Alice=9, Bob=7)` and printing `"Alice: 9"` for each entry. (Recall `kwargs` is a dict.)

    **Sample output**
    ```text
    Alice: 9
    Bob: 7
    ```

???+ question "Exercise 3.7 — unpacking puzzles"
    Predict the value bound to each name.

    ```python
    a, *b, c = 1, 2, 3, 4, 5
    print(a, b, c)

    *d, e = [10, 20, 30]
    print(d, e)
    ```

    **Sample output**
    ```text
    1 [2, 3, 4] 5
    [10, 20] 30
    ```

???+ question "Exercise 3.8 — spreading into a call"
    Given `pair = (3, 4)` and `power(base, exp)` returning `base ** exp`, call `power` by *spreading* `pair` with `*`.

    **Sample output**
    ```text
    81
    ```

???+ question "Exercise 3.9 — a closure that builds functions"
    Write `make_adder(n)` that returns a function adding `n` to its argument. Build `add10` and `add100` and call each on `5`.

    **Sample output**
    ```text
    15
    105
    ```

???+ question "Exercise 3.10 — a counter closure"
    Write `make_counter()` that returns a function which returns 1, 2, 3, … on successive calls (use `nonlocal`). Show that two counters are independent.

    **Sample output**
    ```text
    1 2 3
    1
    ```

???+ question "Exercise 3.11 — closures with private state"
    Write `make_account(balance)` that returns a dict of two functions, `deposit(amount)` and `withdraw(amount)`, sharing a private `balance` (no direct access to it from outside). After depositing 50 and withdrawing 30 from a starting balance of 100, a `balance()` reporter should show 120.

    **Sample output**
    ```text
    120
    ```

???+ question "Exercise 3.12 — lambda"
    Given `people = [("Ada", 36), ("Bob", 41), ("Cleo", 29)]`, use a `lambda` key to find the oldest with `max`, and to sort by name.

    **Sample output**
    ```text
    ('Bob', 41)
    [('Ada', 36), ('Bob', 41), ('Cleo', 29)]
    ```

## 4. Use Cases

### Decorators

???+ question "Exercise 4.1 — a logging decorator"
    Write a decorator `announce` so that decorating `add(a, b)` and calling `add(2, 3)` prints a line before and after, then returns the result.

    **Sample output**
    ```text
    add is being called.
    finished calling add.
    5
    ```

???+ question "Exercise 4.2 — a timing decorator"
    Write a decorator `timed` that prints how long the wrapped function took (use `time.perf_counter()` before and after). Apply it to a function that sums `range(1_000_000)`.

    **Sample output**
    ```text
    sum_range took 0.02s
    499999500000
    ```

???+ question "Exercise 4.3 — memoization"
    Write a decorator `memoize` that caches results in a dict so repeated calls with the same arguments are instant. Apply it to a slow recursive `fib` and confirm the answers match.

    **Sample output**
    ```text
    55
    ```

???+ question "Exercise 4.4 — assert as a guard"
    Write `mean(values)` that uses `assert` to reject an empty list and a list containing `None`, otherwise returns the average.

    **Sample output**
    ```text
    4.0
    AssertionError: mean() needs at least one value
    ```

### Recursion

???+ question "Exercise 4.5 — factorial"
    Write a recursive `factorial(n)` (base case `n == 0` returns `1`). Test it on `5`.

    **Sample output**
    ```text
    120
    ```

???+ question "Exercise 4.6 — recursive sum"
    Write `total(xs)` that returns the sum of a list using recursion, not a loop (base case: the empty list returns `0`).

    **Sample output**
    ```text
    10
    ```

???+ question "Exercise 4.7 — Fibonacci"
    Write a recursive `fib(n)` with `fib(0) = 0`, `fib(1) = 1`, and print the first ten Fibonacci numbers.

    **Sample output**
    ```text
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    ```

???+ question "Exercise 4.8 — recursive power"
    Write `power(base, exp)` recursively (base case `exp == 0` returns `1`). Test `power(2, 10)`.

    **Sample output**
    ```text
    1024
    ```

???+ question "Exercise 4.9 — countdown"
    Write a recursive `count_down(n)` that prints `n, n-1, …, 1` and then `"liftoff!"`.

    **Sample output**
    ```text
    3
    2
    1
    liftoff!
    ```

### map, filter, reduce

???+ question "Exercise 4.10 — map"
    Use `map` to convert `["1", "2", "3"]` into the list `[1, 2, 3]`. (Hint: pass `int`.)

    **Sample output**
    ```text
    [1, 2, 3]
    ```

???+ question "Exercise 4.11 — filter"
    Use `filter` to keep only the words longer than three letters from `["hi", "there", "ok", "world"]`.

    **Sample output**
    ```text
    ['there', 'world']
    ```

???+ question "Exercise 4.12 — reduce"
    Use `reduce` (from `functools`) to compute the product of `[1, 2, 3, 4, 5]`.

    **Sample output**
    ```text
    120
    ```

### Generators

???+ question "Exercise 4.13 — an evens generator"
    Write a generator `evens(limit)` that yields 0, 2, 4, … up to but not including `limit`, and print `list(evens(10))`.

    **Sample output**
    ```text
    [0, 2, 4, 6, 8]
    ```

???+ question "Exercise 4.14 — perfect squares"
    Write a generator that yields the perfect squares 1, 4, 9, 16, … forever, and use it to print the first five.

    **Sample output**
    ```text
    1 4 9 16 25
    ```

???+ question "Exercise 4.15 — generator expression"
    Using a generator expression, build a generator of the cubes of 0–4, print its `type`, then print `list(...)` of it.

    **Sample output**
    ```text
    <class 'generator'>
    [0, 1, 8, 27, 64]
    ```

???+ question "Exercise 4.16 — single use"
    A generator is one-shot. Predict the second `list(...)` below and explain.

    ```python
    g = (x for x in range(3))
    print(list(g))
    print(list(g))
    ```

    **Sample output**
    ```text
    [0, 1, 2]
    []
    ```

### Error handling

???+ question "Exercise 4.17 — safe divide"
    Write `safe_divide(a, b)` that returns `a / b`, or prints a message and returns `None` on division by zero.

    **Sample output**
    ```text
    5.0
    can't divide by zero
    None
    ```

???+ question "Exercise 4.18 — safe index"
    Write `safe_index(seq, i)` that returns `seq[i]`, or `None` if the index is out of range (catch `IndexError`).

    **Sample output**
    ```text
    20
    None
    ```

???+ question "Exercise 4.19 — try / except / else / finally"
    Write `read_int(text)` that returns `int(text)` on success and `None` on a `ValueError`, printing `"ok"` in `else` and `"done"` in `finally`. Call it on `"42"` and on `"oops"`.

    **Sample output**
    ```text
    ok
    done
    42
    done
    None
    ```

## 5. Loose Ends and Style

???+ question "Exercise 5.1 — document a function"
    Add a one-line docstring and type hints to a function `add(a, b)`. Then print its `__doc__`.

    **Sample output**
    ```text
    Return the sum of a and b.
    ```

???+ question "Exercise 5.2 — keyword-only parameter"
    Define `make_user(name, *, admin=False)`. Show that `make_user("Ada", True)` raises a `TypeError` while `make_user("Ada", admin=True)` works. Explain why.

    **Sample output**
    ```text
    TypeError: make_user() takes 1 positional argument but 2 were given
    ```

???+ question "Exercise 5.3 — clean it up (PEP 8)"
    Rewrite this to follow PEP 8 (naming, spacing, layout), keeping the behavior identical.

    ```python
    def Mul (A,B):return A*B
    ```

    **Sample output**
    ```text
    6
    ```

???+ question "Exercise 5.4 — partial application (optional)"
    Using `functools.partial`, build `square` from a two-argument `power(base, exp)` by fixing `exp=2`, and call `square(7)`.

    **Sample output**
    ```text
    49
    ```
