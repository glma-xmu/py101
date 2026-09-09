---
title: Lecture 2.1 · Functions, Namespaces, and Scope
description: Defining functions, return values, call frames, defaults, and LEGB.
lang: en
source: resource/deck2_1_AoL.pptx
sections:
- id: introduction
  title: Introduction
  start: 1
  level: 1
  textbook: ch2-1-defining-functions-0
- id: why-functions
  title: Why functions?
  start: 3
  level: 1
  textbook: ch2-1-defining-functions-2
- id: define-and-call
  title: Define and call
  start: 5
  level: 1
  textbook: ch2-1-defining-functions-2
- id: return-values
  title: Return values
  start: 10
  level: 1
  textbook: ch2-1-defining-functions-5
- id: the-call-stack
  title: The call stack
  start: 13
  level: 1
  textbook: ch2-1-defining-functions-4
- id: default-parameters
  title: Default parameters
  start: 15
  level: 1
  textbook: ch2-1-defining-functions-7
- id: function-factories
  title: Function factories
  start: 16
  level: 1
  textbook: ch2-1-defining-functions-8
- id: newton-s-method
  title: Newton’s method
  start: 17
  level: 1
  textbook: ch2-1-defining-functions-6
- id: namespaces
  title: Namespaces
  start: 18
  level: 1
  textbook: ch2-2-namespaces-scope-2
- id: scope-and-legb
  title: Scope and LEGB
  start: 21
  level: 1
  textbook: ch2-2-namespaces-scope-5
- id: closures-and-nonlocal
  title: Closures and nonlocal
  start: 22
  level: 1
  textbook: ch2-2-namespaces-scope-7
- id: shadowing
  title: Shadowing
  start: 23
  level: 1
  textbook: ch2-2-namespaces-scope-6
- id: why-scopes
  title: Why scopes?
  start: 24
  level: 1
  textbook: ch2-2-namespaces-scope-8
---


<!-- slide: title-slide -->
<p class="eyebrow">Lecture 2.1</p>

# Functions, Namespaces, and Scope

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">How you can <strong>define</strong> and <strong>call</strong> simple functions.</p>
<p class="">How functions, as objects (chunks of memory), are stored, and when you call a function, what will happen inside Python.</p>
<p class="">Functions naturally divide memory into smaller pieces, and names live in such spaces. You’ll see how Python manages the spaces and controls the accessibility of variables.</p>
<p class="">“Functions are first-class objects.”</p>




</div>

---

<!-- slide: lecture-import -->

## 2.1 Simple functions

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.1.1</h3>
<p class="">Review (read text file, work with dict):</p>
<p class="">Context: You are managing a database for a training camp. Under the data folder, there is students’ information from 5 classes. Each class has an age.txt and a gender.txt.</p>
<p class="">Please read the age.txt and gender.txt from class 1.</p>
<p class="">Make a new .txt file to store the information of class 1.</p>
<p class="">Repeat the steps for the other classes.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.1 Simple functions

<div class="lecture-content" markdown="1">

<p class="">From the above example, you probably have noticed that for each class, the job is the same, requiring the same code to be used more than once. What are the disadvantages?</p>
<p class="lecture-subpoint">Prone to errors</p>
<p class="lecture-subpoint">Hard to modify</p>
<p class="lecture-subpoint">…</p>
<p class="">We now introduce how to abstract the procedure and encapsulate it into a <strong>function</strong>.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.1.1 Simple functions: def and call

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">We start from the creation (definition) of a function.</p>
<p class="">How is a function composed?</p>
<p class="lecture-subpoint">As always, the name is so important. A function also needs a <strong>name</strong>.</p>
<p class="lecture-subpoint">The function will work on different classes (or more generally, objects). We need to let it know which one we need to proceed. We provide case-dependent information to the function via <strong>parameters</strong>.</p>
<p class="lecture-subpoint">A function is designed to free us from repetitive jobs so that we can work more efficiently. So we need the function to know what we want to do. This is known as the function <strong>body</strong>.</p>
<p class="lecture-subpoint">There is another component of a function: the <strong>return</strong> value. We’ll talk about it later.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.1.1 Simple functions: def and call

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">Putting the elements together. In code, we create a function with:</p>
<p class="">The above is the Pythonic style to <strong>define </strong>a function.</p>
<h3>In-class exercise 2.1.2</h3>
<p class="">Assemble the code from exercise 2.1.1 to define a function.</p>

```text
def <name>(<parameters>):
    <body>
    return None
```


</div>

---

<!-- slide: lecture-import -->

## 2.1.1 Simple functions: def and call

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.1.3</h3>
<p class="">Call the function you just defined and apply it to class 2.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.1.1 Simple functions: def and call

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.1.4</h3>
<p class="">Summarize the steps to define a function.</p>
<h3>In-class exercise 2.1.5</h3>
<p class="">Define a function that computes the square of all numbers in a list. For example, if the list is l = [1, 2, 3], the function finds [1, 4, 9].</p>
<p class="">Store the new list for future use.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.1.1 Simple functions: def and call

<div class="lecture-content" markdown="1">

<p class="">Once defined, the functions will be stored in the memory as other objects. Try to print the function and see what is printed.</p>
<p class="">Programming functions are very similar to math functions.</p>
<p class="lecture-subpoint">In math, we need to repeatedly find the distance between any two points <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>P</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow></msub><mrow><mtext>=</mtext></mrow><mrow><mo>(</mo><mrow><msub><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow></msub><mrow><mtext>,</mtext></mrow><msub><mrow><mrow><mtext>𝑦</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow></msub></mrow><mo>)</mo></mrow></math></span> and <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>P</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msub><mrow><mtext>=</mtext></mrow><mrow><mtext>(</mtext></mrow><msub><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msub><mrow><mtext>,</mtext></mrow><msub><mrow><mrow><mtext>𝑦</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msub><mrow><mtext>)</mtext></mrow></math></span>. So we define the distance function</p>
<p class="lecture-subpoint"><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑓</mtext></mrow><mrow><mo>(</mo><mrow><msub><mrow><mrow><mtext>𝑃</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow></msub><mrow><mtext>,</mtext></mrow><msub><mrow><mrow><mtext>𝑃</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msub></mrow><mo>)</mo></mrow><mrow><mtext>=</mtext></mrow><msqrt><mrow><msup><mrow><mrow><mo>(</mo><mrow><msub><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow></msub><mrow><mtext>−</mtext></mrow><msub><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msub></mrow><mo>)</mo></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msup><mrow><mtext>+</mtext></mrow><msup><mrow><mrow><mo>(</mo><mrow><msub><mrow><mrow><mtext>𝑦</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow></msub><mrow><mtext>−</mtext></mrow><msub><mrow><mrow><mtext>𝑦</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msub></mrow><mo>)</mo></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msup></mrow></msqrt></math></span>.</p>
<p class="">We define functions so we can use them. In Python, when we use a function, we <strong>call</strong> it.</p>
<p class="lecture-subpoint">In math, given two specific points <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>(1, 2)</mtext></mrow></math></span> and <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>(3, 4)</mtext></mrow></math></span>. We evaluate the <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑓</mtext></mrow></math></span> function by passing the values to the function: <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑓</mtext></mrow><mrow><mtext>(</mtext></mrow><mrow><mo>(</mo><mrow><mrow><mtext>1,2</mtext></mrow></mrow><mo>)</mo></mrow><mrow><mtext>, (3,4))</mtext></mrow></math></span>.</p>
<p class="lecture-subpoint">Python does exactly the same --- pairs of parentheses.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.1.2 Simple functions: return values

<span class="aol">AoL 5 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">return</p>
<p class="">In the previous discussion, we used the print function inside customized functions.</p>
<p class="">The function call communicates with the caller in the global environment through return statements. Without this mechanism, each function call would become a self-contained “little kingdom.”</p>
<h3>In-class exercise 2.1.6</h3>
<p class="">When does a variable disappear in memory?</p>




</div>

---

<!-- slide: lecture-import -->

## Return values — exercise 1

<div class="lecture-content" markdown="1">

Record customers’ purchases and analyze them. Write two functions with these interfaces:

```text
sum_buy(name: str, clothes: int, food: int) -> dict
highest(cus1: dict, cus2: dict, cus3: dict) -> str
```

The first computes the total spent by one customer. The second returns the name of the customer with the largest total.

```python
alice = sum_buy("Alice", 900, 500)
# Create bob and charlie using their purchase records, then:
first = highest(alice, bob, charlie)
print(first)
```

For records where Alice has the largest total, the expected name is `"Alice"`.

</div>

---

<!-- slide: lecture-import -->

## Return values — exercise 2

<div class="lecture-content" markdown="1">

Write a function that converts numerical exam scores to letter grades.

```python
scores = {"Alice": 60, "Bob": 70, "Charlie": 80}
```

Use non-overlapping intervals: **60 ≤ score < 80: C**, **80 ≤ score < 90: B**, and **90 ≤ score ≤ 100: A**. Decide how your function should handle scores outside these intervals.

```text
convert(scores: dict) -> dict
```

For the supplied scores, the expected result is:

```text
{'Alice': 'C', 'Bob': 'C', 'Charlie': 'B'}
```

</div>

---

<!-- slide: lecture-import -->

## Special topic I: the Python call stack

<span class="aol">AoL 5 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">A summary of a Python function call</p>
<p class="lecture-subpoint">Add a local frame, forming a new environment</p>
<p class="lecture-subpoint">Bind the function&#x27;s formal parameters to its arguments in that frame</p>
<p class="lecture-subpoint">Execute the body of the function in that new environment</p>
<p class="caption">source: Prof. John DeNero, CS61A, UC Berkeley</p>
<h3>In-class exercise 2.1.6</h3>
<p class="">How do you distinguish a function from a function call</p>




</div>

---

<!-- slide: lecture-import -->

## Special topic I: the Python call stack

<div class="lecture-content" markdown="1">

<p class=""><strong>Code Example (the call stack)</strong></p>

```python
import inspect


def print_stack():
    stack = inspect.stack()
    for frame in stack:
        print(f"Function: {frame.function}")
        print(f"Code context: {frame.code_context}")
        print("-" * 80)


print_stack()
```


</div>

---

<!-- slide: lecture-import -->

## 2.1.3 Simple functions (default parameters)

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.1.6</h3>
<p class="">Try the code below. What do you find? Can you explain?</p>

```python
def append_to(element, to=[]):
    to.append(element)
    return to
    
my_list = append_to(12)
print(my_list)

my_other_list = append_to(42)
print(my_other_list)
```


</div>

---

<!-- slide: lecture-import -->

## 2.1.3 Simple functions (function factory)

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.1.7</h3>
<p class="">Try the code below. What do you find? Can you explain?</p>

```python
ff = {}

for i in range(5):
    def f():
        return i
    ff[i] = f


ff[3]()
```


</div>

---

<!-- slide: lecture-import -->

## Special topic II: the Newton’s method

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">This is more mathematical …</p>
<p class="">Given any function, how do you find its root?</p>
<p class="">The <a href="https://en.wikipedia.org/wiki/Newton%27s_method">Newton’s method</a> is one of the most commonly used.</p>
<h3>In-class exercise Special topic II.1</h3>
<p class="">Write a function to find the root of <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑓</mtext></mrow><mrow><mo>(</mo><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mo>)</mo></mrow><mrow><mtext>=0.3×</mtext></mrow><msup><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msup><mrow><mtext>−</mtext></mrow><mrow><mrow><mrow><mtext>sin</mtext></mrow></mrow><mrow><mrow><mo>(</mo><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mo>)</mo></mrow></mrow></mrow><mrow><mtext>+</mtext></mrow><mrow><mtext>𝑥</mtext></mrow></math></span> around <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>−4.5</mtext></mrow></math></span>. When the error is smaller than a value, report the root.</p>
<p class="">How do you stop the function iteration?</p>




</div>

---

<!-- slide: lecture-import -->

## 2.2 Namespaces and scopes of variables

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">We have learned that Python interpreter binds names to objects. A <strong>namespace</strong> is a dictionary (more precisely, a hash map) telling us which name is bound to which value.</p>
<p class="">For example, we have the builtins, globals, closure, and the local namespaces.</p>
<p class="">A relative concept is <strong>scope</strong>, which describes the range where an object can be accessed freely.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.2.1 Namespaces and scopes of variables

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.2.1</h3>
<p class="">Write a function to swap the values of two objects. For example, a, b = 1, 2. After swapping, a is 2 and b is 1.</p>
<p class="">Analyze the function for variable names.</p>
<p class="">Check the names in the namespaces</p>

```python
import builtins

print(type(builtins), dir(builtins))

globals()
```


</div>

---

<!-- slide: lecture-import -->

## 2.2.1 Namespaces and scopes of variables

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.2.2</h3>
<p class="">Can you please check the objects living in the local namespace?</p>




</div>

---

<!-- slide: lecture-import -->

## 2.2.2 Scope of a variable

<div class="lecture-content" markdown="1">

<span class="aol">AoL 2 (H)</span>

When Python resolves a name, it searches in **LEGB** order:

<table class="lecture-table">
<tr><td>Search order</td><td>Namespace</td><td>Where it comes from</td></tr>
<tr><td>1 · L</td><td>Local</td><td>The current function call</td></tr>
<tr><td>2 · E</td><td>Enclosing</td><td>Enclosing function calls</td></tr>
<tr><td>3 · G</td><td>Global</td><td>The current module</td></tr>
<tr><td>4 · B</td><td>Built-in</td><td>Python’s built-in names</td></tr>
</table>

`nonlocal` targets an existing binding in an enclosing function; `global` targets the module namespace.

```python
import builtins
print(type(builtins), dir(builtins))
globals()
```

</div>

---

<!-- slide: lecture-import lecture-compact -->

## 2.2.2 Scope of a variable

<div class="lecture-content" markdown="1">

<p class=""><strong>Code Example </strong><strong>(closure </strong><strong>namespaces)</strong></p>

```python
def make_player(name, hp, damage):
    def attack(other):
        nonlocal hp
        other["take_damage"](damage)
        print(f"{name} attacks for {damage} damage.")

    def take_damage(amount):
        nonlocal hp
        hp -= amount

    def status():
        print(f"{name} has {hp} HP and {damage} damage.")

    return {
        "attack": attack,
        "take_damage": take_damage,
        "status": status,
    }
```


</div>

---

<!-- slide: lecture-import -->

## 2.2.2 Scope of a variable

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.2.3</h3>
<p class="">What will the following give us? How can we make it normal?</p>

```python
print(max(1, 2))
max = min
print(max(1, 2))
```


</div>

---

<!-- slide: lecture-import -->

## 2.2.2 Scope of a variable

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">A long example</p>
<p class=""><a href="https://www.bilibili.com/video/BV1edH2eqEno/?spm_id_from=333.999.0.0&amp;vd_source=ec7b194853f6121829b0f428c7736022">A more complicated example</a></p>
<h3>In-class exercise 2.2.4 [purpose of variable scopes]</h3>
<p class="">How does Python count number of references?</p>
<p class="lecture-subpoint">avoid unnecessary global variables</p>
<p class="">How do you modify the function factory in Special case II?</p>
<p class="lecture-subpoint">explicitly refer to a nonlocal variable</p>
<p class="">How do you hide information from the global functions?</p>
<p class="lecture-subpoint">follow the LEGB rule</p>




</div>

---

<!-- slide: lecture-import -->

## The assembly of tools

<span class="aol">AoL 5 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">The creation of tools</p>
<p class="caption">source: https://cn.nytimes.com/culture/20180515/2001-a-space-odyssey-kubrick/</p>


<figure class="diagram"><img src="images/slide-25-3.webp" alt="Functions, Namespaces, and Scope: original illustration, slide 25."></figure>

</div>
