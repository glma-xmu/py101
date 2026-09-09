---
title: 'Lecture 3.2 · pandas: One Table'
description: Series, DataFrames, sorting, aggregation, indexing, and rolling windows.
lang: en
source: resource/deck3_2_AoL.pptx
sections:
- id: introduction
  title: Introduction
  start: 1
  level: 1
  textbook: ch3-2-pandas-0
- id: data-organization
  title: Data organization
  start: 3
  level: 1
  textbook: ch3-2-pandas-2
- id: series
  title: Series
  start: 10
  level: 1
  textbook: ch3-2-pandas-3
- id: dataframes
  title: DataFrames
  start: 11
  level: 1
  textbook: ch3-2-pandas-4
- id: sorting
  title: Sorting
  start: 15
  level: 1
  textbook: ch3-2-pandas-5
- id: aggregation
  title: Aggregation
  start: 17
  level: 1
  textbook: ch3-2-pandas-6
- id: reading-and-writing-data
  title: Reading and writing data
  start: 20
  level: 1
  textbook: ch3-2-pandas-7
- id: stack-unstack-and-multiindex
  title: Stack, unstack, and MultiIndex
  start: 22
  level: 1
  textbook: ch3-2-pandas-10
- id: loc-and-iloc
  title: Loc and iloc
  start: 27
  level: 1
  textbook: ch3-2-pandas-9
- id: practice-new-columns
  title: 'Practice: new columns'
  start: 30
  level: 1
  textbook: ch3-2-pandas-8
- id: lead-lag-and-rolling-windows
  title: Lead, lag, and rolling windows
  start: 32
  level: 1
  textbook: ch3-2-pandas-11
- id: practice-aggregation
  title: 'Practice: aggregation'
  start: 36
  level: 1
  textbook: ch3-2-pandas-6
  related: true
---


<!-- slide: title-slide -->
<p class="eyebrow">Lecture 3.2</p>

# pandas: One Table

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">Data organization</p>
<p class="lecture-subpoint">pandas.DataFrame = 2D numpy array + row info + col info</p>
<p class="lecture-subpoint">Fetching --- taking out rows of a table</p>
<p class="lecture-subpoint">Fetching --- taking out columns of a table</p>
<p class="">Summarizing information in a table</p>
<p class="lecture-subpoint">Sort to prioritize rows</p>
<p class="lecture-subpoint">Aggregation to see a common trend</p>
<p class="">MultiIndexed DataFrame</p>
<p class="">The loc and iloc property, making new columns</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1 Prelude: What is data

<div class="lecture-content" markdown="1">

<p class="caption">pic source: https://zebrabi.com/how-to-pull-information-from-another-sheet-in-excel/</p>


<figure class="diagram"><img src="images/slide-03-1.webp" alt="pandas: One Table: original illustration, slide 3."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.1 Prelude -- working with data

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">We now officially start our journey to work with <strong>datasets</strong>. A data set is where data are stored. Because most datasets appear as <strong>tables</strong>, we use the terms dataset and data table interchangeably. The pandas module specializes in analyzing data tables.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1 Prelude -- working with data

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">Data tables are the most important <strong>carrier</strong> of information. But the information doesn&#x27;t always speak for itself. So we need to <strong>analyze</strong> the data to reveal the information.</p>
<p class="">By looking at one data table, you’ll be able to explain</p>
<p class="lecture-subpoint">how a data table is organized (what the rows and columns of that table represent)</p>
<p class="lecture-subpoint">how to apply some basic manipulations (get the information from the table).</p>
<p class="">These manipulations help us look at the data from different perspectives by changing the format of the table.</p>
<p class="lecture-subpoint">They help us find the specific character of a specific person by locating it.</p>
<p class="lecture-subpoint">These help us divide the data table into smaller ones called groups and summarize information in each group.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1 Prelude – data organization

<span class="aol">AoL 5 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">In <strong>economics</strong>, we often need to work with data. From data, we can gain insights about how the economic world operates. We can also verify our economic theory with data. Such data include a country&#x27;s GDP, a person&#x27;s consumption details, the price of an item, etc. As computing power improves, economic data is growing ever larger. It&#x27;s now common to see data sets of several GB or even TB.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.1 Prelude – data organization

<div class="lecture-content" markdown="1">

<p class="">In <strong>computers</strong>, we often store data in a (real) table. A table is mostly a 2D matrix. It contains rows (each horizontal element) and columns (each vertical element). For example:</p>
<p class=""><strong>GDP</strong></p>


<figure class="diagram"><img src="images/slide-07-2.webp" alt="pandas: One Table: original illustration, slide 7."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.1 Prelude – data organization

<div class="lecture-content" markdown="1">

<p class="">The common principals include:</p>
<p class="lecture-subpoint">each row represents an observational unit (a person, a country, etc.: an entity)</p>
<p class="lecture-subpoint">each column exhibits a perspective or character of the rows (the persons&#x27; height, the countries&#x27; GDP, etc.)</p>
<p class="lecture-subpoint">the top row is reserved for the name of the columns and is called the <strong>header</strong>. It&#x27;s not part of the &quot;contents&quot; of the table</p>
<p class="lecture-subpoint">the first column is reserved for the <strong>index</strong> (name) of the rows. It&#x27;s not part of the &quot;contents.&quot;</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2 One data, One table -- organization -- extract info -- row-col conversion -- subset of a table

<div class="lecture-content" markdown="1">






</div>

---

<!-- slide: lecture-import -->

## 3.2 Just one column

<div class="lecture-content" markdown="1">

A pandas **Series** is a one-dimensional labeled array.

- Each element has an index label.
- The Series has one `dtype`, but that dtype can be `object`, which may hold different Python object types.
- Values can be selected by label or position using the appropriate indexing operation.

A DataFrame brings multiple Series together as columns sharing an index.

</div>

---

<!-- slide: lecture-import -->

## 3.2 Processing one table

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">The type we use to store a data table is called pandas.DataFrame.</p>
<p class="lecture-subpoint">It&#x27;s basically a matrix with index and columns:</p>
<p class="lecture-subpoint">index contains the name of each row</p>
<p class="lecture-subpoint">columns contains the name of each column</p>
<p class="lecture-subpoint">For example, in the following table, the boldfaced numbers on the leftmost side are the index. The boldfaced letters on top are the columns.</p>

```python
import numpy as np
import pandas as pd

df1 = pd.DataFrame(
    np.random.randn(6, 4), # N(0,1)
    index=range(6),
    columns=list("ABCD")
)
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.1 organization

<div class="lecture-content" markdown="1">

<p class="caption">pic source: https://keydifferences.com/difference-between-rows-and-columns.html</p>


<figure class="diagram"><img src="images/slide-12-1.webp" alt="pandas: One Table: original illustration, slide 12."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.2.1 rows and columns

<div class="lecture-content" markdown="1">

<p class="">We can look up (take out) the rows and columns with their names. But the indexing differs:</p>
<p class="">Although look similar, rows and columns are completely different. We can check their types. The type “pandas.core.series.Series” means that col1 is a <strong>Series</strong>.</p>
<p class="lecture-subpoint">A Series is a 1-D object to store information of one aspect.</p>
<p class="lecture-subpoint">pandas.DataFrame is a combination of multiple Series.</p>

```python
row1 = df1[0:1]
col1 = df1['A']
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.1 rows and columns

<div class="lecture-content" markdown="1">

<p class="">The DataFrame provides us with structured information. For example,</p>
<p class="">You’ll see that 1 and 2 do not appear as integers. Why?</p>
<p class="">We can get the analytical information of each column with the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html">.describe</a> method and the storage information with the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dtypes.html">.</a><a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dtypes.html">dtypes</a> <strong>attribute</strong>.</p>

```python
df2 = pd.DataFrame(
    [[1, 2], [1.1, 2.1]],
    index=range(2),
    columns=['col1', 'col2']
)
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.2 extract info

<div class="lecture-content" markdown="1">




<figure class="diagram"><img src="images/slide-15-1.webp" alt="pandas: One Table: original illustration, slide 15."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.2.2 sort and aggregation

<div class="lecture-content" markdown="1">

<p class="">We can look at a table from different angles. Although the information will not change, we can highlight the information in which we are more interested.</p>
<p class="">The first method of highlighting is to put the most important information on top of the table.</p>
<p class="lecture-subpoint">This is done with the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html">.</a><a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html">sort_values</a> or the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_index.html">.</a><a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_index.html">sort_index</a> methods.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.2 sort and aggregation

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">When we want to take a bird-eye view of the table, we summarize information. That is, we do not care about individual data record, but want to know how the overall data look like.</p>
<p class="">Such summarizing is done by the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html">.</a><a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html">agg</a> method.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.2 sort and aggregation

<div class="lecture-content" markdown="1">

<p class="">An example for sorting.</p>

```python
race_score = pd.DataFrame(
    [['Alice', 15.6], ['Bob', 17.3], ['Charlie', 14.5]],
)

race_score.sort_values(1, ascending=True)

race_score.index = [1002, 1001, 1003]

race_score.sort_index()
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.2 sort and aggregation

<div class="lecture-content" markdown="1">

<p class="">An example for aggregation</p>

```python
student_name = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']
langauge_score = [99, 100, 35, 60, 71]
math_score = [25, 89, 36, 40, 91]
score = pd.DataFrame(
    np.array([langauge_score, math_score]).T,
    index=student_name,
    columns=['language', 'math']
)

score.agg("mean", axis=0)

score.agg("sum", axis=1)
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.2 sort and aggregation

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">pandas provides a much simpler <a href="https://en.wikipedia.org/wiki/API">API</a> for reading the csv file: the <a href="https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html">pd.read_csv</a> function.</p>

```python
irisdata = pd.read_csv("./iris/iris.data", header=None)
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.2 sort and aggregation

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 1</h3>
<p class="">1. Read in the data and take a quick look. What are the column names?</p>
<p class="">2. Change column names to &quot;sepal_length,&quot; &quot;sepal_width,&quot; &quot;petal_length,&quot; &quot;petal_width,&quot; and &quot;type. &quot;</p>
<p class="">3. Remove the last column &quot;type&quot; (hint: there&#x27;s a method called <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html">drop</a>).</p>
<p class="">4. Compute (aggregate) the mean and standard deviation of each of the first four columns.</p>
<p class="">5. Subtract the mean from each corresponding column and then divide by its standard deviation. The new data frame should be known as &quot;irisdata_normed&quot;.</p>
<p class="">6. Check the mean and standard deviation of irisdata_normed.</p>
<p class="">7. Write the data to a .csv file (<a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html">.to_csv</a>).</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.3 row-col conversion

<div class="lecture-content" markdown="1">

<p class="caption">pic source: https://medium.com/data-science/reshaping-a-dataframe-with-pandas-stack-and-unstack-925dc9ce1289</p>


<figure class="diagram"><img src="images/slide-22-0.webp" alt="pandas: One Table: original illustration, slide 22."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.2.3 stack and unstack

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">Section 3.2.1 is about changing the way the data contents appear. But we kept the rows as rows and columns as columns (there was no transposition or exchange between rows and columns).</p>
<p class="">The second way of highlighting the data in which we are interested is by swapping the rows and columns.</p>
<p class="lecture-subpoint">This is also an important way to organizing the data without changing the values of the contents (compared to aggregation).</p>
<p class="lecture-subpoint">This can be done with the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.stack.html">.stack</a> and <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.unstack.html">.unstack</a> methods.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.3 stack and unstack

<div class="lecture-content" markdown="1">

<p class="">The index in a data frame shows us the information on the identity of a person, but it is usual that we have multiple levels of identity. For example, if in class 1, grade 1, there is an Alice, it is equally possible that in class 1, grade 3, there is another Alice. So we need <strong>multiple indices</strong> to help identify one person.</p>
<p class="">Let&#x27;s assume we select a student from each class and ask about their height and weight.</p>
<p class="caption">picture sources: https://depositphotos.com/vectors/little-girl-cartoon.html</p>
<p class="">https://www.vecteezy.com/free-png/cartoon-girl</p>


<div class="lecture-figures"><figure class="diagram"><img src="images/slide-24-0.webp" alt="pandas: One Table: original illustration, slide 24."></figure><figure class="diagram"><img src="images/slide-24-1.webp" alt="pandas: One Table: original illustration, slide 24."></figure><figure class="diagram"><img src="images/slide-24-5.webp" alt="pandas: One Table: original illustration, slide 24."></figure><figure class="diagram"><img src="images/slide-24-6.webp" alt="pandas: One Table: original illustration, slide 24."></figure></div>

</div>

---

<!-- slide: lecture-import -->

## 3.2.3 stack and unstack

<div class="lecture-content" markdown="1">



```python
arrays = [
   ["first", "first", "second", "second", "third", "third", "fourth", "fourth"],
   ["one", "two", "one", "two", "one", "two", "one", "two"],
]
height_weight = np.array([
    [173, 176, 185, 167, 165, 193, 156, 163],
    [130, 190, 180, 170, 170, 200, 100, 105]
]).T

# https://pandas.pydata.org/docs/reference/api/pandas.MultiIndex.from_arrays.html
myindex = pd.MultiIndex.from_arrays(arrays,
                                    names=["grade", "class"])
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.3 stack and unstack

<div class="lecture-content" markdown="1">



```python
student_info = pd.DataFrame(height_weight,
                            index=myindex,
                            columns=["height", "weight"])

student_info.stack()

student_info.stack().unstack([1, 2])
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.4 subset of a table

<div class="lecture-content" markdown="1">

<p class="caption">pic source: https://www.linkedin.com/posts/govinda-bobade_choosing-between-loc-and-iloc-when-activity-7098315476195315712-no7b/</p>


<figure class="diagram"><img src="images/slide-27-2.webp" alt="pandas: One Table: original illustration, slide 27."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.2.4 .loc and .iloc

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">The easiest way to take out rows and columns is by the square brackets. However, these methods have limitations.</p>
<p class="lecture-subpoint">We have to use different indexing for rows and columns</p>
<p class="lecture-subpoint">A list passed directly to <code>df[...]</code> selects columns, not row labels</p>
<p class="lecture-subpoint">Use <code>.loc</code> or <code>.iloc</code> to express row and column slices explicitly</p>
<p class="lecture-subpoint">Multi-step selection (<a href="https://pandas.pydata.org/docs/user_guide/indexing.html">advanced selection</a>) is prone to errors</p>
<p class="">Use <code>.loc</code> for label-based selection and <code>.iloc</code> for integer-position-based selection. Both select rows and columns; neither name stands for “label of column.”</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.4 .loc and .iloc

<div class="lecture-content" markdown="1">



```python
student_info.loc[('second', 'one'), 'height']
student_info.iloc[2, 0]
student_info.loc[lambda df: (180 > df['height']) & (df['height'] > 160), :]
```


</div>

---

<!-- slide: lecture-import -->

## Exercises

<div class="lecture-content" markdown="1">






</div>

---

<!-- slide: lecture-import -->

## Example of income data

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2</h3>
<p class="">1. The files income.csv and consumption.csv contain income per capita (means “per person”) and consumption per capita by province, along with the population.</p>
<p class="">2. Please make new columns to find the total income and total consumption of each province in each year and then save the files with new names (income_total.csv and comsumption_total.csv). What are the units?</p>
<p class="">3. How do you compute the savings ratio (savings defined as the amount that is not used for consumption)?</p>




</div>

---

<!-- slide: lecture-import -->

## Example of production function data

<div class="lecture-content" markdown="1">

<h3>In-class exercise 3</h3>
<p class="">Another useful operation with one data set is lead/lag. Let’s consider the production function:</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝑌</mtext></mrow></mrow><mrow><mrow><mtext>𝑡</mtext></mrow></mrow></msub><mrow><mtext>=</mtext></mrow><msub><mrow><mrow><mtext>𝐴</mtext></mrow></mrow><mrow><mrow><mtext>𝑡</mtext></mrow></mrow></msub><msubsup><mrow><mrow><mtext>𝐾</mtext></mrow></mrow><mrow><mrow><mtext>𝑡</mtext></mrow></mrow><mrow><mrow><mtext>𝛼</mtext></mrow></mrow></msubsup><msubsup><mrow><mrow><mtext>𝐿</mtext></mrow></mrow><mrow><mrow><mtext>𝑡</mtext></mrow></mrow><mrow><mrow><mtext>1−</mtext></mrow><mrow><mtext>𝛼</mtext></mrow></mrow></msubsup></math></span></p>
<p class="">Here <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝐾</mtext></mrow></mrow><mrow><mrow><mtext>𝑡</mtext></mrow></mrow></msub><mrow><mtext> </mtext></mrow></math></span>is the capital that is used to generate the output <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝑌</mtext></mrow></mrow><mrow><mrow><mtext>𝑡</mtext></mrow></mrow></msub></math></span>. In accounting, you have learned that firms will disclose financial statements at the end of the fiscal year. The output is the total output over the year, the labor is the number of employees at the end of the year. The capital is also at the end of the year. This generates misalignment between the input and output. We use the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html">shift</a> function to align them.</p>
<p class="">In terms of labor, since we are not sure which one gives the most accurate measure, we typically take the average of labor of the current year and the previous year.</p>




</div>

---

<!-- slide: lecture-import -->

## Example of production function data

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 3 (Cont’d)</h3>
<p class="">The file cdprod.<a href="https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html">xlsx</a> contains the capital, labor, and output information collected from a fake capital-intensive firm from 2000 to 2021. But the output of 2000 is missing.</p>
<p class="">1. Please write a function to find the return-to-scale on capital without correcting for the alignment.</p>
<p class=""><strong>Hint: </strong>you can write a for loop to see which value of <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝛼</mtext></mrow></math></span> produces the output that is closest to the observed.</p>
<p class="">2. Please correctly align capital and labor and then redo step 1.</p>




</div>

---

<!-- slide: lecture-import -->

## Example of finance data

<div class="lecture-content" markdown="1">

<h3>In-class exercise 4</h3>
<p class="">In the theory of asset pricing, an important idea is called <a href="https://en.wikipedia.org/wiki/Momentum_(finance)">momentum</a>, which gives clues on how the stock returns in the future using the past return information. By definition, momentum is</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝑚</mtext></mrow></mrow><mrow><mrow><mtext>𝑡</mtext></mrow></mrow></msub><mrow><mtext>=</mtext></mrow><mrow><munderover><mo>∏</mo><mrow><mrow><mtext>𝑡</mtext></mrow><mrow><mtext>=2</mtext></mrow></mrow><mrow><mrow><mtext>12</mtext></mrow></mrow></munderover><mrow><msub><mrow><mrow><mtext>𝑟</mtext></mrow></mrow><mrow><mrow><mtext>𝑡</mtext></mrow><mrow><mtext>−</mtext></mrow><mrow><mtext>𝑗</mtext></mrow><mrow><mtext> </mtext></mrow></mrow></msub></mrow></mrow></math></span></p>
<p class="">Here <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝑟</mtext></mrow></mrow><mrow><mrow><mtext>𝑡</mtext></mrow></mrow></msub></math></span> is the return at time <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝑡</mtext></mrow></math></span>.</p>
<p class="">The file return1.csv contains information about the returns of one firm. Please compute its momentum when data are available.</p>
<p class=""><strong>Hint: </strong>you probably will find it useful to look at the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html">rolling</a> method.</p>




</div>

---

<!-- slide: lecture-import -->

## Example of finance data

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 4 (Cont’s)</h3>
<p class="">The file return4.csv contains return information of four firms.</p>
<p class="lecture-subpoint">Look at the data and find the cross-sectional average returns. What is the average of the cross-sectional average returns?</p>
<p class="lecture-subpoint">Please read in the data and check if any necessary changes are needed.</p>
<p class="lecture-subpoint">Please compute the momentum of these four firms when data are available.</p>




</div>

---

<!-- slide: lecture-import -->

## Example of sector GDP by country

<div class="lecture-content" markdown="1">

<h3>In-class exercise 5</h3>
<p class="">The file country_sector.xlsx contains sector-level GDP of four countries. Please find the average per country and the average per sector.</p>




</div>
