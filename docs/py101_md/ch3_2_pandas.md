# pandas: One Table

```motto
A table is a matrix that knows what its rows and columns are called.
```

## Introduction

You have spent this course learning Python the language. Now we start using it for the thing most economists actually open a laptop to do: **work with data**. A dataset is where data is stored, and because almost every dataset arrives as a **table**, we will use "dataset" and "data table" interchangeably. The library that specialises in tables is **pandas**.

Data tables are the most important carrier of information we have. But information does not speak for itself — it has to be *revealed*, and revealing it is what the rest of this chapter is about. By the end you should be able to look at an unfamiliar table and say what its rows and columns represent, then apply a small number of manipulations that let you see it from a different angle, find one specific value in it, and summarise the whole thing in a line.

This page covers everything you can do with **one** table. That is more than it sounds: reshaping it, sorting it, summarising it, adding columns, and lining up rows that belong to different points in time. Splitting a table into groups comes in 3.3, and combining several tables comes in 3.4.

pandas is built directly on NumPy, so everything from [3.1](ch3_1_numpy.md) still applies — vectorization, broadcasting, and the `axis` argument in particular. If those words are not yet comfortable, read 3.1 first. As always, the code here is **runnable**; the first Run installs pandas into your browser, which takes a few seconds once.

## 1. How a data table is organised

In economics we work with data constantly — the GDP of a country, the consumption of a household, the price of an item. As computing power has grown, so have the datasets: a few gigabytes is unremarkable now, and terabytes are no longer exotic. Whatever the size, the organising principle is the same, and it is worth stating explicitly because everything pandas does depends on it.

A table is essentially a 2-D matrix: **rows** run horizontally, **columns** run vertically. Four conventions turn that matrix into a dataset:

- **Each row represents one observational unit** — a person, a firm, a country, a country-year. One entity, one row.
- **Each column exhibits one perspective or characteristic** of those units — the person's height, the country's GDP.
- **The top row is reserved for the names of the columns.** It is called the **header**, and it is *not* part of the contents.
- **The first column is reserved for the names of the rows**, called the **index**. It is *not* part of the contents either.

<div style="text-align:center;margin:1.3rem 0;">
<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg" role="img" width="620" style="max-width:100%;height:auto;font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-size:14px;">
  <title>The four parts of a data table: index, header, contents, and one row as one entity</title>
  <desc>A table with a shaded top row labelled "header (the column names)" holding height and weight, a shaded left column labelled "index (the row names)" holding Alice, Bob and Charlie, and an unshaded four-cell block in the middle labelled "contents". An arrow marks one row as one observational unit and another marks one column as one characteristic.</desc>
  <rect x="130" y="52" width="240" height="34" fill="var(--md-primary-fg-color)" opacity="0.16"/>
  <rect x="40" y="86" width="90" height="102" fill="var(--md-primary-fg-color)" opacity="0.16"/>
  <g stroke="var(--md-default-fg-color--light, #777)" stroke-width="1" fill="none">
    <rect x="40" y="52" width="330" height="136"/>
    <line x1="40" y1="86" x2="370" y2="86"/><line x1="40" y1="120" x2="370" y2="120"/>
    <line x1="40" y1="154" x2="370" y2="154"/>
    <line x1="130" y1="52" x2="130" y2="188"/><line x1="250" y1="52" x2="250" y2="188"/>
  </g>
  <g fill="var(--md-default-fg-color, #111)" text-anchor="middle">
    <text x="190" y="74" font-weight="700">height</text><text x="310" y="74" font-weight="700">weight</text>
    <text x="85" y="108" font-weight="700">Alice</text><text x="85" y="142" font-weight="700">Bob</text>
    <text x="85" y="176" font-weight="700">Charlie</text>
    <text x="190" y="108">173</text><text x="310" y="108">130</text>
    <text x="190" y="142">176</text><text x="310" y="142">190</text>
    <text x="190" y="176">185</text><text x="310" y="176">180</text>
  </g>
  <g stroke="var(--md-default-fg-color--light, #777)" stroke-width="1.2" fill="none">
    <path d="M400,69 L378,69"/><path d="M400,120 L378,120"/><path d="M85,30 L85,48"/><path d="M190,212 L190,194"/>
  </g>
  <g fill="var(--md-default-fg-color--light, #777)" font-size="12.5">
    <text x="406" y="73">header — the column names</text>
    <text x="406" y="124">one row = one entity</text>
    <text x="85" y="26" text-anchor="middle">index</text>
    <text x="190" y="228" text-anchor="middle">one column = one characteristic</text>
  </g>
</svg>
</div>

Keep that picture in mind, because pandas takes it literally. A `DataFrame` really does store the contents, the index, and the columns as three separate things — which is exactly what makes it more than a NumPy array, and what the rest of this page is about.

???+ note "Key concept: observational unit"
    The **observational unit** is what one row of your table stands for. Getting this
    straight before you write any code is the single most useful habit in data work:
    a table of "countries" and a table of "country-years" look alike and behave
    completely differently. If you cannot finish the sentence "each row of this table
    is one …", you are not ready to analyse it yet.

## 2. `Series`: just one column

pandas stores sequence data much as NumPy does — a 1-D sequence — but here it is called a **`Series`**. Two properties define it.

First, like a NumPy array, **its elements must all be of the same type**. That is what lets pandas store a column compactly and operate on it at C speed.

Second, and this is the real distinction: **its elements have names**. That collection of names is the `Series`' **index**, and we say the values are *indexed*. A NumPy array can only be reached by position; a `Series` can be reached by position *or* by label.

???+ example "Example: a Series is an array with labels"
    ```python
    import numpy as np
    import pandas as pd

    arr = np.array([1300, 2500, 90, 870])
    s = pd.Series(arr)
    print(s)                      # note the numbers on the left: that is the index
    print()

    named = pd.Series([1300, 2500, 90, 870],
                      index=["rent", "tuition", "coffee", "books"])
    print(named)
    print()
    print(named["tuition"], "|", named.iloc[1])   # by label, or by position
    print(named.dtype, "|", named.index)
    ```

The default index is just `0, 1, 2, 3`, which is why an unlabelled `Series` looks like an array wearing a numbered gutter. Give it real labels and the difference becomes the point: `named["tuition"]` says what you mean, and it keeps saying what you mean after the rows are sorted, filtered, or joined with something else.

## 3. `DataFrame`: the whole table

The type that stores a data table is **`pandas.DataFrame`**. It is a matrix plus an index plus columns:

- **`index`** contains the name of each row,
- **`columns`** contains the name of each column.

Which means the constructor takes three things, in that order — the contents, the index, and the columns:

???+ example "Example: the three parts of a DataFrame"
    ```python
    import numpy as np
    import pandas as pd

    np.random.seed(0)

    df1 = pd.DataFrame(
        # 1. contents
        np.random.randn(6, 4),        # 6x4 draws from N(0, 1)
        # 2. index (row names)
        index=[2 * x for x in range(1, 7)],
        # 3. columns (header of the columns)
        columns=list("ABCD"),
    )
    print(df1.round(2))
    print()
    print("index  :", df1.index.tolist())
    print("columns:", df1.columns.tolist())
    print("shape  :", df1.shape)
    ```

Notice the index here is `2, 4, 6, 8, 10, 12` — deliberately *not* the row positions. Row labels are yours to choose, and once they are not positions, the difference between "the row called 2" and "the row at position 2" stops being academic. §8 is entirely about that distinction.

### 3.1 Taking out rows and columns

You can look up rows and columns by name — but the two are not written the same way, and the asymmetry surprises everyone once.

**Square brackets holding a slice take rows. Square brackets holding a name take a column.**

???+ example "Example: rows by slice, columns by name"
    ```python
    import numpy as np
    import pandas as pd

    np.random.seed(0)
    df1 = pd.DataFrame(np.random.randn(6, 4),
                       index=[2 * x for x in range(1, 7)], columns=list("ABCD"))

    row1 = df1[0:1]          # a SLICE gives you rows -- by position, not label
    col1 = df1['A']          # a NAME gives you a column

    print(row1.round(2))
    print()
    print(col1.round(2))
    print()
    print(type(row1), "\n", type(col1))
    ```

The two results are not even the same type. `df1[0:1]` is still a `DataFrame` — a table one row tall. `df1['A']` is a **`Series`**: `pandas.core.series.Series`, the 1-D object from §2 that stores one aspect of every row.

That is the sentence to remember: **a `DataFrame` is a combination of `Series`, one per column.** The column is the natural unit of a table, which is why taking one out is so much easier to write than taking out a row.

???+ warning "Pitfall: `df1[2]` is not the third row"
    Because a bare name means *column*, `df1[2]` looks for a **column labelled `2`**.
    Our columns are `A, B, C, D`, so this raises `KeyError: 2` — even though there is
    a row labelled `2`. And on a table whose columns happen to be numbers, the same
    expression would quietly hand you a column when you wanted a row. Do not index a
    `DataFrame` with bare brackets when you mean a row; use `.loc` or `.iloc` (§8).

### 3.2 Look at the table before you touch it

A `DataFrame` gives you structured information, and pandas gives you three ways to inspect that structure. Get in the habit of running them **every time** you load a table or change one — it takes two seconds and it is how you catch the problem while it is still small.

???+ example "Example: `.head`, `.dtypes`, and `.describe`"
    ```python
    import pandas as pd

    df2 = pd.DataFrame(
        [[1, 2], [1.1, 2.1]],
        index=range(2),
        columns=['col1', 'col2'],
    )
    print(df2)
    print()
    print(df2.dtypes)        # storage information: what each column holds
    print()
    print(df2.describe())    # analytical information: count, mean, std, quartiles
    ```

Look carefully at the printed table: **`1` and `2` did not stay integers.** They print as `1.0` and `2.0`. Why?

Because of the rule from §2: every value in a column must be of the same type. `col1` was handed a `1` and a `1.1`. There is no type that holds both an integer and a float, so pandas promoted the whole column to `float64` — and the `1` came along. This is not pandas being careless; it is the same **`dtype`** discipline that makes a column fast, and it is why `.dtypes` deserves a look every time.

The two methods answer different questions and you want both. **`.dtypes`** is the *storage* view — what is in there, mechanically. **`.describe()`** is the *analytical* view — count, mean, standard deviation, min, quartiles, max for every numeric column. A column you expected to be numeric that is missing from `.describe()` is a column pandas read as text, which is the single most common surprise when loading a real file.

```recall
A table is a matrix that knows what its rows and columns are called: `.describe()` returns its answer *labelled by column*, so you never have to remember that position 3 was `petal_width`.
```

## 4. Sorting: putting what matters on top

We can look at one table from many angles. The information does not change, but we can **highlight** the part we care about — and the first and simplest way to highlight something is to move it to the top.

Two methods do this. **`.sort_values()`** orders rows by what is *in* a column; **`.sort_index()`** orders them by their row *labels*.

???+ example "Example: sorting by a value and by the index"
    ```python
    import pandas as pd

    race_score = pd.DataFrame(
        [['Alice', 15.6],
         ['Bob', 17.3],
         ['Charlie', 14.5]],
    )
    print(race_score)                             # no column names given: 0 and 1
    print()
    print(race_score.sort_values(1))              # fastest time first
    print()
    print(race_score.sort_values(1, ascending=False))
    print()

    race_score.index = [1002, 1001, 1003]         # give the runners bib numbers
    print(race_score.sort_index())                # now order by bib number
    ```

Since no `columns` were supplied, pandas numbered them `0` and `1`, so `sort_values(1)` sorts on the *column labelled 1* — the times. Assigning to `.index` afterwards replaces the row labels wholesale, and `sort_index()` then reorders by those labels rather than by any value in the table.

???+ warning "Pitfall: sorting returns a new table"
    `race_score.sort_values(1)` does **not** change `race_score`; it hands back a
    sorted copy. Print the original afterwards and it is exactly as it was. To sort in
    place, either rebind the name — `race_score = race_score.sort_values(1)` — or pass
    `inplace=True`. Most pandas methods work this way, and forgetting it is the reason
    a "sorted" table turns up unsorted three lines later.

## 5. Aggregating: the bird's-eye view

Sorting rearranges every record. Sometimes you want the opposite: not the individual records at all, but a statement about the **overall** shape of the data. That is **aggregation**, and it is what the **`.agg`** method does.

Aggregation always has a direction, and the direction is the `axis` argument from [3.1 §5](ch3_1_numpy.md#5-universal-functions-and-aggregations). `axis=0` collapses *down* the rows, giving one number per column. `axis=1` collapses *across* the columns, giving one number per row.

???+ example "Example: aggregating down columns and across rows"
    ```python
    import numpy as np
    import pandas as pd

    student_name = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']
    language_score = [99, 100, 35, 60, 71]
    math_score = [25, 89, 36, 40, 91]

    score = pd.DataFrame(
        np.array([language_score, math_score]).T,   # .T so students are rows
        index=student_name,
        columns=['language', 'math'],
    )
    print(score)
    print()
    print(score.agg("mean", axis=0))    # one number per SUBJECT
    print()
    print(score.agg("sum", axis=1))     # one number per STUDENT
    ```

Read the two results and notice that they answer different questions. Down the columns you learn that the class is better at language than at maths; across the rows you learn which student has the highest total. Same table, same contents, two different summaries — which is what "looking at it from another angle" means in practice.

???+ warning "Pitfall: `np.array` makes every column the same type"
    We built the array from the two *numeric* lists only, then attached the names as
    the index. Try building it from all three — `np.array([student_name,
    language_score, math_score]).T` — and look at the `dtypes`: NumPy has no mixed
    array, so it promotes everything to strings — every column comes back as `dtype:
    object` and `99` becomes `'99'`. Aggregation then fails or, worse, sorts `'100'`
    before `'35'`. Build a `DataFrame` from a **dict of columns** when the types
    differ:

    ```python
    score = pd.DataFrame({'name': student_name,
                          'language': language_score,
                          'math': math_score}).set_index('name')
    ```

`.agg` takes a name as a string (`"mean"`, `"sum"`, `"std"`, `"median"`, `"count"`, `"min"`, `"max"`), a list of them for several at once, or a dict mapping columns to different functions.

???+ example "Example: several statistics at once"
    ```python
    import pandas as pd

    score = pd.DataFrame({'language': [99, 100, 35, 60, 71],
                          'math': [25, 89, 36, 40, 91]},
                         index=['Alice', 'Bob', 'Charlie', 'David', 'Eva'])

    print(score.agg(["mean", "std", "max"]))                  # a table of statistics
    print()
    print(score.agg({'language': "mean", 'math': ["min", "max"]}))
    ```

## 6. Reading and writing data files

Everything so far was typed by hand. Real work starts by reading a file, and pandas offers a much simpler API for that than anything we could write ourselves: **`pd.read_csv`**.

!!! note "The data files for this course"
    The datasets used in the exercises below are distributed **in class, over the
    college network** — they are not published on this site. Put them somewhere
    predictable, such as a `data/` folder next to your notebook, and open them with a
    path relative to where your code is running:

    ```python
    income = pd.read_csv("data/income.csv")       # a folder next to your notebook
    income = pd.read_csv("../data/income.csv")    # ".." means "go up one level"
    ```

    If you get `FileNotFoundError`, the file is not where you think your code is.
    Check with `import os; print(os.getcwd())`, and see
    [A2 The Command Line and Paths](appendix_a2_shell.md) for the full story on
    relative paths.

CSV stands for **comma-separated values**, and that is exactly what the file is: plain text, one row per line, fields separated by commas. `pd.read_csv` turns one into a `DataFrame` in a single call:

```python
irisdata = pd.read_csv("data/iris.data")
```

The one argument you will reach for immediately is **`header`**. By default pandas treats the first line of the file as the column names. When the file has no header row — as `iris.data` does not — that silently eats your first observation and names your columns after it. Say so explicitly:

```python
irisdata = pd.read_csv("data/iris.data", header=None)   # 0, 1, 2, 3, 4 as names
```

The others worth knowing now:

| Argument | What it does |
|---|---|
| `header=None` | the file has no header row; number the columns instead |
| `index_col=0` or `index_col=[0, 1]` | use these columns as the row index rather than as contents |
| `sep=";"`, `delimiter=" "` | the fields are separated by something other than a comma |
| `encoding="utf-8"` | how the text is encoded; try `"gbk"` or `"latin-1"` if you get a `UnicodeDecodeError` |
| `na_values=["-", "N/A"]` | treat these strings as missing rather than as text |

Excel files work the same way through **`pd.read_excel`**, which additionally needs the `openpyxl` package installed (`pip install openpyxl` — a plain `ImportError` about `openpyxl` is what a missing one looks like):

```python
cdprod = pd.read_excel("data/cdprod.xlsx")
country_sector = pd.read_excel("data/country_sector.xlsx", index_col=[0, 1])
```

Writing is the mirror image, `.to_csv`. One argument matters:

```python
irisdata_normed.to_csv("data/iris_normed.csv", index=False)
```

Without `index=False`, pandas writes the row labels out as an extra unnamed first column. Read that file back and you get a spurious `Unnamed: 0` column — the classic sign of a file that has made a round trip one time too many. Write `index=False` whenever the index is just row numbers, and leave it off when the index is real information you need to keep.

???+ question "In-class exercise: normalising the iris data"
    Using `iris.data`:

    1. Read in the data and take a quick look. What are the column names?
    2. Change the column names to `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, and `type`.
    3. Remove the last column, `type`. (Hint: there is a method called `drop`; it needs an `axis`.)
    4. Aggregate the mean and the standard deviation of each of the first four columns.
    5. Subtract each column's mean and divide by its standard deviation. Call the result `irisdata_normed`.
    6. Check the mean and standard deviation of `irisdata_normed`. What should they be?
    7. Write the result to a `.csv` file.

    Step 5 needs no loop at all — see §7.

## 7. New columns: arithmetic across a table

Assigning to a column name that does not exist **creates** it. Combined with the fact that arithmetic on a `Series` is vectorized, that is how nearly every variable you will ever construct gets built: in one line, with no loop.

???+ example "Example: building new columns from old ones"
    ```python
    import pandas as pd

    # a small stand-in for the province-level income data
    income = pd.DataFrame({
        'region': ['Beijing', 'Tianjin', 'Hebei'],
        'Year': [2023, 2023, 2023],
        'Income': [81752.0, 51271.0, 32903.0],        # yuan per person
        'Population': [2186.0, 1364.0, 7393.0],       # 10 thousand people
    })

    income['total_income'] = income['Income'] * income['Population']
    print(income)
    print()

    consumption = pd.Series([47586.0, 34914.0, 22920.0])      # per person
    income['total_consumption'] = consumption * income['Population']
    income['savings_ratio'] = (
        (income['total_income'] - income['total_consumption']) / income['total_income']
    )
    print(income[['region', 'savings_ratio']].round(3))
    ```

Two things are happening here and both are worth naming. `income['Income'] * income['Population']` multiplies **element by element, row by row** — vectorization, straight from 3.1. And `income['total_income'] = ...` on the left of an assignment adds a column to the table in place.

Units deserve a paragraph of their own, because they are where this kind of arithmetic goes wrong silently. `Income` is yuan per person and `Population` is in units of ten thousand people, so `total_income` is in units of *ten thousand yuan* — not yuan. pandas will never tell you this. Write the unit in a comment next to every constructed column, or you will be the third author to recompute it.

The other pattern is **broadcasting** a summary back across the table, which is what normalising a dataset is:

???+ example "Example: broadcasting an aggregate back over the columns"
    ```python
    import numpy as np
    import pandas as pd

    np.random.seed(1)
    data = pd.DataFrame(np.random.normal(loc=[5, 50, 500], scale=[1, 10, 100],
                                         size=(200, 3)),
                        columns=['a', 'b', 'c'])

    col_avg = data.agg("mean", axis=0)        # a Series, one value per column
    col_std = data.agg("std", axis=0)

    normed = (data - col_avg) / col_std       # broadcast down every row

    print(col_avg.round(2))
    print()
    print(normed.agg(["mean", "std"]).round(6))   # 0 and 1, as they must be
    ```

`data - col_avg` subtracts a 3-element `Series` from a 200×3 table. pandas lines the `Series` index up with the table's **columns** and repeats it down every row — NumPy broadcasting, but matched by *label* rather than by position. That label-matching is the deep difference between pandas and NumPy, and it is why the same expression keeps working after you reorder the columns.

???+ question "In-class exercise: income, consumption, and the savings ratio"
    The files `income.csv` and `consumption.csv` contain income per capita and
    consumption per capita by province, together with the population.

    1. Read both in and look at them. What is the observational unit?
    2. Make new columns holding the **total** income and total consumption of each province in each year, then save the results as `income_total.csv` and `consumption_total.csv`. **What are the units?**
    3. Compute the savings ratio, where savings is the part of income not spent on consumption.

    For step 3, think carefully before you write the subtraction: are the rows of the
    two files guaranteed to be in the same order? What would pandas do if they were
    not? (We come back to this properly in 3.4.)

## 8. `.loc` and `.iloc`

The square brackets of §3.1 are the quick way to reach into a table, and they run out of road fast. They have three limitations:

- rows and columns need **different** syntax (a slice for one, a name for the other),
- you cannot select a **list** of rows,
- you cannot **slice** columns at all.

The general tools solve all three at once, and both take **`[rows, columns]`**:

- **`.loc`** selects by **label** — the names in the index and the columns.
- **`.iloc`** selects by **integer position** — where the row or column sits, counting from 0.

???+ example "Example: label-based and position-based selection"
    ```python
    import numpy as np
    import pandas as pd

    student_info = pd.DataFrame(
        {'height': [173, 176, 185, 167, 165],
         'weight': [130, 190, 180, 170, 170]},
        index=['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    )
    print(student_info)
    print()

    print(student_info.loc['Charlie', 'height'])        # by name
    print(student_info.iloc[2, 0])                      # by position -- same cell
    print()
    print(student_info.loc[['Alice', 'Eva'], :])        # a LIST of rows
    print()
    print(student_info.loc[:, 'height':'weight'])       # a SLICE of columns
    ```

Note the one asymmetry that catches people: **`.loc` slices are inclusive of the endpoint** — `'height':'weight'` includes `weight` — while `.iloc` slices follow ordinary Python rules and exclude it. That is deliberate. With labels you have no "one past the end" to name, so pandas includes what you asked for.

`.loc` also accepts a **boolean mask**, which is how filtering is written. And it accepts a **function** that produces one, which is what lets a filter sit in the middle of a chain without naming the intermediate table:

???+ example "Example: filtering rows with `.loc`"
    ```python
    import pandas as pd

    student_info = pd.DataFrame(
        {'height': [173, 176, 185, 167, 165],
         'weight': [130, 190, 180, 170, 170]},
        index=['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    )

    tall = student_info['height'] > 170          # a Series of True/False
    print(tall)
    print()
    print(student_info.loc[tall, :])
    print()
    # the same thing as a callable: df is whatever the chain has produced so far
    print(student_info.loc[lambda df: (180 > df['height']) & (df['height'] > 160), :])
    ```

???+ warning "Pitfall: `and` is not `&`"
    Combine masks with **`&`** (and), **`|`** (or), and **`~`** (not), and parenthesise
    each comparison. Python's `and`/`or` ask a whole `Series` for one true-or-false
    answer and raise `ValueError: The truth value of a Series is ambiguous`. The
    parentheses are not optional either: `&` binds more tightly than `>`, so
    `df['h'] > 160 & df['h'] < 180` parses as `df['h'] > (160 & df['h']) < 180`.

???+ note "Key concept: `.loc` and `.iloc` are not methods"
    They are **properties**, and you index them with **square brackets**, never
    parentheses. `df.loc('Alice')` raises `ValueError: No axis named Alice`, which is
    a confusing message for a simple typo; `df.loc['Alice']` is the row.

## 9. Two-level indices: `stack` and `unstack`

Everything so far changed how the contents *appear* while keeping rows as rows and columns as columns. The second way of highlighting information goes further: it **exchanges** rows and columns.

The motivation is that identity often has more than one level. A `student_info` index of names works until two students share a name; in practice a student is identified by grade *and* class *and* name. pandas handles this with a **`MultiIndex`** — an index with several levels.

???+ example "Example: building a two-level index"
    ```python
    import numpy as np
    import pandas as pd

    arrays = [
        ["first", "first", "second", "second", "third", "third", "fourth", "fourth"],
        ["one", "two", "one", "two", "one", "two", "one", "two"],
    ]
    myindex = pd.MultiIndex.from_arrays(arrays, names=["grade", "class"])

    height_weight = np.array([
        [173, 176, 185, 167, 165, 193, 156, 163],
        [130, 190, 180, 170, 170, 200, 100, 105],
    ]).T

    student_info = pd.DataFrame(data=height_weight, index=myindex,
                                columns=["height", "weight"])
    print(student_info)     # two index levels, one column level
    ```

Now the two operations. **`.stack()`** pushes a level of *columns* down into the *index*, making the table taller and narrower. **`.unstack()`** does the reverse, pulling an index level up into the columns.

???+ example "Example: `stack` and `unstack`"
    ```python
    import numpy as np
    import pandas as pd

    arrays = [["first", "first", "second", "second", "third", "third", "fourth", "fourth"],
              ["one", "two", "one", "two", "one", "two", "one", "two"]]
    myindex = pd.MultiIndex.from_arrays(arrays, names=["grade", "class"])
    height_weight = np.array([[173, 176, 185, 167, 165, 193, 156, 163],
                              [130, 190, 180, 170, 170, 200, 100, 105]]).T
    student_info = pd.DataFrame(height_weight, index=myindex,
                                columns=["height", "weight"])

    stacked = student_info.stack()
    print(stacked.head(6))
    print()
    print(type(stacked))                     # a Series: 2-D became 1-D
    print("shape:", student_info.shape, "->", stacked.shape)
    print()
    print(stacked.unstack())                 # back where we started
    print()
    print(stacked.unstack([1]))              # pull 'class' up instead
    ```

Watch the shape: `(8, 2)` becomes `(16,)`. Stacking every column level leaves nothing across, so the result is not a `DataFrame` at all — it is a `Series` with a three-level index. `unstack()` takes the innermost level back up by default; passing a level number chooses a different one, and `unstack([1, 2])` takes two.

**No number changed anywhere in that example.** That is the whole idea: the same sixteen measurements, laid out four different ways. You choose the layout that puts the comparison you care about side by side.

???+ question "In-class exercise: sector GDP by country"
    The file `country_sector.xlsx` contains sector-level GDP for four countries, with
    `country` and `sector` as the first two columns. Read it with
    `index_col=[0, 1]` so those two become a `MultiIndex`, then find **the average per
    country** and **the average per sector**.

    Hint: `unstack()` first, then aggregate along one axis and then the other. Which
    `axis` gives you which average?

## 10. Lead, lag, and rolling windows

The last thing you can do to one table involves rows that are *next to* each other. This is where economic data stops being a generic table and starts being a time series.

The motivating problem is real. Consider a Cobb–Douglas production function, $Y_t = K^{\alpha} L^{1-\alpha}$. Firms disclose financial statements at the end of the fiscal year, so the output $Y$ is the **total over the year**, while the labour $L$ and the capital $K$ are measured **at the end of the year**. The capital that produced this year's output is therefore *last year's* reported capital, and the relevant labour is somewhere between last year's and this year's. Left uncorrected, that misalignment biases everything you estimate from it.

**`.shift()`** fixes it. It moves a column up or down by a number of rows, filling the gap with `NaN`:

???+ example "Example: `.shift` for lags and leads"
    ```python
    import pandas as pd

    cdprod = pd.DataFrame({
        'fyear': [2000, 2001, 2002, 2003, 2004],
        'K': [50.00, 70.18, 76.43, 71.82, 65.49],
        'L': [26.42, 23.57, 24.51, 22.77, 19.07],
        'Y': [None, 40.61, 50.89, 53.75, 49.61],     # 2000 output is missing
    })

    cdprod['Kprev'] = cdprod['K'].shift()             # last year's capital (lag 1)
    cdprod['Lavg'] = (cdprod['L'] + cdprod['L'].shift()) / 2
    cdprod['Knext'] = cdprod['K'].shift(-1)           # next year's capital (a lead)

    print(cdprod.round(2))
    ```

`shift()` lags by one row; `shift(-1)` leads. The `NaN` in the first row is honest — there is no year before 2000 in this table — and every aggregation you run afterwards will skip it rather than poison the result.

???+ warning "Pitfall: `.shift()` shifts *rows*, not *time*"
    It moves values by position, with no idea what your dates mean. If the table is
    not sorted by date, or if it holds several firms stacked on top of one another,
    `shift()` will happily lag the last row of one firm into the first row of the
    next. **Sort first**, and when a table has multiple entities use
    `df.groupby('firm')['K'].shift()` so the shift restarts for each one — the subject
    of 3.3.

**`.rolling()`** generalises this to a window of several rows: `.rolling(12)` looks at the current row and the eleven before it, and `min_periods` says how many of them must be present before pandas will produce a number instead of `NaN`.

The classic use in finance is **momentum**: the cumulative return over the past twelve months, *excluding* the most recent one. Working in logs turns the compounding into a sum, so the whole thing is a rolling sum minus the part you want to leave out:

???+ example "Example: a rolling window, and momentum"
    ```python
    import numpy as np
    import pandas as pd

    np.random.seed(2)
    r1 = pd.DataFrame({'firm1': np.random.normal(0.01, 0.05, size=24)})

    r1['gross'] = r1['firm1'] + 1                     # 1 + r
    r1['loggross'] = np.log(r1['gross'])              # log(1 + r): now additive

    # sum the last 13 months of log returns, drop the most recent 2 -> months t-12..t-2
    r1['momentum'] = np.exp(
        r1['loggross'].rolling(13, min_periods=13).sum()
        - r1['loggross'].rolling(2, min_periods=2).sum()
    )

    print(r1.round(4).head(15))
    print()
    print("rows with a defined momentum:", r1['momentum'].notna().sum(), "of", len(r1))
    ```

The first twelve rows have no momentum, and that is correct: there is not yet a year of history behind them. `min_periods=13` is what enforces it — leave it out and pandas will happily average whatever it has, handing you a "twelve-month momentum" computed from three months of data.

???+ question "In-class exercise: the return to scale on capital"
    `cdprod.xlsx` holds capital, labour, and output for a fake capital-intensive firm
    from 2000 to 2021; the output for 2000 is missing.

    1. Write a function that, for a given $\alpha$, computes the predicted output $K^{\alpha}L^{1-\alpha}$ and returns the sum of squared errors against the observed $Y$. Loop $\alpha$ over `np.linspace(0.01, 0.99, 99)` and find the value that fits best — **without** correcting the alignment.
    2. Now align capital and labour properly (last year's capital; the average of this year's and last year's labour) and redo step 1. How much does the answer move?

???+ question "In-class exercise: momentum for one firm and for four"
    1. `return1.csv` holds the returns of a single firm. Compute its momentum wherever the data allow. (Hint: `rolling`.)
    2. `return4.csv` holds returns for four firms. Read it in and look at it first — does anything need fixing before you can use it? Find the **cross-sectional average** return in each period, and then the average of those. Finally, compute the momentum of each of the four firms.

    Question worth answering before you code part 2: for the cross-sectional average,
    which `axis` are you aggregating along?

## Summary

| | |
|---|---|
| **A table has four parts** | Contents, index (row names), columns (header). One row = one observational unit. |
| **`Series`** | One column: same type throughout, and *labelled*. A `DataFrame` is a set of `Series`. |
| **`df[...]`** | A slice gives **rows**; a name gives a **column**. `df[2]` looks for a *column* named 2. |
| **Look before you touch** | `.head()`, `.dtypes` (storage), `.describe()` (analysis) — every time. |
| **One type per column** | Mix an `int` and a `float` and the column becomes `float64`. |
| **`.sort_values` / `.sort_index`** | By contents, or by row label. Both return a **copy** unless `inplace=True`. |
| **`.agg`** | `axis=0` collapses down the rows (one number per column); `axis=1` across the columns. |
| **New columns** | `df['new'] = ...` — vectorized, no loop. Write down the units. |
| **`.loc` / `.iloc`** | Label vs. position, both `[rows, columns]`. Properties, not methods. `.loc` slices include the endpoint. |
| **Masks** | Combine with `&`, `|`, `~`, and parenthesise. Never `and`/`or`. |
| **`stack` / `unstack`** | Move levels between index and columns. The contents never change. |
| **`.shift` / `.rolling`** | Lag, lead, and windows — by **row position**, so sort first. |

Next, 3.3 takes the same single table further — reshaping it between long and wide form with `pivot_table` and `melt`, and splitting it into groups with `groupby` — and 3.4 puts several tables together with `merge`.
