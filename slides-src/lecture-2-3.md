---
title: Lecture 2.3 · Five Function Use Cases
description: Decorators, recursion, map/filter/reduce, generators, errors, and PEP
  8.
lang: en
source: ../course materials/deck2_3_AoL.pptx
sections:
- id: introduction
  title: Introduction
  start: 1
  level: 1
  textbook: ch2-4-use-cases-0
- id: decorators
  title: Decorators
  start: 3
  level: 1
  textbook: ch2-4-use-cases-2
- id: recursion
  title: Recursion
  start: 9
  level: 1
  textbook: ch2-4-use-cases-3
- id: map-filter-and-reduce
  title: Map, filter, and reduce
  start: 18
  level: 1
  textbook: ch2-4-use-cases-4
- id: lambda-expressions
  title: Lambda expressions
  start: 20
  level: 1
  textbook: ch2-3-first-class-6
- id: map-and-filter
  title: Map and filter
  start: 21
  level: 1
  textbook: ch2-4-use-cases-4
- id: reduce
  title: Reduce
  start: 23
  level: 1
  textbook: ch2-4-use-cases-4
- id: generators
  title: Generators
  start: 24
  level: 1
  textbook: ch2-4-use-cases-5
- id: errors-and-try-except
  title: Errors and try/except
  start: 30
  level: 1
  textbook: ch2-4-use-cases-6
- id: pep-8
  title: PEP 8
  start: 33
  level: 1
  textbook: ch2-5-loose-ends-4
- id: further-reading
  title: Further reading
  start: 34
  level: 1
  textbook: ch2-4-use-cases-7
  related: true
---

<!-- slide: title-slide -->

<p class="eyebrow">Lecture 2.3</p>

# Five Function Use Cases

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">Five use cases of Python functions.</p>
<p class="">The Eighth Python Enhancement Proposal.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case I: decorator

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">Before we start decorators, let’s review what we’ve learned.</p>
<h3>In-class exercise 1</h3>
<p class="">Write a function to compute the <a href="https://baike.baidu.com/item/%E5%B9%B3%E5%9D%87%E5%80%BC/8353298">average</a> of t1.</p>
<p class="">Write a function to compute the <a href="https://baike.baidu.com/item/%E6%A0%87%E5%87%86%E5%B7%AE/1415772">standard deviation</a> of t1.</p>
<p class="">Write a function to compute the <a href="https://baike.baidu.com/item/%E5%81%8F%E5%BA%A6/8626571">skewness</a> of t1.</p>

```python
t1 = (1, 2, 3, 4, 5)
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case I: decorator

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">If you encountered an error when we tried to pass t2 to our function. The right thing to do is to make sure there is no invalid values in the arguments passed to our function. Here we introduce the assert statement.</p>
<p class="">assert is a claim, we assert an expression (what is an expression?). If the value of the expression is True, nothing happens and the program proceeds. But if the value is False the assertion fails, and an error occurs.</p>
<h3>In-class exercise 2</h3>
<p class="">Apply your average function to t2.</p>

```python
t2 = (1, 2, 3, None, 5)
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case I: decorator

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">Examples of assert statements</p>
<h3>In-class exercise 3</h3>
<p class="">1. Use assert to improve your functions.</p>

```python
assert None in [1, 2, 3], "All values look good!"

assert None not in [1, 2, 3], "Contains None!"
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case I: decorator

<div class="lecture-content" markdown="1">

<p class="">Although assert is handy, if we have written so many functions, it is hard for us to modify all of them. In other cases, if someone else defines the function for us, we cannot modify the function ourselves.</p>
<p class="">So when we want to extend the functionality of a function, what we can do is to define a higher-order function, and use the function we want to modify as its argument. Do whatever we want, and then send out the new function.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case I: decorator

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">Syntax template</p>

```python
# to define a decorator as a higher order function
def decor(func):

    def wrapper(*args, **kwargs):
        ...
        return func(*args, **kwargs)
        ...

    return wrapper

# to decorate a function
@decor
def func():
    pass
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case I: decorator

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 4</h3>
<p class="">Write decorators to:</p>
<p class="">Print a line “&lt;function name&gt; function is being called.&quot; before the execution and print a line after the execution. &quot;finish calling &lt;function name&gt; function.</p>
<p class="">Record return values of previous function calls. Every time a function is called, record the return value so next time the function is called, we don&#x27;t have to wait the function to run.</p>

```text
In[]: print(1)
Out[]: print function is being called.
       finish calling print function.
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case II: recursion

<div class="lecture-content" markdown="1">

<p class="">A function is recursive when it calls itself, directly or indirectly. Recursion does not require passing the function as an argument.</p>
<p class="">We’ll rewrite two functions we have already written and introduce three more examples:</p>
<p class="lecture-subpoint">Revisit Newton’s method</p>
<p class="lecture-subpoint">Revisit the sums function</p>
<p class="lecture-subpoint">Finding square root</p>
<p class="lecture-subpoint">Fibonacci sequence</p>
<p class="lecture-subpoint">Factorial function</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case II: recursion (Newton’s method)

<div class="lecture-content" markdown="1">

<p class="">Suppose we want to find the root of <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑓</mtext></mrow><mrow><mo>(</mo><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mo>)</mo></mrow><mrow><mtext>=</mtext></mrow><msup><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msup><mrow><mtext>−3</mtext></mrow></math></span>. Start from <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>0</mtext></mrow></math></span>.5.</p>
<p class="">By Newton’s method,</p>
<p class="lecture-subpoint"><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mrow><mtext>𝑓</mtext></mrow></mrow><mrow><mrow><mtext>′</mtext></mrow></mrow></msup><mrow><mo>(</mo><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mo>)</mo></mrow><mrow><mtext>=2</mtext></mrow><mrow><mtext>𝑥</mtext></mrow></math></span></p>
<p class="lecture-subpoint"><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>next</mtext></mrow></mrow></msup><mrow><mtext>=</mtext></mrow><msup><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>current</mtext></mrow></mrow></msup><mrow><mtext>−</mtext></mrow><mfrac><mrow><mrow><mtext>𝑓</mtext></mrow><mrow><mo>(</mo><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mo>)</mo></mrow></mrow><mrow><msup><mrow><mrow><mtext>𝑓</mtext></mrow></mrow><mrow><mrow><mtext>′</mtext></mrow></mrow></msup><mrow><mo>(</mo><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mo>)</mo></mrow></mrow></mfrac><mrow><mtext>=</mtext></mrow><msup><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>current</mtext></mrow></mrow></msup><mrow><mtext>−</mtext></mrow><mfrac><mrow><msup><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msup><mrow><mtext>−3</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow><mrow><mtext>𝑥</mtext></mrow></mrow></mfrac></math></span>.</p>

```python
def newton(x):
    return x-(x**2-3)/(2*x)


x = 0.5
for _ in range(10):
    x = newton(x)
    print(x)
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case II: recursion (Newton’s method)

<div class="lecture-content" markdown="1">

<p class="">Pay attention to the relation</p>
<p class="">Is it the same as</p>

```python
for _ in range(10):
    x = newton(x)
```

```python
newton(newton(newton(newton(newton(newton(newton(newton(newton(newton(0.5))))))))))
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case II: recursion (Newton’s method)

<div class="lecture-content" markdown="1">

<div class="columns" markdown="1">
<div class="column" markdown="1">
<p class="">We can simplify the manual recursive calls</p>
<p class="">This unfinished starting point recurses without making progress. Add an update and a stopping condition before running it.</p>
<p class="">Summary:</p>
<p class="lecture-subpoint">A boundary condition is used to …</p>
<p class="lecture-subpoint">A recursion body is used to …</p>
<p class="lecture-subpoint">The difference between recursion and loops include …</p>
</div>
<div class="column" markdown="1">

```python
def newton_recursion(x):
    return newton_recursion(x)  # unfinished: no update or stopping condition
```


</div>
</div>

</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case II: recursion (sum)

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">Based on what we learned from the previous example, can you see how the sum_recursion function works?</p>

```python
def sum_recursion(x):
    if len(x) == 0:
        return 0
    else:
        return x[0] + sum_recursion(x[1:])
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case II: recursion (square root)

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">We have relied on the Newton’s method to find the square root of a number. There is another method.</p>
<p class="">Mathematically, if we want to find the root of <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑥</mtext></mrow></math></span>, the root must satisfy</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑟</mtext></mrow><mrow><mtext>=</mtext></mrow><mfrac><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>𝑟</mtext></mrow></mrow></mfrac></math></span></p>
<p class="">If the relation is satisfied, then we will see</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>2</mtext></mrow><mrow><mtext>𝑟</mtext></mrow><mrow><mtext>=</mtext></mrow><mrow><mtext>𝑟</mtext></mrow><mrow><mtext>+</mtext></mrow><mfrac><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>𝑟</mtext></mrow></mrow></mfrac></math></span></p>
<p class="">Or,</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑟</mtext></mrow><mrow><mtext>=0.5×(</mtext></mrow><mrow><mtext>𝑟</mtext></mrow><mrow><mtext>+</mtext></mrow><mfrac><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>𝑟</mtext></mrow></mrow></mfrac><mrow><mtext>)</mtext></mrow></math></span></p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case II: recursion (square root)

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑟</mtext></mrow><mrow><mtext>=0.5×(</mtext></mrow><mrow><mtext>𝑟</mtext></mrow><mrow><mtext>+</mtext></mrow><mfrac><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>𝑟</mtext></mrow></mrow></mfrac><mrow><mtext>)</mtext></mrow></math></span> is a recursive relation</p>
<p class="">Why? If we add superscripts you’ll see</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mrow><mtext>𝑟</mtext></mrow></mrow><mrow><mrow><mtext>next</mtext></mrow></mrow></msup><mrow><mtext>=0.5×</mtext></mrow><mrow><mo>(</mo><mrow><msup><mrow><mrow><mtext>𝑟</mtext></mrow></mrow><mrow><mrow><mtext>current</mtext></mrow></mrow></msup><mrow><mtext>+</mtext></mrow><mfrac><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><msup><mrow><mrow><mtext>𝑟</mtext></mrow></mrow><mrow><mrow><mtext>current</mtext></mrow></mrow></msup></mrow></mfrac></mrow><mo>)</mo></mrow></math></span></p>
<h3>In-class exercise 5</h3>
<p class="">Write a root_recursion function to find the square root of a number.</p>
<p class="">Hint: Start from finding the square root of 7 and then generalize your function.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case II: recursion (square root)

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">Recursive relation is fundamental in guiding the implementation of a recursion function. You’re (or should be) extremely familiar with it</p>
<h3>In-class exercise 6</h3>
<p class="">请推导斐波那契数列的通项公式。它的递推公式为：</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝑎</mtext></mrow></mrow><mrow><mrow><mtext>𝑛</mtext></mrow><mrow><mtext>+2</mtext></mrow></mrow></msub><mrow><mtext>=</mtext></mrow><msub><mrow><mrow><mtext>𝑎</mtext></mrow></mrow><mrow><mrow><mtext>𝑛</mtext></mrow><mrow><mtext>+1</mtext></mrow></mrow></msub><mrow><mtext>+</mtext></mrow><msub><mrow><mrow><mtext>𝑎</mtext></mrow></mrow><mrow><mrow><mtext>𝑛</mtext></mrow></mrow></msub></math></span></p>
<p class="">Please implement a Python function to compute the values of the Fibonacci sequence.</p>
<p class="">Hint: you can choose either approach.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case II: recursion (square root)

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">As a last exercise, we work on an easier one.</p>
<h3>In-class exercise 7</h3>
<p class="">Please write a function to compute the factorial of some number.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case III: map, filter, and reduce

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">Let’s start from the familiar max function. You already know the output of the max function:</p>
<p class="">If you try <code>max(“hello”, “world”, “Python”)</code>, you’ll see Python can also compute the maximum. But what does it mean?</p>

```python
max((1, 2, 3))
max(1, 2, 3, 4)
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case III: map, filter, and reduce

<div class="lecture-content" markdown="1">

<p class="">If we’re not satisfied with the default behavior, we can change it by defining a helper function that</p>
<p class="lecture-subpoint">takes the elements for comparison as parameters</p>
<p class="lecture-subpoint">returns the criterion by which we want to sort</p>

```python
def helper(s):
    return len(s)


max("hello", "world", "Python", key=helper)
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case III: map, filter, and reduce

<div class="lecture-content" markdown="1">

<p class="">Is it unnecessary to define the helper function every time we want to find the maximum of some elements according to some standards. We can abandon the name of the function and just use it.</p>
<p class="">This is known as <strong>anonymous functions</strong></p>
<p class="">The syntax is …</p>

```python
max("hello", "world", "Python", key=lambda x: len(x))
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case III: map, filter, and reduce

<div class="lecture-content" markdown="1">

<p class="">Now let’s turn to three useful <strong>reducing </strong>functions.</p>
<p class="lecture-subpoint">The map function applies a function to every element of a sequence.</p>
<p class="lecture-subpoint">The filter function selects the elements according to a standard. Similar to the helper function in the map function. We need to set the standard as a function. But this time, the return value of the helper function has to be Boolean.</p>

```python
map(len, ("hello", "world", "Python"))
```

```python
def long_string(x):
    return len(x) > 5


filter(long_string, ("hello", "world", "Python"))
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case III: map, filter, and reduce

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 8</h3>
<p class="">Replace the helper function with an anonymous function.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case III: map, filter, and reduce

<div class="lecture-content" markdown="1">

<div class="columns" markdown="1">
<div class="column" markdown="1">
<p class="">The last technique is the reduce function. Unlike the other two, we need to import it from the functools module.</p>
<p class="">The reduce function requires a helper function. The helper function for reduce must</p>
<p class="lecture-subpoint">take two parameters</p>
<p class="lecture-subpoint">return an accumulator that can be combined with the next item</p>
<h3>In-class exercise 9</h3>
<p class="">Search the web and explain what functional programming means.</p>
</div>
<div class="column" markdown="1">

```python
from functools import reduce

reduce(lambda x, y: x + " " + y, ("hello", "world", "Python"))
```


</div>
</div>

</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case IV: generators

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">We have learned iterators (what is an iterator?). Generators are a special way to create iterators. There are several ways we can make generators.</p>
<p class="">We can create our own generators in two ways:</p>
<p class="lecture-subpoint">through generator expression and</p>
<p class="lecture-subpoint">through a generator function.</p>
<h3>In-class exercise 10</h3>
<p class="">List examples of functions that output generators.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case IV: generators (expression)

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">We learned the idea of comprehensions in Chapter 1. The parentheses enclosed comprehensions were not &quot;tuple comprehensions.&quot; They are generators.</p>
<h3>In-class exercise 11</h3>
<p class="">Make a generator to help compute squares (1, 4, 9, 16, ...). What is necessary for you to define a generator like this?</p>

```python
type((x for x in range(5)))
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case IV: generators (function)

<div class="lecture-content" markdown="1">

<p class="">Generator functions are almost the same as regular functions, except that we use the word yield. Wherever in a function there is an yield, the function becomes a generator function.</p>
<p class="">Yield means to give up right to someone else. The yield signs we see on road tell us to give up road right to others.</p>


<figure class="diagram"><img src="images/slide-26-2.webp" alt="Five Function Use Cases: original illustration, slide 26."></figure>

</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case IV: generators (function)

<div class="lecture-content" markdown="1">

<p class="">In a computer program, when a generator function sees yield, it does the same thing. The generator function is suspended and other functions can use the computing resources. When we resume the generator with <code>next()</code> or iteration, it regains the computing resources until it sees yield next time.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case IV: generators (function)

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 2.4.1 generator function</strong></p>

```python
import time

def g():
    print(f'g() sleeping: gi_state: {g1.gi_running}')
    time.sleep(3)
    print(f'g() sees yield: gi_state: {g1.gi_running}')
    yield 1


g1 = g()
next(g1)
print("after, gi_state:", g1.gi_running)
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case IV: generators (function)

<div class="lecture-content" markdown="1">

<p class="">Now we see how generator function works, and we can define a generator with it. Suppose we want to compute the squares of integers from 1 to infinity. This is impossible if we are using a list (why?). But with a generator, we don&#x27;t need to store all squares in computer. Just compute them on-the-fly.</p>

```python
def squares():
    i = 1
    while True:
        yield i ** 2
        i += 1
```


</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case V: Error message

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<div class="columns" markdown="1">
<div class="column" markdown="1">
<p class="">We introduce error message reading and handling here.</p>
<p class="">To handle an error, we rely on the <strong>try-except </strong>control flow.</p>
<p class="lecture-subpoint">The following code shows you how to print a hand-written number:</p>
</div>
<div class="column" markdown="1">

```python
with open("../data/numbers/number1.csv", "r") as f:
    header = f.readline()
    data = f.readline()


import matplotlib.pyplot as plt
import numpy as np

pixels = np.array(data.split(","), dtype='uint8').reshape((28, 28))
plt.imshow(pixels)
plt.imsave("./mnist1.png", pixels)
```


</div>
</div>

</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case V: Error message

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<p class="">You can see that the flow is interrupted because of an error. But all other pictures are good. Checking all data before we plot and save the pictures is a daunting task. So we need to rely on the try-except control flow. The syntax is as follows:</p>
<h3>In-class exercise 12</h3>
<p class="">Plot and save all numbers in the numbers folder.</p>




</div>

---

<!-- slide: lecture-import -->

## 2.4 Use case V: Error message

<div class="lecture-content" markdown="1">



```python
try:
    ...
except KeyError as e:
    ...
else:
    ...
finally:
    ...
```


</div>

---

<!-- slide: lecture-import -->

## 2.5 PEP 8

<div class="lecture-content" markdown="1">

<p class="">The Python Enhancement Proposals (PEPs) are a set of documents aiming at improving the Python programming language.</p>
<p class=""><a href="https://peps.python.org/pep-0008/">PEP 8</a> is a <strong>style guide </strong>for coding in Python.</p>
<p class="lecture-subpoint">It is not required.</p>
<p class="lecture-subpoint">It is recommended.</p>




</div>

---

<!-- slide: lecture-import -->

## References and read more

<span class="aol">AoL 5 (H)</span>

<div class="lecture-content" markdown="1">

<p class=""><a href="https://www.bilibili.com/video/BV1Y2421A7sB/?spm_id_from=333.337.search-card.all.click&amp;vd_source=ec7b194853f6121829b0f428c7736022">https://www.bilibili.com/video/BV1Y2421A7sB/?spm_id_from=333.337.search-card.all.click&amp;vd_source=ec7b194853f6121829b0f428c7736022</a></p>
<p class="">Mastering Functional Programming with Python, Steven Lott, 2015</p>




</div>
