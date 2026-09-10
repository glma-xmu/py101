---
title: 'Chapter 2 Project · Project: Function Practice'
description: Four practice problems drawn from class and past exams.
lang: en
source: ../course materials/deck2_3_project.pptx
sections:
- id: practice-overview
  title: Practice overview
  start: 1
  level: 1
  textbook: ch2-1-defining-functions-0
  related: true
- id: counting-runs
  title: Counting runs
  start: 3
  level: 1
  textbook: ch1-3-control-flow-2
  related: true
- id: timing-decorator
  title: Timing decorator
  start: 4
  level: 1
  textbook: ch2-4-use-cases-2
  related: true
- id: secant-method
  title: Secant method
  start: 5
  level: 1
  textbook: ch2-1-defining-functions-6
  related: true
- id: two-generators
  title: Two generators
  start: 6
  level: 1
  textbook: ch2-4-use-cases-5
  related: true
---

<!-- slide: title-slide -->

<p class="eyebrow">Chapter 2 Project</p>

# Project: Function Practice

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2025</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">A few practice questions on functions</p>
<p class="lecture-subpoint">from past exams</p>
<p class="lecture-subpoint">the ones mimicking what you expect to see in the midterm</p>




</div>

---

<!-- slide: lecture-import -->

## 1. Question 3 from midterm of 2024 Fall

<div class="lecture-content" markdown="1">

<div class="columns" markdown="1">
<div class="column" markdown="1">
<p class="">If we toss a coin, it has two possible outcomes: head and tail. When a head (the number 1) appears, we write a “1” on a piece of paper. If a tail (flower) appears, we write a “0”. We toss the coin n times, and record all the outcomes.</p>
<p class="lecture-subpoint">For example:</p>
<p class="lecture-subpoint">This sequence is recorded as 1 0 1 1 1 0 1 0 1 1 0 0.</p>
<p class="">We define consecutive 1s as a run. So this sequence has 4 runs.</p>
<p class="lecture-subpoint">In Python, you can use the following code to generate a random sequence:</p>
<p class="">Please make a function to compute the number of runs of a sequence.</p>
</div>
<div class="column" markdown="1">

```python
import random
n = 10
s1 = [random.randint(0, 1) for _ in range(n)]
```
<figure class="diagram"><img src="images/slide-07-2.webp" alt="Project: Function Practice: original illustration, slide 7."></figure>

</div>
</div>

</div>

---

<!-- slide: lecture-import -->

## 2. Question 4 from midterm of 2024 Fall

<div class="lecture-content" markdown="1">

<p class="">For programmers, an important aspect of their code is the speed. Hence, it is common for programmers to try different ways to write functions. They will then test how long it takes to run each version of their code. To simplify the process, please make a decorator that can run the decorated function 100 times. Then after the function call, print a line including the average time and standard deviation of the 100 times. Please name this decorator timer_100.</p>
<p class="lecture-subpoint">sample usage:</p>
<p class="lecture-subpoint">sample output:</p>

```python
import random
@timer_100
def sums():
    numbers = [random.random() for _ in range(10000)]
    sum(numbers)
sums()
```

```text
The average run time is 0.000609s; the std is 0.000076s.
```


</div>

---

<!-- slide: lecture-import -->

## 3. Quasi-Newton’s method

<div class="lecture-content" markdown="1">

Newton’s method needs a derivative and a suitable starting point. The **secant method** approximates the derivative using two previous iterates:

<span class="lecture-math"><math display="block" xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>x</mi><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>x</mi><mi>n</mi></msub><mo>−</mo><mfrac><mrow><mi>f</mi><mo>(</mo><msub><mi>x</mi><mi>n</mi></msub><mo>)</mo><mo>(</mo><msub><mi>x</mi><mi>n</mi></msub><mo>−</mo><msub><mi>x</mi><mrow><mi>n</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>)</mo></mrow><mrow><mi>f</mi><mo>(</mo><msub><mi>x</mi><mi>n</mi></msub><mo>)</mo><mo>−</mo><mi>f</mi><mo>(</mo><msub><mi>x</mi><mrow><mi>n</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>)</mo></mrow></mfrac></math></span>

Implement the method and solve **f(x) = |x − 3| − 1 = 0**.

Choose two initial values and a stopping rule. Consider what to do if the denominator becomes zero.

</div>

---

<!-- slide: lecture-import -->

## 4. Generator

<div class="lecture-content" markdown="1">

<p class="">Make two generators.</p>
<p class="lecture-subpoint">generator 1 is in charge of printing a line: “it is an odd second.” and saves the current time for future use.</p>
<p class="lecture-subpoint">generator 2 is in charge of printing a line: “it is an even second.” and saves the current time for future use.</p>
<p class="">Then write a function, which calls the two generators depending on if the current time.time() has an even or odd integer part.</p>




</div>
