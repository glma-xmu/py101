# 函数是一等对象

## 引言

我们已经两次说过，函数也不过是一个**对象**——一次在 2.1 的格言里，又一次在每当我们把 `square` 像任何别的值一样画进堆里的时候。本页终于要把这一点兑现。因为函数是一个普通对象，凡是你能对一个数或一个列表做的事，都能对它做：把它绑定到一个名字、把它存进列表或字典、**把它传给另一个函数**、以及**从一个函数里把它返回**。这种自由就是“一等（first-class）”的含义，而它解锁了一个强大的想法——**高阶函数（higher-order function）**——整个 2.4 都建立在它之上。

和往常一样，代码可运行。

## 1. 函数是一个对象

第 1 章里我们用 `id()` 和 `type()` 查看一个对象的标识和类型。一个函数对这两者都答得上来，跟一个整数一样——而且没有什么能拦着你给它起第二个名字，或把它塞进一个列表或一个字典。

???+ example "示例：函数是可以搬来搬去的值"
    ```python
    def square(n):
        return n * n

    print(type(square))      # <class 'function'>

    sq = square              # 同一个函数对象的第二个名字
    print(sq(5))             # 25 —— 同一个函数，新名字

    ops = {"sq": square, "neg": lambda n: -n}   # 把函数存进一个字典
    print(ops["sq"](4))      # 16
    ```

```recall
名称指向对象：那个函数对象像 2.1 里的每一个值一样住在**堆**里，而 `sq = square` 正是 1.2 里那同一种别名——两个名字，一个对象。这个对象只不过恰好是可调用的，所以两个名字都能被调用。
```

???+ note "核心概念：一等对象"
    当一门语言对一个对象不施加任何限制时，它就是**一等的（first-class）**：它能被
    命名、被存进数据结构、被作为实参传入、被作为结果返回。在 Python 里，函数是一等的
    ——本页其余部分利用的正是这一点。

## 2. 高阶函数

因为函数是一个值，所以一个函数可以把*另一个函数*当作它的实参之一。一个**把函数作为实参、或把函数作为结果返回**的函数，叫做**高阶函数**。有些你已经用过了：`sorted` 接受一个 `key` 函数，`max` 也一样。

下面的示例写了我们自己的一个小小高阶函数，并且把内置的 `len` 作为实参传给 `sorted`。

???+ example "示例：把函数作为实参传入"
    ```python
    def apply_twice(func, x):
        return func(func(x))        # 把传进来的函数调用两次

    def increment(n):
        return n + 1

    print(apply_twice(increment, 5))   # 7

    words = ["python", "is", "great"]
    print(sorted(words, key=len))      # ['is', 'great', 'python'] —— 按长度排序
    ```

???+ note "核心概念：高阶函数"
    **高阶函数**是把函数作为实参、或把函数作为结果返回的函数。普通函数作用于数据；
    高阶函数作用于*行为*。

到这里都不错——但 `apply_twice` 能用，只因为 `increment` 恰好只取一个实参。如果我们想交出去的那个函数需要的实参个数不同呢？要想干净地把实参传过去，我们得先更仔细地看看实参究竟是如何抵达形参的。

## 3. 实参如何抵达形参

### 3.1 位置实参与关键字实参

当一个函数有好几个形参时，你可以用两种方式提供实参。**位置（positional）**实参按顺序匹配形参。**关键字（keyword）**实参显式地点名形参，于是顺序不再要紧、调用也读得更清楚。

???+ example "示例：位置实参 vs 关键字实参"
    ```python
    def power(base, exponent):
        return base ** exponent

    print(power(2, 10))                # 1024 —— 位置，按顺序匹配
    print(power(exponent=10, base=2))  # 1024 —— 关键字，与顺序无关
    print(power(2, exponent=10))       # 1024 —— 先位置后关键字
    ```

???+ warning "易错点：位置实参必须在前"
    一旦一次调用里出现了一个关键字实参，它之后的每一个实参也都必须是关键字。
    `power(base=2, 10)` 是一个 `SyntaxError`。把位置实参放在前面，然后才是关键字。

### 3.2 变长实参：`*args` 与 `**kwargs`

有时你事先并不知道会有多少个实参。两个特殊记号专门对付这件事。在**定义**里，`*args` 把任何多出来的位置实参**收集**进一个*元组*，`**kwargs` 把任何多出来的关键字实参收集进一个*字典*。`args` 和 `kwargs` 这两个名字只是约定——干活的是 `*` 和 `**`。

???+ example "示例：用 `*` 和 `**` 收集实参"
    ```python
    def total(*args):
        print("args 是", args)      # 一个装着所有传入项的元组
        return sum(args)

    print(total(1, 2, 3, 4))        # args 是 (1, 2, 3, 4) -> 10

    def show(**kwargs):
        for key, value in kwargs.items():
            print(key, "=", value)

    show(a=1, b=2)                  # a = 1 / b = 2  （kwargs 是一个字典）
    ```

这两个星号也能反着用。在一次**调用**里，`*` 把一个序列**铺开**成位置实参，`**` 把一个字典铺开成关键字实参。一个符号，两种相反的活儿：定义时*收集*，调用时*铺开*。

???+ example "示例：把实参铺进一次调用"
    ```python
    nums = [3, 1, 4, 1, 5]
    print(max(*nums))               # 等同于 max(3, 1, 4, 1, 5) -> 5

    settings = {"sep": "-", "end": "!\n"}
    print("a", "b", "c", **settings)   # a-b-c!
    ```

现在 §2 那个高阶难题迎刃而解。一个包装器可以用 `*args, **kwargs` 接收*任意*实参，再把它们原封不动地直接传给它所调用的那个函数——这个写法正是 2.4 里装饰器的核心。

???+ example "示例：一个透传的高阶函数"
    ```python
    def call_it(func, *args, **kwargs):
        print("正在调用", func.__name__)
        return func(*args, **kwargs)        # 原样转发一切

    print(call_it(max, 3, 7, 2))            # 正在调用 max -> 7
    call_it(print, "a", "b", "c", sep=", ") # 正在调用 print -> a, b, c
    ```

???+ note "核心概念：`*args` 与 `**kwargs`"
    在*定义*里，`*args` 把多出来的位置实参聚成一个元组，`**kwargs` 把多出来的关键字
    实参聚成一个字典。在*调用*里，`*` 和 `**` 把一个序列或字典重新铺开成一个个独立的
    实参。定义里的顺序是固定的：普通形参，然后 `*args`，然后 `**kwargs`；而带默认值的
    形参必须排在不带默认值的之后。

??? info "深入了解：同一个星号也用来解包赋值"
    那个收集用的 `*` 并非函数独有——把一个序列解包到名称里时它同样有效，本身就很顺手：

    ```python
    first, *rest = [10, 20, 30, 40]
    print(first)   # 10
    print(rest)    # [20, 30, 40] —— '*rest' 收走剩下的一切
    ```

    左边可以出现一个 `*`，把剩余的项收集进一个列表。这和 `*args` 是同一个想法：一个
    星号就意味着“剩下多少都算”。

???+ question "课堂练习：变长实参"
    1. 写 `my_sum(*args)`，返回它收到的、无论多少个数字之和，用两个、再用五个数字测试。
    2. 写 `greet_all(**people)`，接受像 `greet_all(Alice=9, Bob=7)` 这样的关键字实参，并为每一项打印 `"Alice is 9"`。（回忆 `kwargs` 是一个字典。）
    3. 给定 `pair = (3, 4)`，用 `power(*pair)` 调用 §3.1 的 `power`，确认它返回 `81`。

## 4. 把函数作为返回值：闭包

“高阶”的另一半是**返回**一个函数。当一个函数定义了一个内层函数并把它返回时，内层那个会带着它的**外层（enclosing）**作用域一起走——也就是造出它的那个函数的局部名称（回忆 2.2 的外层作用域）。一个内层函数连同它仍在引用的那些外层名称捆在一起，就叫做**闭包（closure）**。

???+ example "示例：一个造函数的函数"
    ```python
    def make_linear(a, b):
        def line(x):
            return a * x + b      # 'a' 和 'b' 来自外层作用域
        return line

    double_plus_one = make_linear(2, 1)
    triple = make_linear(3, 0)

    print(double_plus_one(5))     # 11
    print(triple(5))              # 15
    ```

下面的图把 `make_linear(2, 1)` 返回的那一瞬间定格下来。它的帧里有 `a → 2`、`b → 1`，以及刚刚建好的内层函数 `line`；那条绿色箭头把这个函数交回给全局名称 `double_plus_one`。

```memory
memory: 堆
stack: 调用栈
objects:
  ln: 一个函数
  i2: 2
  i1: 1
globals: 全局命名空间
  double_plus_one -> ln @return
frame: make_linear(a, b)
  a -> i2
  b -> i1
  line -> ln
```

现在看看什么存活了下来。`make_linear` 返回的那一刻，上面那个帧就被丢弃——可等到你调用 `double_plus_one(5)` 时，`a` 和 `b` *还在那儿*。这正是 2.1 那个堆的想法被推到了尽头：**帧**是临时的，但对象 `2` 和 `1` **没有**被释放，因为返回的那个闭包仍在引用它们。闭包恰恰就是这个——一个函数，连同它一直让其存活的、堆里的一小块私有空间。

```recall
格言的现身：`make_linear` 的帧消失了，但 `a` 和 `b` 是堆里的对象，被那个指着它们的闭包保活着。每一次调用 `make_linear` 都会造出一个*新*闭包，带着它自己捕获的值。
```

要让内层函数*改变*一个被捕获的名称（而不只是读它），用 `nonlocal`——正是 2.2 那个关键字。一个经典用法是一个在各次调用间记住自己计数的计数器。

???+ example "示例：一个会计数的闭包"
    ```python
    def make_counter():
        count = 0
        def step():
            nonlocal count        # 重新绑定外层的 'count'，而不是新建一个局部
            count += 1
            return count
        return step

    c = make_counter()
    print(c(), c(), c())          # 1 2 3
    d = make_counter()
    print(d())                    # 1 —— 一个全新的、独立的计数器
    ```

???+ note "核心概念：闭包"
    **闭包**是一个内层函数，连同它仍在引用的外层作用域名称。闭包在外层调用返回之后
    依然让那些对象存活，从而给内层函数一份私有的、持久的记忆。

闭包不只是一个计数小把戏——它们让你把**数据和作用于它的行为捆在一起**，同时把数据保持**私有**。下面的示例造了一些简单的游戏角色。每一次 `make_player` 调用都捕获它自己的 `hp` 和 `damage`，并返回一小束共享它们的函数。注意 `hp` *不是*返回出来的键之一：改变一个角色血量的唯一途径是经由它自己的 `take_damage`——外面没有谁能伸手进来把 `hp` 设成一个荒唐的值。

???+ example "示例：带私有状态的闭包（游戏角色）"
    ```python
    def make_player(name, hp, damage):
        def attack(other):
            other["take_damage"](damage)      # 把我的伤害用到别人身上
        def take_damage(amount):
            nonlocal hp
            hp -= amount
        def status():
            print(f"{name}: {hp} hp")
        return {"attack": attack, "take_damage": take_damage, "status": status}

    bob = make_player("Bob", 100, 10)
    charlie = make_player("Charlie", 100, 5)

    bob["attack"](charlie)
    charlie["status"]()        # Charlie: 90 hp
    bob["status"]()            # Bob: 100 hp —— 没被动过
    ```

这三个内层函数都闭合在来自同一次 `make_player` 调用的*同一个* `hp` 和 `damage` 之上，于是它们彼此协作：`attack` 触发对方的 `take_damage`，后者更新那个 `status` 稍后会读取的 `hp`。两个不同的玩家带着两套独立的、被捕获的值。如果这听起来像一个带私有字段和方法的**对象**——它确实是。闭包是获得封装最古老的方式之一，也是你将在第 3 章见到的类的种子。

??? info "深入了解：被捕获的变量到底住在哪里"
    闭包总得把它捕获的变量存在*某处*，而你可以直接看到它们。Python 把它们放在附着于
    函数对象上的**单元（cell）**里，经由 `__closure__` 可达：

    ```python
    print(charlie["take_damage"].__closure__)              # 一个由 cell 对象组成的元组
    print(charlie["take_damage"].__closure__[0].cell_contents)   # 90 —— 当前的 hp
    ```

    这是堆的想法被坐实了：被捕获的 `hp` 是一个由内层函数上的一个单元持有的对象，这正是
    它为何能比创建它的那次 `make_player` 调用活得更久。而且因为 `attack`、`take_damage`
    和 `status` 来自*同一次*调用，它们为 `hp` 共享**同一个**单元——通过其中之一改动它，
    其余的立刻就看见。同胞闭包靠它们共同持有的堆单元被绑在一起。

??? info "深入了解：`x=[0]` 计数小把戏"
    在闭包还没想通之前，人们有时会用一个*可变默认值*来伪造一个持久计数器——
    `def step(_cache=[0]): _cache[0] += 1`。它能用，全靠利用我们在 2.1 警告过的那个
    陷阱：默认列表只被创建一次、又在各次调用间被共享。它很巧妙，但脆弱又出人意料。一个
    用 `nonlocal` 的闭包把你的意思说清楚了，才是对的工具。

## 5. `lambda`：没有名字的函数

很多时候，你想传到某处去的那个函数小到给它一个 `def` 加一个名字都显得笨重。**`lambda`** 把一个函数*就地*作为一个表达式造出来，没有名字。它的函数体是单个表达式，其值会被自动返回。

语法是 `lambda 形参: 表达式`。下面两种定义是等价的：

???+ example "示例：lambda 不过是一个紧凑的函数值"
    ```python
    def square_def(n):
        return n * n

    square_lambda = lambda n: n * n      # 行为相同，就地写出

    print(square_def(6), square_lambda(6))   # 36 36
    ```

`lambda` 大放异彩之处，是把一个一次性的函数传给一个高阶函数，这样你就永远不必给它起名。

???+ example "示例：lambda 作为 key 函数"
    ```python
    people = [("Ada", 36), ("Bob", 41), ("Cleo", 29)]

    print(sorted(people, key=lambda person: person[1]))   # 按年龄排序
    print(max(people, key=lambda person: person[1]))      # 最年长者 -> ('Bob', 41)
    ```

???+ warning "易错点：让 lambda 保持小巧"
    一个 `lambda` 只能装*单个表达式*——没有语句，没有多行。这是有意为之：如果一个函数
    需要的不止一个简短表达式，就给它一个真正的 `def` 和一个有描述性的名字。把 `lambda`
    留给那些你传给 `sorted`、`max`、`map` 之流的、用完即弃的小函数。

## 小结

Python 里的函数是**一等对象**，所以它们能像任何值一样被命名、存储、传递、返回：

| 想法 | 含义 |
|------|------|
| **一等** | 函数可以被起别名、放进列表/字典、传入、返回 |
| **高阶函数** | 把函数作为实参、或返回一个函数 |
| **`*args` / `**kwargs`** | 定义时收集多出来的实参；调用时把它们铺开 |
| **闭包** | 一个内层函数，加上它一直保活着的外层名称 |
| **`lambda`** | 一个小巧的匿名函数，作为单个表达式就地写出 |

这不是五个各自独立的小把戏，而是同一个想法的不同侧面：*函数是一个值*。接下来，**2.4 实践用例** 会把这个想法用在你课程围绕展开的五个模式里——装饰器、递归、`map`/`filter`/`reduce`、生成器、错误处理——它们每一个都是乔装打扮的高阶函数。
