# 习题 — 第 2 章：函数

一组练习题，按它们所练习的小节分组。请自己动手；凡题目中给出代码，都当作给定数据或起点。每题都附**示例输出**，让你知道目标是什么。本页不提供解答。

## 1. 定义与调用函数

???+ question "练习 1.1 — 你的第一个函数"
    写一个函数 `double(x)`，返回 `x * 2`，然后对 `21` 和 `3.5` 各调用一次。

    **示例输出**
    ```text
    42
    7.0
    ```

???+ question "练习 1.2 — 一个没有形参的函数"
    写 `greet()`，不取任何实参，返回 `"Hello, class!"`。调用它。然后打印 `greet`（*不带*括号），并解释其中的差别。

    **示例输出**
    ```text
    Hello, class!
    <function greet at 0x...>
    ```

???+ question "练习 1.3 — return vs print"
    写两个函数：`add_return(a, b)` **返回** `a + b`，`add_print(a, b)` 把它**打印**出来。把每次调用的结果存进一个变量并打印那个变量。为什么其中一个是 `None`？

    **示例输出**
    ```text
    7
    7
    None
    ```

???+ question "练习 1.4 — 返回多个值"
    写 `min_max(numbers)`，把最小值和最大值作为一个元组一起返回，并把结果解包到 `low, high`。用 `[4, 9, 1, 7]` 测试。

    **示例输出**
    ```text
    1 9
    ```

???+ question "练习 1.5 — 默认形参"
    写 `power(base, exponent=2)`，使 `power(5)` 求平方、`power(5, 3)` 求立方。

    **示例输出**
    ```text
    25
    125
    ```

???+ question "练习 1.6 — 被共享的可变默认值"
    先预测输出，再运行。解释是*默认列表住在哪里*，让第二次和第三次调用越长越大。

    ```python
    def append_to(element, to=[]):
        to.append(element)
        return to

    print(append_to(1))
    print(append_to(2))
    print(append_to(3))
    ```

    **示例输出**
    ```text
    [1]
    [1, 2]
    [1, 2, 3]
    ```

???+ question "练习 1.7 — 修好这个陷阱"
    用 `None` 哨兵的写法重写 `append_to`，让每次不带列表的调用都从头开始。确认 `append_to(1)` 和 `append_to(2)` 各返回一个单元素列表。

    **示例输出**
    ```text
    [1]
    [2]
    ```

???+ question "练习 1.8 — 局部是私有的"
    运行下面的代码。为什么最后一行抛出 `NameError`？

    ```python
    def square(n):
        result = n * n
        return result

    print(square(4))
    print(result)
    ```

    **示例输出**
    ```text
    16
    NameError: name 'result' is not defined
    ```

## 2. 命名空间与作用域

???+ question "练习 2.1 — 预测 LEGB"
    先预测全部三行输出，再运行。

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

    **示例输出**
    ```text
    local
    enclosing
    global
    ```

???+ question "练习 2.2 — 读取一个全局"
    写一个函数 `show()`，*不*把模块层变量 `counter`（设为 `0`）作为实参，而是直接打印它的值。解释这个名字是在哪个作用域里被找到的。

    **示例输出**
    ```text
    0
    ```

???+ question "练习 2.3 — 遮蔽一个内置"
    先预测每一行。然后加一行，恢复对内置 `max` 的访问。

    ```python
    print(max(1, 2))
    max = min
    print(max(1, 2))
    ```

    **示例输出**
    ```text
    2
    1
    ```

???+ question "练习 2.4 — UnboundLocalError"
    解释这为什么会报错，并用两种方式修好它：一次用 `global`，一次把 `counter` 传进来、再返回新值。

    ```python
    counter = 0
    def bump():
        counter = counter + 1
        return counter
    bump()
    ```

    **示例输出**
    ```text
    UnboundLocalError: ...local variable 'counter'...
    ```

???+ question "练习 2.5 — global 关键字"
    用 `global` 写 `add(n)`，使反复调用都累加进一个模块层的 `total`。调用 `add(3)` 再 `add(4)`，并打印 `total`。

    **示例输出**
    ```text
    7
    ```

???+ question "练习 2.6 — nonlocal"
    写 `outer()`，定义 `message = "before"`，再写一个嵌套的 `inner()`，用 `nonlocal` 把它设为 `"after"`。调用 `inner()`，再从 `outer` 里打印 `message`。

    **示例输出**
    ```text
    after
    ```

???+ question "练习 2.7 — 为什么一个交换函数会失败"
    运行这段代码。为什么之后 `a` 和 `b` 没变？用局部名称来讨论它。

    ```python
    def swap(x, y):
        x, y = y, x

    a, b = 1, 2
    swap(a, b)
    print(a, b)
    ```

    **示例输出**
    ```text
    1 2
    ```

???+ question "练习 2.8 — 查看命名空间"
    写一个有一个局部变量的函数，打印 `list(locals())`，以及名字 `"print"` 是否在 `dir(__builtins__)` 里。确认那个局部出现了、而 `print` 是个内置。

    **示例输出**
    ```text
    ['note']
    True
    ```

## 3. 一等与高阶函数

???+ question "练习 3.1 — 字典里的函数"
    建一个字典 `ops`，把 `"sq"` 映射到一个求平方的函数、`"neg"` 映射到一个取反的函数，然后经由字典对值 `4` 各调用一次。

    **示例输出**
    ```text
    16
    -4
    ```

???+ question "练习 3.2 — 一个高阶函数"
    写 `apply_twice(func, x)`，返回 `func(func(x))`。用一个“加 3”的函数、从 10 开始测试。

    **示例输出**
    ```text
    16
    ```

???+ question "练习 3.3 — 用 key 排序"
    给定 `words = ["python", "is", "great"]`，用带 `key` 的 `sorted` 按长度把它们排序。

    **示例输出**
    ```text
    ['is', 'great', 'python']
    ```

???+ question "练习 3.4 — 位置 vs 关键字"
    定义 `rect(width, height)`，返回面积。先按位置调用一次，再用两个关键字、以相反顺序调用一次；确认结果相同。然后解释为什么 `rect(height=3, 4)` 是个错误。

    **示例输出**
    ```text
    12
    12
    ```

???+ question "练习 3.5 — `*args`"
    写 `my_sum(*args)`，把它收到的、无论多少个数字相加。用两个、再用五个数字测试。

    **示例输出**
    ```text
    3
    15
    ```

???+ question "练习 3.6 — `**kwargs`"
    写 `scoreboard(**players)`，接受像 `scoreboard(Alice=9, Bob=7)` 这样的调用，并为每一项打印 `"Alice: 9"`。（回忆 `kwargs` 是一个字典。）

    **示例输出**
    ```text
    Alice: 9
    Bob: 7
    ```

???+ question "练习 3.7 — 解包谜题"
    预测每个名称被绑定到的值。

    ```python
    a, *b, c = 1, 2, 3, 4, 5
    print(a, b, c)

    *d, e = [10, 20, 30]
    print(d, e)
    ```

    **示例输出**
    ```text
    1 [2, 3, 4] 5
    [10, 20] 30
    ```

???+ question "练习 3.8 — 铺进一次调用"
    给定 `pair = (3, 4)` 和返回 `base ** exp` 的 `power(base, exp)`，用 `*` 把 `pair` *铺开*来调用 `power`。

    **示例输出**
    ```text
    81
    ```

???+ question "练习 3.9 — 一个造函数的闭包"
    写 `make_adder(n)`，返回一个把 `n` 加到其实参上的函数。造出 `add10` 和 `add100`，各对 `5` 调用一次。

    **示例输出**
    ```text
    15
    105
    ```

???+ question "练习 3.10 — 一个计数器闭包"
    写 `make_counter()`，返回一个在相继调用时返回 1、2、3、… 的函数（用 `nonlocal`）。展示两个计数器彼此独立。

    **示例输出**
    ```text
    1 2 3
    1
    ```

???+ question "练习 3.11 — 带私有状态的闭包"
    写 `make_account(balance)`，返回一个含两个函数的字典：`deposit(amount)` 和 `withdraw(amount)`，它们共享一个私有的 `balance`（外面无法直接访问它）。从起始余额 100 存入 50、取出 30 后，一个 `balance()` 报告器应当显示 120。

    **示例输出**
    ```text
    120
    ```

???+ question "练习 3.12 — lambda"
    给定 `people = [("Ada", 36), ("Bob", 41), ("Cleo", 29)]`，用一个 `lambda` key 配合 `max` 找出最年长者，并按名字排序。

    **示例输出**
    ```text
    ('Bob', 41)
    [('Ada', 36), ('Bob', 41), ('Cleo', 29)]
    ```

## 4. 实践用例

### 装饰器

???+ question "练习 4.1 — 一个记日志的装饰器"
    写一个装饰器 `announce`，使装饰 `add(a, b)` 后调用 `add(2, 3)` 时，会在前后各打印一行，然后返回结果。

    **示例输出**
    ```text
    add is being called.
    finished calling add.
    5
    ```

???+ question "练习 4.2 — 一个计时装饰器"
    写一个装饰器 `timed`，打印被包装函数花了多长时间（前后各用一次 `time.perf_counter()`）。把它用到一个对 `range(1_000_000)` 求和的函数上。

    **示例输出**
    ```text
    sum_range took 0.02s
    499999500000
    ```

???+ question "练习 4.3 — 记忆化"
    写一个装饰器 `memoize`，把结果缓存进一个字典，让用相同实参的重复调用瞬间完成。把它用到一个慢的递归 `fib` 上，确认答案一致。

    **示例输出**
    ```text
    55
    ```

???+ question "练习 4.4 — assert 作为守卫"
    写 `mean(values)`，用 `assert` 拒绝空列表和含 `None` 的列表，否则返回平均值。

    **示例输出**
    ```text
    4.0
    AssertionError: mean() needs at least one value
    ```

### 递归

???+ question "练习 4.5 — 阶乘"
    写一个递归的 `factorial(n)`（基准情形 `n == 0` 返回 `1`）。用 `5` 测试。

    **示例输出**
    ```text
    120
    ```

???+ question "练习 4.6 — 递归求和"
    写 `total(xs)`，用递归（而非循环）返回一个列表之和（基准情形：空列表返回 `0`）。

    **示例输出**
    ```text
    10
    ```

???+ question "练习 4.7 — 斐波那契"
    写一个递归的 `fib(n)`，`fib(0) = 0`、`fib(1) = 1`，并打印前十个斐波那契数。

    **示例输出**
    ```text
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    ```

???+ question "练习 4.8 — 递归的幂"
    递归地写 `power(base, exp)`（基准情形 `exp == 0` 返回 `1`）。测试 `power(2, 10)`。

    **示例输出**
    ```text
    1024
    ```

???+ question "练习 4.9 — 倒计时"
    写一个递归的 `count_down(n)`，打印 `n, n-1, …, 1`，然后是 `"liftoff!"`。

    **示例输出**
    ```text
    3
    2
    1
    liftoff!
    ```

### map、filter、reduce

???+ question "练习 4.10 — map"
    用 `map` 把 `["1", "2", "3"]` 变成列表 `[1, 2, 3]`。（提示：传 `int`。）

    **示例输出**
    ```text
    [1, 2, 3]
    ```

???+ question "练习 4.11 — filter"
    用 `filter` 从 `["hi", "there", "ok", "world"]` 里只保留长度超过三个字母的词。

    **示例输出**
    ```text
    ['there', 'world']
    ```

???+ question "练习 4.12 — reduce"
    用 `reduce`（来自 `functools`）计算 `[1, 2, 3, 4, 5]` 的乘积。

    **示例输出**
    ```text
    120
    ```

### 生成器

???+ question "练习 4.13 — 一个偶数生成器"
    写一个生成器 `evens(limit)`，产出 0、2、4、… 直到（不含）`limit`，并打印 `list(evens(10))`。

    **示例输出**
    ```text
    [0, 2, 4, 6, 8]
    ```

???+ question "练习 4.14 — 完全平方数"
    写一个生成器，永远产出完全平方数 1、4、9、16、…，并用它打印前五个。

    **示例输出**
    ```text
    1 4 9 16 25
    ```

???+ question "练习 4.15 — 生成器表达式"
    用一个生成器表达式，构建一个 0–4 立方的生成器，打印它的 `type`，再打印它的 `list(...)`。

    **示例输出**
    ```text
    <class 'generator'>
    [0, 1, 8, 27, 64]
    ```

???+ question "练习 4.16 — 一次性"
    生成器是一次性的。预测下面第二次 `list(...)` 并解释。

    ```python
    g = (x for x in range(3))
    print(list(g))
    print(list(g))
    ```

    **示例输出**
    ```text
    [0, 1, 2]
    []
    ```

### 错误处理

???+ question "练习 4.17 — 安全除法"
    写 `safe_divide(a, b)`，返回 `a / b`，或在除以零时打印一条消息并返回 `None`。

    **示例输出**
    ```text
    5.0
    can't divide by zero
    None
    ```

???+ question "练习 4.18 — 安全取下标"
    写 `safe_index(seq, i)`，返回 `seq[i]`，或在下标越界时返回 `None`（接住 `IndexError`）。

    **示例输出**
    ```text
    20
    None
    ```

???+ question "练习 4.19 — try / except / else / finally"
    写 `read_int(text)`，成功时返回 `int(text)`、遇 `ValueError` 时返回 `None`，在 `else` 里打印 `"ok"`、在 `finally` 里打印 `"done"`。对 `"42"` 和 `"oops"` 各调用一次。

    **示例输出**
    ```text
    ok
    done
    42
    done
    None
    ```

## 5. 补遗与风格

???+ question "练习 5.1 — 给函数写文档"
    给一个函数 `add(a, b)` 加上一行文档字符串和类型提示。然后打印它的 `__doc__`。

    **示例输出**
    ```text
    Return the sum of a and b.
    ```

???+ question "练习 5.2 — 仅关键字形参"
    定义 `make_user(name, *, admin=False)`。展示 `make_user("Ada", True)` 抛出 `TypeError`、而 `make_user("Ada", admin=True)` 能用。解释为什么。

    **示例输出**
    ```text
    TypeError: make_user() takes 1 positional argument but 2 were given
    ```

???+ question "练习 5.3 — 收拾干净（PEP 8）"
    把这个重写成符合 PEP 8 的样子（命名、空格、排布），保持行为完全一致。

    ```python
    def Mul (A,B):return A*B
    ```

    **示例输出**
    ```text
    6
    ```

???+ question "练习 5.4 — 偏应用（选做）"
    用 `functools.partial`，把一个两实参的 `power(base, exp)` 通过固定 `exp=2` 造出 `square`，并调用 `square(7)`。

    **示例输出**
    ```text
    49
    ```
