---
title: Lecture 1.2 · Collections and Control Flow
description: Dictionaries, strings, sets, loops, conditions, and comprehensions.
lang: en
source: ../course materials/deck1_2.pptx
sections:
- id: introduction
  title: Introduction
  start: 1
  level: 1
  textbook: ch1-2-collections-0
- id: dictionaries
  title: Dictionaries
  start: 3
  level: 1
  textbook: ch1-2-collections-4
- id: for-loops-and-range
  title: For loops and range
  start: 7
  level: 1
  textbook: ch1-3-control-flow-2
- id: conditional-execution
  title: Conditional execution
  start: 10
  level: 1
  textbook: ch1-3-control-flow-5
- id: comparisons-and-identity
  title: Comparisons and identity
  start: 12
  level: 1
  textbook: ch1-3-control-flow-6
- id: updating-dictionaries
  title: Updating dictionaries
  start: 15
  level: 1
  textbook: ch1-2-collections-4
- id: zip
  title: Zip
  start: 18
  level: 1
  textbook: ch1-4-iterators-2
- id: review-of-types
  title: Review of types
  start: 19
  level: 1
  textbook: type-organisation
- id: strings
  title: Strings
  start: 20
  level: 1
  textbook: ch1-1-objects-5
- id: sets
  title: Sets
  start: 22
  level: 1
  textbook: ch1-2-collections-3
- id: pythonic-style
  title: Pythonic style
  start: 25
  level: 1
  textbook: ch1-3-control-flow-8
- id: comprehensions
  title: Comprehensions
  start: 26
  level: 1
  textbook: ch1-3-control-flow-7
- id: mutability
  title: Mutability
  start: 28
  level: 1
  textbook: mutability
- id: further-reading-and-review
  title: Further reading and review
  start: 30
  level: 1
  textbook: ch1-2-collections-7
  related: true
---

<!-- slide: title-slide -->

<p class="eyebrow">Lecture 1.2</p>

# Collections and Control Flow

## Programming for AI (Python)

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2025</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">Very elementary Python theory</p>
<p class="">More building blocks and more functions</p>
<p class="">Control flow (for loop and if condition)</p>
<p class="">If we liken a program to a building, the variables are blocks and syntax tells the programmer how to put the blocks together to form walls. Different programs are just different ways to put the walls together.</p>




</div>

---

<!-- slide: lecture-import -->

## 1.2.3 Mapping — dictionary

<div class="lecture-content" markdown="1">

Lists and tuples select elements by **position**: `items[0]`, `items[1]`, and so on.

A dictionary selects a value by its **key**. Keys can be strings or other hashable objects; they are not restricted to names.

The dictionary stores **key–value pairs**.

</div>

---

<!-- slide: lecture-import -->

## 1.2.3 Mapping — dictionary

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 1.2.3.1 ways to create a dictionary</strong></p>

```python
age = {"Alice": 21,
       "Bob": 32,
       "Charlie": 44}
name = dict(stu1="Alice",
            stu2="Bob",
            stu3="Charlie")
grade = dict([['stu1', 87],
              ['stu2', 99],
              ['stu3', 65]])
dict.fromkeys(["key1", "key2"], ...)
```


</div>

---

<!-- slide: lecture-import -->

## 1.2.3 Mapping — dictionary

<div class="lecture-content" markdown="1">

Dictionary entries consist of **keys** and **values**. Look up a value by passing its key, as in `age["Alice"]`.

If the key is absent, subscription raises `KeyError`. The `get()` method instead returns a default value (`None` unless you supply another value).

### In-class exercise 1.2.3.1

What are the keys and values in the three dictionaries on the previous slide?

</div>

---

<!-- slide: lecture-import -->

## 1.2.3 Mapping — dictionary

<div class="lecture-content" markdown="1">

<p class="">Taking out elements by subscripting</p>
<p class="">Error handling and the get function</p>

```python
age[Alice]
age["Alice"]
```

```python
l = [1, 2, 3]
l[3]
age["David"]
```


</div>

---

<!-- slide: lecture-import -->

## Special topic: Flow control (I) — for loop

<div class="lecture-content" markdown="1">

<p class="">How can we access all the elements in a list one by one?</p>
<p class="lecture-subpoint">We could take them out manually by l[0], l[1], l[2], etc.</p>
<p class="lecture-subpoint">We could create an index variable i to help us:</p>
<p class="lecture-subpoint">A more convenient way it to rely on the <strong>automated for-loop</strong></p>

```python
l = [1, 2, 3]
i = 0
l[i]
i = 1
l[i] # note: notebook cells can display a final expression without print
```

```python
for element in container:
    ...
```


</div>

---

<!-- slide: lecture-import -->

## Special topic: Flow control (I) — for loop

<div class="lecture-content" markdown="1">

<h3>In-class exercise Special (I).1</h3>
<p class="">Make a list and use for loop to print its elements</p>
<p class="">Make a tuple and use for loop to print its elements</p>
<p class="">Make a dictionary and use for loop to print its <strong>values</strong></p>
<p class="">Make a dictionary and use for loop to print its <strong>keys</strong></p>
<p class="">Print the key-value pairs in a formatted way using the f-string</p>




</div>

---

<!-- slide: lecture-import -->

## Special topic: Flow control (I) — for loop

<div class="lecture-content" markdown="1">

<p class="">We informally introduce a useful function for for-loops: range</p>
<p class="">range is very similar to slices</p>

```python
range(10)
range(1, 11)
range(0, 30, 5)
range(0, 10, 3)
range(0, -10, -1)
range(0)
range(1, 0)
```


</div>

---

<!-- slide: lecture-import -->

## Special topic: Flow control (I) — if statement

<div class="lecture-content" markdown="1">

<p class="">There are circumstances when we only want to print out certain elements of a list/a tuple/a dictionary.</p>
<p class="">For example, given a list</p>
<p class="">We only need the numbers that are squares of some integer. Or we only need the numbers that are cubics of some integers. Or just odd numbers.</p>
<p class="">In other words, only <strong>if </strong>the element satisfy a <strong>condition</strong>.</p>
<p class="">Here we use the if control flow</p>

```python
l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
```

```python
if element % 2 == 0:
    ...
```


</div>

---

<!-- slide: lecture-import -->

## Special topic: Flow control (I) — if statement

<div class="lecture-content" markdown="1">

<h3>In-class exercise Special (I).2</h3>
<p class="">For the list containing 13 elements</p>
<p class="">Print elements that are odd</p>
<p class="">Print elements that are squares</p>
<p class="">Print elements that are cubics</p>




</div>

---

<!-- slide: lecture-import -->

## Special topic: Flow control (I) — if statement

<div class="lecture-content" markdown="1">

<p class="">== vs. is</p>
<p class="">In the if-statement, the most commonly used condition is comparisons</p>
<p class="lecture-subpoint">compare the values two numbers by magnitude: &lt;, &gt;, ==</p>
<p class="lecture-subpoint">compare the identity: is</p>
<p class="">None is a special object in Python. Investigate it.</p>




</div>

---

<!-- slide: lecture-import -->

## Special topic: Flow control (I) — if statement

<div class="lecture-content" markdown="1">

<p class="">Comparison expressions return boolean variables. By <strong>expression</strong>, we refer to Python code that can be evaluated. The formal definition is involved and we will talk about it in future courses. Comparison expressions rely on &lt;, &gt;, &lt;=, &gt;=, != and is and not.</p>
<p class="">Evaluation of comparisons support chained expressions. For example:</p>

```python
a, b, c, d, e = 1, 4, 3, 3, 5
a < b > c == d != e
```


</div>

---

<!-- slide: lecture-import -->

## Comparisons with None

<div class="lecture-content" markdown="1">

`None` is Python’s singleton object used to represent the absence of a value.

Use **`is None`** or **`is not None`** to test for it. Multiple names can refer to that same object.

```python
a = None
b = None
a is b
```

`is` compares object identity; `==` compares values using the type’s equality operation.

</div>

---

<!-- slide: lecture-import -->

## 1.2.3 Mapping — dictionary

<div class="lecture-content" markdown="1">

<p class="">Sometimes we want to add more elements to a dictionary.</p>
<p class="lecture-subpoint">We can use the [] operator</p>
<p class="">Sometimes we want to combine two dictionaries.</p>
<p class="lecture-subpoint">We can use the update method.</p>
<p class="lecture-subpoint">Read this: <a href="https://python-reference.readthedocs.io/en/latest/docs/dict/update.html">https://python-reference.readthedocs.io/en/latest/docs/dict/update.html</a></p>




</div>

---

<!-- slide: lecture-import -->

## 1.2.3 Mapping — dictionary

<div class="lecture-content" markdown="1">

<p class="">Dictionaries are very different from lists or tuples</p>
<p class=""><strong>Example 1.2.3.3 list differs from dictionary</strong></p>

```python
d = {'a': [1], 'b': [1, 2], 'c': [], 'd':[]}

for i in d:
    if not d[i]:
        d.pop(i)

d = [1, 2, 3, 0, 5]

for i in range(4):
    if not d[i]:
        d.pop(i)
```


</div>

---

<!-- slide: lecture-import -->

## 1.2.3 Mapping — dictionary

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 1.2.3.4 JSON file as a dictionary</strong></p>

```python
import json

with open("settings.json", "r") as f:
    setting_dict = json.load(f)

setting_dict

setting_dict.items()
```


</div>

---

<!-- slide: lecture-import -->

## 1.2.3 Mapping — dictionary

<div class="lecture-content" markdown="1">

<p class="">Before we end the discussion of dictionaries, there is one last topic: the zips.</p>
<p class="">zip, in language means 拉链</p>
<p class="">As the name suggests, Python zips involve two sequences just as the real-life zippers. For example:</p>

```python
account = ["622848", "600314", "500297"]
balance = (1_000_000, 1_300_500, 500)
z1 = zip(account, balance)

for k, v in z1:
    print(k, "has a balance of", v)
```


</div>

---

<!-- slide: lecture-import -->

## 1.2 Objects’ types

<div class="lecture-content" markdown="1">

<h3>In-class exercise 1.2.2</h3>
<p class="">What simple types have we learned?</p>
<p class="">What complex types have we learned?</p>
<p class="">How do you tell them apart?</p>




</div>

---

<!-- slide: lecture-import -->

## 1.2.4 Strings

<div class="lecture-content" markdown="1">

Quotation marks distinguish string values from variable names. Single and double quotes both delimit strings.

A string is an **immutable sequence of Unicode characters**. Indexing it produces another string of length one.

Three groups of tools to explore:

- Case conversion: `upper`, `lower`, `title`.
- Removing leading/trailing characters: `strip`, `lstrip`, `rstrip`.
- Pattern replacement: `re.sub` from the `re` module.

A module is Python code stored separately for reuse.

</div>

---

<!-- slide: lecture-import -->

## 1.2.4 String

<div class="lecture-content" markdown="1">

<h3>In-class exercise 1.2.4.1</h3>
<p class="">Reverse a string. For example, given s = “desserts”, reverse it to get “stressed”. Reverse “drawer” to get “reward”. These are known as anadromes.</p>
<p class="">Remove vowels from a string. For example, “drawer” would become “drwr”.</p>
<p class="">Count the number of words in a string (using the split method).</p>




</div>

---

<!-- slide: lecture-import -->

## 1.2.5 Unordered nonduplicate — set

<div class="lecture-content" markdown="1">

<p class="">By definition. A set object is an unordered collection of distinct hashable objects: <a href="https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset">https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset</a></p>
<p class="">Python doc provides a glossary page for your reference: <a href="https://docs.python.org/3/glossary.html#term-hashable">https://docs.python.org/3/glossary.html#term-hashable</a></p>
<p class="">Set behaves just like the set concept we encounter in math courses. The elements of a set are unique and unordered. We can also use math concepts like in (<span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>∈</mtext></mrow></math></span>), issubset (<span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>⊂</mtext></mrow></math></span>), union (<span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>∪</mtext></mrow></math></span>), intersection (<span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>∩</mtext></mrow></math></span>), difference (<span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>−</mtext></mrow></math></span>), and symmetric difference (<span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>Δ</mtext></mrow></math></span>) to work on sets.</p>
<h3>In-class exercise 1.2.5.1</h3>
<p class="">How do you check if an object is hashable?</p>




</div>

---

<!-- slide: lecture-import -->

## 1.2.5 Unordered nonduplicate — set

<div class="lecture-content" markdown="1">

<p class="">There are several ways to create a set</p>
<p class="lecture-subpoint">Use braces such as <code>{1, 2}</code>; <code>{}</code> alone creates an empty dictionary</p>
<p class="lecture-subpoint">Use the set function set()</p>
<p class="lecture-subpoint">Use set comprehension (later)</p>
<p class="">We can modify a set once it&#x27;s created. See the exercise.</p>
<p class="">We create a frozenset mainly using frozenset()</p>




</div>

---

<!-- slide: lecture-import -->

## 1.2.5 Unordered nonduplicate — set

<div class="lecture-content" markdown="1">

<h3>In-class exercise 1.2.5.2</h3>
<p class="">1. Create a set containing the numbers 1, 2, 3, 4, and 5.</p>
<p class="">2. Add the number 6 to the set.</p>
<p class="">3. Create two sets: set_a = {1, 2, 3, 4} and set_b = {3, 4, 5, 6}.</p>
<p class="">4. Find the union of set_a and set_b.</p>
<p class="">5. Find the intersection of set_a and set_b.</p>
<p class="">6. Find the difference between set_a and set_b.</p>
<p class="">7. Find the symmetric difference between set_a and set_b.</p>
<p class="">8. Given the list numbers = [1, 2, 2, 3, 4, 4, 4, 5]. Create a set to remove duplicate elements.</p>
<p class="">9. Convert the set back into a list (with fewer elements).</p>




</div>

---

<!-- slide: lecture-import -->

## 1.3 Pythonic style

<div class="lecture-content" markdown="1">

**Pythonic** means writing clear, idiomatic Python. It does not mean every technique is unique to Python.

We have already encountered `zip`, `with`, `None`, `sorted`, and f-strings.

Next, explore **comprehensions** and **`enumerate`**.

</div>

---

<!-- slide: lecture-import -->

## 1.3 Pythonics — comprehensions (1)

<div class="lecture-content" markdown="1">

<p class="">List comprehension</p>
<p class="">Set comprehension</p>
<p class="">Dictionary comprehension</p>
<p class="">The one missing is &quot;tuple comprehension&quot;. But when you write</p>
<p class="">you do not get a tuple. What do you get?</p>

```python
[x for x in range(5)] # usually faster than list, if not too complicated
```

```python
{c for c in 'abcdcba'}
```

```python
{x: x ** 2 for x in range(5)}
```

```python
(i for i in range(3))
```


</div>

---

<!-- slide: lecture-import -->

## 1.3 Pythonics — comprehensions (1)

<div class="lecture-content" markdown="1">

<p class="">We can also add the if control flow to comprehensions:</p>
<p class="lecture-subpoint">Only the if condition</p>
<p class="lecture-subpoint">if condition with else condition</p>
<p>Import <code>time</code> before running the following expressions.</p>
<h3>In-class exercise 1.3.1</h3>
<p class="">How long does each of the following code take to run?</p>

```python
[x for x in range(10) if x % 2 == 0]
```

```python
[x if x % 2 == 0 else x + 1 for x in range(10)]
```

```python
[time.sleep(1), time.sleep(1), time.sleep(1)][0]
(time.sleep(1), time.sleep(1), time.sleep(1))[0]
```


</div>

---

<!-- slide: lecture-import -->

## 1.4 Objects’ values

<div class="lecture-content" markdown="1">

<p class="">Let’s step back before the end of this section.</p>
<p class="">Recall that an object is stored by its (i) id, (ii) type, and (iii) contents</p>
<p class="lecture-subpoint">What roles do these components play?</p>
<p class="lecture-subpoint">What if “你的打开方式不对?”</p>
<p class="lecture-subpoint">type-casting using the name of the type</p>
<p class="">Type conversion returns an object of the requested type; it does not change the type of the original object. What about changing an object’s value?</p>
<p class="lecture-subpoint">When the value change does not alter the address, the name reference is not changed. We say the object and the type of the object is <strong>mutable</strong>.</p>
<p class="lecture-subpoint">Mutable objects are very useful and sometimes tricky. We’ll explore more in the next Chapter.</p>




</div>

---

<!-- slide: lecture-import -->

## 1.4 Objects’ values

<div class="lecture-content" markdown="1">

<h3>In-class exercise 1.4.1</h3>
<p class="">What types of objects are mutable? How do you verify it?</p>




</div>

---

<!-- slide: lecture-import -->

## Further readings/watching

<div class="lecture-content" markdown="1">

<p class=""><a href="https://nedbatchelder.com/text/names.html">Python</a><a href="https://nedbatchelder.com/text/names.html">开发者 </a><a href="https://nedbatchelder.com/text/names.html">https://nedbatchelder.com/text/names</a><a href="https://nedbatchelder.com/text/names.html">.html</a></p>
<p class=""><a href="https://cs61a.org/">高端</a><a href="https://cs61a.org/">学院派</a> <a href="https://cs61a.org/">https://cs61a.org/</a></p>




</div>
