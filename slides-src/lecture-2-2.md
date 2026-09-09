---
title: Lecture 2.2 · First-Class Functions and Arguments
description: Higher-order functions, closures, argument unpacking, args, and kwargs.
lang: en
source: resource/deck2_2_AoL.pptx
sections:
- id: introduction
  title: Introduction
  start: 1
  level: 1
  textbook: ch2-3-first-class-0
- id: first-class-objects
  title: First-class objects
  start: 3
  level: 1
  textbook: ch2-3-first-class-2
- id: functions-as-return-values
  title: Functions as return values
  start: 4
  level: 1
  textbook: ch2-3-first-class-5
- id: functions-as-arguments
  title: Functions as arguments
  start: 5
  level: 1
  textbook: ch2-3-first-class-3
- id: passing-arguments
  title: Passing arguments
  start: 7
  level: 1
  textbook: ch2-3-first-class-4
- id: unpacking-with-a-star
  title: Unpacking with a star
  start: 8
  level: 1
  textbook: ch2-3-first-class-4
- id: keyword-arguments
  title: Keyword arguments
  start: 11
  level: 1
  textbook: ch2-3-first-class-4
- id: argument-order
  title: Argument order
  start: 12
  level: 1
  textbook: ch2-5-loose-ends-3
---


<!-- slide: title-slide -->
<p class="eyebrow">Lecture 2.2</p>

# First-Class Functions and Arguments

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">“Functions are first-class objects.”</p>
<p class="lecture-subpoint">Functions are also objects.</p>
<p class="lecture-subpoint">Functions as arguments.</p>
<p class="lecture-subpoint">Functions as return values.</p>
<p class="">We’ll rely on several specific use cases to introduce these topics.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.3 Functions are first-class objects

<span class="aol">AoL 2 (H)</span>

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

<span class="aol">AoL 3 (M)</span>

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

<span class="aol">AoL 3 (M)</span>

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

<span class="aol">AoL 3 (M)</span>

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

<span class="aol">AoL 3 (M)</span>

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
