---
title: Lecture 2.1 · Functions, Namespaces, and Scope
description: Defining functions, call frames, defaults, scope, first-class functions,
  and unpacking.
lang: en
source: ../course materials/deck2_1.pptx
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
- id: the-call-stack
  title: The call stack
  start: 10
  level: 1
  textbook: ch2-1-defining-functions-4
- id: newton-s-method
  title: Newton’s method
  start: 12
  level: 1
  textbook: ch2-1-defining-functions-6
- id: default-parameters
  title: Default parameters
  start: 13
  level: 1
  textbook: ch2-1-defining-functions-7
- id: function-factories
  title: Function factories
  start: 15
  level: 1
  textbook: ch2-1-defining-functions-8
- id: namespaces
  title: Namespaces
  start: 16
  level: 1
  textbook: ch2-2-namespaces-scope-2
- id: scope-and-legb
  title: Scope and LEGB
  start: 19
  level: 1
  textbook: ch2-2-namespaces-scope-5
- id: shadowing
  title: Shadowing
  start: 20
  level: 1
  textbook: ch2-2-namespaces-scope-6
- id: why-scopes
  title: Why scopes?
  start: 21
  level: 1
  textbook: ch2-2-namespaces-scope-8
- id: first-class-objects
  title: First-class objects
  start: 22
  level: 1
  textbook: ch2-3-first-class-2
- id: functions-as-return-values
  title: Functions as return values
  start: 23
  level: 1
  textbook: ch2-3-first-class-5
- id: functions-as-arguments
  title: Functions as arguments
  start: 24
  level: 1
  textbook: ch2-3-first-class-3
- id: passing-arguments
  title: Passing arguments
  start: 26
  level: 1
  textbook: ch2-3-first-class-4
- id: unpacking-with-a-star
  title: Unpacking with a star
  start: 27
  level: 1
  textbook: ch2-3-first-class-4
- id: keyword-arguments
  title: Keyword arguments
  start: 30
  level: 1
  textbook: ch2-3-first-class-4
- id: argument-order
  title: Argument order
  start: 31
  level: 1
  textbook: ch2-5-loose-ends-3
---

<!-- slide: title-slide -->

<p class="eyebrow">Lecture 2.1</p>

# Functions, Namespaces, and Scope

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2025</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">How you can <strong>define</strong> and <strong>call</strong> simple functions.</p>
<p class="">How functions, as objects (chunks of memory), are stored, and when you call a function, what will happen inside Python.</p>
<p class="">Functions naturally divide memory into smaller pieces, and names live in such spaces. You’ll see how Python manages the spaces and controls the accessibility of variables.</p>
<p class="">“Functions are first-class objects.”</p>




</div>

---

<!-- slide: lecture-import -->

## 2.1 Simple functions

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

## 2.1 Simple functions

How is a function composed?

<p class="lecture-subpoint">A function is designed to free us from repetitive jobs so that we can work more efficiently. So we need the function to know what we want to do. This is known as the function <strong>body</strong>.</p>

<p class="lecture-subpoint">The function will work on different classes (or more generally, objects). We need to let it know which one we need to proceed. We provide case-dependent information to the function via <strong>parameters</strong>.</p>

<p class="lecture-subpoint">As always, the name is so important. A function also needs a <strong>name</strong>.</p>

<p class="lecture-subpoint">There is another component of a function: the <strong>return</strong> value. We’ll talk about it later.</p>

---

<!-- slide: lecture-import -->

## 2.1.1 Simple functions: def and call

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

## 2.1.1 Simple functions: def and call

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.1.3</h3>
<p class="">Call the function you just defined and apply it to class 2.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.1.1 Simple functions: def and call

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.1.4</h3>
<p class="">Summarize the steps to define a function.</p>
<h3>In-class exercise 2.1.5</h3>
<p class="">Define a function that computes the square of all numbers in a list. For example, if the list is l = [1, 2, 3], the function finds [1, 4, 9].</p>
<p class="">Store the new list for future use.</p>




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

## Special topic I: the Python call stack

<div class="lecture-content" markdown="1">

<p class="">A summary of a Python function call</p>
<p class="lecture-subpoint">Add a local frame, forming a new environment</p>
<p class="lecture-subpoint">Bind the function&#x27;s formal parameters to its arguments in that frame</p>
<p class="lecture-subpoint">Execute the body of the function in that new environment</p>
<p class="caption">source: Prof. John DeNero, CS61A, UC Berkeley</p>
<h3>In-class exercise Special topic.1</h3>
<p class="">How do you distinguish a function from a function call</p>




</div>

---

<!-- slide: lecture-import -->

## Special topic II: the Newton’s method

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

## 2.1 Simple functions (special case I)

In Newton’s method, we can choose an **error bound** each time we call the function.

Usually we want to use the same bound, changing it only when needed.

A **default parameter value** supplies that value when the caller omits the argument.

---

<!-- slide: lecture-import -->

## 2.1.3 Simple functions (default parameters)

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

## 2.2 Namespaces and scopes of variables

<div class="lecture-content" markdown="1">

<p class="">We have learned that Python interpreter binds names to objects. A <strong>namespace</strong> is a dictionary (more precisely, a hash map) telling us which name is bound to which value.</p>
<p class="">For example, we have the builtins, globals, closure, and the local namespaces.</p>
<p class="">A related concept is <strong>scope</strong>, which describes the range where a name can be resolved.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.2.1 Namespaces and scopes of variables

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.2.2.1</h3>
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

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.2.2.2</h3>
<p class="">Can you please check the objects living in the local namespace?</p>




</div>

---

<!-- slide: lecture-import -->

## 2.2.2 Scope of a variable

<div class="lecture-content" markdown="1">

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

<!-- slide: lecture-import -->

## 2.2.2 Scope of a variable

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

<div class="lecture-content" markdown="1">

<p class="">A long example</p>
<p class=""><a href="https://www.bilibili.com/video/BV1edH2eqEno/?spm_id_from=333.999.0.0&amp;vd_source=ec7b194853f6121829b0f428c7736022">A more complicated example</a></p>
<h3>In-class exercise 2.2.2.3 [purpose of variable scopes]</h3>
<p class="">How does Python count number of references?</p>
<p class="lecture-subpoint">avoid unnecessary global variables</p>
<p class="">How do you modify the function factory in Special case II?</p>
<p class="lecture-subpoint">explicitly refer to a nonlocal variable</p>
<p class="">How do you hide information from the global functions?</p>
<p class="lecture-subpoint">follow the LEGB rule</p>




</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions are first-class objects

<div class="lecture-content" markdown="1">

<p class="">First-class objects are flexible. Being first class means there is no restrictions on the use of the object. We can pass this object as an argument to a function and can return it as a return value. We can also create dictionaries to store it, etc.</p>
<p class="">When we use a function as an argument and return values of another &quot;higher-level&quot; functions, we are using <strong>higher-order functions</strong>.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions are first-class objects

<div class="lecture-content" markdown="1">

<p class="">Functions as return values</p>

```python
def intercept_1():
    a = 1
    def slope_2(x):
        return 2 * x + a
    return slope_2


linear_trans = intercept_1()
linear_trans(3)
```


</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions are first-class objects

<div class="lecture-content" markdown="1">

<p class="">Functions as arguments</p>

```python
def call_count(func, x=[0]):
    print(f"calling {x[0] + 1} times")
    x[0] += 1
    func()


call_count(print)
call_count(print)
call_count(print)
```


</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions are first-class objects

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.3.1</h3>
<p class="">Modify code example 1, so that we can select the intercept.</p>
<p class="">Modify code example 1, so that we can also select the slope.</p>
<p class="">Modify code example 2, so that we do not need default parameters.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions … objects (special case III)

<div class="lecture-content" markdown="1">

<div class="columns" markdown="1">
<div class="column" markdown="1">
<p class="">In the call_count example, we can pass a function as an argument to the function. But this function cannot have its own parameters. How can we pass arguments to the function being counted?</p>
</div>
<div class="column" markdown="1">

```python
def call_count(func, arg_to_called, x=[0]):
    print(f"calling {x[0]} times")
    x[0] += 1
    func(arg_to_called)


call_count(print, "hello")
call_count(print, "python")
call_count(print, "world")
```


</div>
</div>

</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions … objects (special case III)

<div class="lecture-content" markdown="1">

<p class="">When we are not sure about how many parameters to pass to the function, the conventional parameter names are <code>args</code> and <code>kwargs</code>. The special syntax is <code>*args</code> and <code>**kwargs</code>; the names themselves are not keywords.</p>
<p class="lecture-subpoint">The * operator. A star is known as the (un)packing operator.</p>
<h3>In-class exercise 2.3.2</h3>
<p class="">How do they differ?</p>

```python
a = 1, 2, 3

a, b, c = 1, 2, 3

a, b = 1, 2, 3

a, *b, c = 1, 2, 3, 4, 5
```


</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions … objects (special case III)

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.3.3</h3>
<p>Some cases deliberately contain errors. Consider and run each assignment separately.</p>
<p class="">Summarize the pattern by considering</p>

```	ext
*a, b = 1, 2, 3, 4, 5

a, *b = 1, 2, 3, 4, 5

*a, *b = 1, 2, 3, 4, 5

*a, b, c = 1, 2, 3, 4, 5

*a, b = 1
```


</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions … objects (special case III)

<div class="lecture-content" markdown="1">

<p class="">Note that a is a list but *a <strong>unpacks</strong> the list into several elements. Passing indefinite number of arguments to a function involves two steps:</p>
<p class="lecture-subpoint">collecting positional arguments in a tuple (when defining <code>*args</code>)</p>
<p class="lecture-subpoint">unpacking an iterable with <code>*</code> when making a call</p>
<p class="">To check the unpacking behavior, we can use the sep parameter.</p>

```python
def call_count(func, *args, x=[0]):
    print(f"calling {x[0]} times")
    x[0] += 1
    func(*args, sep=", ")


call_count(print, "hello", "python", "world")
```


</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions … objects (special case III)

<div class="lecture-content" markdown="1">

<div class="columns" markdown="1">
<div class="column" markdown="1">
<p class="">The ** operator.</p>
<p class="lecture-subpoint">Another type of arguments is called <strong>keyword arguments</strong>, which must be passed to a function with the form param=arg. These are named arguments. Unlike * that unpacks a list, we use ** to unpack a dictionary. There are fewer use cases than the unpacking of a list.</p>
</div>
<div class="column" markdown="1">

```python
dict1 = {"a": 1,
         "b": 2,
         "c": 3}

dict2 = {"d": 4,
         "e": 5,
         "f": 6}

combined_dict = {**dict1, **dict2}
```


</div>
</div>

</div>

---

<!-- slide: lecture-import -->

## Argument and parameter order

<div class="lecture-content" markdown="1">

Ordinary positional arguments precede keyword arguments in a call:

```python
print("hello", "Python", sep=", ")
```

In the positional parameter list of a function definition, required parameters come before parameters with defaults.

Keyword-only parameters follow `*` or `*args`; `**kwargs`, when present, comes last.

```text
def function(required, optional=0, *args, keyword_only, **kwargs):
    ...
```

</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions … objects (special case III)

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2.3.4</h3>
<p class="">Note that **kwargs is actually unpacking a dict. This is to say, kwargs is a dict. We learned that a dict has keys and values. Read the document about named arguments: <a href="https://docs.python.org/3/library/stdtypes.html#dict">https://docs.python.org/3/library/stdtypes.html#dict</a></p>
<p class="">Write a function to take the sum of several (the numbers are unknown) named arguments. For example,</p>

```text
def sum_of_kwargs(???):
    pass

sum_of_kwargs(Alice=5, Bob=3, Charlie=4)
```


</div>

---

<!-- slide: lecture-import -->

## The assembly of tools

<div class="lecture-content" markdown="1">

<p class="">The creation of tools</p>
<p class="caption">source: https://cn.nytimes.com/culture/20180515/2001-a-space-odyssey-kubrick/</p>


<figure class="diagram"><img src="images/slide-25-3.webp" alt="Functions, Namespaces, and Scope: original illustration, slide 25."></figure>

</div>
