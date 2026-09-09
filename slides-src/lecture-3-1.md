---
title: Lecture 3.1 · NumPy
description: Arrays, vectorization, broadcasting, matrix operations, and views versus
  copies.
lang: en
source: resource/deck3_1.pptx
sections:
- id: introduction
  title: Introduction
  start: 1
  level: 1
  textbook: ch3-1-numpy-0
- id: installing-numpy
  title: Installing NumPy
  start: 4
  level: 1
  textbook: ch3-1-numpy-1
- id: the-ndarray
  title: The ndarray
  start: 5
  level: 1
  textbook: ch3-1-numpy-2
- id: vectorization
  title: Vectorization
  start: 11
  level: 1
  textbook: ch3-1-numpy-3
- id: matrix-operations-and-broadcasting
  title: Matrix operations and broadcasting
  start: 15
  level: 1
  textbook: ch3-1-numpy-4
- id: transpose-and-reshape
  title: Transpose and reshape
  start: 19
  level: 1
  textbook: ch3-1-numpy-5
- id: vectorization-and-ufuncs
  title: Vectorization and ufuncs
  start: 22
  level: 1
  textbook: ch3-1-numpy-6
- id: views-and-copies
  title: Views and copies
  start: 31
  level: 1
  textbook: ch3-1-numpy-7
---


<!-- slide: title-slide -->
<p class="eyebrow">Lecture 3.1</p>

# NumPy

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

<!-- slide: lecture-import -->

## Original classroom announcement

<div class="lecture-content" markdown="1">

<p class="caption">Preserved from the source lecture; these are historical discussion prompts, not the current course schedule.</p>

### Midterm discussion

- May 6 or May 8?
- Is a computer-based test feasible?

### Homework questions

- Grading?
- Confusions?

</div>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">A new and more general data structure: array</p>
<p class="">Introductory numpy data structure: ndarray</p>
<p class="">Basic numpy functions</p>
<p class="lecture-subpoint"><strong>You’ll need to read a lot of function documents.</strong></p>
<p class="">Matrix operations with numpy</p>
<p class="lecture-subpoint">the broadcast mechanism</p>
<p class="lecture-subpoint">*accelerating by vectorization</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1 The NumPy module

<div class="lecture-content" markdown="1">

Install NumPy and pandas into the Python environment used by your notebook. In an IPython/Jupyter notebook cell:

```text
%pip install numpy pandas
```

In a terminal, with the intended environment activated:

```bash
python -m pip install numpy pandas
```

We will mostly use pandas, but NumPy provides important tools for working with arrays. This lecture covers a small part of the library.

[NumPy’s official beginner’s guide](https://numpy.org/doc/stable/user/absolute_beginners.html)

</div>

---

<!-- slide: lecture-import -->

## 3.1.1 ndarray

<div class="lecture-content" markdown="1">

<p class="caption">source: https://towardsdatascience.com/introducing-numpy-part-1-understanding-arrays-3f6fecc97e3d/</p>


<figure class="diagram"><img src="images/slide-05-1.webp" alt="NumPy: original illustration, slide 5."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.1.1 The numpy module (ndarrays)

<div class="lecture-content" markdown="1">

<p class="">We&#x27;ve learned that a complex data type can hold several elements (e.g., a list or a tuple). A similar idea of putting numbers into a sequence gives rise to the <strong>array</strong> type. According to the numpy document,</p>
<p class="lecture-subpoint">&quot;In computer programming, an array is a structure for storing and retrieving data.&quot;</p>
<p class="">We emphasize two features of numpy arrays:</p>
<p class="lecture-subpoint">They have fixed sizes (number of elements).</p>
<p class="lecture-subpoint">The elements must be of the same type.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1.1 The numpy module (ndarrays)

<div class="lecture-content" markdown="1">

<p class="">Let’s create some arrays</p>
<p class="">We can use the dtype<strong> </strong>(stands for <strong>d</strong>ata <strong>type</strong>) parameter to specify the type of the elements.</p>

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([1, 2, 'a'])
c = np.array([a, b])
# d = np.array([a, 'python'])
```

```python
a = np.array([1, 2, 3])
print(a)
a = np.array(a, dtype=float)
print(a)
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.1 The numpy module (ndarrays)

<div class="lecture-content" markdown="1">

<p class="">The numpy module also provides us with some useful functions to create special ndarrays:</p>
<p class="lecture-subpoint"><a href="https://numpy.org/doc/2.0/reference/generated/numpy.ones.html">ones</a> that creates all-one ndarrays</p>
<p class="lecture-subpoint"><a href="https://numpy.org/doc/2.0/reference/generated/numpy.zeros.html">zeros</a> that creates all-zero ndarrays</p>
<p class="lecture-subpoint"><a href="https://numpy.org/doc/stable/reference/generated/numpy.eye.html">eye</a> that creates diagonal matrices</p>
<p class="lecture-subpoint"><a href="https://numpy.org/doc/stable/reference/random/generated/numpy.random.random.html">random.random</a> for random ndarrays with entries <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑥</mtext></mrow><mrow><mtext>:0&lt;</mtext></mrow><mrow><mtext>𝑥</mtext></mrow><mrow><mtext>&lt;1</mtext></mrow></math></span></p>
<p class="lecture-subpoint"><a href="https://numpy.org/doc/2.0/reference/random/generated/numpy.random.normal.html">random.normal</a> for random ndarrays with entries <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑥</mtext></mrow></math></span> normally distributed</p>
<p class="lecture-subpoint"><a href="https://numpy.org/doc/2.0/reference/random/generated/numpy.random.randint.html">random.randint</a> for random ndarrays with entries randomly drwan</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1.1 The numpy module (ndarrays)

<div class="lecture-content" markdown="1">

<p class="">We can use numpy.arange to make a range-like object.</p>
<p class="">We can use numpy.linspace to create sequence.</p>
<h3>In-class exercise 1</h3>
<p class="">Create a 3-D ndarray. Each entry of this ndarray should follow a normal distribution with mean 5 and standard deviation 3.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1.1 The numpy module (ndarrays)

<div class="lecture-content" markdown="1">

<p class="">We can use <a href="https://numpy.org/doc/stable/reference/generated/numpy.arange.html">numpy.arange</a> to make a range-like object.</p>
<p class="">We can use <a href="https://numpy.org/doc/stable/reference/generated/numpy.linspace.html">numpy.linspace</a> to create sequence.</p>
<h3>In-class exercise 1</h3>
<p class="">Create a 3-D ndarray. Each entry of this ndarray should follow a normal distribution with mean 5 and standard deviation 3.</p>
<h3>In-class exercise 2</h3>
<p class="">What’s the difference between numpy.arange and numpy.linspace?</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1.2 Vectorization

<div class="lecture-content" markdown="1">

<p class="caption">source: https://pabloinsente.github.io/intro-numpy-fundamentals</p>


<figure class="diagram"><img src="images/slide-11-1.webp" alt="NumPy: original illustration, slide 11."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.1.2 The numpy module (vectorization)

<div class="lecture-content" markdown="1">

<p class="">What makes numpy so popular and important in Python data analysis is its power in math operations, especially matrix algebra. This makes numpy efficient in dealing with vector and matrix operations. Some <a href="https://github.com/rougier/from-python-to-numpy/blob/master/02-introduction.rst">authors</a> even wrote</p>
<p class="">&quot;NumPy is all about vectorization.&quot;</p>
<p class="">numpy is implemented in the C programming language and is very fast even though we write code in Python.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1.2 The numpy module (vectorization)

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 3.1.2.1 How much faster is numpy than list?</strong></p>

```python
import numpy as np
import time
size = 10_000_000

python_list = list(range(size))
numpy_array = np.arange(size, dtype=np.int64)

# List timing
stime = time.perf_counter()
python_list_squared = [x**2 for x in python_list]
etime = time.perf_counter()
list_time = etime - stime
print(f"Time taken by list: {list_time:.5f} seconds")
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.2 The numpy module (vectorization)

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 3.1.2.1 (Continued)</strong></p>

```python
# numpy timing
stime = time.perf_counter()
numpy_array_squared = numpy_array**2
etime = time.perf_counter()
numpy_time = etime - stime
print(f"Time taken by NumPy array: {numpy_time:.5f} seconds")

# results
print(f"NumPy is {list_time / numpy_time:.2f} times faster than lists in this example.")
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.3 Linear algebra

<div class="lecture-content" markdown="1">

<p class="caption">source: https://www.britannica.com/science/linear-algebra</p>


<figure class="diagram"><img src="images/slide-15-1.webp" alt="NumPy: original illustration, slide 15."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.1.3 The numpy module (matrix algebra)

<div class="lecture-content" markdown="1">

<p class="">In linear algebra, you learn how to add two matrices, as long as the <strong>dimensions</strong> <strong>match</strong>:</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝑀</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow></msub><mrow><mtext>=</mtext></mrow><mrow><mo>(</mo><mrow><mtable><mtr><mtd><mrow><mrow><mtext>1</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>2</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>3</mtext></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mrow><mtext>4</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>5</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>6</mtext></mrow></mrow></mtd></mtr></mtable></mrow><mo>)</mo></mrow><mrow><mtext>, </mtext></mrow><msub><mrow><mrow><mtext>𝑀</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msub><mrow><mtext>=</mtext></mrow><mrow><mo>(</mo><mrow><mtable><mtr><mtd><mrow><mrow><mtext>6</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>5</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>4</mtext></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mrow><mtext>3</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>2</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>1</mtext></mrow></mrow></mtd></mtr></mtable></mrow><mo>)</mo></mrow></math></span></p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝑀</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow></msub><mrow><mtext>+</mtext></mrow><msub><mrow><mrow><mtext>𝑀</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msub><mrow><mtext>=(</mtext></mrow><mtable><mtr><mtd><mrow><mrow><mtext>7</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>7</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>7</mtext></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mrow><mtext>7</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>7</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>7</mtext></mrow></mrow></mtd></mtr></mtable><mrow><mtext>)</mtext></mrow></math></span></p>
<h3>In-class exercise 3</h3>
<p class="">Use lists to implement the above matrix addition.</p>
<p class="">Use numpy to implement the above matrix addition.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1.3 The numpy module (matrix algebra)

<div class="lecture-content" markdown="1">

<p class="">We can add a one-dimensional array across the rows of a matrix</p>
<p class="">The mechanism that numpy introduce when we use math operators (+, -, *, /, etc.) is called <a href="https://numpy.org/doc/stable/user/basics.broadcasting.html"><strong>broadcasting</strong></a>. It means that the “smaller” ndarray is broadcast to each element of the “larger” ndarray.</p>

```python
m1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
v1 = np.array([1, 1, 1])
m1 + v1
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.3 The numpy module (matrix algebra)

<div class="lecture-content" markdown="1">

<h3>In-class exercise 4</h3>
<p class="">What does it mean by smaller and larger?</p>
<p class="">What if the size does not match any of the dimensions?</p>

```python
m = np.array([[1, 2], [4, 5], [7, 8]])
v = np.array([1, 1])
A = np.ones((2, 3))
B = np.ones((2,))
x = np.ones((4, 2, 3))
y = np.ones((4, 3))
```

```python
m1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
v1 = np.array([1, 1])
m1 + v1
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.3 The numpy module (matrix algebra)

<div class="lecture-content" markdown="1">

<p class="">In linear algebra, we also learned how to <a href="https://numpy.org/doc/2.2/reference/generated/numpy.ndarray.T.html">transpose a matrix</a>:</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝑀</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow></msub><mrow><mtext>=</mtext></mrow><mrow><mo>(</mo><mrow><mtable><mtr><mtd><mrow><mrow><mtext>1</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>2</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>3</mtext></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mrow><mtext>4</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>5</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>6</mtext></mrow></mrow></mtd></mtr></mtable></mrow><mo>)</mo></mrow><mrow><mtext>, </mtext></mrow><msubsup><mrow><mrow><mtext>𝑀</mtext></mrow></mrow><mrow><mrow><mtext>1</mtext></mrow></mrow><mrow><mrow><mtext>T</mtext></mrow></mrow></msubsup><mrow><mtext>=</mtext></mrow><mrow><mo>(</mo><mrow><mtable><mtr><mtd><mrow><mrow><mtext>1</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>4</mtext></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mrow><mtext>2</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>5</mtext></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mrow><mtext>3</mtext></mrow></mrow></mtd><mtd><mrow><mrow><mtext>6</mtext></mrow></mrow></mtd></mtr></mtable></mrow><mo>)</mo></mrow></math></span></p>
<p class="">This can also be done with numpy:</p>

```python
m1 = np.array([
    [ 0, 1, 2, 3],
    [ 4, 5, 6, 7],
    [ 8, 9, 10, 11]
  ])

m1T = m1.T
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.3 The numpy module (matrix algebra)

<div class="lecture-content" markdown="1">

<h3>In-class exercise 4</h3>
<p class="">There is a <a href="https://numpy.org/doc/2.2/reference/generated/numpy.transpose.html">numpy.transpose</a>. What’s the difference with .T?</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1.3 The numpy module (matrix algebra)

<div class="lecture-content" markdown="1">

<p class="">The numpy.ndarray is even more flexible, we can use the <a href="https://numpy.org/doc/2.0/reference/generated/numpy.reshape.html">.reshape</a> method to change the shape of a numpy.ndarray.</p>

```python
m11 = m1.reshape(12)
print(m11, ":", m11.shape)

m12 = m1.reshape([12,])
print(m12, ":", m12.shape)

m13 = m1.reshape([12, 1])
print(m13.T, ":", m13.shape)

m14 = m1.reshape([2, 6])
print(m14.T, ":", m14.shape)
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.4 Vectorization (again)

<div class="lecture-content" markdown="1">

<p class="caption">source: https://pabloinsente.github.io/intro-numpy-fundamentals</p>


<figure class="diagram"><img src="images/slide-22-1.webp" alt="NumPy: original illustration, slide 22."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.1.4 Revisit vectorization

<div class="lecture-content" markdown="1">

<p class="">numpy is fasters because of its vectorized nature. recall that we once tried to add a number to a list:</p>
<p class="lecture-subpoint">and there was an error.</p>
<p class="lecture-subpoint">But with numpy.ndarray, we can easily add a scalar to an array.</p>

```python
lst = [1, 2, 3]
lst + 4
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.4 Revisit vectorization

<div class="lecture-content" markdown="1">

<p class="">More generally, we introduce some <strong>universal functions (</strong><strong>ufuns</strong><strong>)</strong> of numpy. The reason is not only their speed but also their ease of use. We&#x27;ve seen that list operations are much slower than ndarray. Now let&#x27;s focus our attention on the comparison between loops and ufuns, both applied to a ndarray. (Part of the code are excerpts from <a href="https://jakevdp.github.io/PythonDataScienceHandbook">Python Data Science Handbook</a> by Jake Vanderplas.)</p>
<p class="">Let&#x27;s start with &quot;normal&quot; functions.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1.4 Revisit vectorization

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 3.1.4.1</strong></p>

```python
def timer_100(func):
    times = []
    def wrapper(*args, **kwargs):
        for i in range(100):
            stime = time.perf_counter()
            func(*args, **kwargs)
            etime = time.perf_counter()
            times.append(etime - stime)
        avg = np.mean(times)
        std = np.std(times)
        print(f"The average run time is {avg:.6f}s; the std is {std:.6f}s")
    return wrapper
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.4 Revisit vectorization

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 3.1.4.1</strong></p>

```python
@timer_100
def compute_reciprocals(nums):
    output = np.empty(len(nums))
    for i in range(len(nums)):
        output[i] = 1.0 / nums[i]
    return output


compute_reciprocals(np.random.randint(1, 10, size=10_000))
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.4 Revisit vectorization

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 3.1.4.1</strong></p>
<h3>In-class exercise 7</h3>
<p class="">Although we saw that the time difference was huge between compute_reciprocals and numpy_reciprocals, we haven&#x27;t checked if the answers are correct. Verify the correctness of these two functions.</p>

```python
@timer_100
def numpy_reciprocals(nums):
    return 1.0 / nums


numpy_reciprocals(np.random.randint(1, 10, size=10_000))
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.4 Universal functions and vectorize

<div class="lecture-content" markdown="1">

NumPy’s universal functions (**ufuncs**) operate elementwise. Examples include `abs`, `sin`, `cos`, `tan`, `arcsin`, `arccos`, `arctan`, `exp`, and `log`.

`expm1(x)` computes exp(x) − 1, and `log1p(x)` computes log(1 + x), with improved accuracy near zero.

`np.vectorize` wraps a Python callable so that it accepts array inputs. It is a **convenience interface**, not a way to compile a function or automatically make its loop fast.

[NumPy: vectorize](https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html)

</div>

---

<!-- slide: lecture-import -->

## 3.1.4 Revisit vectorization

<div class="lecture-content" markdown="1">

<p class="">An example</p>
<h3>In-class exercise 8</h3>
<p class="">Read the documentation and write your own function to compute <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑓</mtext></mrow><mrow><mtext>(</mtext></mrow><mrow><mtext>𝑥</mtext></mrow><mrow><mtext>)=1/(1 + </mtext></mrow><msup><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mrow><mrow><mtext>2</mtext></mrow></mrow></msup><mrow><mtext>)</mtext></mrow></math></span>. Then test the speed of the vectorized function.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1.4 Revisit vectorization

<div class="lecture-content" markdown="1">

<h3>In-class exercise 9</h3>
<p class="">Read the documentation of the <a href="https://numpy.org/doc/stable/reference/generated/numpy.min.html">min</a> and <a href="https://numpy.org/doc/stable/reference/generated/numpy.mean.html">mean</a> functions. Given a ndarray</p>
<p class="lecture-subpoint">select those entries whose values are greater than 3 (the <a href="https://numpy.org/doc/2.0/reference/maskedarray.html"><strong>mask</strong></a>);</p>
<p class="lecture-subpoint">find the min value of each row;</p>
<p class="lecture-subpoint">find the mean of each column.</p>

```python
arr = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.5 View and Copy

<div class="lecture-content" markdown="1">

<p class="caption">source: https://www.dataquest.io/blog/settingwithcopywarning/</p>


<figure class="diagram"><img src="images/slide-31-1.webp" alt="NumPy: original illustration, slide 31."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.1.5 View vs. copy

<div class="lecture-content" markdown="1">

<p class="">A very complex phenomenon of numpy is the difference between a <strong>view</strong> and a <strong>copy</strong>. If we use analogy, a view offers us a way to look at the data so the data remains itself (no subdata is taken out). A copy, on the contrary, means we create a subdata and give it a new name. The main difference between a view and a copy is when we change their contents. For example, y is a view of part of x below:</p>

```python
x = np.arange(10)
y = x[1:3]
print(f"before changing x, y: {y}")
x[1:3] = [10, 11]
print(f"after changing x, y: {y}")
```


</div>

---

<!-- slide: lecture-import -->

## 3.1.5 View vs. copy

<div class="lecture-content" markdown="1">

<div class="columns" markdown="1">
<div class="column" markdown="1">
<p class="">We can check if y is a view of x using the .base attribute:</p>
<p class="">We will not talk too much for now. You can find more of it from <a href="https://numpy.org/doc/2.0/user/basics.copies.html">here</a>.</p>
<p class="">Further readings:</p>
<p class="lecture-subpoint"><a href="https://numpy.org/doc/2.0/user/basics.copies.html">https://numpy.org/doc/2.0/user/basics.copies.html</a></p>
<p class="lecture-subpoint"><a href="https://scipy-cookbook.readthedocs.io/items/ViewsVsCopies.html">https://scipy-cookbook.readthedocs.io/items/ViewsVsCopies.html</a></p>
<p class="lecture-subpoint"><a href="https://stackoverflow.com/questions/47181092/numpy-views-vs-copy-by-slicing">https://stackoverflow.com/questions/47181092/numpy-views-vs-copy-by-slicing</a></p>
</div>
<div class="column" markdown="1">

```python
y.base is x
```


</div>
</div>

</div>
