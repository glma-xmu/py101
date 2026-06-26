# 可迭代对象与迭代器

## 引言

在 **1.3 控制流程** 里，`for` 循环对列表、字符串、字典、`range` 都“直接好使”。可它究竟是怎么遍历它们的？为什么它还能遍历一个从不在内存里建出完整列表的 `range` 或生成器表达式？答案是一份小而优雅的约定，叫**迭代器协议（iterator protocol）**。理解它，就能看懂 `range`（来自 1.2）和生成器表达式（来自 1.3）背后的惰性，也能让你造出自己的按需序列。一如既往，这里的代码可运行。

## 1. 可迭代对象：for 循环需要什么

**可迭代对象（iterable）**就是任何能被 `for` 循环遍历的对象。循环的第一步，是对该对象调用内置的 `iter()`——而这只有在对象提供了一个名为 `__iter__` 的特殊方法时才行得通。

???+ note "核心概念：可迭代对象"
    **可迭代对象**实现了 `__iter__`，因而 `iter(obj)` 能成功并交回一个*迭代器*。
    列表、元组、字符串、字典、集合、`range` 以及文件对象，都是可迭代的。

下面的示例展示 `iter()` 对列表成功、对整数失败——区别正在于对象是否带有 `__iter__`。

???+ example "示例：什么是可迭代的？"
    ```python
    a = [1, 2, 3]
    it = iter(a)                   # 行：列表是可迭代的
    print(it)                      # <list_iterator object ...>

    print(hasattr(a, "__iter__")) # True
    print(hasattr(1, "__iter__")) # False —— 整数不可迭代
    # iter(1)                      # 会报错：TypeError: 'int' object is not iterable
    ```

```recall
一切皆对象：“可迭代”并不是什么魔法类别——它只是表示对象带有一个 __iter__ 方法，就像每个对象都带有类型和值一样。
```

??? info "深入了解：遗留的 `__getitem__` 路径"
    在 `__iter__` 出现之前，`for` 循环可以遍历任何支持整数索引（`obj[0]`、`obj[1]`……）
    的对象，直到抛出 `IndexError` 为止。Python 至今仍兼容这种回退，所以很老的序列类型
    仍然可迭代。在现代代码中，请定义 `__iter__`——这是让对象可迭代的、明确而标准的方式。

## 2. 迭代器：一次产出一个值

调用 `iter()` 会返回一个**迭代器（iterator）**——真正产出值的那个对象。迭代器实现了 `__next__`，内置的 `next()` 会调用它来取下一个元素；没有元素时，`__next__` 抛出 `StopIteration`。一个 `for` 循环其实就是这套动作：用 `iter()` 取得迭代器，反复调用 `next()`，直到抛出 `StopIteration` 为止。

???+ note "核心概念：迭代器"
    **迭代器**按需产出值。它实现 `__next__`（返回下一个值，用尽时抛出 `StopIteration`）
    和 `__iter__`（返回 `self`）。所以每个迭代器也都是可迭代的——但一个普通的可迭代对象
    （比如列表）在你对它调用 `iter()` 之前，它自己*并不是*迭代器。

下面的示例亲手驱动这套协议，正如 `for` 循环在幕后所做的。

???+ example "示例：用 next() 手动迭代"
    ```python
    it = iter([10, 20, 30])
    print(next(it))   # 10
    print(next(it))   # 20
    print(next(it))   # 30
    # next(it)        # StopIteration —— 没有可交回的了
    ```

???+ warning "易错点：迭代器是一次性的"
    迭代器一旦被走到尽头就用尽了——没有倒带。重新 `iter()`（或对原来的*可迭代对象*重开一个
    `for` 循环）才能得到一个新的迭代器。这就是为什么对同一个 `range` 循环两次没问题
    （每次循环都会再次调用 `iter()`），而对同一个生成器循环两次却不行。

## 3. 为什么重要：惰性求值

把迭代器与可迭代对象分开，全部意义就在于**惰性求值（lazy evaluation）**：迭代器不会预先计算或存下它的所有值，而是只在被索要时才产出每一个。这买来三样东西——处理大到装不进内存的数据（一个数 GB 文件的各行）、表示概念上*无穷*的序列、以及跳过你从不查看的元素的计算。

下面的示例把这份节省讲得很具体：一个真有一百万整数的列表要花掉数 MB，而表示同样这些数的惰性 `range` 却小得可怜。

???+ example "示例：惰性的 range vs. 真实的列表"
    ```python
    import sys
    big  = list(range(1_000_000))   # 真的建出一个百万元素的列表
    lazy = range(1_000_000)         # 只存起点、终点、步长
    print(sys.getsizeof(big) > 1_000_000)  # True —— 数 MB
    print(sys.getsizeof(lazy))              # 几十字节，恒定不变
    ```

这正是你在 1.2 的 `range` 和 1.3 的生成器表达式里见过的同一种惰性——现在你能看到，它底下就是迭代器协议。

## 4. 生成器：制造迭代器的简便方式

亲手写 `__iter__` 和 `__next__` 是很少见的。日常制造迭代器的方式是**生成器函数（generator function）**：一个普通的 `def`，只是用 `yield` 代替 `return`。每个 `yield` 交回一个值并*暂停*函数、冻结它的状态；下一次调用 `next()` 时，函数从 `yield` 之后恢复。结果就是一个几乎白送给你的惰性迭代器——而 1.3 的生成器*表达式*，不过是它紧凑的表亲。

???+ note "核心概念：生成器"
    **生成器**是由含 `yield` 的函数（或一个生成器表达式）产出的迭代器。它按需计算每个值，
    并记住自己上次停在哪里。

下面的示例定义一个小生成器，并用 `for` 循环和 `list()` 来遍历它。

???+ example "示例：一个生成器函数"
    ```python
    def countdown(n):
        while n > 0:
            yield n        # 交回 n，然后在此暂停
            n -= 1

    for x in countdown(3):
        print(x)           # 3, 2, 1

    print(list(countdown(5)))   # [5, 4, 3, 2, 1]
    ```

因为值是一次一个地产出，生成器甚至能描述一个*无尽*的序列——你拿够了就不再取。

???+ example "示例：一个实际上无穷的生成器"
    ```python
    def squares():         # 概念上无穷
        n = 1
        while True:
            yield n * n
            n += 1

    g = squares()
    print(next(g), next(g), next(g))   # 1 4 9 —— 只计算我们索要的部分
    ```

???+ question "课堂练习：迭代器与生成器"
    1. 用 `iter()` 和 `next()` 手动从字符串 `"hi"` 取出前两个字符。
    2. 写一个生成器 `evens(limit)`，产出 0、2、4……直到（不含）`limit`，并打印 `list(evens(10))`。
    3. 写一个产出 2 的幂（1、2、4、8……）的生成器，并用它打印前五个。

??? info "深入了解：表达式 vs. 函数"
    生成器*表达式*——来自 1.3 的 `(x*x for x in range(5))`——和带 `yield` 的生成器*函数*
    产出的是同一种惰性迭代器。逻辑一行能写完时用表达式；当你需要循环、条件或单个表达式
    装不下的状态时，写一个带 `yield` 的函数。

## 小结

迭代器协议是每个循环底下那台安静的机器：

| 术语 | 实现 | 角色 |
|------|------|------|
| **可迭代对象** | `__iter__` | 可交给 `iter()` / `for` 循环（list、str、dict、`range`……） |
| **迭代器** | `__iter__`（返回 `self`）+ `__next__` | 用 `next()` 一次产出一个值，用尽时抛出 `StopIteration` |
| **生成器** | 含 `yield` 的 `def`，或 `(… for …)` 表达式 | 制造迭代器的简便、惰性的方式 |

一个 `for` 循环不过是 `iter()` 之后反复 `next()`、直到 `StopIteration`。把迭代器与可迭代对象分开，正是**惰性求值**的来由——这也是为什么 `range`、生成器表达式、以及你自己的生成器，能够替代那些永远装不进内存的序列。

在实际使用中，你几乎从不会从零造一个可迭代对象。日常的工作流恰恰相反：你拿一个 Python 内置的可迭代对象，从中取得一个迭代器——显式地用 `iter()`，或在 `for` 循环、推导式、`list()` 遍历它的那一刻隐式地取得。而当你需要自己*产出*一个序列时，你会用**生成器**，因为它是得到一个具备迭代器全部能力的东西的最简便方式。这三个概念层层相套——每个生成器都是迭代器，每个迭代器都是可迭代对象：

<div style="text-align:center;margin:1.2rem 0;">
<svg viewBox="0 0 360 340" xmlns="http://www.w3.org/2000/svg" role="img" width="320" style="max-width:100%;height:auto;font-family:-apple-system,Segoe UI,Roboto,sans-serif;">
  <title>可迭代对象包含迭代器，迭代器包含生成器</title>
  <desc>三个同心圆：外层是可迭代对象（由 __iter__ 定义），中层是迭代器（额外实现 __next__），内层是生成器（由 yield 函数或生成器表达式创建的特殊迭代器）。</desc>
  <circle cx="180" cy="185" r="150" fill="none" stroke="var(--md-primary-fg-color, #3f6ec6)" stroke-width="1.6"/>
  <circle cx="180" cy="185" r="104" fill="none" stroke="var(--md-primary-fg-color, #3f6ec6)" stroke-width="1.6"/>
  <circle cx="180" cy="185" r="58" fill="none" stroke="var(--md-primary-fg-color, #3f6ec6)" stroke-width="1.6"/>
  <text x="180" y="56" text-anchor="middle" font-size="14" font-weight="700" fill="var(--md-default-fg-color, #222222)">可迭代对象</text>
  <text x="180" y="74" text-anchor="middle" font-size="12" font-family="monospace" fill="var(--md-default-fg-color--light, #666666)">__iter__</text>
  <text x="180" y="104" text-anchor="middle" font-size="14" font-weight="700" fill="var(--md-default-fg-color, #222222)">迭代器</text>
  <text x="180" y="122" text-anchor="middle" font-size="12" font-family="monospace" fill="var(--md-default-fg-color--light, #666666)">+ __next__</text>
  <text x="180" y="181" text-anchor="middle" font-size="13" font-weight="700" fill="var(--md-default-fg-color, #222222)">生成器</text>
  <text x="180" y="199" text-anchor="middle" font-size="11" font-family="monospace" fill="var(--md-default-fg-color--light, #666666)">yield / (… for …)</text>
</svg>
</div>

有了第 1 章的根基——对象与类型、容器集合、控制流程，以及现在的迭代——你已经准备好把逻辑打包成可复用的单元，进入 **第 2 章：函数**。
