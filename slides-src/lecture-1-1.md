---
title: "Lecture 1.1 · Python Basics"
description: "Names, objects, types, sequences, and slices — Python and Big Data in Economics."
lang: en
source: resource/deck1_1_AoL.pptx
sections:
  - id: introduction
    title: Introduction
    start: 1
    level: 1
    textbook: objects-overview
  - id: learning-goals
    title: Learning goals
    start: 2
    level: 2
    textbook: objects-introduction
  - id: variables
    title: Variables and objects
    start: 3
    level: 1
    textbook: objects-identity
  - id: object-structure
    title: Object structure and memory
    start: 7
    level: 2
    textbook: objects-identity
  - id: types
    title: Types
    start: 10
    level: 1
    textbook: numbers
  - id: boolean
    title: Boolean and isinstance
    start: 11
    level: 2
    textbook: numbers
  - id: containers
    title: Containers
    start: 13
    level: 2
    textbook: type-organisation
  - id: sequences
    title: Lists and tuples
    start: 14
    level: 1
    textbook: sequences
  - id: methods
    title: Methods
    start: 16
    level: 2
    textbook: sequences
  - id: mutability
    title: Mutability and identity
    start: 17
    level: 2
    textbook: mutability
  - id: slicing
    title: Slicing
    start: 19
    level: 1
    textbook: slicing
  - id: slice-objects
    title: Slice objects
    start: 20
    level: 2
    textbook: slicing
  - id: slice-practice
    title: Slicing practice
    start: 21
    level: 2
    textbook: slicing
  - id: other-sequences
    title: Other sequences
    start: 22
    level: 1
    textbook: sequences
    related: true
  - id: review
    title: Review
    start: 23
    level: 1
    textbook: objects-summary
---

<!-- slide: title-slide -->
<p class="eyebrow">Lecture 1.1</p>

# Python and Big Data<br>in Economics

## Chapter 1 · Basics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

## What you will learn

- Very elementary Python theory
- Some building blocks
- Some functions
    - Memorize the names
    - Know the meaning of their parameters
    - Understand and interpret the output

<div class="callout" markdown="1">
If a program is a **building**, variables are the **blocks**, and syntax tells us how to put the blocks together to form walls. Different programs are different ways to put the walls together.
</div>

---

<!-- slide: dense -->
## 1. The boring ⚠ variables

<div class="columns" markdown="1">
<div class="column" markdown="1">

### From counting to abstraction

Programming puts mathematical ideas into practice. You have already encountered **abstraction** in mathematics.

In primary school, we counted **1, 2, 3, …**. In middle school, we used <var>x</var> to represent a generic number.

So <var>x</var> = 1, <var>x</var> = 2, or <var>x</var> = 100 does not surprise us: a single letter <var>x</var> can be versatile.

</div>
<div class="column" markdown="1">

### From names to memory

In Python, <var>x</var> is a **name**. We want a variable to represent a value.

Python stores that value in an object in memory, then **binds the name to the object**. An existing object can also be reused.

[See the original explanatory video →](https://www.bilibili.com/video/BV1os421A7nd)

</div>
</div>

---

## 1. Variables

<p class="caption">Quick verification · names and object identity</p>

```python
# quick verification
a = 1
print(id(a))
b = a
print(id(b))

# not appearing as an address? format it
print(f"{id(b):02X}")
```

---

## 1. Variables
<p class="aol">AoL 2 (H)</p>

In the previous chunk of code, we saw:

1. **`print`** — displays the supplied content.
2. **`id`** — returns an object's identity. In CPython, this is its memory address.
3. **f-strings** — format text using `f"..."` and `{...}`.

---

<!-- slide: exercise-slide -->
## 1. Variables
<p class="aol">AoL 3 (M)</p>

<div class="exercise" markdown="1">
### In-class exercise 1.1

1. Create a name–value pair to store the name of a person: `"Alice"`.
2. Print Alice's `name`.
3. Bind the variable to `"Bob"`.
4. Use an f-string to print the contents of `name`.
</div>

---

<!-- slide: diagram-slide -->
## 1.1 “Names refer to objects”

- “Everything in Python is an object.”
- For now, think of objects as chunks of memory with specific structures.

<figure class="diagram">
  <img src="images/objects.png" width="835" height="504" alt="Original diagram: names a, b, and c point to separate objects in memory, each with its own structure.">
</figure>

<p class="caption"><a href="https://peps.python.org/pep-0008/#naming-conventions">Python naming conventions</a></p>

---

<!-- slide: exercise-slide -->
## 1.1 “Names refer to objects”
<p class="aol">AoL 3 (M)</p>

What is special about an object?

<div class="exercise" markdown="1">
### In-class exercise 1.1.1

Can you summarize some features of an object?

**Hint:** We have learned that everything is an object. What do they have in common?
</div>

An object comprises …

---

<!-- slide: diagram-slide -->
## 1.1 “Names refer to objects”
<p class="aol">AoL 2 (H)</p>

- An object's **memory layout** describes how its contents are arranged in memory.
- This arrangement tells us how the chunk of memory stores the data.

<figure class="diagram memory-layout">
  <img src="images/memory-layout.png" width="707" height="295" alt="Original memory-layout diagram: the name b refers to an object with an address, a type, and a value.">
</figure>

```python
import sys
sys.getsizeof(a)
```

---

## 1.2 Objects’ types
<p class="aol">AoL 2 (H)</p>

Types are a large topic: [Python's built-in types documentation](https://docs.python.org/3/library/stdtypes.html) is long. Let's start with a few examples.

```python
a = 1
b = 2.0
c = 3.14 - 5j
cond = True
```

<div class="exercise" markdown="1">
### In-class exercise 1.2.1

Use the `type` function to find the type of each object.
</div>

---

## 1.2.1 Simple types — Boolean

The Boolean type is special in Python. Let's investigate.

We need a new function, **`isinstance`**, to determine whether an object is an instance of a type.

<div class="columns" markdown="1">
<div class="column" markdown="1">

### Start here

```python
a = 1
isinstance(a, int)
isinstance(a, type(a))
```

</div>
<div class="column" markdown="1">

### Now, please try

```python
cond = True
isinstance(cond, int)
print(cond + 1)
```

</div>
</div>

---

<!-- slide: exercise-slide -->
## 1.2.1 Simple types — Boolean
<p class="aol">AoL 3 (M)</p>

<div class="exercise" markdown="1">
### In-class exercise 1.2.1.1

1. If `True` in Python is also `1`, what about `False`?
2. Try other types with `isinstance`. Do you find anything interesting?
3. Search the web for the documentation of `isinstance` and read it.
</div>

---

## 1.2.2 Complex types

- Our previous examples held individual values. In Python, we can also put several values together in a container.
- In school mathematics, **1** is a number, **2** is a number, and **{1, 2}** is a set.
- Python has **sequences**, **mappings**, **strings**, and other types that bring values together.

---

## 1.2.2 Sequences — list & tuple
<p class="aol">AoL 3 (M)</p>

**Lists** and **tuples** are frequently encountered. Here, we create them by enumerating their elements:

```python
l = [1, 2, 3]
t = (1, 2, 3)
```

<div class="exercise" markdown="1">
### In-class exercise 1.2.2.1

1. Try to print a list.
2. Try to print one element of a list.
3. Create a list containing 100 numbers, from 1 to 100.
</div>

---

<!-- slide: exercise-slide -->
## 1.2.2 Sequences — list & tuple
<p class="aol">AoL 3 (M)</p>

<div class="exercise" markdown="1">
### In-class exercise 1.2.2.2

1. Try to print a tuple.
2. Try to print one element of a tuple.
3. Create a tuple containing 100 numbers, from 1 to 100.
</div>

---

## 1.2.2 Sequences — list & tuple

### List functions and tuple functions

- Lists and tuples have operations designed for their types.
- A function accessed through a particular object is called a **method**.
- Some methods change the object; others do not. Check each method's behavior.

### Operations to investigate

- `append` vs. `extend`
- `pop`
- The `+` operator

---

<!-- slide: exercise-slide -->
## 1.2.2 Sequences — list & tuple
<p class="aol">AoL 3 (M)</p>

You know how to get an element from a list or a tuple. Now let's try to **set** an element's value.

<div class="exercise" markdown="1">
### In-class exercise 1.2.2.3

1. Use `l` and `t` that you just created.
2. Set the second element of `l` to `-1`.
3. Set the second element of `t` to `-1`.
4. Analyze the changes in the memory layout.
</div>

---

<!-- slide: comparison-slide -->
## 1.2.2 Sequences — list & tuple

<p class="caption">Similarities and comparisons · each column starts afresh. “OK” means a valid operation, not a True result.</p>

<div class="comparison-grid" markdown="1">
<div class="column" markdown="1">

### Access & membership

```python
l = [1, 2, 3]
t = (4, 5, 6)

print(l[1])  # OK
print(t[2])  # OK

l[1] = "list"  # OK
t[2] = "tuple" # TypeError

1 in l  # OK
2 in t  # OK; False

# Both are sequences.
```

</div>
<div class="column" markdown="1">

### Assignment & deletion

```python
l = [1, 2, 3]
t = (4, 5, 6)

l[0] = 1  # OK
t[0] = 1  # TypeError

del l[1]  # OK
del t[1]  # TypeError
```

</div>
<div class="column" markdown="1">

### Methods

```python
l = [1, 2, 3]
t = (4, 5, 6)

l.append(4)    # OK
l.reverse()    # OK
l.extend((5,)) # OK
l.pop(0)       # OK

# AttributeError:
t.append()
t.reverse()
t.extend()
t.pop()
```

</div>
<div class="column" markdown="1">

### In-place addition

```python
l = [1, 2, 3]
t = (4, 5, 6)

l += [6, 7]
# Same id as before.

t += (8,)
# id changes.
```

</div>
</div>

<p class="caption">Try the statements individually in your notebook: an intentional error stops a cell.</p>

---

<!-- slide: diagram-slide slice-slide -->
## 1.2.2.1 Slices
<p class="aol">AoL 2 (H)</p>

We can take one element from a list — or many elements, using a **slice**.

The notation is `start:stop[:step]`.

<div class="columns" markdown="1">
<div class="column">
<figure class="diagram slice-notation">
  <img src="images/slice-notation.png" width="664" height="270" alt="Original slice grammar diagram: literal colons are marked green, chosen start/stop/step values red, and the optional step part blue.">
</figure>
</div>
<div class="column" markdown="1">

- **Colons:** must appear as written.
- **Start, stop, step:** numbers you choose.
- **Square brackets in this grammar:** mark an optional part. If included, it follows the same rules.

</div>
</div>

---

## 1.2.2.1 Slices

### Slice objects

- Create a slice object with `slice(start, stop, step)`.
- Use it in square brackets: `l[s]`. Colon notation such as `l[1:10:2]` also creates a slice.

```python
s = slice(1, 10, 2)
l[s]
```

<div class="exercise" markdown="1">
### In-class exercise 1.2.2.4

1. Is `slice` a function?
2. Is `l` a function?
</div>

---

<!-- slide: exercise-slide -->
## 1.2.2.1 Slices
<p class="aol">AoL 3 (M)</p>

<div class="exercise" markdown="1">
### In-class exercise 1.2.2.5

Are these slices?

<ol class="slice-examples">
  <li><code>1:2:1</code></li>
  <li><code>2:4:7</code></li>
  <li><code>9:1:-1</code></li>
  <li><code>a:b:c</code></li>
  <li><code>1.5:2.3:3.14</code></li>
  <li><code>a:2:3</code></li>
  <li><code>6:7</code></li>
  <li><code>:-5:-1</code></li>
  <li><code>::-1</code></li>
</ol>
</div>

---

## 1.2.2 Sequences — array & deque

These are also sequence types. We will not cover them in detail, but …

- An **array** is list-like, but its elements are restricted to a type specified by a type code.
- Arrays store basic values compactly. Performance depends on the operation; an array is not always faster than a list.
- Import `array` before using it.
- Explore [the documentation for `deque`](https://docs.python.org/3/library/collections.html#collections.deque).

There are too many functions and methods to cover in class. You have learned the **“how to.”**

---

<!-- slide: diagram-slide review-slide -->
## Review
<p class="aol">AoL 5 (H)</p>

- Python **names refer to objects**.
- Objects have an **identity**, a **type**, and a **value**.
- Basic types include **Boolean**, **sequences**, and more.

<figure class="diagram review-meme">
  <img src="images/review-meme.jpg" alt="The original end-of-lecture meme: two confused characters ask who killed whom.">
</figure>
