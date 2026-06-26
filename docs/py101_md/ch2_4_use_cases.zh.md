# 函数实战：五个用例

## 引言

在 2.3 我们学到，函数是一个值：它可以被传递、被返回、被即兴造出来。本页就来花掉这笔本钱。我们走一遍每个 Python 程序员都会用到的五个经典模式——**装饰器**、**递归**、**`map`/`filter`/`reduce`**、**生成器**和**错误处理**。前三个彻头彻尾是高阶函数；后两个则补全了日常工具箱，让你写出在该惰性时惰性、出岔子时也稳健的函数。每一个都直接建立在第 1–2 章之上，所以请留意那些回扣。

和往常一样，每个代码块都可运行。

## 1. 装饰器

设想你写了十几个函数，现在想让它们每一个在开始和结束时都通报一声——为了记日志、计时或调试。你大可以把同样的两句 `print` 粘进所有十二个函数体里，但这恰恰是函数本想消灭的那种重复。而且如果这些函数是*别人*写的，你可能根本没法去改它们。

出路是一个**装饰器（decorator）**：一个高阶函数，它接收一个函数，给它裹上一些额外行为，再把裹好的版本返回。它就是 2.3 §3.2 那个透传包装器，被赋予了一个名字和一个用途。

???+ example "示例：一个记日志的装饰器"
    ```python
    def announce(func):
        def wrapper(*args, **kwargs):
            print(f"{func.__name__} is being called.")
            result = func(*args, **kwargs)        # 干真正的活
            print(f"finished calling {func.__name__}.")
            return result
        return wrapper

    @announce
    def add(a, b):
        return a + b

    print(add(2, 3))
    ```

这里干所有活的是 2.3 的两个想法。`wrapper` 是一个**闭包**——它从外层作用域记住了 `func`——而且它转发 `*args, **kwargs`，于是它对*任何*函数都管用，不管那函数的实参是什么。`@announce` 那一行纯粹是便利写法：它的意思正是 `add = announce(add)`，把名字 `add` 重新绑定到裹好的版本上。

???+ note "核心概念：装饰器"
    **装饰器**是一个高阶函数，它接收一个函数、返回一个包住它的新函数。在一个 `def`
    上方写 `@decorator`，是 `name = decorator(name)` 的简写。包装器用一个闭包（来记住
    原函数）和 `*args`/`**kwargs`（来原样透传实参）。

装饰的一个近亲是 **`assert`** 语句，包装器常用它来守卫一个函数的输入。`assert 条件, "消息"` 在条件为真时什么都不做，为假时则带着你的消息抛出 `AssertionError`——这是一种声明假设、并在它被违反时大声失败的快捷方式。

???+ example "示例：assert 作为守卫"
    ```python
    def mean(values):
        assert len(values) > 0, "mean() needs at least one value"
        assert None not in values, "values must not contain None"
        return sum(values) / len(values)

    print(mean([2, 4, 6]))     # 4.0
    # print(mean([]))          # AssertionError: mean() needs at least one value
    ```

???+ warning "易错点：包装器必须转发并返回"
    如果你的 `wrapper` 忘了把 `*args, **kwargs` 传给 `func`，或忘了 `return func(...)`
    的结果，被装饰的函数就会悄悄丢掉它的实参或它的返回值。一个不返回的包装器，会变成
    一个返回 `None` 的函数——也就是 2.1 那个陷阱，只是上升了一层。

??? info "深入了解：记忆化与 `functools.wraps`"
    装饰器能做的不只是记日志——它还能*记住*。一个**记忆化（memoizing）**装饰器把结果
    缓存起来，于是用相同实参的重复调用瞬间完成：

    ```python
    def memoize(func):
        cache = {}                       # 闭包状态
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        return wrapper
    ```

    一个小瑕疵：包装替换了原函数，于是 `add.__name__` 变成了 `"wrapper"`。用
    `@functools.wraps(func)` 装饰 `wrapper`，会把原函数的名字和文档字符串拷过来，让
    内省保持诚实。

???+ question "课堂练习：装饰器"
    1. 写一个装饰器 `timed`，打印被包装函数花了多长时间（在前后各用一次 `time.perf_counter()`）。
    2. 把 `announce` 用到一个带关键字实参的函数上，确认它们仍然正确地抵达。
    3. 用一句话解释为什么 `wrapper` 需要 `*args, **kwargs`，而不是固定的形参。

## 2. 递归

一个**递归（recursive）**函数就是会调用自己的函数。对任何“由它自己的一个更小副本来定义”的问题，它都是天然的形状——而且它直接倚靠 2.1 的**调用栈**，因为每一次调用都拿到它自己的帧。

每个递归都需要两部分：一个让下探停下的**基准情形（base case）**，和一个朝它迈出一步的**递归情形（recursive case）**。

???+ example "示例：阶乘"
    ```python
    def factorial(n):
        if n == 0:                 # 基准情形：到此停下
            return 1
        return n * factorial(n - 1)   # 递归情形：一个更小的问题

    print(factorial(4))            # 24
    ```

为什么这不用循环也能行？因为每一次对 `factorial` 的调用都在调用栈上拿到它*自己*的帧，各有各的 `n`。下面的图把 `factorial(3)` 定格在它最深的那一点，正好是 `factorial(0)` 即将返回之时。四个帧叠在一起，都在乘法中途暂停，各自等着它上面的那一个。

```memory
memory: 堆
stack: 调用栈
objects:
  fn: 一个函数
  i3: 3
  i2: 2
  i1: 1
  i0: 0
globals: 全局命名空间
  factorial -> fn
frame: factorial(3)
  n -> i3
frame: factorial(2)
  n -> i2
frame: factorial(1)
  n -> i1
frame: factorial(0)
  n -> i0
```

当每一次调用触到它的基准情形或运行完毕时，它的帧返回一个值并被丢弃，它下面那个帧随即恢复——`factorial(0)` 返回 `1`，然后 `factorial(1)` 返回 `1*1`，再然后 `factorial(2)` 返回 `2*1`，如此沿着栈一路回落。

```recall
调用栈的现身：递归不是魔法——它只是*同一个*函数的许多个帧，各有各的局部，像 2.1 里那样叠起来。是基准情形让这摞栈不会无止境地长下去。
```

同样的形状能解许多问题。比如，对一个列表求和，就是“第一个元素加上其余部分之和”。

???+ example "示例：递归求和与斐波那契"
    ```python
    def total(xs):
        if len(xs) == 0:           # 基准情形
            return 0
        return xs[0] + total(xs[1:])

    def fib(n):
        if n < 2:                  # 基准情形：fib(0)=0, fib(1)=1
            return n
        return fib(n - 1) + fib(n - 2)

    print(total([1, 2, 3, 4]))     # 10
    print([fib(i) for i in range(8)])   # [0, 1, 1, 2, 3, 5, 8, 13]
    ```

???+ warning "易错点：忘了基准情形"
    一个没有可达基准情形的递归，会永不停歇地调用自己。不过 Python 不会真的死循环——
    每次调用都耗掉一个帧，当栈太深时（默认大约一千个帧），它会以一个 `RecursionError`
    停下。如果你看到这个错误，说明你的基准情形缺失了、或永远到不了。

???+ question "课堂练习：递归"
    1. 用递归（而非循环）写 `count_down(n)`，打印 `n, n-1, …, 1, "liftoff!"`。
    2. 写一个递归的 `power(base, exp)`，计算 `base ** exp`（基准情形 `exp == 0` 返回 `1`）。
    3. 上面的 `fib` 把同样的值重算了很多遍。用 §1 的 `memoize` 装饰器装饰它，比较一下你能往上算到多远。

## 3. `map`、`filter` 与 `reduce`

三个内置的高阶函数，囊括了你对一个序列最常做的几件事：变换每个元素、保留某些元素、或把整个东西归结成一个值。每个都接收一个**函数**加一个**可迭代对象**——正是 2.3 那个 `lambda` 的绝佳归宿。

- **`map(func, iterable)`** 把 `func` 作用到每个元素上。
- **`filter(func, iterable)`** 保留那些 `func` 返回 `True` 的元素。
- **`reduce(func, iterable)`**（来自 `functools` 模块）从左到右两两合并元素，归结成单个结果。

???+ example "示例：map、filter、reduce"
    ```python
    from functools import reduce

    nums = [1, 2, 3, 4, 5]

    print(list(map(lambda x: x * x, nums)))        # [1, 4, 9, 16, 25]
    print(list(filter(lambda x: x % 2 == 0, nums)))# [2, 4]
    print(reduce(lambda a, b: a + b, nums))        # 15  (((1+2)+3)+4)+5
    ```

注意 `map` 和 `filter` 外面套的 `list(...)`：像 1.2 的 `range` 一样，它们返回的是**惰性迭代器**，只在你索要时才计算每个值（1.4 的迭代器协议）。`reduce` 则不同——它消耗整个可迭代对象来产出一个值，所以不需要 `list`。

???+ note "核心概念：map / filter / reduce"
    这些是作用于可迭代对象的高阶函数：**`map`** 变换，**`filter`** 筛选，**`reduce`**
    归并。前两个是惰性迭代器；`reduce` 返回单个值，住在 `functools` 里。

???+ warning "易错点：很多时候推导式更清楚"
    `map` 和 `filter` 与 1.3 的推导式有重叠。许多 Python 老手会写 `[x*x for x in nums]`
    而不是 `list(map(lambda x: x*x, nums))`，写 `[x for x in nums if x % 2 == 0]` 而不是
    `filter` 版本——它们读起来更顺。当你已经有一个具名函数可传时（`map(str, nums)`）就
    用 `map`/`filter`，而把 `reduce` 留给真正的累计归并。

???+ question "课堂练习：map / filter / reduce"
    1. 用 `map` 把 `["1", "2", "3"]` 变成 `[1, 2, 3]`。（提示：传 `int`。）
    2. 用 `filter` 从 `["hi", "there", "ok", "world"]` 里只保留长度超过三个字母的词。
    3. 用 `reduce` 求 `[3, 9, 2, 7]` 的最大值，不准调用 `max`。

## 4. 生成器

一个**生成器（generator）**是一个产出值的*流*的函数，一次产出一个，而不是一开始就把它们全算出来。我们在 1.4 简短地见过生成器，把它当作制造迭代器的一种方式；这里讲它的机理。一个函数，只要它的函数体里含有关键字 **`yield`**，就成了一个**生成器函数**。调用它并不会运行函数体——它交回一个生成器对象，而每个值只在被索要时才产出。

`yield` 的魔法在于它对**帧**做了什么。在 2.1，一次普通的 `return` 会把这次调用的帧彻底丢弃。`yield` 反其道而行：它交回一个值，却**把帧挂起、而不是丢弃**——局部变量、当前所在的行，统统都在——并把那个帧保活着，附在堆里的那个生成器对象上。当你索要下一个值时，正是那同一个帧从它暂停的地方恢复，就在 `yield` 的下一行。一个生成器，实际上就是一个你可以放下、再拿起来的、有帧的函数。

???+ example "示例：一个生成器函数"
    ```python
    def countdown(n):
        while n > 0:
            yield n          # 交回 n，然后在此暂停
            n -= 1           # 下一次索要时从这里恢复

    for x in countdown(3):
        print(x)             # 3, 2, 1

    print(list(countdown(5)))   # [5, 4, 3, 2, 1]
    ```

```recall
调用栈的现身：普通的 `return` 把它的帧扔掉；`yield` 把它留住。那个被保留的帧——像 2.3 闭包捕获的作用域一样活在堆里——正是为什么生成器的局部 `n` 能从一次 `next()` 记到下一次。
```

因为值是按需产出的，一个生成器可以描述一个大到——甚至*无穷*到——永远装不进内存的序列。你拿够了就不再索要。

???+ example "示例：一条没有尽头的平方流"
    ```python
    def squares():
        n = 1
        while True:          # 永不结束……
            yield n * n
            n += 1

    g = squares()
    print(next(g), next(g), next(g))   # 1 4 9 —— 一次算一个
    ```

而来自 1.3 的紧凑表亲——**生成器表达式**——是同一个想法的一行写法：用圆括号而不是列表推导式的方括号：

???+ example "示例：一个生成器表达式"
    ```python
    gen = (x * x for x in range(5))
    print(type(gen))         # <class 'generator'>
    print(list(gen))         # [0, 1, 4, 9, 16]
    ```

???+ note "核心概念：生成器"
    **生成器**是一个迭代器，由含 `yield` 的函数、或一个生成器表达式 `(… for …)` 产出。
    它惰性地计算值，在每个 `yield` 处暂停、在下一次索要时恢复，因此从不需要存下整个序列。

???+ warning "易错点：生成器是一次性的"
    像每一个迭代器（1.4）一样，生成器只跑一次。在你遍历过它、或用 `list()` 把它耗尽
    之后，它就空了——再遍历什么也不产出。再调用一次那个生成器函数，才能得到一个新的。

## 5. 用 `try` / `except` 处理错误

即便正确的函数也会遇上坏输入：一个缺失的文件、一个为零的除数、一个本该是数字处的 `None`。§1 的 `assert` 是用来在开发期捕捉*你自己*弄错的假设；**`try` / `except`** 则是用来优雅地处理那些你预料运行时可能发生的错误，好让一个坏值不至于让整个程序崩掉。

它的形状是：把有风险的代码放进一个 `try` 块；如果它抛出了一个异常，就由匹配的 `except` 块来处理它，而不是让程序停下。

???+ example "示例：捕捉一个特定的错误"
    ```python
    def safe_divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            print("can't divide by zero; returning None")
            return None

    print(safe_divide(10, 2))   # 5.0
    print(safe_divide(10, 0))   # 先打印消息，再 None
    ```

完整形式还有两个可选块。**`else`** 只在 `try` 块*什么都没*抛出时运行；**`finally`** 无论如何都运行，是放那些必须总是发生的收尾工作的地方。

???+ example "示例：else 与 finally"
    ```python
    def read_int(text):
        try:
            value = int(text)
        except ValueError:
            print(f"{text!r} is not a whole number")
            return None
        else:
            print("parsed successfully")
            return value
        finally:
            print("done trying")

    read_int("42")     # parsed successfully / done trying -> 42
    read_int("oops")   # not a whole number / done trying -> None
    ```

这正是让一个批处理作业能跳过那几条坏记录、把其余的跑完的办法：把每一项的有风险步骤用 `try`/`except` 包起来，记下失败，继续往下走。

???+ note "核心概念：try / except / else / finally"
    把有风险的代码放进 **`try`**；在 **`except SomeError`** 里处理一个具名的异常；用
    **`else`** 放那些只在没出错时才该运行的代码；用 **`finally`** 放那些无论如何都得
    运行的收尾。

???+ warning "易错点：别盲目地把一切都接住"
    一个光秃秃的 `except:`（或 `except Exception`）会把*每一个*错误都吞掉——包括你
    自己代码里的笔误、以及用户按下的 Ctrl-C——从而把真正的 bug 藏起来。只接住你确实
    预料的*特定*异常（`ZeroDivisionError`、`ValueError`、`FileNotFoundError`），让那些
    意料之外的浮出水面。

???+ question "课堂练习：错误处理"
    1. 写 `safe_index(seq, i)`，返回 `seq[i]`，或在下标越界时返回 `None`（接住 `IndexError`）。
    2. 把 `int(input(...))` 包进一个 `try`/`except` 循环里，一直问下去，直到用户输入一个有效的数字。
    3. 解释你会在什么时候用 `assert`、什么时候用 `try`/`except`。

## 小结

五个日常模式，全都立足于“函数是一个值”这个想法：

| 用例 | 它是什么 | 建立在 |
|------|---------|--------|
| **装饰器** | 一个扩展函数功能的高阶包装器 | 闭包、`*args`/`**kwargs`（2.3） |
| **递归** | 一个调用自己的函数 | 调用栈（2.1） |
| **map / filter / reduce** | 作用于可迭代对象的高阶函数 | `lambda`（2.3）、迭代器（1.4） |
| **生成器** | 产出一条惰性流的函数 | 迭代器（1.4）、推导式（1.3） |
| **try / except** | 优雅地处理运行时错误 | — |

接下来，**2.5 补遗与风格** 从特性退回到风格：那些让 Python 代码——包括你刚刚写下的一切——对所有人都易读的共同约定。
