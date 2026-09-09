---
title: 'Lecture 3.3 · pandas: Reshaping and Grouping'
description: Pivot tables, melt, groupby, and economic data exercises.
lang: en
source: resource/deck3_3_26S-AoL.pptx
sections:
- id: introduction
  title: Introduction
  start: 1
  level: 1
  textbook: ch3-3-reshape-group-0
- id: long-and-wide-tables
  title: Long and wide tables
  start: 3
  level: 1
  textbook: ch3-3-reshape-group-2
- id: pivot-tables
  title: Pivot tables
  start: 6
  level: 1
  textbook: ch3-3-reshape-group-3
- id: melt
  title: Melt
  start: 11
  level: 1
  textbook: ch3-3-reshape-group-4
- id: groupby
  title: Groupby
  start: 15
  level: 1
  textbook: ch3-3-reshape-group-5
- id: other-methods
  title: Other methods
  start: 18
  level: 1
  textbook: ch3-3-reshape-group-6
- id: grouping-practice
  title: Grouping practice
  start: 20
  level: 1
  textbook: ch3-3-reshape-group-5
- id: provincial-savings
  title: Provincial savings
  start: 23
  level: 1
  textbook: ch3-3-reshape-group-7
- id: stock-and-portfolio-exercises
  title: Stock and portfolio exercises
  start: 26
  level: 1
  textbook: ch3-3-reshape-group-5
  related: true
---


<!-- slide: title-slide -->
<p class="eyebrow">Lecture 3.3</p>

# pandas: Reshaping and Grouping

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">More about processing one table.</p>
<p class="lecture-subpoint">long-and-wide table conversion</p>
<p class="lecture-subpoint">divide a table into groups</p>
<p class="">More practice examples</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.4 Long and wide table conversion

<div class="lecture-content" markdown="1">

<p class="caption">source: https://link.springer.com/chapter/10.1007/978-3-030-76394-7_3</p>


<figure class="diagram"><img src="images/slide-03-1.webp" alt="pandas: Reshaping and Grouping: original illustration, slide 3."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">stack and unstack switches the information by changing the index and columns but the contents will remain unchanged. In other words, only the way they are presented changes (from a 6-by-2 table to a 3-by-4 table but the numbers do not change).</p>
<p class="">We now introduce methods that interchange index/column and table contents.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<div class="lecture-content" markdown="1">

<p class="">We say a table is (relatively) long when the table contains more rows than we want. A table is (relatively) wide when the table contains more columns than we want.</p>
<p class="lecture-subpoint">We pivot long tables to wider ones</p>
<p class="lecture-subpoint">We melt wide tables to longer ones</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<div class="lecture-content" markdown="1">

<p class="">Let’s make a long table for pivoting.</p>

```python
import numpy as np
import pandas as pd

["2020-01-03","2020-01-04","2020-01-05"] * 4
["A"] * 3 + ["B"] * 3 + ["C"] * 3 + ["D"] * 3

data = {
   "score": [90, 91, 92, 80, 81, 82, 60, 61, 62, 50, 51, 52],
   "grades": ["A"] * 3 + ["B"] * 3 + ["C"] * 3 + ["D"] * 3,
   "date": pd.to_datetime(["2020-01-03","2020-01-04","2020-01-05"] * 4)
}
df = pd.DataFrame(data)
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">We use <a href="https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html">.</a><a href="https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html">pivot_table</a> to convert a long table to wide.</p>
<p class="">The table we want is like:</p>
<table class="lecture-table"><tr><td>grades</td><td>A</td><td>B</td><td>C</td><td>D</td></tr><tr><td>2020-01-03</td><td>90</td><td>80</td><td>60</td><td>50</td></tr><tr><td>2020-01-04</td><td>91</td><td>81</td><td>61</td><td>51</td></tr><tr><td>2020-01-05</td><td>92</td><td>82</td><td>62</td><td>52</td></tr></table>

```python
pivoted = df.pivot_table(index="date", # whose values will be indices?
                         columns="grades", # whose values will be colnames?
                         values="score")
pivoted
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<div class="lecture-content" markdown="1">

<h3>In-class exercise 1</h3>
<p class="">Pivot the this table:</p>

```python
data = {
   "value": range(13),
   "variable": ["A"] * 4 + ["B"] * 3 + ["C"] * 3 + ["D"] * 3,
   "date": pd.to_datetime(["2020-01-03"] * 5 + ["2020-01-04"] * 4 + ["2020-01-05"] * 4)
}
df = pd.DataFrame(data)
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">The .pivot_table method is more powerful than simply change the locations of data. Its aggfunc parameter can summarize information for each group.</p>

```python
pivoted = df.pivot_table(index="date",
                         columns="variable",
                         values="value",
                         aggfunc="sum") # aggregate
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 1</h3>
<p class="">Read in the MallSales.csv data.</p>
<p class="">Pivot the table to compute the sum of Sales by Year and Category.</p>
<p class="lecture-subpoint">What issues do you encounter?</p>
<p class="">Pivot the table to compute the average Sales by Year.</p>
<p class="">Pivot the table to see the average rating by Product.</p>
<p class="lecture-subpoint">For string operations, use the <code>.str</code> accessor; convert values first with <code>.astype("string")</code> if needed.</p>
<p class="lecture-subpoint">To remove a trailing character, use <code>.str.rstrip(character)</code>; to remove exactly one final character, use <code>.str[:-1]</code></p>
<p class="">Pivot the table to show both sum and mean of Sales by Year and Category.</p>
<p class="">Nest Product under Category and redo question 4.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">We use .<a href="https://pandas.pydata.org/docs/reference/api/pandas.melt.html">melt</a> to convert a wide table to long.</p>
<p class="">When a data frame contains too many columns, it&#x27;s considered &quot;messy&quot; because useful information becomes harder to find. For example:</p>

```python
messydata1 = pd.read_csv("messydata1.csv")
messydata1
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<div class="lecture-content" markdown="1">

<p class="">We melt it with</p>
<p class="">Then we can make smaller and neater DataFrames:</p>

```python
wide_messy = messydata1.melt(id_vars=["Name"])
```

```python
ids = wide_messy.loc[lambda df: df['variable'] == 'ID', :]
ages = wide_messy.loc[lambda df: df['variable'] == 'Age', :]
genders = wide_messy.loc[lambda df: df['variable'] == 'Gender', :]
...
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<div class="lecture-content" markdown="1">

<p class="">Another example is about French fries:</p>
<p class="">We are looking for a table like:</p>
<table class="lecture-table"><tr><td>time</td><td>treatment</td><td>subject</td><td>rep</td><td>scale</td><td>score</td></tr><tr><td>1</td><td>1</td><td>3</td><td>1</td><td>potato</td><td>2.9</td></tr><tr><td>1</td><td>1</td><td>3</td><td>1</td><td>buttery</td><td>0</td></tr><tr><td>1</td><td>1</td><td>3</td><td>1</td><td>grassy</td><td>0</td></tr><tr><td>…</td><td></td><td></td><td></td><td></td><td></td></tr></table>

```python
ffm = pd.read_csv("french_fries.dat", delimiter=' ')
```

```python
ffm.melt(id_vars=['time', 'treatment', 'subject', 'rep'],
         var_name='scale',
         value_name='score')
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.4 pivot_table and melt

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 2</h3>
<p class="">Read in the cake.dat data and melt it to a long table:</p>
<table class="lecture-table"><tr><td>cr</td><td>fr</td><td>variable</td><td>value</td></tr><tr><td>1</td><td>1</td><td>baker1</td><td>7.5</td></tr><tr><td>2</td><td>1</td><td>baker1</td><td>6.1</td></tr><tr><td>1</td><td>1</td><td>baker2</td><td>4.2</td></tr><tr><td>2</td><td>1</td><td>baker2</td><td>3.7</td></tr><tr><td>1</td><td>2</td><td>baker3</td><td>3.8</td></tr><tr><td>…</td><td></td><td></td><td></td></tr></table>




</div>

---

<!-- slide: lecture-import -->

## 3.2.5 Analysis by group

<div class="lecture-content" markdown="1">

<p class="caption">source: https://towardsdatascience.com/pandas-groupby-vs-sql-group-by-39ccd7d2b779/</p>


<figure class="diagram"><img src="images/slide-15-1.webp" alt="pandas: Reshaping and Grouping: original illustration, slide 15."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.2.5 groupby

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">The last data frame operation is to separate the rows into different groups. For example, students from grade 1 form a group, students from grade 2 form a group, etc. This uses the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html">.</a><a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html">groupby</a> method.</p>
<p class="">Let&#x27;s use the iris data for an example and put different flowers into groups according to their type.</p>

```python
irisdata = pd.read_csv("./iris/iris.data",
                       names=["sepal_length", "sepal_width",
                              "petal_length", "petal_width",
                              "type"], header=None)
iris_group = irisdata.groupby("type")
iris_group.size()
```


</div>

---

<!-- slide: lecture-import -->

## 3.2.5 groupby

<div class="lecture-content" markdown="1">

<p class="">Note that these groups don&#x27;t mean we have multiple new data frames. It simply records which rows are in which group. And we don&#x27;t directly use this information. But there are many methods that can be applied to each group. Try them out and summarise your findings.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.2.6 Other methods &amp; Exercises

<div class="lecture-content" markdown="1">






</div>

---

<!-- slide: lecture-import -->

## 3.2.6 other methods

<span class="aol">AoL 5 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">We’ll not introduce these methods in detail, but please read the documents and do the exercises.</p>
<p class="lecture-subpoint"><a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html">dropna</a></p>
<p class="lecture-subpoint"><a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html">drop_duplicates</a></p>
<p class="lecture-subpoint"><a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html">reset_index</a></p>




</div>

---

<!-- slide: lecture-import -->

## Practice

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 3</h3>
<p class="">An example: We want to count how many people selected two courses from different channels (online or onsite) from the course_form.csv file. We rely on the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.count">.count</a> method:</p>
<p class="">In this example, the .count is applied to each group as if they were different data frames. And then the counts are put back into a new data frame.</p>

```python
course_form = pd.read_csv("./course_form.csv")
course_form.groupby(["class", "form"]).count()
```


</div>

---

<!-- slide: lecture-import -->

## Practice

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 4</h3>
<p class="">Now, please</p>
<p class="">read in the animal.csv data and find the fastest animal in each class using <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.first.html">.first</a>.</p>
<p class="">read in the animal.csv data and find the fastest _and the second fastest_ animal in each class using <a href="https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.nth.html">.nth</a>.</p>
<p class="">read in the animal.csv data and find the index of the fastest animal in each class using <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.idxmax.html">.</a><a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.idxmax.html">idxmax</a>.</p>
<p class="">read in the animal.csv data and get the bird group using the <a href="https://pandas.pydata.org/pandas-docs/version/1.3/reference/api/pandas.core.groupby.GroupBy.get_group.html">get_group</a> method.</p>
<p class="">read in the race.csv file containing information of a competition. The column id shows the athletes&#x27; id and the column `time` records their times spent for several tries. Find the average time for each athlete.</p>




</div>

---

<!-- slide: lecture-import lecture-side-tables -->

## Practice

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 5</h3>
<p class="">class1.xlsx and class2.csv contain information on the average scores from two classes: both language and math. Please reorganize the <strong>information </strong>in the two tables so that we can compare the language scores and math scores.</p>
<p class="">That is, make two DataFrames to store the language scores of the two classes and the math scores of the two classes. Your new tables should be like these:</p>
<p class="">DataFrame: language</p>
<p class="">DataFrame: math</p>
<table class="lecture-table"><tr><td>Year</td><td>Class1</td><td>Class2</td></tr><tr><td>2022</td><td>…</td><td>…</td></tr><tr><td>2023</td><td>…</td><td>…</td></tr><tr><td>2024</td><td>…</td><td>…</td></tr></table>
<table class="lecture-table"><tr><td>Year</td><td>Class1</td><td>Class2</td></tr><tr><td>2022</td><td>…</td><td>…</td></tr><tr><td>2023</td><td>…</td><td>…</td></tr><tr><td>2024</td><td>…</td><td>…</td></tr></table>




</div>

---

<!-- slide: lecture-import -->

## Example I: of GDP from stats.gov.cn

<div class="lecture-content" markdown="1">

<p class="">The Bureau of Statistics of our country provides rich information about the country’s economy, especially macroeconomic balances. For example, we can easily find GPD data by province and by sector.</p>
<p class="">Previously, we have seen the consumption and income data. However, the data we used then were already processed. Now let’s turn to the raw data.</p>




</div>

---

<!-- slide: lecture-import -->

## Example I: of GDP from stats.gov.cn

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 6</h3>
<p class="">We will need four files: consumption.csv, cpi.csv, gpd.csv, and population.csv</p>
<p class="">1. Please read in these data and make necessary changes so we can have one data frame with all the information.</p>
<p class=""><strong>Hint: </strong>when setting new columns, you need to make sure that the order is correct.</p>
<p class="">2. Please compute the total savings of each province in each year and store the DataFrame in the “long” format.</p>
<p class=""><strong>Hint:</strong> you can also store them with the “wide” format but it would cause trouble.</p>




</div>

---

<!-- slide: lecture-import -->

## Example I: of GDP from stats.gov.cn

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 6 (Cont’d)</h3>
<p class="">3. We know that the price of products changes every year, as indicated by the consumer price index (CPI). The file cpi.csv contains the price index <strong>relative to 2013 (in 2013 Yuan) </strong>over the years. Please adjust the total savings of each province by the price index. We call the adjusted savings “real savings.”</p>
<p class="">4. What’s the average real savings of each province across the years?</p>
<p class="">5. Which province saves the most on average?</p>




</div>

---

<!-- slide: lecture-import -->

## Example II: returns of individual stocks

<div class="lecture-content" markdown="1">

<p class=""><strong>⚠</strong>This exercise is more difficult!</p>
<p class="">The file stock_utf.csv contains daily information of 10 listed stocks on the Chinese stock market from 1990 to 2000. The data is a subsample of the whole market but can serve as an example.</p>
<p class="">The file contains 75 variables (columns) but we cannot use all of them.</p>




</div>

---

<!-- slide: lecture-import -->

## Example II: returns of individual stocks

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 7</h3>
<p class="">What are the variables?</p>
<p class="">We focus on PrevClPr and Clpr. Please create a new DataFrame to only include relevant columns.</p>
<p class="">We have seen how to construct momentum using monthly return data. Please create returns from the new DataFrame. It’s defined as</p>
<p class=""><span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>𝐶𝑙𝑝𝑟</mtext></mrow><mrow><mtext>/</mtext></mrow><mrow><mtext>𝑃𝑟𝑒𝑣𝐶𝑙𝑃𝑟</mtext></mrow></math></span></p>
<p class="">Please compute the cumulative return every 5 days for each stock.</p>




</div>

---

<!-- slide: lecture-import -->

## Example III: market return

<div class="lecture-content" markdown="1">

<p class="">The file Chiense_market.csv contains all Chinese listed firms but due to privacy concerns, we have added tremendous noise to the original data. It contains four columns: stkcd is the stock code; trdmnt indicates the trading month; mclsprc shows the closing price; msmvttl stands for the total market values.</p>
<p class="">We need to compute the weighted (by total market value) average of closing price of all the firms <strong>in each month</strong>. This is a weighted average price level, not a portfolio return. A return analysis must use changes in prices and appropriately timed portfolio weights.</p>




</div>

---

<!-- slide: lecture-import -->

## Example IV: index return

<div class="lecture-content" markdown="1">

<p class="">We use Chinese_market.csv again. This time, we have another data FT50.xlsx, which contains the composite of Financial Times 50 index.</p>
<p class="">Now, please take a subset of the FT50 composites from Chinese_market and compute the weighted average of these firms.</p>




</div>

---

<!-- slide: lecture-import -->

## Example V: portfolio returns

<div class="lecture-content" markdown="1">

<p class="">Now, let’s compute by far the most complex returns: the portfolio returns. We need first to construct some portfolios. To do so, let’s first divide the stock universe into ten parts. According to the <strong>log of the market value </strong>of stocks. The largest 10% of stocks are put together, and we compute the simple average return of them (called a portfolio and portfolio returns). The following 10% to 20% stocks are put together, and we compute their simple average returns, etc.</p>
<p class="">Please construct ten portfolios according to the market value in each month and compute the simple average of the <strong>price </strong>of each portfolio.</p>




</div>

---

<!-- slide: lecture-import -->

## Example V: portfolio returns

<div class="lecture-content" markdown="1">

<p class="">Please find the gross return of <strong>each stock in each month</strong>.</p>
<p class="">Please construct ten portfolios according to the log of market value in each month and compute the simple average of <strong>return </strong>of each portfolio.</p>
<p class="">Please find the average return of each portfolio series.</p>




</div>
