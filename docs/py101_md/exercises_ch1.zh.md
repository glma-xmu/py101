# 习题 — 第 1 章：Python 基础

一组练习题，按它们所练习的小节分组。请自己动手；凡题目中给出代码，都当作给定数据或起点。每题都附**示例输出**，让你知道目标是什么。本页不提供解答。

???+ note "关于函数的说明"
    少数题目会用 `def name(args): … return …` 定义一个小函数，迭代器相关的题目还会用带 `yield` 的生成器函数。`yield` 的写法在 1.4 讲过；函数这个主题会在 **第 2 章** 正式登场，但这里用到的基本 `def` 形式就够了。

## 1. 对象与类型

???+ question "练习 1.1 — 预测类型"
    先预测每个值的 `type()`，再运行核对。哪个是 `set`，哪个是 `dict`？哪个是 `tuple`？

    ```python
    for v in [1, 1.0, True, "1", [1], (1,), {1}, {1: "a"}, 3 - 2j, None]:
        print(v, "->", type(v))
    ```

    **示例输出**
    ```text
    1 -> <class 'int'>
    1.0 -> <class 'float'>
    True -> <class 'bool'>
    1 -> <class 'str'>
    [1] -> <class 'list'>
    (1,) -> <class 'tuple'>
    {1} -> <class 'set'>
    {1: 'a'} -> <class 'dict'>
    (3-2j) -> <class 'complex'>
    None -> <class 'NoneType'>
    ```

???+ question "练习 1.2 — 布尔表现得像数字"
    解释每个结果。`True` 在什么意义上是一个整数？为什么对一串 `True`/`False` 求和能数出 `True` 的个数？

    ```python
    print(True + True)
    print(sum([True, False, True, True]))
    print("yes" if 3 else "no")
    ```

    **示例输出**
    ```text
    2
    3
    yes
    ```

???+ question "练习 1.3 — 但布尔*不只是*数字"
    因为 `1 == True == 1.0`（且它们哈希相同），预测这个字典最终有几个键、哪个值胜出。然后写一个检查 `is_real_bool(x)`，只对真正的布尔值返回 `True`。在什么场景下，坚持要一个真正的 `bool`（而非任何为真的值）才真正重要？（提示：`isinstance(x, bool)`。）

    ```python
    d = {1: "one", True: "true", 1.0: "float"}
    print(d)
    print(is_real_bool(1))      # 应为 False
    print(is_real_bool(True))   # 应为 True
    ```

    **示例输出**
    ```text
    {1: 'float'}
    False
    True
    ```

???+ question "练习 1.4 — 何时是*同一个*对象？"
    预测每个比较，再运行。为什么 `==` 是比较值的正确工具，而 `is` 问的是另一个问题？（257 那一例与实现相关——一次典型运行会打印 `False`。）

    ```python
    a = 256; b = 256
    print(a is b)
    c = 257; d = 257
    print(c is d)
    print(c == d)
    ```

    **示例输出**
    ```text
    True
    False
    True
    ```

???+ question "练习 1.5 — 哪种数值类型？"
    对每个表达式，预测结果是 `int`、`float` 还是 `complex`，再用 `type()` 核对。

    ```python
    for e in [7 / 2, 7 // 2, 2 ** 0.5, 3 + 4.0, 1 + 2j]:
        print(type(e))
    ```

    **示例输出**
    ```text
    <class 'float'>
    <class 'int'>
    <class 'float'>
    <class 'float'>
    <class 'complex'>
    ```

???+ question "练习 1.6 — `None` 也是一个值"
    预测输出，然后解释*内层*和*外层*的 `print` 各显示什么，以及 `print(...)` 返回什么。

    ```python
    print(print("hello"))
    x = print("world")
    print(x is None)
    ```

    **示例输出**
    ```text
    hello
    None
    world
    True
    ```

???+ question "练习 1.7 — `type()` vs `isinstance()`"
    给定 `x = True`，比较下面两个检查。哪个为 `True`，为什么？要问“这是个数字吗？”该用哪个；要问“这正好是个布尔值吗？”又该用哪个？

    ```python
    x = True
    print(type(x) is int)
    print(isinstance(x, int))
    print(isinstance(x, bool))
    ```

    **示例输出**
    ```text
    False
    True
    True
    ```

### 可选：基础之外的类型

下面探索几个我们**没有**正式讲过的内置类型——在真实代码里遇到时能认出来就好。全部可选。

???+ question "练习 1.8 — array（可选）"
    `array.array` 像列表，但所有元素必须是同一种数值类型。创建一个、索引它，看看加入错误类型会怎样。

    ```python
    import array
    a = array.array('i', [1, 2, 3, 4, 5])   # 'i' = 有符号整数
    print(a)
    print(type(a))
    print(a[0], a[-1])
    # a.append(6.0)   # 取消注释：会怎样？
    ```

    **示例输出**
    ```text
    array('i', [1, 2, 3, 4, 5])
    <class 'array.array'>
    1 5
    # a.append(6.0)  ->  TypeError: 'float' object cannot be interpreted as an integer
    ```

???+ question "练习 1.9 — bytes 与 bytearray（可选）"
    `bytes` 是不可变的原始字节序列；`bytearray` 是它可变的孪生兄弟。两者都试试，并用一种编码在文本与字节之间往返。

    ```python
    b = b"hi"
    print(b, type(b))
    ba = bytearray(b"hi")
    ba[0] = 72            # 'H' 对应的字节
    print(ba)
    print("café".encode("utf-8"))
    print(b"caf\xc3\xa9".decode("utf-8"))
    ```

    **示例输出**
    ```text
    b'hi' <class 'bytes'>
    bytearray(b'Hi')
    b'caf\xc3\xa9'
    café
    ```

???+ question "练习 1.10 — 精确算术：Fraction 与 Decimal（可选）"
    浮点数是近似的。把一个浮点求和与 `Fraction`、`Decimal` 给出的精确答案比较。

    ```python
    from fractions import Fraction
    from decimal import Decimal
    print(0.1 + 0.2)
    print(0.1 + 0.2 == 0.3)
    print(Fraction(1, 10) + Fraction(2, 10))
    print(Decimal("0.1") + Decimal("0.2"))
    ```

    **示例输出**
    ```text
    0.30000000000000004
    False
    3/10
    0.3
    ```

???+ question "练习 1.11 — 复数的各部分（可选）"
    `complex` 是内置数值类型。取出它的实部、虚部和模。

    ```python
    z = 3 + 4j
    print(z.real, z.imag)
    print(abs(z))
    print(type(z))
    ```

    **示例输出**
    ```text
    3.0 4.0
    5.0
    <class 'complex'>
    ```

???+ question "练习 1.12 — frozenset（可选）"
    `frozenset` 是不可变的集合——因此与 `set` 不同，它可哈希，能作字典键或另一个集合的成员。

    ```python
    fs = frozenset([1, 2, 2, 3])
    print(fs)
    # fs.add(4)              # 取消注释：会怎样？
    d = {fs: "ok"}           # frozenset 可以作键
    print(d[frozenset([3, 2, 1])])
    ```

    **示例输出**
    ```text
    frozenset({1, 2, 3})
    # fs.add(4)  ->  AttributeError: 'frozenset' object has no attribute 'add'
    ok
    ```

## 2. 容器集合

???+ question "练习 2.1 — 正确使用 set() 与 {}"
    逐行运行，并总结规则：`set(...)` 何时成功？`{...}` 何时建出的是*集合*而非别的东西？最后，如何用 `set()` 函数创建 `{(1, 2, 3)}`——一个元素、一个元组？

    ```python
    print(set((1, 2, 3)))
    print(set((1,)))
    print({1, 2, 3})
    print({(1, 2, 3)})
    ```

    **示例输出**
    ```text
    {1, 2, 3}
    {1}
    {1, 2, 3}
    {(1, 2, 3)}
    ```

???+ question "练习 2.2 — KeyError vs get()"
    展示索引一个不存在的键会引发 `KeyError`，而 `get()` 不会。然后查找 `"key3"`，让它返回默认值 `"missing"` 而不崩溃。

    ```python
    d = {"key1": "value1", "key2": "value2"}
    print(d["key1"])
    print(d.get("key3", "missing"))
    ```

    **示例输出**
    ```text
    value1
    missing
    ```

???+ question "练习 2.3 — 去重"
    从 `nums` 得到一个只含唯一值、且已排序的列表。

    ```python
    nums = [1, 2, 2, 3, 4, 4, 4, 5, 1]
    ```

    **示例输出**
    ```text
    [1, 2, 3, 4, 5]
    ```

???+ question "练习 2.4 — 集合运算"
    用下面两个集合，求并集、交集、在 `a` 但不在 `b` 的元素、以及对称差。再判断 `{2, 3}` 是否为 `a` 的子集。

    ```python
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    ```

    **示例输出**
    ```text
    {1, 2, 3, 4, 5, 6}
    {3, 4}
    {1, 2}
    {1, 2, 5, 6}
    True
    ```

???+ question "练习 2.5 — 用两个列表构建字典"
    把名字与分数配成一个字典（一次调用即可）。然后添加 `"Dan"`（88）、把 `"Bob"` 更新为 90、并查找可能不存在的 `"Eve"`，不存在时返回 `"unknown"`。

    ```python
    names  = ["Ada", "Bob", "Cleo"]
    scores = [91, 85, 78]
    ```

    **示例输出**
    ```text
    {'Ada': 91, 'Bob': 90, 'Cleo': 78, 'Dan': 88}
    unknown
    ```

???+ question "练习 2.6 — 列表可变，元组不可变"
    预测哪些编辑成功、哪些报错，并用可变性来解释。原地编辑之后，`id(l)` 会变吗？

    ```python
    l = [10, 20, 30]
    t = (10, 20, 30)
    l[0] = 99
    del l[1]
    print(l)
    # t[0] = 99   # 取消注释：会怎样？
    ```

    **示例输出**
    ```text
    [99, 30]
    # t[0] = 99  ->  TypeError: 'tuple' object does not support item assignment
    ```

???+ question "练习 2.7 — 字符串处理"
    从下面这段杂乱的标题，生成 slug `"data-science-101"`（去空白、转小写、空格变连字符）。再打印它有几个单词，以及原字符串的反转。

    ```python
    title = "  Data Science 101  "
    ```

    **示例输出**
    ```text
    data-science-101
    3
      101 ecneicS ataD  
    ```

### 列表入门小练习

一组“手指操”，用来练熟列表的**索引**、**切片**、**嵌套**，以及一个名称如何*指向*一个列表——这是 Python 里与 C 语言经典指针练习相对应的部分。

???+ question "练习 2.8 — 从两端索引"
    用索引打印：第一个元素、最后一个元素、第二个元素、倒数第二个元素（靠近末尾的可试试负索引）。

    ```python
    xs = [10, 20, 30, 40, 50]
    ```

    **示例输出**
    ```text
    10
    50
    20
    40
    ```

???+ question "练习 2.9 — 预测切片"
    运行前先预测每个切片。

    ```python
    xs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(xs[2:5])
    print(xs[:3])
    print(xs[7:])
    print(xs[::2])
    print(xs[::-1])
    ```

    **示例输出**
    ```text
    [2, 3, 4]
    [0, 1, 2]
    [7, 8, 9]
    [0, 2, 4, 6, 8]
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ```

???+ question "练习 2.10 — 原地修改"
    按顺序执行下列操作，每步后打印 `xs`：末尾追加 `60`；在索引 1 处插入 `15`；`pop` 掉索引 3 的元素；把切片 `xs[0:2]` 替换为 `[1, 2, 3]`。

    ```python
    xs = [10, 20, 30, 40, 50]
    ```

    **示例输出**
    ```text
    [10, 20, 30, 40, 50, 60]
    [10, 15, 20, 30, 40, 50, 60]
    [10, 15, 20, 40, 50, 60]
    [1, 2, 3, 20, 40, 50, 60]
    ```

???+ question "练习 2.11 — 列表的列表（矩阵）"
    打印第 1 行第 2 列的元素（下标从 0 起）；整条中间行；以及中间列（取列需要一个循环或推导式）。

    ```python
    m = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
    ```

    **示例输出**
    ```text
    6
    [4, 5, 6]
    [2, 5, 8]
    ```

???+ question "练习 2.12 — 两个名称，一个列表（“指针”陷阱）"
    预测两次打印。为什么第一种情形里改 `b` 也改了 `a`，第二种却没有？（回忆：名称指向对象；`a[:]` 是一份拷贝。）

    ```python
    a = [1, 2, 3]
    b = a
    b.append(4)
    print(a)

    a = [1, 2, 3]
    b = a[:]          # 一份拷贝
    b.append(4)
    print(a)
    ```

    **示例输出**
    ```text
    [1, 2, 3, 4]
    [1, 2, 3]
    ```

???+ question "练习 2.13 — 手写，不走捷径"
    不使用 `[::-1]`、`reversed()`、`max()`、`sum()`，用循环打印列表的反转、它的最大值、以及总和。

    ```python
    xs = [4, 9, 2, 7, 5, 1]
    ```

    **示例输出**
    ```text
    [1, 5, 7, 2, 9, 4]
    9
    28
    ```

## 3. 控制流程

???+ question "练习 3.1 — 带小数步长的序列"
    打印 `0.0, 0.5, 1.0, …, 10.0`。必须用 `range`（它只产出整数，所以要适当地缩放）。

    **示例输出**
    ```text
    0.0
    0.5
    1.0
    ...
    9.5
    10.0
    ```

???+ question "练习 3.2 — 手动追踪循环"
    先不运行，写出**每个**变量在每一步的值，再运行核对。

    ```python
    def naive_by2(lst, by):
        n = len(lst) // by
        res = []
        for i in range(n):
            res.append([lst[2 * i], lst[2 * i + 1]])
        return res

    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(naive_by2(nums, 2))
    ```

    **示例输出**
    ```text
    [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
    ```

???+ question "练习 3.3 — 重新分组"
    把列表分成 `[[1, 3, 5, 7, 9], [2, 4, 6, 8, 10]]`——先奇后偶——且不使用迭代器或生成器。（提示：带步长的切片 `lst[start::step]`。）

    ```python
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ```

    **示例输出**
    ```text
    [[1, 3, 5, 7, 9], [2, 4, 6, 8, 10]]
    ```

???+ question "练习 3.4 — FizzBuzz"
    对 1 到 30：3 的倍数打印 `"fizz"`，5 的倍数打印 `"buzz"`，两者都是的打印 `"fizzbuzz"`，其余打印数字本身。

    **示例输出**
    ```text
    1
    2
    fizz
    4
    buzz
    fizz
    7
    8
    fizz
    buzz
    11
    fizz
    13
    14
    fizzbuzz
    ...
    ```

???+ question "练习 3.5 — 够了就停"
    累加整数 1、2、3……一旦累计值首次**超过 100** 就停下。打印最终的累计值，以及你一共加了多少个数。（用 `while` 循环。）

    **示例输出**
    ```text
    105
    14
    ```

???+ question "练习 3.6 — 50 以内的素数"
    只用循环和 `if`（不导入任何库），打印 2 到 50 之间的每一个素数。

    **示例输出**
    ```text
    2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
    ```

???+ question "练习 3.7 — 用循环做最小二乘"
    对下面的数据和模型 $y = b x$，找出使 $L(b)=\sum_{i=1}^{5}(y_i - b x_i)^2$ 最小的斜率 $b$。用循环在 `0.50, 0.51, …, 1.50` 上搜索 `b`，记录目前最优的 `b`。**不要**使用 `min` 或 `numpy.argmin`。

    ```python
    xs = [0, 1, 2, 3, 4]
    ys = [0, 0, 1, 3, 5]
    ```

    **示例输出**
    ```text
    best b = 1.03
    ```

## 4. 可迭代对象与迭代器

???+ question "练习 4.1 — 手动迭代"
    用 `iter()` 和 `next()` 一次一个地取出列表中的值，并展示取完最后一个之后会发生什么。

    ```python
    data = [10, 20, 30]
    ```

    **示例输出**
    ```text
    10
    20
    30
    # 再调用一次 next(it) -> StopIteration
    ```

???+ question "练习 4.2 — 迭代器是一次性的"
    预测两次输出，并解释为什么第二次是空的。

    ```python
    it = iter([1, 2, 3])
    print(list(it))
    print(list(it))
    ```

    **示例输出**
    ```text
    [1, 2, 3]
    []
    ```

???+ question "练习 4.3 — 平方数生成器，两种写法"
    产出平方数 `1, 4, 9, 16, …`：(a) 用带 `yield` 的生成器**函数**；(b) 用生成器**表达式**。表达式那种在 100 处停下，并打印结果列表。

    **示例输出**
    ```text
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    ```

???+ question "练习 4.4 — 无穷斐波那契"
    写一个无限产出斐波那契数的生成器（$F_0=0$、$F_1=1$、$F_n=F_{n-1}+F_{n-2}$），然后打印前 10 个。

    ```python
    def fibonacci():
        ...   # 你的代码
    ```

    **示例输出**
    ```text
    0 1 1 2 3 5 8 13 21 34
    ```

???+ question "练习 4.5 — 带筛选的生成器表达式"
    写一个**生成器表达式**，产出那些以辅音开头、以元音（a、e、i、o、u）结尾的单词的*长度*。对下面的列表，它应产出 6、4、5（对应 "banana"、"kiwi"、"grape"）。

    ```python
    words = ["apple", "banana", "orange", "kiwi", "grape",
             "elephant", "tiger", "lion", "mouse"]
    vowels = "aeiou"
    ```

    **示例输出**
    ```text
    [6, 4, 5]
    ```

???+ question "练习 4.6 — 用生成器产出完全平方数"
    写一个生成器，产出不超过 100 的**完全平方数**（1、4、9……），然后把它们打印在一行里。（完全平方数是某个整数 $n$ 的 $n^2$。）

    **示例输出**
    ```text
    1 4 9 16 25 36 49 64 81 100
    ```

???+ question "练习 4.7 — 列表 vs 生成器的内存占用"
    比较同一计算下列表与生成器的内存占用，并解释其差异。（具体字节数因平台而异。）

    ```python
    import sys
    print(sys.getsizeof([x * x for x in range(10000)]))
    print(sys.getsizeof((x * x for x in range(10000))))
    ```

    **示例输出**
    ```text
    85176
    200
    ```

???+ question "练习 4.8 — 两参数的 iter()（可选）"
    `iter(f, sentinel)` 会反复调用函数 `f`，直到它返回 `sentinel`。用它（而非 `while` 循环）从 0–9 中抽取随机整数，直到首次抽到 `0`，并打印此前抽到的数字（`0` 本身不打印）。

    ```python
    import random
    # 提示：定义 f() 返回一个 random.choice(range(10))，再用 iter(f, 0)。
    ```

    **示例输出**（每次运行不同）
    ```text
    2
    6
    4
    ```

???+ question "练习 4.9 — 平均序列长度（可选）"
    在上一题的基础上，把实验**重复 50 次**，报告首次抽到 `0` 之前所抽数字个数的平均值。（把每次的长度收集到一个列表里，再取 `sum(lengths) / 50`。理论平均约为 9。）

    **示例输出**（每次运行不同）
    ```text
    average length over 50 runs: 8.74
    ```
