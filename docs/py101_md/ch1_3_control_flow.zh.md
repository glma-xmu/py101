# 控制流程

## 引言

程序不只是一串从上到下顺序执行的语句。真实的程序需要**重复**做事——对班里的每个学生都做一遍——也需要**选择**做事——只在某个条件成立时才动作。决定*哪些*语句运行、运行*多少次*的工具，称为**控制流程（control flow）**。本页讲两种最常用的：**循环（loop）**，负责重复；**条件（conditional）**，负责选择。一路上我们都依赖 1.1–1.2：你所遍历、所检验的，正是你已经认识的那些对象与容器。

和之前一样，这里的代码可运行——按 *Run*（或 Ctrl/Cmd+Enter）执行、修改、再运行。

## 1. for 循环

对容器最常做的事，就是逐个访问它的元素。`for` 循环正是如此：它依次取出容器的每个元素，把你的循环变量绑定到它，并对每个元素运行一次循环体。

下面的示例依次遍历一个列表、一个字符串、一个字典——你在 1.1–1.2 见过的每一种容器，都能用同样的方式遍历。

???+ example "示例：遍历容器"
    ```python
    for n in [10, 20, 30]:
        print(n)

    for ch in "hi":
        print(ch)

    prices = {"apple": 3, "pear": 5}
    for key in prices:          # 遍历字典得到的是它的键
        print(key, prices[key])
    ```

```recall
名称指向对象：每一轮里，循环变量只是一个被重新绑定到容器下一个对象的名称——什么都没有被复制。
```

### 1.1 用 range 计数

有时你并没有一个容器要遍历——你只是想做固定次数的事，或生成一串整数。这正是 `range` 的用武之地，而它最自然的归宿就在这里，作为 `for` 循环计数的对象。回忆 1.2：`range` 是一个*惰性*序列，`range(5)` 代表 0、1、2、3、4，却不会真的造出一个列表。

???+ example "示例：在 for 循环里用 range"
    ```python
    for i in range(5):          # 0, 1, 2, 3, 4
        print(i)

    for i in range(2, 11, 2):   # 起点、终点（不含）、步长
        print(i)                # 2, 4, 6, 8, 10
    ```

### 1.2 更 Pythonic 的遍历：enumerate 与 zip

当你以为需要*下标加元素*时，请用 `enumerate`，而不要手动数下标。当你需要并排遍历两个序列时，用 `zip`。它们更易读，也能避开一个经典 bug。

???+ example "示例：enumerate 与 zip"
    ```python
    colors = ["red", "green", "blue"]
    for i, color in enumerate(colors):
        print(i, color)

    names  = ["Ada", "Bob"]
    scores = [95, 88]
    for name, score in zip(names, scores):
        print(name, "scored", score)
    ```

`zip` 也是用两个并行列表构建字典的自然方式：`dict(zip(names, scores))`。（`zip` 会在较短的那个用尽时停止。）

???+ warning "易错点：不要遍历 `range(len(...))`"
    一个来自其他语言的常见习惯是 `for i in range(len(colors)): color = colors[i]`。在 Python 里这既笨拙又易错——需要元素时直接遍历（`for color in colors`），确实需要下标时用 `enumerate`。

???+ question "课堂练习：for 循环"
    1. 把 `"python"` 的每个字符各打印一行。
    2. 用 `range` 打印 0 到 20 的偶数。
    3. 给定 `names = ["Ada", "Bob", "Cleo"]`，用 `enumerate` 把每个打印成 `"1. Ada"`、`"2. Bob"`……（计数从 1 开始）。

## 2. while 循环

`for` 循环*每个元素重复一次*。有时你想要的是*只要条件成立就一直重复*，事先并不知道要循环多少轮——一直问用户直到他输入有效答案，一直对一个数折半直到它足够小。这就是 **`while`** 循环：它检查一个条件，条件为真就运行循环体，然后重复。

下面的示例用了经典的*累加器*模式：一个每轮更新的累计值。

???+ example "示例：带累加器的 while 循环"
    ```python
    total = 0
    n = 1
    while n <= 5:        # 只要条件为真就继续
        total += n       # 累加
        n += 1           # 朝着条件变假的方向前进
    print(total)         # 15  (1+2+3+4+5)
    ```

当你在遍历一个已知集合或固定次数时用 `for`；当“是否继续”取决于一个每轮重新检验的条件时，用 `while`。

???+ warning "易错点：死循环"
    `while` 循环只有在条件变假时才结束，所以循环体必须朝那个方向推进。漏掉上面的 `n += 1` 就会永远循环。如果你需要在循环体*内部*发现某个条件才停下，请用 `break`（见下一节）。

???+ question "课堂练习：while 循环"
    1. 从 `n = 100` 开始，用整除不断折半（`n //= 2`），每次打印，直到它变成 0。
    2. 累加整数 1、2、3……一旦累计值超过 50 就停下；打印你一共加了多少个数。

## 3. break、continue 与循环 else

在任何循环内部，你有时需要更精细的控制。**`break`** 立即退出循环。**`continue`** 跳过当前这一轮余下的部分，直接进入下一轮。循环还可以带一个 **`else`** 子句，它只在循环*没有*因 `break` 而中断、自然结束时才运行——很适合“查找”型循环。

???+ example "示例：break、continue 与 else"
    ```python
    for n in range(2, 10):
        if n % 2 == 0:
            continue          # 跳过偶数
        print("odd:", n)

    target = 7
    for n in [3, 5, 7, 9]:
        if n == target:
            print("found", target)
            break             # 停止查找
    else:
        print("not found")    # 只有在没发生 break 时才运行
    ```

## 4. 条件执行：if / elif / else

循环决定代码*运行多少次*；**`if`** 语句决定它*是否*运行。你给它一个条件，缩进的代码块只有在条件为真时才运行。用 `elif`（“否则如果”）依次检验更多条件，用末尾的 `else` 作为兜底。

下面的示例把一条 `if` 链与一个 `for` 循环结合起来——这正是对每个元素区别处理的日常套路。

???+ example "示例：给数字分类"
    ```python
    for n in range(-2, 3):
        if n > 0:
            print(n, "is positive")
        elif n < 0:
            print(n, "is negative")
        else:
            print(n, "is zero")
    ```

???+ question "课堂练习：条件筛选"
    使用 `l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`：
    
    1. 只打印奇数。
    2. 对 3 的倍数打印 `"fizz"`，对 5 的倍数打印 `"buzz"`，其余打印数字本身。

## 5. 条件：比较与布尔

每个 `if` 和 `while` 都依赖一个条件——一个求值为 `True` 或 `False` 的表达式。本节讲如何把这些条件写好。

### 5.1 比较值 vs. 比较标识

比较*值*时，Python 提供了熟悉的运算符 `<`、`>`、`<=`、`>=`、`==`（相等）和 `!=`（不等）。而要问另一个不同的问题——两个名称是否指向*同一个对象*（标识，来自 1.1）——则用 `is`。

???+ example "示例：== 与 is"
    ```python
    a = [1, 2, 3]
    b = [1, 2, 3]
    print(a == b)   # True  —— 内容相同
    print(a is b)   # False —— 两个不同的对象

    c = a
    print(a is c)   # True  —— 同一个对象（两个名称，一个列表）
    ```

```recall
一切皆对象：== 比较对象的值，而 is 比较它们的标识（id）——正是我们在 1.1 中画出来的那个东西。
```

???+ warning "易错点：判断 `None` 要用 `is`"
    `None` 是唯一、单例的对象，所以惯用的判断是 `x is None`（以及 `x is not None`），而非 `x == None`。当你想表达“同一个对象”时就用 `is`，对 `None` 尤其如此。

### 5.2 布尔逻辑与真值

条件用 **`and`**、**`or`**、**`not`** 组合。两点便利让 Python 的条件十分简洁。其一，每个对象自身都有**真值（truthy/falsy）**：`0`、`0.0`、`""`、空容器（`[]`、`{}`、`set()`）以及 `None` 都算作假，其余大多算作真——所以 `if items:` 的意思就是“如果 `items` 非空”。其二，`and`/`or` 会**短路**：一旦结果已定就立即停止。

???+ example "示例：真值与布尔运算符"
    ```python
    items = []
    if not items:
        print("the list is empty")

    name = ""
    print(name or "anonymous")   # "anonymous" —— or 返回第一个为真的值

    x = 5
    print(0 < x < 10)            # True —— 链式比较
    ```

Python 还允许**链式比较**，如 `0 < x < 10`，它读作 `(0 < x) and (x < 10)`——更贴近数学记法，也是把条件写得 Pythonic 的好例子。

???+ question "课堂练习：条件"
    1. 写一个条件，当字符串 `s` 为空*或*只含空格时为真。（提示：`s.strip()`。）
    2. 给定 `age = 20`，用一条链式比较检查它是否落在 13 到 64（含）之间。

## 6. 推导式：把循环写成表达式

很多时候，一个循环存在的唯一目的，就是*从旧集合构建一个新集合*——把每个数平方、留下偶数、把名字和分数配对。Python 为此提供了一种紧凑、可读的写法：**推导式（comprehension）**。它是把控制流程浓缩成一个表达式，也是最具辨识度的 Pythonic 写法之一。

下面的示例用两种方式构建同一个列表——先用显式循环，再用推导式——好让你看清它们的对应关系。

???+ example "示例：列表推导式"
    ```python
    # 显式循环
    squares = []
    for x in range(6):
        squares.append(x * x)
    print(squares)

    # 同一件事，用推导式
    squares = [x * x for x in range(6)]
    print(squares)
    ```

推导式可以用末尾的 `if` 进行**筛选**，它还有**集合**和**字典**两种形式，与 1.2 的容器相呼应——同样的花括号，同样的思路。

???+ example "示例：筛选、集合与字典推导式"
    ```python
    evens = [x for x in range(10) if x % 2 == 0]
    print(evens)

    unique_lengths = {len(w) for w in ["hi", "bye", "ok"]}   # 一个集合
    print(unique_lengths)

    squares_map = {x: x * x for x in range(5)}               # 一个字典
    print(squares_map)
    ```

??? info "深入了解：圆括号给出的是*生成器*，不是元组"
    把方括号换成圆括号并**不会**造出“元组推导式”——它造出的是一个**生成器表达式**，它*惰性地*、一次一个地产生值，而不是一次性建好整个集合：

    ```python
    gen = (x * x for x in range(5))
    print(gen)            # <generator object ...>
    print(list(gen))      # [0, 1, 4, 9, 16]
    ```

    这种惰性正是 `range` 背后的同一个思路，也是 **1.4 可迭代对象与迭代器** 的主题。要得到元组，用 `tuple(...)` 包住一个生成器即可。

???+ question "课堂练习：推导式"
    1. 构建一个列表，包含 1 到 19 中奇数的平方。
    2. 从 `words = ["Ada", "bob", "CLEO"]` 构建一个全小写形式的列表。
    3. 构建一个把 `words` 中每个词映射到其长度的字典。

## 小结

控制流程决定一个程序做什么、做多少次。你现在已掌握全部日常工具：

| 结构 | 用来 |
|------|------|
| `for ... in` | 对容器中的每个元素重复一次（配合 `range`、`enumerate`、`zip`） |
| `while` | 只要条件成立就重复 |
| `break` / `continue` / 循环 `else` | 提前退出、跳过一轮、或在没发生 `break` 时动作 |
| `if` / `elif` / `else` | 只在条件为真时运行一个代码块 |
| `==` / `is`、`and`/`or`/`not`、真值 | 写出这些选择所依赖的条件 |
| 推导式 | 用一个表达式构建新的列表、集合或字典 |

这里的一切都作用于 1.1–1.2 的对象与容器——循环遍历它们，条件检验它们，推导式重建它们。接下来，**1.4 可迭代对象与迭代器** 将揭示迭代*究竟如何*运作，以及为什么像 `range` 和生成器这样的惰性序列如此重要。
