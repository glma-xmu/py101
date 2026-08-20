# 5. Object-Oriented Python

```motto
`@property` is not a feature. It is one instance of a protocol you can implement yourself.
```

## Introduction

Day two opens with the part of Python most people use without ever looking inside. You have written `class MyNet(torch.nn.Module)`, you have decorated something with `@property`, and both worked. This chapter is about what was actually happening — and it pays off immediately, because once you can see the machinery you can design with it instead of around it.

§5.1 is the anatomy of a class: what attributes and methods really are, how the underscore conventions differ (one is a promise, two is enforced), and why `__call__` makes the boundary between "function" and "object" disappear. §5.2 shows that `@property` is a special case of the **descriptor protocol**, and that knowing the general case lets you write things `@property` cannot. §5.3 is inheritance, `super()`, abstract base classes, and the method resolution order — including why multiple inheritance is a loaded weapon.

## 5.1 Members

The **members** of a class are its attributes and its methods. Attributes are like variables; methods are functions that live inside. Both are entries in the class's namespace, which — as in [§3.1.2](camp_ch3_names.md#312-namespaces) — is a dictionary you can print.

### 5.1.1 Naming conventions: private names and name mangling

Python **encourages** a single leading underscore to mark a name as private, and **enforces** a double leading underscore in a way that surprises people.

The single underscore is a convention with no teeth: `_cache` means "this is mine, do not touch", and Python does nothing at all to stop you. The double underscore is different. When you bind a name beginning with two underscores and *not* ending in two — inside a class body — the compiler rewrites it to `_ClassName__name`. That rewriting is called **name mangling**, and it happens at compile time, everywhere inside the class body.

???+ example "Example 5.1: name mangling in action"
    ```python
    class Student:
        def __init__(self, name):
            self.__name = name        # compiled as self._Student__name

    s1 = Student("Santhosh")
    s1.__name = "see"                 # OUTSIDE the class: no mangling, a NEW attribute
    s1.age = 20

    print(s1.__name)                  # 'see'         -- the one you just made
    print(s1._Student__name)          # 'Santhosh'    -- the one __init__ set
    print(s1.age)                     # 20
    print(sorted(vars(s1)))           # both are sitting there in the instance dict
    ```

The last line is the punchline: the instance has *two* attributes that look like the same name. Mangling only applies inside the class body, so the assignment on line 6 — written outside — created a plain new attribute called `__name`.

???+ warning "Pitfall: mangling is not privacy"
    `_Student__name` is entirely accessible, so double underscores do not protect data.
    Their real purpose is **avoiding collisions in subclasses**: if a base class stores
    `self.__state` and a subclass also stores `self.__state`, mangling keeps them apart.
    Use a single underscore for "internal"; reserve the double one for the collision
    problem it was designed to solve.

**Class attributes store data shared by every instance.** An attribute bound in the class body — not in `__init__` — belongs to the *class*, and every instance sees the same object. Which is exactly as dangerous as it sounds when the object is mutable.

???+ example "Example 5.2: one object, every instance"
    ```python
    class ML:
        data = {'x': [0, 1, 2, 3, 4],
                'y': [1, 2, 3, 4, 5]}       # a CLASS attribute

        def __init__(self, method):
            self.method = method            # an INSTANCE attribute

        def run(self):
            print(f'{self.method}: x={self.data["x"]}  id={id(self.data)}')

    pca = ML('PCA')
    rf = ML('RF')
    pca.run()
    rf.run()                                # same id -- literally one dictionary

    rf.data['x'][0] = -1                    # mutate through one instance...
    pca.run()                               # ...and every instance sees it
    ```

Reading a class attribute through `self` works, and it reads well, but it hides which kind of attribute you are touching. `type(self).data` says "class attribute" out loud. And note the asymmetry from [§3.3.2](camp_ch3_names.md#332-assignment-statements): `rf.data['x'][0] = -1` *mutates* the shared dictionary, while `rf.data = {}` would create an instance attribute that shadows the class one for `rf` alone. Same object, two very different statements.

### 5.1.2 Instance, class, and static methods

Three kinds of method live in a class body, and they differ in what they receive.

An **instance method** is bound to an instance; the instance is the caller and arrives as the first parameter, `self`. A **static method** receives nothing automatic at all — it is a plain function that happens to live in the class's namespace, and either a class or an instance may call it. A **class method** receives the *class* as its first parameter, `cls`, which is what makes it work correctly under inheritance.

Start with a `Student` class that records scores. Turning a score into a letter grade does not depend on any particular student, so it is a natural static method.

???+ example "Example 5.10: a static method that needs no instance"
    ```python
    class Student:
        def __init__(self):
            self.score = []

        def score_input(self, value):        # instance method: needs self
            self.score.append(value)

        @staticmethod
        def grade(value):                    # static: needs nothing
            if 0 <= value < 60:
                return "fail"
            elif 60 <= value < 90:
                return "pass"
            else:
                return "great"

    s = Student()
    s.score_input(85)
    print(s.score, Student.grade(85), s.grade(42))   # class or instance may call it
    ```

Now suppose you need a class specifically for first-year students, keeping the structure of the general `Student`. In practice you would read the records from a spreadsheet and build one instance per row:

| | A | B |
|---|---|---|
| **1** | name | grade |
| **2** | Alice | [60, 70, 90] |
| **3** | Bob | [60, 70, 90] |
| **4** | … | |

A static method could do the reading. Watch what it returns.

???+ example "Example 5.11: why `@staticmethod` is the wrong tool here"
    ```python
    class Student:
        def __init__(self):
            self.score = []

        @staticmethod
        def read(name, score):
            s = Student()            # hard-wired to Student
            s.name, s.score = name, score
            return s

        @classmethod
        def read_cls(cls, name, score):
            s = cls()                # whatever class this was called on
            s.name, s.score = name, score
            return s

    class FirstYear(Student):
        def orientation_done(self):
            return True

    a = FirstYear.read("Alice", [60, 70, 90])
    b = FirstYear.read_cls("Bob", [60, 70, 90])

    print(type(a).__name__, type(b).__name__)   # Student  FirstYear
    print(b.orientation_done())                 # fine
    try:
        a.orientation_done()                    # 'a' is a plain Student
    except AttributeError as e:
        print("AttributeError:", e)
    ```

That last line is the point. `FirstYear.read(...)` gave back a plain `Student`, so the methods you defined on `FirstYear` are not there. `@classmethod` receives the class the call was made on and builds *that*, which is why alternative constructors — `dict.fromkeys`, `pd.DataFrame.from_records`, `datetime.fromtimestamp` — are class methods without exception.

???+ note "Key concept: which decorator when"
    | | First parameter | Use it for |
    |---|---|---|
    | instance method | `self` | anything that acts on one object's data |
    | `@classmethod` | `cls` | alternative constructors, anything that must respect subclassing |
    | `@staticmethod` | *(nothing)* | a helper that belongs to the class by topic only |

### 5.1.3 Special methods: `__call__()` and `__new__()`

**The `__call__` method.** An object is **callable** when `obj()` or `obj(*args, **kwargs)` means something. Functions are callable, classes are callable, and so are instances of any class that defines `__call__`. There is no separate category of "function" in the way you might assume — being callable is just implementing one method.

Names surrounded by double underscores are **special methods** (dunders): Python calls them for you in response to syntax. `obj()` invokes `type(obj).__call__`.

???+ example "Example 5.3: what makes something callable"
    ```python
    def func():
        pass

    print('__call__' in dir(func))     # True -- even a plain function has one

    class A:
        def __call__(self):            # note the self
            print("called from A")

    a = A()
    a()                                # invokes A.__call__(a)
    print(callable(a), callable(A), callable(func))
    ```

We can put that to work. Suppose you want to count how many times something is called — state that has to live *between* calls. A function cannot easily hold state; an instance can, in an attribute.

???+ example "Example 5.4: an instance that counts its own calls"
    ```python
    class Counter:
        def __init__(self, func=None):
            self.func = func           # optional: something to wrap
            self.count = 0

        def __call__(self, *args, **kwargs):
            self.count += 1
            if self.func is not None:
                return self.func(*args, **kwargs)

    c1 = Counter()
    c2 = Counter()
    print(c1.count, c2.count)          # 0 0 -- separate instances, separate state
    c1()
    c1()
    print(c1.count, c2.count)          # 2 0
    ```

Do not confuse `__init__` with `__call__`. A simple way to keep them apart: `__init__` runs when the instance is being *created* — the class is on the right of the `=` — and `__call__` runs when an existing instance is *used* with parentheses.

**Classes as decorators.** Now recall from [§4.4](camp_ch4_functions.md#44-decorators) that `@decor` means nothing more than `func = decor(func)`. Nothing in that requires `decor` to be a function — it only has to be *callable*. So any callable object can be a decorator, including a class.

???+ example "Example 5.5: `Counter` as a decorator"
    ```python
    class Counter:
        def __init__(self, func=None):
            self.func = func
            self.count = 0

        def __call__(self, *args, **kwargs):
            self.count += 1
            if self.func is not None:
                return self.func(*args, **kwargs)

    @Counter                    # timed_func = Counter(timed_func)
    def timed_func(x):
        return x * 2

    print(timed_func(3))        # 6  -- the call is forwarded
    print(timed_func(4))        # 8
    print(timed_func.count)     # 2  -- state kept on the instance
    print(type(timed_func))     # <class '__main__.Counter'>, not a function!
    ```

The last line is worth noticing: `timed_func` is no longer a function at all. That is the cost of this pattern — it is why `functools.wraps` exists for the function form, and why a class-based decorator needs care before you put it on a method.

??? info "Deep dive: `__new__`, the step before `__init__`"
    `__init__` does not create the instance; it *initialises* one that already exists.
    The creation is `__new__`, a static method that runs first and returns the new
    object. You rarely need it — except when subclassing an immutable type (there is
    no object to mutate in `__init__`), or when controlling instance creation itself:

    ```python
    class Singleton:
        _instance = None

        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    print(Singleton() is Singleton())   # True -- one object, always
    ```

    This is the singleton pattern the course mentioned in passing as a way to keep one
    shared copy of expensive data. Note the trap: `__init__` still runs on *every*
    call, on the same object, so any initialisation there is repeated.

## 5.2 Descriptors and the myths of `@property`

### 5.2.1 Introduction

You have almost certainly used `@property`. Start from the problem it solves. Here is a class recording the temperature of a day, with nothing guarding it:

???+ example "Example 5.6: an attribute anyone can set to anything"
    ```python
    class Weather:
        def __init__(self, temp):
            self.temp = temp

    w1 = Weather(-300)
    print(f"today's temperature is {w1.temp} degrees")   # below absolute zero
    ```

Nothing stops `-300`, which is colder than physically possible. We want assignment to `temperature` to run a check — that is, we want an attribute with *methods bound to it*. `property` does that, and it is illuminating to write it in its original, undecorated form, because the decorator syntax hides what is going on.

???+ example "Example 5.7: `property` without the decorator"
    ```python
    class Weather:
        def getter(self):
            try:
                return self.z
            except AttributeError:
                print("temperature not set")

        def setter(self, y):
            print("entering setter")
            if y > -275:
                self.z = y
            else:
                raise ValueError("too low")

        temperature = property(getter, setter)   # <- a CLASS attribute

    w = Weather()
    print(w.temperature)      # 'temperature not set' then None
    w.temperature = 20        # runs setter
    print(w.temperature)      # 20
    try:
        w.temperature = -300
    except ValueError as e:
        print("rejected:", e)
    ```

Look at where `temperature` lives: it is a **class attribute** bound to a `property` object. Reading `w.temperature` does not find an instance attribute of that name at all — it finds the class attribute, notices it is a `property`, and calls `getter`. The `@property` decorator you normally write produces exactly this, one method at a time.

So `@property` turns an attribute into an attribute-with-methods. The **myth** is that this is a feature of its own. It is one instance of a much wider mechanism: the **descriptor protocol**. A descriptor is any object implementing one or more of

- `__get__(self, instance, owner)`
- `__set__(self, instance, value)`
- `__delete__(self, instance)`

and `property` is simply a class that implements all three. Descriptors are how methods themselves become bound to instances, how `classmethod` and `staticmethod` work, and how `django` and `SQLAlchemy` model fields.

A descriptor is used by assigning an *instance of it* as a class attribute:

???+ example "Example 5.8: the smallest possible descriptor"
    ```python
    import time

    class TimeDesc:
        def __get__(self, instance, owner=None):
            return time.time()          # computed fresh on every access

    class UseCase:
        size = TimeDesc()               # an instance of the descriptor

    u = UseCase()
    print(u.size)
    print(u.size)                       # a different number: __get__ ran again
    print(UseCase.size)                 # works on the class too (instance is None)
    ```

`size` looks like a plain attribute at the call site and is in fact a method call. Now let us rewrite [Example 5.7](#521-introduction) in descriptor style — same behaviour, but the validation logic is now a reusable object rather than something welded into `Weather`.

???+ example "Example 5.9: the temperature check as a descriptor"
    ```python
    class TempDesc:
        def __get__(self, instance, owner=None):
            try:
                return instance.z
            except AttributeError:
                print("haven't set temperature.")

        def __set__(self, instance, value):
            if value > -273:
                instance.z = value
            else:
                print("not allowed.")

    class NewTemp:
        temperature = TempDesc()

    n = NewTemp()
    print(n.temperature)     # haven't set temperature. -> None
    n.temperature = 25
    print(n.temperature)     # 25
    n.temperature = -300     # not allowed.
    print(n.temperature)     # still 25
    ```

After all that effort, why bother? Because `TempDesc` can now be attached to *any* class, as many times as you like, while a `@property` is written once for one attribute of one class.

The other reason is the **lazy property**: a value expensive enough that you want it computed at most once, then cached. Every run of a machine-learning routine can take a long time, and recomputing a result you already have is pure waste.

???+ example "Example 5.10: a lazy property ([source](https://realpython.com/python-descriptors/#how-to-use-python-descriptors-properly))"
    ```python
    import time

    class LazyProperty:
        def __init__(self, function):
            self.function = function
            self.name = function.__name__

        def __get__(self, obj, type=None):
            print("(computing...)")
            value = self.function(obj)
            obj.__dict__[self.name] = value   # <- the trick
            return value

    class DeepThought:
        @LazyProperty
        def meaning_of_life(self):
            time.sleep(0.5)                   # pretend this is expensive
            return 42

    d = DeepThought()
    print(d.meaning_of_life)   # (computing...) 42   -- slow, once
    print(d.meaning_of_life)   # 42                  -- instant, no message
    print(d.__dict__)          # the cached value now lives on the instance
    ```

The trick is in one line. `LazyProperty` defines `__get__` but **not** `__set__`, which makes it a *non-data* descriptor — and for those, an instance attribute of the same name wins. So writing the result into `obj.__dict__` means every later access finds the plain instance attribute first and the descriptor is never consulted again. (The standard library ships this as `functools.cached_property`; now you know how it works.)

???+ note "Key concept: data and non-data descriptors"
    A **data descriptor** defines `__set__` (or `__delete__`) and takes precedence over
    the instance dictionary. A **non-data descriptor** defines only `__get__` and yields
    to it. That single rule explains both why you cannot shadow a `@property` by
    assigning to the instance, and why `cached_property` can cache itself away.

### 5.2.2 An example

Now combine what we have. Imagine a class that needs a decorator defined *inside* it — a timer applied to one of its own methods. The pieces are all here: a decorator is a callable applied at definition time, and a `staticmethod` is a plain function living in the class namespace.

???+ example "Example 5.12: a decorator defined inside its own class"
    ```python
    import time

    class Example:
        def __init__(self, ML):
            self.ML = ML

        @staticmethod
        def decor(func):
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)      # remember to return this
                print(f"elapsed: {time.perf_counter() - start:.4f}s")
                return result
            return wrapper

        @decor                       # 'decor' is a name in the class body being built
        def run(self):
            print(f'calling {self.ML}')
            return 0

    print(Example('PCA').run())
    ```

Two subtleties make this work. First, `@decor` is resolved while the class body is still executing, so `decor` is an ordinary name in that namespace — no `self`, no `Example.` prefix, and it must be defined *above* `run`. Second, `decor` at that moment is a `staticmethod` **object**, not a function; calling one directly only became legal in Python 3.10. On 3.9 and earlier this raises `TypeError: 'staticmethod' object is not callable`, and the workaround was to define the decorator outside the class.

💡 **Can you think of other ways?** Defining `decor` at module level is the simplest and usually the right answer. Making it a `classmethod` does not work — the same callability problem, unsolved. And `functools.wraps` should be inside `wrapper`'s definition here too; it was left out only to keep the example minimal.

## 5.3 Inheritance

Inheritance is the feature you have already used — `class MyNet(torch.nn.Module)` — so we will review the basics quickly and spend the time on `super()`, abstract base classes, and multiple inheritance, which is where the real decisions are.

Consider implementing a family of machine-learning methods: neural networks (DNN, CNN, RNN), tree-based models (boosting, random forests), correlation-based models (PCA, PLS), and penalised regressions (lasso, ridge). You have to organise all of it, and the organising is worth doing *before* you write the first line.

One way in is bottom-up: look for what the algorithms have in common and group them. What is left is a set of detailed implementations that differ only where they must. Something like this:

<div style="text-align:center;margin:1.3rem 0;">
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg" role="img" width="700" style="max-width:100%;height:auto;font-family:-apple-system,Segoe UI,Roboto,sans-serif;">
  <title>A three-level class hierarchy rooted at MLClass</title>
  <desc>MLClass sits at the top. Four subclasses inherit from it: NeuralNets, TreeModels, CorrModels and RegModels. Each of those has one concrete subclass beneath it: DNN, Boosting, PCA and Lasso respectively.</desc>
  <g stroke="#306998" stroke-width="1.6" fill="none">
    <path d="M360,106 L360,128"/>
    <path d="M120,128 L620,128"/>
    <path d="M120,128 L120,150"/>
    <path d="M290,128 L290,150"/>
    <path d="M450,128 L450,150"/>
    <path d="M620,128 L620,150"/>
    <path d="M120,190 L120,236"/>
    <path d="M290,190 L290,236"/>
    <path d="M450,190 L450,236"/>
    <path d="M620,190 L620,236"/>
  </g>
  <g fill="none" stroke="#306998" stroke-width="1.8">
    <rect x="290" y="66" width="140" height="40" rx="7"/>
    <rect x="55" y="150" width="130" height="40" rx="7"/>
    <rect x="225" y="150" width="130" height="40" rx="7"/>
    <rect x="385" y="150" width="130" height="40" rx="7"/>
    <rect x="555" y="150" width="130" height="40" rx="7"/>
    <rect x="60" y="236" width="120" height="38" rx="7"/>
    <rect x="230" y="236" width="120" height="38" rx="7"/>
    <rect x="390" y="236" width="120" height="38" rx="7"/>
    <rect x="560" y="236" width="120" height="38" rx="7"/>
  </g>
  <g fill="var(--md-default-fg-color, #111)" font-size="15" text-anchor="middle">
    <text x="360" y="92" font-weight="700">MLClass</text>
    <text x="120" y="176">NeuralNets</text>
    <text x="290" y="176">TreeModels</text>
    <text x="450" y="176">CorrModels</text>
    <text x="620" y="176">RegModels</text>
    <text x="120" y="261">DNN</text>
    <text x="290" y="261">Boosting</text>
    <text x="450" y="261">PCA</text>
    <text x="620" y="261">Lasso</text>
  </g>
</svg>
</div>

Every one of these needs data, so that goes at the root:

```python
class MLClass:
    def __init__(self, data):
        self.data = data

    def build_model(self):
        pass
```

One level down, every neural network needs a forward step and a training method:

```python
class NeuralNet(MLClass):
    def __init__(self, data):
        super().__init__(data)

    def forward(self, x):
        pass

    def train_model(self, data, labels):
        pass
```

The drawback of writing it this way is that nothing stops you creating a `NeuralNet` directly — and if you do, `forward` and `train_model` silently do nothing at all, which is far worse than an error. §5.3.2 fixes that.

### 5.3.1 The `super()` instance

The documentation says `super()` returns a "proxy object", and that phrasing is exact. It is not the parent class, and it is not a cached thing — each call builds a fresh proxy that knows the instance and where in the MRO to continue looking.

???+ example "Example 5.12: what `super()` actually gives you"
    ```python
    class Parent:
        def __init__(self, x):
            print("Parent.__init__ on instance", id(self))
            self.x = x

        def pmethod(self):
            print("from parent class")

    class Child(Parent):
        def __init__(self, x, y):
            first = super()
            second = super()
            second.pmethod()
            print("two proxies, two objects:", id(first) != id(second))
            print("both bound to this instance:", id(self))
            first.__init__(x)          # the usual super().__init__(x)
            self.y = y

    child = Child(1, 2)
    child.pmethod()
    print(child.x, child.y)
    ```

The two proxies have different `id`s but do the same job, because what they carry is a *pair* — this instance, and the position in the MRO after `Child`. That is also why zero-argument `super()` only works inside a class body: the compiler quietly supplies both halves.

### 5.3.2 The **A**bstract **B**ase **C**lasses

An **abstract base class** specifies an API while refusing to be instantiated. That converts the silent failure above into an error at the earliest possible moment.

???+ example "Example: an ABC you cannot instantiate"
    ```python
    from abc import ABC, abstractmethod

    class NeuralNet(ABC):
        def __init__(self, data):
            self.data = data

        @abstractmethod
        def forward(self, x):
            """Every subclass must implement this."""

        def train_model(self, data, labels):
            print("shared training loop")

    try:
        NeuralNet([1, 2, 3])
    except TypeError as e:
        print("refused:", e)

    class DNN(NeuralNet):
        def forward(self, x):          # supplying the abstract method
            return x * 2

    d = DNN([1, 2, 3])
    print(d.forward(21), d.data)
    d.train_model(None, None)          # inherited, concrete
    ```

Note what the abstract method buys you: `NeuralNet` cannot be built, but `DNN` can, *because* it implements `forward`. Delete `DNN.forward` and the `DNN([1,2,3])` line fails too. The contract is checked at instantiation, not at import.

In real code the concrete classes then fill in the details, in the shape you already know:

```python
class DNN(NeuralNet):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
```

### 5.3.3 Multiple inheritance

Multiple inheritance lets a class derive from several parents at once: if you want behaviour from two places, combine them. The idea is simple; the execution has one requirement, and it is the requirement people miss.

When a name could come from several parents, Python picks using the **method resolution order** — a linearisation of the inheritance graph (🎨 **Time to draw!**), computed once per class and readable as `Cls.__mro__`. `super()` does not mean "my parent". It means "**the next class in the MRO** after this one", which depends on the class of the *instance*, not on where the code was written.

Here is the naive version, and why it breaks:

```python
class MLClass:
    def __init__(self, data):
        self.data = data

class NeuralNet(MLClass):
    def __init__(self, data):
        super().__init__(data)

class Predictor(MLClass):
    def __init__(self, data, model=""):
        super().__init__(data)
        self.model = model

class DNN(NeuralNet, Predictor):
    def __init__(self, data):
        super().__init__(data)

d1 = DNN(1, "model1")     # TypeError: DNN.__init__() takes 2 positional arguments
```

The MRO is `DNN → NeuralNet → Predictor → MLClass → object`, so `Predictor.__init__` *is* on the chain — but `DNN.__init__` accepts only `data` and passes only `data`, so `model` can never reach it. Drop the second argument and `DNN(1)` does construct, silently leaving `model` at `""`. Either way the chain is not through.

The fix is **cooperative** `super()`: every `__init__` accepts `**kwargs` and forwards what it does not consume.

???+ example "Example: multiple inheritance done cooperatively"
    ```python
    class MLClass:
        def __init__(self, data, **kwargs):
            super().__init__(**kwargs)        # keep the chain going
            self.data = data

    class NeuralNet(MLClass):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def forward(self, x):
            return x

    class Predictor(MLClass):
        def __init__(self, model="", **kwargs):
            super().__init__(**kwargs)
            self.model = model

        def pred(self, x):
            print(f"{self.model} predicts at {x}")

    class DNN(NeuralNet, Predictor):
        pass

    d1 = DNN(data=1, model="model1")
    print(d1.data, d1.model)
    d1.pred(0.5)
    print([c.__name__ for c in DNN.__mro__])
    ```

Three rules make this reliable, and breaking any one of them breaks the chain: every class in the hierarchy calls `super().__init__(...)`, every one accepts `**kwargs`, and callers pass **keyword** arguments. Note that `MLClass` calls `super().__init__(**kwargs)` even though its "parent" is `object` — because under a different subclass, the next class in the MRO may not be `object` at all. That is cooperation: no class knows who follows it.

???+ warning "Pitfall: reach for composition first"
    Multiple inheritance is the right tool for **mixins** — small classes adding one
    orthogonal behaviour, with no state and no `__init__`. For anything else, an
    object holding another object is easier to read, easier to test, and cannot
    produce an MRO error you have to draw a graph to understand.
    [This tutorial on inheritance versus composition](https://realpython.com/inheritance-composition-python/)
    is the fullest treatment.

## Misc

**1. Function or method?** The difference is smaller than it looks. A `def` inside a class body creates an ordinary function; what turns it into a *method* is the attribute lookup, which uses the descriptor protocol from §5.2 to bind the instance.

???+ example "Example 5.13: the same object, three ways"
    ```python
    class A:
        def func(self):
            pass

        print("inside the class body:", func)      # a plain function

    print("via the class:   ", A.func)             # still a plain function
    print("via an instance: ", A().func)           # a BOUND METHOD
    print(A().func.__func__ is A.func)             # True -- same function inside
    ```

`A.func` is a function; `A().func` is a bound method wrapping it, which is precisely how `self` gets supplied. `function.__get__` is a non-data descriptor, so this is the machinery of §5.2 doing everyday work.

**2. A useful decorator.** Closing the loop with [Example 4.8](camp_ch4_functions.md#44-decorators): the memoisation we hand-wrote is one line from the standard library.

???+ example "Example 5.14: `functools.cache` on the recursive `fibonacci`"
    ```python
    import functools, time

    @functools.cache                 # since 3.9; lru_cache(maxsize=None) before that
    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        return fibonacci(n - 1) + fibonacci(n - 2)

    start = time.perf_counter()
    print(fibonacci(100), f"in {time.perf_counter() - start:.5f}s")
    print(fibonacci.cache_info())
    ```

`fibonacci(100)` without the cache would take longer than the remaining life of the sun; with it, the answer is immediate and `cache_info()` shows exactly how many calls were served from memory.

## Summary

| | |
|---|---|
| **`_name` vs `__name`** | One underscore is a promise; two triggers name mangling to `_Class__name`, for collision-avoidance, not privacy. |
| **Class attributes are shared** | One object for every instance. Mutating it is visible everywhere; rebinding creates an instance attribute. |
| **`@classmethod` over `@staticmethod`** | For alternative constructors, `cls()` respects subclasses; a hard-wired class name does not. |
| **Callable is a protocol** | Anything implementing `__call__` — including an instance — can be called, and can be a decorator. |
| **`@property` is a descriptor** | `__get__`/`__set__`/`__delete__` is the general mechanism; `property` is one implementation of it. |
| **Data vs non-data descriptors** | With `__set__`, the descriptor wins over the instance dict; without it, the instance dict wins — which is how caching works. |
| **`super()` follows the MRO** | Not "the parent". Cooperative `super()` with `**kwargs` is what makes multiple inheritance survivable. |
| **ABCs fail early** | `@abstractmethod` turns a silently-broken instance into a `TypeError` at construction. |
