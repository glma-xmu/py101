# 命名空间与作用域

## 引言

在 2.1 我们看到，名称住在**帧（frame）**里，而它们所指的对象住在**堆（heap）**里。一次正在运行的调用把自己的局部名称保存在它的帧里；模块则把它的名称保存在顶层。每一组这样的名称都有一个正式的名字：**命名空间（namespace）**。本页回答紧随其后的两个问题。同一时刻有多少个命名空间在起作用？以及，当你写下一个光秃秃的名字（比如 `x`）时，Python 会到哪个命名空间里去找它？第二个问题的答案是一条四个字母的规则——**LEGB**——你几乎会用它来推断你读到的每一个函数。

和往常一样，这里的代码可运行——按 *Run*、修改、再运行。

## 1. 命名空间就是一部名称的字典

**命名空间**正是 2.1 那些帧所暗示的东西：一个从名称到它们所指对象的映射——底下其实就是一部 Python 字典。写 `x = 5` 就是在你当前所处的那个命名空间里添加或更新条目 `"x" → <对象 5>`。没有比这更玄乎的了。

而且 Python **同时维护着好几个命名空间**。其中两个你已经见过：**全局（global）**命名空间（模块顶层的名称，`globals()` 会把它返回）和一个**局部（local）**命名空间（正在运行的那次函数调用内部的名称，`locals()` 会把它返回）。

下面的示例表明，这两者确实是彼此独立的字典。

???+ example "示例：globals() 与 locals()"
    ```python
    title = "第 2 章"             # 一个全局名称

    def show():
        note = "在 show 内部"      # 一个局部名称
        print("locals:", list(locals()))                # ['note']
        print("title 在全局里吗:", "title" in globals())  # True
        print("note 在全局里吗:", "note" in globals())    # False

    show()
    ```

```recall
名称指向对象：命名空间不过是记录“哪个名称指向哪个对象”的那本账——还是我们一直在画的那些箭头，如今被收进了一部带标签的字典。
```

???+ note "核心概念：命名空间"
    **命名空间**是一个从名称到对象的映射（一部字典）。Python 同时维护着好几个——
    **内置（built-in）**、**全局（global）**、**外层（enclosing）**和**局部
    （local）**——你用到的每一个名称，都是靠在它们之间逐层查找来解析的。

## 2. 函数可以定义在函数内部

函数体不过是普通代码，没有什么能阻止这段代码里再含一个 `def`。定义在另一个函数内部的函数叫做**嵌套函数（nested function）**——它能做一件新鲜事：它能*看见*包住它的那个函数的名称。

下面的示例把 `inner` 定义在 `outer` 内部。当 `inner` 运行时，它读取了 `message`——一个属于 `outer` 的局部名称——尽管 `message` 并不是 `inner` 自己的局部名称。

???+ example "示例：内层函数看得见外层的名称"
    ```python
    def outer():
        message = "hello from outer"
        def inner():
            print(message)      # inner 读取 outer 的局部名称 'message'
        inner()

    outer()                     # hello from outer
    ```

有两点要注意。第一，写 `def inner` 只是在每次 `outer` 运行时*创建* `inner`；和任何函数一样，不**调用**它就什么都不做，所以我们接着写了 `inner()`。第二，`inner` 只在 `outer` 运行期间存在——它只是 `outer` 的一个局部名称，随那次调用而生、随它而灭。

`inner` 能看见的那个外围作用域——`outer` 的命名空间——叫做**外层（enclosing）**作用域。它就是我们马上要见到的 LEGB 规则里的“E”，也正是 `nonlocal` 存在的全部理由。眼下知道这些就够了；在 2.3，我们会让嵌套函数真正派上用场——把它们传来传去、把它们返回。

```recall
名称指向对象：这里没有魔法——`inner` 只是没有自己的 `message`，所以当它需要这个名字时，Python 就到它周围的作用域里去找，找到了 `outer` 的那个。
```

## 3. 四个命名空间

在任意一刻，最多可以有四种命名空间同时在作用域中：

- **局部（Local）**——此刻正在运行的那次函数调用内部的名称：它的帧。调用开始时创建，返回时丢弃。
- **外层（Enclosing）**——某个外层函数的局部名称，被定义在它内部的嵌套函数所看见（就是我们 §2 刚见过的情形）。那个外层命名空间就是内层函数的*外层*命名空间。我们在 2.3 让嵌套函数真正派上用场。
- **全局（Global）**——在你模块顶层定义的名称。每个模块一个，模块启动时创建，整个程序期间存活。
- **内置（Built-in）**——Python 预先定义、处处可用的名称：`print`、`len`、`range`、`max`、`True`、`None` 等等。它们住在 `builtins` 模块里。

下面的示例确认，内置名称确实住在它们自己的一个模块里。

???+ example "示例：内置命名空间"
    ```python
    import builtins
    print("print" in dir(builtins))   # True
    print("len" in dir(builtins))     # True
    print(len(dir(builtins)) > 100)   # True —— 内置名称有很多
    ```

## 4. 作用域与 LEGB 规则

**作用域（scope）**是程序中一个名称无需任何限定就能够到的范围。每个命名空间都有一个作用域。当你使用一个光秃秃的名字时，Python 按一个固定的顺序在各命名空间里搜索，并在**第一个**匹配处停下：

> **局部（L）** → **外层（E）** → **全局（G）** → **内置（B）**

这就是 **LEGB 规则**。如果这四个里都找不到，Python 就抛出 `NameError`。

这四个作用域层层**嵌套**，一个套在下一个里：名称搜索从最内层（局部）开始，一路向外直到内置。下面这张图就是地图。左边是作用域的名字；右边是住在各层里的代码。它还预告了 §6 的两个“逃生口”——`global` 让最内层的函数一直够到模块作用域去重新绑定一个名称，`nonlocal` 让它去重新绑定外层函数里的一个名称。

<div style="text-align:center;margin:1.3rem 0;">
<svg viewBox="0 0 660 290" xmlns="http://www.w3.org/2000/svg" role="img" width="640" style="max-width:100%;height:auto;font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-weight:700;">
  <title>LEGB 作用域层层嵌套：内置 ⊃ 全局 ⊃ 外层 ⊃ 局部</title>
  <desc>四个嵌套的方框。内置（解释器）包含全局（模块），全局包含外层（嵌套函数），外层包含局部（正在运行的函数）。一条标着 global 的箭头从局部函数一直够到全局/模块作用域；一条标着 nonlocal 的箭头从局部够到外层作用域。</desc>
  <defs>
    <marker id="legb-fg" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--md-default-fg-color, #111111)"/></marker>
    <marker id="legb-red" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#e0303a"/></marker>
  </defs>
  <rect x="8" y="12" width="470" height="266" rx="12" fill="#2f6db5"/>
  <rect x="26" y="48" width="436" height="212" rx="11" fill="#3a9d4f"/>
  <rect x="44" y="92" width="404" height="150" rx="10" fill="#f0a500"/>
  <rect x="62" y="140" width="290" height="64" rx="9" fill="#c8202a"/>
  <line x1="243" y1="24" x2="243" y2="250" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.85"/>
  <text x="22" y="35" fill="#ffffff" font-size="17">内置</text>
  <text x="40" y="71" fill="#ffffff" font-size="17">全局</text>
  <text x="58" y="116" fill="#1a1a1a" font-size="17">外层</text>
  <text x="86" y="180" fill="#ffffff" font-size="17">局部</text>
  <text x="300" y="35" fill="#ffffff" font-size="16">解释器</text>
  <text x="312" y="71" fill="#10331c" font-size="16">模块</text>
  <text x="280" y="116" fill="#3a2600" font-size="16">嵌套函数</text>
  <text x="262" y="180" fill="#ffffff" font-size="16">函数</text>
  <path d="M352,170 C600,168 602,44 468,62" fill="none" stroke="var(--md-default-fg-color, #111111)" stroke-width="2.3" marker-end="url(#legb-fg)"/>
  <text x="588" y="108" fill="var(--md-default-fg-color, #111111)" font-size="16">global</text>
  <path d="M352,186 C520,202 520,122 452,122" fill="none" stroke="#e0303a" stroke-width="2.3" marker-end="url(#legb-red)"/>
  <text x="498" y="170" fill="#e0303a" font-size="16">nonlocal</text>
</svg>
</div>

下面的示例把三个 `x` 放进三个不同的作用域；每一句 `print(x)` 都在搜索顺序里找到离它最近的那个。

???+ example "示例：LEGB 实战"
    ```python
    x = "全局"

    def outer():
        x = "外层"
        def inner():
            x = "局部"
            print(x)        # 局部
        inner()
        print(x)            # 外层

    outer()
    print(x)                # 全局
    ```

下面的图把 `inner()` 正在运行的那一刻定格下来。这里有三个不同的名称，都拼作 `x`，各自在自己的命名空间里，各自指向堆里自己的那个字符串。`inner` 的查找先找到局部的 `x`，从不去问其余的。（内置命名空间还在更外一层，图里没画。）

```memory
memory: 堆
stack: 调用栈
objects:
  s1: '全局'
  s2: '外层'
  s3: '局部'
globals: 全局命名空间
  x -> s1
frame: outer()
  x -> s2
frame: inner()
  x -> s3
```

当一个名称在局部*找不到*时，搜索只是径直向外继续——这正是为什么一个函数不必任何仪式就能读取一个全局名称。

???+ example "示例：查找一路落到全局"
    ```python
    greeting = "hi"          # 全局

    def f():
        print(greeting)      # 没有局部的 'greeting' —— 在全局作用域里找到

    f()
    ```

```recall
格言的现身：“全局”没什么特别——它只是搜索在局部和外层之后才到达的那个命名空间。内置名称不过是它最后才到达的那一批。
```

## 5. 遮蔽：当一个名称盖住另一个

在内层作用域里绑定一个外层也存在的名称，那么在这个作用域余下的部分里，内层的绑定就**遮蔽（shadow）**——盖住——外层的那个。通常这无害、甚至有用（每个函数都可以有自己的 `i` 或 `result`）。但偶尔它是个陷阱，尤其当你遮蔽了一个**内置**名称时最为痛苦。

???+ example "示例：遮蔽内置的 `max`"
    ```python
    print(max(1, 2))   # 2  —— 内置的 max

    max = min          # 把全局名称 'max' 绑定到 min 函数上
    print(max(1, 2))   # 1  —— 'max' 现在先找到我们的全局，而不是内置！

    del max            # 删掉我们的全局；内置又变得可达了
    print(max(1, 2))   # 2
    ```

???+ warning "易错点：别拿内置的名字给东西命名"
    人们很容易顺手用 `list`、`dict`、`sum`、`max`、`id`、`type` 或 `str` 当变量名——
    而你一这么做，就在这个作用域余下的部分里失去了那个内置。症状令人摸不着头脑：
    `list(...)` 突然抛出 `TypeError: 'list' object is not callable`，因为 `list` 现在
    是你的数据、不再是那个类型。换个别的名字吧（`items`、`total`、`kind`、`text`）。

## 6. 在函数里赋值：默认就是局部

这条规则能解释大多数作用域上的意外：**在一个函数里的任何地方给一个名称赋值，都会让那个名称在整个函数里都是局部的**——哪怕存在一个同名的全局，哪怕是在赋值*之前*的行上。*读取*一个名称没问题（LEGB 会向外走、找到那个全局）；但你一旦*赋值*，就等于声明了一个局部。

所以从函数内部读取一个全局，照样能行。

???+ example "示例：读取一个全局"
    ```python
    counter = 0

    def show():
        print(counter)   # 读取那个全局 —— 打印 0

    show()
    ```

但*给*同一个名称*赋值*，会让它在整个函数里都是局部的——如果你又先读了它，就会冒出一个著名的错误。

???+ warning "易错点：`UnboundLocalError`"
    ```python
    counter = 0

    def bump():
        counter = counter + 1   # UnboundLocalError
        return counter

    # bump()
    ```

    因为 `counter` 在 `bump` 内部被赋值，它在*整个*函数里都是局部的——于是右边的
    `counter + 1` 读到的是一个还没有值的局部。Python 在这里*不会*回退到那个全局。
    修法是把你的意图说明白：用 `global` 或 `nonlocal`。

要从函数内部重新绑定一个**全局**，用 `global` 声明它。要重新绑定一个**外层**函数里的名称，用 `nonlocal` 声明它。

???+ example "示例：global 与 nonlocal"
    ```python
    total = 0
    def add(n):
        global total            # 'total' 指模块层那个名称
        total += n
    add(3); add(4)
    print(total)                # 7

    def outer():
        message = "before"
        def inner():
            nonlocal message    # 'message' 指 outer 的那个局部
            message = "after"
        inner()
        print(message)          # after
    outer()
    ```

???+ warning "易错点：优先用 `return`，而不是 `global`"
    `global` 能用，但一个悄悄改写模块层变量的函数难以跟踪、也容易出错。更清楚的习惯
    是**把值作为实参传进来、用 `return` 把结果交回去**，让每个函数自成一体。把
    `global`/`nonlocal` 留给少数真正需要共享、可变状态的情形。

## 7. 到底为什么要有作用域？

??? info "深入了解：作用域给你带来了什么"
    作用域不是繁文缛节——它们物有所值。**封装：** 因为一个函数的局部名称在外面看不见，
    你可以在每个函数里重复使用 `i`、`x`、`result` 这样朴素的名字而不必担心撞车。
    **信息隐藏：** 一个函数的内部名称保持私有，于是调用者只依赖它返回什么，而不依赖它
    怎么干。**回收内存：** 因为局部命名空间在调用返回时消失，那些只被它引用过的对象
    失去了最后一个引用，可以立刻被释放——也就是我们在 2.1 提过的引用计数清理。小而
    作用域清楚的函数之所以更易读、易测、易推理，正是因为它们的名称漏不出去。

## 小结

Python 通过一摞命名空间来解析每一个光秃秃的名字：

| 命名空间 | 适用范围 | 查看方式 | 生命期 |
|---------|---------|---------|--------|
| **局部** | 某一次正在运行的调用内部 | `locals()` | 那次调用 |
| **外层** | 嵌套函数内部 | — | 外层调用运行期间 |
| **全局** | 整个模块 | `globals()` | 整个程序 |
| **内置** | 处处（除非被遮蔽） | `dir(builtins)` | 整个程序 |

一个名字按 **L → E → G → B** 查找，在第一个匹配处停下（或抛 `NameError`）。**赋值**会让一个名称在整个函数里都是局部的，所以只有当你真的想重新绑定一个外层名称时，才动用 `global` 或 `nonlocal`——否则更推荐传入实参、返回结果。遮蔽你自己的名字没问题，但遮蔽内置则很危险。

接下来，**2.3 函数是一等对象** 会把我们刚刚倚靠的嵌套函数推上主舞台：把函数作为实参传入、把它们返回，以及那让内层函数记住其外层作用域的闭包。
