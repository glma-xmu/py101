# 补遗与风格

## 引言

这是一页简短的收尾，留给那些较小、但实在的话题——它们没能塞进前面四个大主题：如何给一个函数写**文档**，好让别人（和未来的你）能用它；关于**形参列表**的两个更细的点；以及那些让所有人的 Python 都保持易读的共同**风格约定**。这些都不改变你的函数*做*什么；它们改变的是你的函数读起来、调用起来、信得过的难易程度。

和往常一样，代码可运行。

## 1. 给函数写文档：文档字符串与类型提示

我们在 2.1 预告过这两者；这里是更完整的图景，因为一个没人看得懂的函数，只能算完成了一半。

**文档字符串（docstring）**是写在函数体最开头一行的字符串字面量。它不是注释——Python 把它作为 `__doc__` 存在函数上，而 `help()`、编辑器和文档工具都会读它。一行的文档字符串说明这个函数做什么；更长的则补充关于实参和返回值的细节。

???+ example "示例：一个文档字符串"
    ```python
    def clamp(value, low, high):
        """Return value limited to the range [low, high]."""
        return max(low, min(value, high))

    print(clamp(15, 0, 10))    # 10
    print(clamp.__doc__)       # Return value limited to the range [low, high].
    help(clamp)                # 显示签名和文档字符串
    ```

**类型提示（type hints）**标注一个函数期望和返回哪些种类的对象。它们**不**改变代码的运行方式——Python 并不强制它们——但它们精确地记录了你的意图，并让编辑器和检查器在你运行任何东西之前就抓出错误。

???+ example "示例：类型提示"
    ```python
    def repeat(text: str, times: int = 2) -> str:
        """Return text joined to itself, separated by spaces."""
        return " ".join([text] * times)

    print(repeat("hi", 3))     # hi hi hi
    print(repeat("ok"))        # ok ok
    ```

```recall
名称只是一张标签：像 `text: str` 这样的类型提示并不会让 `text` 成为一个字符串——它只是*说*它应当是。正如 1.1 所讲，是对象自己决定它的类型；提示只是给人和工具看的一条说明。
```

???+ note "核心概念：文档字符串和提示用来说明，不用来强制"
    **文档字符串**（函数体第一行，用三引号）说明一个函数*做什么*，由 `help()` 读取。
    **类型提示**说明它处理*哪些种类*的值。两者都不在运行时被检查——它们的存在都是为了
    让一个函数自带说明。

## 2. 更细的形参列表：仅关键字与仅位置

默认情况下，每个形参都既能按位置、也能按关键字来填（2.3 §3.1）。偶尔你想*限制*这一点，好让调用处更清楚、或让一个 API 更稳定。形参列表里的两个记号能做到。

签名里一个光秃秃的 **`*`** 意思是“我之后的每一个形参都必须**按关键字**传”。这对那些作为光秃秃的位置值就毫无意义的选项特别合适。

???+ example "示例：仅关键字形参"
    ```python
    def connect(host, *, timeout=30, secure=True):
        return f"{host} (timeout={timeout}, secure={secure})"

    print(connect("server", timeout=5))     # 没问题 —— 关键字
    # print(connect("server", 5))           # TypeError：timeout 是仅关键字的
    ```

一个 **`/`** 则相反：它*之前*的每一个形参都必须**按位置**传。你主要在内置函数里遇到它，它在那里阻止调用者依赖内部的形参名。

???+ example "示例：仅位置形参"
    ```python
    def power(base, exp, /):
        return base ** exp

    print(power(2, 10))          # 1024 —— 位置
    # print(power(base=2, exp=10))  # TypeError：仅位置
    ```

???+ note "核心概念：签名里的 `*` 与 `/`"
    一个单独的 **`*`** 强制它之后的形参为**仅关键字（keyword-only）**；一个 **`/`**
    强制它之前的形参为**仅位置（positional-only）**。两者都是用来设计更清楚、更有分寸
    的函数签名的可选工具。

## 3. PEP 8：共同的风格指南

Python 有一连串设计文档，叫做 **PEP**——Python Enhancement Proposals（Python 增强提案）。其中之一，**PEP 8**，是社区的**风格指南**：一套排布代码的约定。它*不*被语言强制——你的代码两种写法都照样运行——但遵循它能让你的代码对其余每一个 Python 程序员都一眼就熟悉，而这正是风格的大半意义所在。

你会不断用到的那些约定，许多都与函数有关：

- **命名：** 函数和变量用 `snake_case`（`read_file`，而不是 `ReadFile` 或 `readfile`）；常量用 `UPPER_CASE`；类用 `CapWords`。函数名通常应当是一个动词短语：`compute_total`、`is_valid`。
- **缩进：** 每级 4 个空格，绝不用制表符。
- **空格：** 每个逗号之后、运算符两侧各留一个空格（`a + b`、`f(x, y)`），但括号内侧紧邻处、以及调用的括号之前*不*留（写 `f(x)`，不写 `f ( x )`）。
- **空行：** 顶层函数之间空两行，好让眼睛把它们分开。
- **行长：** 让每行保持适度地短（PEP 8 说 79 个字符；许多项目用 88 左右）。

同一个函数，前后对比：

???+ example "示例：杂乱 vs. PEP 8"
    ```python
    # 不符合 PEP 8
    def Add (X,Y):return X+Y

    # 符合 PEP 8
    def add(x, y):
        return x + y

    print(add(2, 3))   # 5
    ```

???+ note "核心概念：PEP 8 是推荐，不是强制"
    **PEP 8** 是 Python 的标准风格指南。它是一个约定，不是解释器强制的规则——但遵循它
    能让你的代码对所有人都易读。工具能替你应用它：像 `black` 这样的**格式化器**会把你的
    代码改写成一致的风格，像 `ruff` 或 `flake8` 这样的**检查器（linter）**会标出违规之处。

??? info "深入了解：用 functools.partial 固定部分实参"
    再来一个值得知道的一等小技巧。`functools.partial` 接收一个函数和它的*部分*实参，
    返回一个把那些实参填好了的新函数——是一个小 `lambda` 或闭包之外的利落替代：

    ```python
    from functools import partial

    def power(base, exp):
        return base ** exp

    square = partial(power, exp=2)   # 一个新函数：exp 固定为 2 的 power
    print(square(5))                 # 25
    ```

    这和 2.3 那个一等的想法是同一个——函数是值，你可以由它造出新函数——只是被打包成了
    一个标准工具。

???+ question "课堂练习：风格与签名"
    1. 把这个重写成符合 PEP 8 的样子：`def Mul(A ,B):return A*B`。
    2. 给你 §3 的 `add` 函数加上一行文档字符串和类型提示。
    3. 定义 `make_user(name, *, admin=False)`，并展示 `make_user("Ada", True)` 会失败、而 `make_user("Ada", admin=True)` 能成功。解释为什么。

## 小结

这些是把能用的函数变成*好*函数的收尾功夫：

| 工具 | 它添了什么 |
|------|-----------|
| **文档字符串** | 一段人类可读的描述，由 `help()` 读取 |
| **类型提示** | 一条关于所涉及值之种类的说明（不被强制） |
| **签名里的 `*` / `/`** | 仅关键字与仅位置形参 |
| **PEP 8** | 让代码保持易读的共同风格约定 |

这就为**第 2 章**画上句号。你现在能定义函数并调用它们；能就帧、堆、命名空间和作用域进行推理；能把函数作为一等的值来传递、返回、构造；并能通过装饰器、递归、`map`/`filter`/`reduce`、生成器和错误处理来运用它们——全都写成干净、有文档、合乎约定的 Python。
