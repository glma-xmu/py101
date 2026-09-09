---
title: 'Chapter 2 Project · Project: Function Practice'
description: Eight practice problems drawn from class and past exams.
lang: en
source: resource/deck2_project_AoL.pptx
sections:
- id: practice-overview
  title: Practice overview
  start: 1
  level: 1
  textbook: ch2-1-defining-functions-0
  related: true
- id: dictionary-mapping
  title: Dictionary mapping
  start: 3
  level: 1
  textbook: ch1-2-collections-4
  related: true
- id: bank-account-closure
  title: Bank account closure
  start: 4
  level: 1
  textbook: ch2-3-first-class-5
  related: true
- id: type-checking-decorator
  title: Type-checking decorator
  start: 5
  level: 1
  textbook: ch2-4-use-cases-2
  related: true
- id: numerical-integration
  title: Numerical integration
  start: 6
  level: 1
  textbook: ch2-3-first-class-3
  related: true
- id: counting-runs
  title: Counting runs
  start: 7
  level: 1
  textbook: ch1-3-control-flow-2
  related: true
- id: timing-decorator
  title: Timing decorator
  start: 8
  level: 1
  textbook: ch2-4-use-cases-2
  related: true
- id: secant-method
  title: Secant method
  start: 9
  level: 1
  textbook: ch2-1-defining-functions-6
  related: true
- id: two-generators
  title: Two generators
  start: 10
  level: 1
  textbook: ch2-4-use-cases-5
  related: true
---


<!-- slide: title-slide -->
<p class="eyebrow">Chapter 2 Project</p>

# Project: Function Practice

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">A few practice questions on functions</p>
<p class="lecture-subpoint">from past exams</p>
<p class="lecture-subpoint">the ones mimicking what you expect to see in the midterm</p>




</div>

---

<!-- slide: lecture-import -->

## 1. MBTI simplified

<div class="lecture-content" markdown="1">

<p class="">What’s your MBTI type? Let’s find out.</p>
<p class="">But MBTI determination has too many questions, let’s use a simpler version  SBTI conversion</p>
<p class="">IF you SBTI type is “ATM-er”, you probably are ENFJ/ESFJ</p>
<p class="">Other maps are:</p>
<p class="lecture-subpoint">IMFW  INFP/INTJ</p>
<p class="lecture-subpoint">LOVER-R  ENFP/ESFP</p>
<p class="lecture-subpoint">FAKE  ENFJ/INFJ</p>
<p class="">Write a function that takes in SBTI and produces MBTI.</p>




</div>

---

<!-- slide: lecture-import -->

## 2. Bank account

<div class="lecture-content" markdown="1">

<p class="">A bank creates account for each customer, allowing the customers to change their username and view the balance. The initial balance is set by the bank.</p>
<p class="">Write a nested function to:</p>
<p class="lecture-subpoint">Create users and store each user’s bank account privately (so others cannot change it). Hint: use nonlocal variables.</p>
<p class="lecture-subpoint">Write an inner function change_name.</p>
<p class="lecture-subpoint">Write an inner function view_balance.</p>




</div>

---

<!-- slide: lecture-import -->

## 3. Decorator

<div class="lecture-content" markdown="1">

<p class="">Write a decorator to check the types of inputs of functions. Suppose the decorated function has <strong>only one </strong>parameter.</p>
<p class="">For example, when I call sum([1, 2, 3]), the output should be:</p>
<p class="lecture-subpoint">Ah-ha! The input is a list.</p>
<p class="lecture-subpoint">6</p>




</div>

---

<!-- slide: lecture-import lecture-small-figure -->

## 4. Numerical integration

<div class="lecture-content" markdown="1">

<p class="">You have learned (torturing, right?) integration. In Python, nothing is difficult.</p>
<p class="">Write a function to help you compute integrals.</p>
<p class="">The inputs are a function and the integration area (supposing one variable). The output is the integral.</p>
<p class="">The integral can be approximated as</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>Δ</mtext></mrow><mrow><mtext>×[</mtext></mrow><mrow><mtext>𝑓</mtext></mrow><mrow><mo>(</mo><mrow><mrow><mtext>𝑎</mtext></mrow></mrow><mo>)</mo></mrow><mrow><mtext>+</mtext></mrow><mrow><mtext>𝑓</mtext></mrow><mrow><mo>(</mo><mrow><mrow><mtext>𝑎</mtext></mrow><mrow><mtext>+</mtext></mrow><mrow><mtext>Δ</mtext></mrow></mrow><mo>)</mo></mrow><mrow><mtext>+</mtext></mrow><mrow><mtext>𝑓</mtext></mrow><mrow><mo>(</mo><mrow><mrow><mtext>𝑎</mtext></mrow><mrow><mtext>+2</mtext></mrow><mrow><mtext>Δ</mtext></mrow></mrow><mo>)</mo></mrow><mrow><mtext>+…+</mtext></mrow><mrow><mtext>𝑓</mtext></mrow><mrow><mo>(</mo><mrow><mrow><mtext>𝑏</mtext></mrow></mrow><mo>)</mo></mrow><mrow><mtext>]</mtext></mrow></math></span></p>
<p class="">Hint: How do you determine the step <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>Δ</mtext></mrow></math></span>?</p>


<figure class="diagram"><img src="images/slide-06-2.webp" alt="Project: Function Practice: original illustration, slide 6."></figure>

</div>

---

<!-- slide: lecture-import -->

## 5. Question 3 from midterm of 2024 Fall

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

## 6. Question 4 from midterm of 2024 Fall

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

## 7. Quasi-Newton’s method

<div class="lecture-content" markdown="1">

Newton’s method needs a derivative and a suitable starting point. The **secant method** approximates the derivative using two previous iterates:

<span class="lecture-math"><math display="block" xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>x</mi><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>x</mi><mi>n</mi></msub><mo>−</mo><mfrac><mrow><mi>f</mi><mo>(</mo><msub><mi>x</mi><mi>n</mi></msub><mo>)</mo><mo>(</mo><msub><mi>x</mi><mi>n</mi></msub><mo>−</mo><msub><mi>x</mi><mrow><mi>n</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>)</mo></mrow><mrow><mi>f</mi><mo>(</mo><msub><mi>x</mi><mi>n</mi></msub><mo>)</mo><mo>−</mo><mi>f</mi><mo>(</mo><msub><mi>x</mi><mrow><mi>n</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>)</mo></mrow></mfrac></math></span>

Implement the method and solve **f(x) = |x − 3| − 1 = 0**.

Choose two initial values and a stopping rule. Consider what to do if the denominator becomes zero.

</div>

---

<!-- slide: lecture-import -->

## 8. Generator

<div class="lecture-content" markdown="1">

<p class="">Make two generators.</p>
<p class="lecture-subpoint">generator 1 is in charge of printing a line: “it is an odd second.” and saves the current time for future use.</p>
<p class="lecture-subpoint">generator 2 is in charge of printing a line: “it is an even second.” and saves the current time for future use.</p>
<p class="">Then write a function, which calls the two generators depending on if the current time.time() has an even or odd integer part.</p>




</div>
