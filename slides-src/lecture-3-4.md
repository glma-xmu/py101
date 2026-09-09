---
title: 'Lecture 3.4 · pandas: Combining Tables'
description: Merge keys, join types, validation, and a provincial GDP analysis.
lang: en
source: resource/deck3_4-26S_Aol.pptx
sections:
- id: introduction
  title: Introduction
  start: 1
  level: 1
  textbook: ch3-4-merge-0
- id: combining-tables
  title: Combining tables
  start: 3
  level: 1
  textbook: ch3-4-merge-2
- id: merge-keys
  title: Merge keys
  start: 6
  level: 1
  textbook: ch3-4-merge-3
- id: join-types
  title: Join types
  start: 8
  level: 1
  textbook: ch3-4-merge-4
- id: merge-exercises
  title: Merge exercises
  start: 11
  level: 1
  textbook: ch3-4-merge-3
  related: true
- id: different-key-names
  title: Different key names
  start: 14
  level: 1
  textbook: ch3-4-merge-5
- id: comparing-sources
  title: Comparing sources
  start: 17
  level: 1
  textbook: ch3-4-merge-5
  related: true
- id: validating-matches
  title: Validating matches
  start: 18
  level: 1
  textbook: ch3-4-merge-6
- id: provincial-gdp-analysis
  title: Provincial GDP analysis
  start: 19
  level: 1
  textbook: ch3-4-merge-7
---


<!-- slide: title-slide -->
<p class="eyebrow">Lecture 3.4</p>

# pandas: Combining Tables

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">How to combine multiple tables into one table</p>
<p class="lecture-subpoint">so that you can analyze it using what weve learned</p>
<p class="">A lot practice questions</p>




</div>

---

<!-- slide: lecture-import -->

## 3.3 Multiple tables

<div class="lecture-content" markdown="1">

<p class="caption">source: https://www.shanelynn.ie/merge-join-dataframes-python-pandas-index-1/</p>


<figure class="diagram"><img src="images/slide-03-1.webp" alt="pandas: Combining Tables: original illustration, slide 3."></figure>

</div>

---

<!-- slide: lecture-import -->

## 3.3 Processing more tables

<span class="aol">AoL 5 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">Thinking about your high school grades, you may recall that you Chinese teacher recorded your Chinese scores (information A), your math teacher recorded your math scores (information B), and English teacher kept track of your English scores (information C). But when your class teachers held a parent-teacher meeting, they had all your scores. This is because they combined information A, B, and C.</p>
<p class="">Suppose your teachers store your subject scores in different tables. The class teachers need to combine these tables. Thats what we are going to learn. Instead of working with multiple data tables, we will focus on two tables. Then you can easily generalize the processes to multiple tables.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.3 Processing more tables

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">We will mainly learn one pandas function, <a href="https://pandas.pydata.org/docs/reference/api/pandas.merge.html">merge</a>.</p>
<p class="">Other methods, like <a href="https://pandas.pydata.org/docs/reference/api/pandas.concat.html">concat</a>, <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.join.html">join</a>, and <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.update.html">update</a> are also useful. Please read the documents for more information.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.3 Processing more tables

<div class="lecture-content" markdown="1">

<p class="">When we combine two data frames, we need to make sure that the records match between the two. For example, if each teacher decides to put the scores in descending order, the Chinese and math scores are</p>
<p class="">We need to make sure that Alice got a Chinese score of 90 and a math score of 77. This can be guaranteed by the on parameter of the merge function.</p>
<table class="lecture-table"><tr><td>name</td><td>Chinese</td></tr><tr><td>Alice</td><td>90</td></tr><tr><td>Bob</td><td>85</td></tr><tr><td>Charlie</td><td>75</td></tr></table>
<table class="lecture-table"><tr><td>name</td><td>math</td></tr><tr><td>Bob</td><td>95</td></tr><tr><td>Charlie</td><td>86</td></tr><tr><td>Alice</td><td>77</td></tr></table>




</div>

---

<!-- slide: lecture-import -->

## 3.3 Processing more tables

<div class="lecture-content" markdown="1">

```python
import pandas as pd

C_score = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "Chinese": [90, 85, 75],
})
m_score = pd.DataFrame({
    "name": ["Bob", "Charlie", "Alice"],
    "math": [95, 86, 77],
})

pd.merge(C_score, m_score, on="name")
```

</div>

---

<!-- slide: lecture-import -->

## Choosing which students to retain

<div class="lecture-content" markdown="1">

David missed the Chinese exam but took the math exam and scored 60:

```python
m_score.loc[len(m_score)] = {"name": "David", "math": 60}
```

- **Both exams required:** use an inner join.
- **At least one exam required:** use an outer join.
- **Keep the Chinese roster:** use a left join.
- **Keep the math roster:** use a right join.

The `how` parameter determines the rule. In this particular example the Chinese roster is a subset of the math roster, so left/inner and right/outer happen to agree.

</div>

---

<!-- slide: lecture-import -->

## Practice

<div class="lecture-content" markdown="1">



```python
rule1 = pd.merge(C_score, m_score, how="left", on="name")
rule1

rule2 = pd.merge(C_score, m_score, how="right", on="name")
rule2
```


</div>

---

<!-- slide: lecture-import -->

## 3.3.1 Five common modes of “how”

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">Note that the arguments &quot;left&quot; and &quot;right&quot; refers the left and right of the first two arguments (C_score, m_score).</p>
<p class="">These are five commonly used values of <code>how</code>:</p>
<p class="lecture-subpoint">left: use the left as anchor, bring in information from the right</p>
<p class="lecture-subpoint">right: opposite to left</p>
<p class="lecture-subpoint">outer: only keep data that appear in left <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>∪</mtext></mrow></math></span> right</p>
<p class="lecture-subpoint">inner [default]: keep all data from left <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>∩</mtext></mrow></math></span> right</p>
<p class="lecture-subpoint">cross: the Cartesian product; pair every row on the left with every row on the right</p>
<p class="">Well do some exercises to enhance our understanding.</p>




</div>

---

<!-- slide: lecture-import -->

## Exercises

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 1</h3>
<p class="">Two companies jointly operate a zoo. Company A is responsible to measure the weights of animals. Company B is in charge of assign food to each animal.</p>
<p class="">In practice, company B has set a standard for each animal: if the animal is heavier than the standard, they will feed with it less food; otherwise more.</p>
<p class="">The two tables are stored in zooA.csv and zoob.csv.</p>
<p class="">Make a table to show the amount of food to feed each animal.</p>




</div>

---

<!-- slide: lecture-import -->

## Merge exercise: matching firm identifiers

<div class="lecture-content" markdown="1">

<span class="aol">AoL 3 (M)</span>

### In-class exercise 2

Read `gvkey.csv`, `permno.csv`, and `linktable.csv`. The two data sources identify the same firms differently.

<div class="columns" markdown="1"><div class="column" markdown="1">

**Exchange data: `permno.csv`**

- `permno`: the firm/security identifier used in this exercise.
- `year`: observation year.
- `price`: year-end price.

**Financial reports: `gvkey.csv`**

- `gvkey`: the S&amp;P/Compustat company identifier.
- `year`: observation year.
- `size`: firm size.

</div><div class="column" markdown="1">

**Identifier history: `linktable.csv`**

- `permno` and `gvkey`: a candidate match.
- `stime` and `etime`: the years when that match is valid.

For example, `permno=100000` matches `gvkey=237816` during 2000–2002, but matches `gvkey=124451` during 2003–2005.

**Task:** build a table containing both size and price for each firm-year. Respect the validity interval of each match.

</div></div>

</div>

---

<!-- slide: lecture-import -->

## Exercises

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 3</h3>
<p class="">University X allows students to take either exam A or exam B. To be fair, the score of the students will be adjusted, according to the following rule:</p>
<p class="">If the student take exam A, and receives $x$, the score will be <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>90+</mtext></mrow><mfrac><mrow><mrow><mtext>𝑥</mtext></mrow><mrow><mtext>−</mtext></mrow><msub><mrow><mover><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mo>̅</mo></mover></mrow><mrow><mrow><mtext>𝐴</mtext></mrow></mrow></msub></mrow><mrow><msub><mrow><mrow><mtext>𝑠</mtext></mrow></mrow><mrow><mrow><mtext>𝐴</mtext></mrow></mrow></msub></mrow></mfrac></math></span>, where <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mover><mrow><mrow><mtext>𝑥</mtext></mrow></mrow><mo>̅</mo></mover></mrow><mrow><mrow><mtext>𝐴</mtext></mrow></mrow></msub><mrow><mtext> </mtext></mrow></math></span>is the average score of students taking exam A and <span class="lecture-math"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mrow><mrow><mtext>𝑠</mtext></mrow></mrow><mrow><mrow><mtext>𝐴</mtext></mrow></mrow></msub></math></span> is the standard deviation. Score of students taking exam B will also be adjusted similarly.</p>
<p class="">The scores are stored in scoreA.csv and scoreB.csv. Make a table to report the score of the class.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.3.2 left_on and right_on

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">When the left table and the right table use different column names to identify the person, we cannot use on to merge them (why?). But there are two mor parameters to help, left_on and right_on. Let&#x27;s check out the following example and their usage will be self-explanatory.</p>




</div>

---

<!-- slide: lecture-import -->

## Example

<div class="lecture-content" markdown="1">



```python
Ultramen = pd.DataFrame({
    "name": ["Ultraman", "Ultraseven", "UltraReturn", "UltraAce", "UltraTaro"],
    "time": [1967, 1968, 1972, 1973, 1974]
})

Monster = pd.DataFrame({
    "name": ["Bemular", "Eleking", "Bemstar", "Hipporit", "Birdon"],
    "year": [1967, 1968, 1972, 1973, 1974]
})

pd.merge(Ultramen, Monster, 
         how="inner")
```


</div>

---

<!-- slide: lecture-import -->

## Example

<div class="lecture-content" markdown="1">



```python
pd.merge(Ultramen, Monster, 
         how="inner", 
         left_on="time", right_on="year")

pd.merge(Ultramen, Monster, 
         how="inner", 
         left_on="time", right_on="year",
         suffixes=["_ultraman", "_monster"])
```


</div>

---

<!-- slide: lecture-import -->

## Exercise

<span class="aol">AoL 3 (M)</span>

<div class="lecture-content" markdown="1">

<h3>In-class exercise 4</h3>
<p class="">Suppose we have three countries reporting some values.</p>
<p class="">Read in the table country_self.csv, which contains the value reported by the countries themselves.</p>
<p class="">Read in the table country_UN.csv, which contains the value reported by the United Nations.</p>
<p class="">We want to merge the two tables so that we can compare the values reported from different sources.</p>
<p class="">Compute the difference between the self-reported value and UN-reported value for each country in each year.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.3.3 validate

<span class="aol">AoL 2 (H)</span>

<div class="lecture-content" markdown="1">

<p class="">The last situation to consider is when one table has more than one records. In such cases, we need the validate parameter.</p>

```python
advisor = pd.read_csv("advisors.csv")
advisee = pd.read_csv("advisees.csv")

result = pd.merge(advisor, advisee, how="outer",
                  left_on='name', right_on='advisor',
                  validate="one_to_many")

result = pd.merge(advisor, advisee, how="outer",
                  left_on='name', right_on='advisor',
                  validate="one_to_one")
```


</div>

---

<!-- slide: lecture-import -->

## 3.4 Practice questions from old finals

<div class="lecture-content" markdown="1">






</div>

---

<!-- slide: lecture-import -->

## 3.4 Real data analysis of China’s GDP

<div class="lecture-content" markdown="1">

<p class="">The file GDP_by_province.csv contains the gross domestic product (GDP) of 31 provinces in China, obtained from the official site of the National Bureau of Statistics (NBS) (https://data.stats.gov.cn/easyquery.htm?cn=E0103).</p>
<p class="">The file pop_by_provnce.csv contains the information of total population of the same 31 provinces, also obtained from the website.</p>




</div>

---

<!-- slide: lecture-import -->

## 3.4 Real data analysis of China’s GDP

<div class="lecture-content" markdown="1">

<p class="">Please combine the two tables into one so that for each province, in each year, we have both its GDP and population.</p>
<p class="">Please compute for each province in each year, the average GDP per person. The file unemp_by_province.csv contains information about unemployment rate of urban population. Use it as a proxy of total unemployment rate. Compute for each year the average GDP per working people.</p>
<p class="">GDP computation might be influenced by the price index. Fortunately, NBS provides us with the price index data in CPI_by_province.csv. In that table, the numbers are the price index compared to THE previous year. For example, the index of Beijing in 2022 is 101.8, meaning that compared to 2021, the price raised by 1.8%. Now please compute the price indices of each year, using 2014 as the benchmark (i.e., all price indices must be in 2014 RMB Yuan).</p>




</div>

---

<!-- slide: lecture-import -->

## 3.4 Real data analysis of China’s GDP

<div class="lecture-content" markdown="1">

<p class="">Please compute the average population of each province and then find the median (np.median) of the averages. Provinces with average populations greater than that number is taken as provinces large populations. Use the region.csv file to get the geographical information. Then compute the average regional real GDP by year.</p>
<p class="">Compute the average real GDP of all provinces by region and year. Then find the percentages of how the provinces with large populations contribute to their corresponding regions. Explain the results.</p>




</div>
