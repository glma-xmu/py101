# 6. Data Manipulation with pandas

```motto
pandas aligns before it computes. Every surprise in this chapter is that sentence.
```

## Introduction

This chapter assumes you can already load a CSV and take a mean. It is about the two things that separate someone who *uses* pandas from someone who *trusts* pandas: knowing how to change the **shape** of a table on purpose, and knowing that pandas silently matches up labels before doing arithmetic.

The reshaping half — §6.1.1 through §6.1.3 — is mostly a vocabulary problem. `stack`, `unstack`, `pivot_table`, and `melt` do a small number of things, and once you can say which one you want, the code is one line. The alignment half, §6.1.4, is where results quietly go wrong: pandas will happily add two frames whose rows do not correspond, produce `NaN` where you expected numbers, or accept an assignment that does nothing at all. None of these raise an error.

[3.1 NumPy](ch3_1_numpy.md) in the main course covers the array machinery pandas is built on; read it first if `dtype` and vectorisation are new.

!!! warning "About running these cells"
    The cells on this page `import pandas`, which the browser must fetch and install
    on the first Run — several megabytes, once per session, and a few seconds of
    waiting. Everything after that is instant. If a cell reports that it could not
    load the package, the environment does not have the pandas wheel available; the
    code is standard pandas and runs unchanged on your own machine.

## 6.1 pandas basics

### 6.1.1 `stack()` and `unstack()`

A DataFrame identifies rows by its **index** and columns by its **columns**. Neither has to be a single level: a **MultiIndex** stacks several labels per row, which is how you represent panel data — a firm and a year, a grade and a class, a country and a quarter.

???+ example "Example: a DataFrame with a two-level index"
    ```python
    import numpy as np
    import pandas as pd

    arrays = [
        ["First", "First", "Second", "Second", "Third", "Third", "Fourth", "Fourth"],
        ["one", "two", "one", "two", "one", "two", "one", "two"],
    ]
    myindex = pd.MultiIndex.from_arrays(arrays, names=["grade", "class"])

    data_class = np.arange(0, 16).reshape(8, 2)

    df1 = pd.DataFrame(data_class, index=myindex, columns=["height", "weight"])
    print(df1)
    ```

You can slice rows by position without thinking about the index — `df1[:4]` — but the preferred way is explicit: `.loc` for labels and `.iloc` for positions.

```python
df1.loc[("First", "one"), "height"]   # by label: grade 'First', class 'one'
df1.iloc[1, 1]                        # by position: second row, second column
```

Those operations select; they leave the index and the columns alone. When you are cleaning data, though, the more common need is to change the **shape** — and because pandas keeps the row labels and column labels as first-class structures, reshaping is mostly a matter of moving labels between the two.

`stack()` pushes a level of *columns* down into the *index*, making the frame taller and narrower — in the limit, a Series. `unstack()` does the reverse, pulling an index level up into the columns.

???+ example "Example: moving labels between the index and the columns"
    ```python
    import numpy as np
    import pandas as pd

    myindex = pd.MultiIndex.from_arrays(
        [["First", "First", "Second", "Second", "Third", "Third", "Fourth", "Fourth"],
         ["one", "two", "one", "two", "one", "two", "one", "two"]],
        names=["grade", "class"],
    )
    df1 = pd.DataFrame(np.arange(0, 16).reshape(8, 2),
                       index=myindex, columns=["height", "weight"])

    stacked = df1.stack()
    print(stacked.head(6))            # 'height'/'weight' are now index labels
    print()
    print(type(stacked))              # a Series -- one column of numbers
    print(stacked.index.names)        # ['grade', 'class', None]
    print()
    print(stacked.unstack(level=0))   # pull 'grade' back up into the columns
    ```

Note what did **not** happen: no number changed. `unstack(level=0)` moved `grade` from the index to the columns, so the same sixteen values are laid out differently. The data is identical; only the view of it moved.

### 6.1.2 The `dplyr` pipeline

If you have used R, you will miss `%>%`. pandas has the same idea, because nearly every DataFrame method returns a *new* DataFrame — so calls chain, and a chain reads top to bottom as a sequence of transformations rather than inside out as nested calls.

Take the iris data, familiar from classification examples. Compute two ratios,

$$x = \frac{\textit{sepal\_width}}{\textit{sepal\_length}}, \qquad y = \frac{\textit{petal\_width}}{\textit{petal\_length}},$$

and then summarise them by species. On your own machine you would read the file directly — [`iris.csv`](../assets/camp/iris.csv) is the full 150-row dataset:

```python
irisdata = pd.read_csv("iris.csv")
```

In the browser we build a small sample inline instead, so the cell is self-contained. The pipeline itself is identical either way:

???+ example "Example: a chained pipeline with `.assign()`"
    ```python
    import io
    import pandas as pd

    SAMPLE = (
        "sepal_length,sepal_width,petal_length,petal_width,species\n"
        "5.1,3.5,1.4,0.2,setosa\n"
        "4.9,3.0,1.4,0.2,setosa\n"
        "4.7,3.2,1.3,0.2,setosa\n"
        "4.6,3.1,1.5,0.2,setosa\n"
        "7.0,3.2,4.7,1.4,versicolor\n"
        "6.4,3.2,4.5,1.5,versicolor\n"
        "6.9,3.1,4.9,1.5,versicolor\n"
        "5.5,2.3,4.0,1.3,versicolor\n"
        "6.3,3.3,6.0,2.5,virginica\n"
        "5.8,2.7,5.1,1.9,virginica\n"
        "7.1,3.0,5.9,2.1,virginica\n"
        "6.3,2.9,5.6,1.8,virginica\n"
    )
    irisdata = pd.read_csv(io.StringIO(SAMPLE))

    result = (
        irisdata
        .assign(
            sepal_ratio=irisdata["sepal_width"] / irisdata["sepal_length"],
            petal_ratio=lambda df: df.petal_width / df.petal_length,
        )
        .groupby("species")[["sepal_ratio", "petal_ratio"]]
        .mean()
        .round(3)
    )
    print(result)
    ```

The two arguments to `.assign()` are written differently on purpose. `sepal_ratio` refers to `irisdata` by name — which works, but only because `irisdata` happens to be the frame at that point in the chain. `petal_ratio` uses a **lambda**, which receives whatever the chain has produced *so far*. The lambda form is the one to learn: it keeps working when you insert a `.query(...)` or a `.dropna()` earlier in the chain, whereas the named form silently goes on using the original, unfiltered frame.

To plot the two ratios instead of summarising them, end the chain with `.plot`:

```python
(
    irisdata
    .assign(
        sepal_ratio=lambda df: df.sepal_width / df.sepal_length,
        petal_ratio=lambda df: df.petal_width / df.petal_length,
    )
    .plot(kind="scatter", x="sepal_ratio", y="petal_ratio")
)
```

### 6.1.3 Long–wide conversion

`stack`/`unstack` move labels while keeping every value. The next pair goes further: it lets the *contents* of the table trade places with the index and columns. That is a bigger change, and the distinction is worth stating carefully.

When the contents stay put, the index and columns give you **aspects** — different ways of viewing the same numbers. When contents become index or column labels, you are **summarising**: many rows collapse into one cell, and something has to decide how.

`pivot_table` goes long → wide, and that "something" is `aggfunc`:

???+ example "Example: long to wide with `pivot_table`"
    ```python
    import pandas as pd

    data = {
        "value": range(12),
        "variable": ["A"] * 3 + ["B"] * 3 + ["C"] * 3 + ["D"] * 3,
        "date": pd.to_datetime(["2020-01-03", "2020-01-04", "2020-01-05"] * 4),
    }
    df3 = pd.DataFrame(data)
    print(df3.head())
    print()

    print(df3.pivot_table(index="variable", columns="date", values="value"))
    print()
    print(df3.pivot_table(index="date", columns="variable", values="value"))
    ```

Swapping `index` and `columns` transposes the result — the same aspects, viewed the other way round. And because `aggfunc` defaults to `"mean"`, a value silently appears wherever several rows share an index/column pair. Pass `aggfunc="sum"`, `"count"`, or a list of them when that matters; and use [`pivot`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html) rather than `pivot_table` when duplicates should be an *error* instead of an average.

The reverse direction, wide → long, is `melt`. This is the one you want when columns are really repeated observations of the same thing. In machine learning and in most data analysis, rows are observations and columns are attributes of the unit; pulling columns down into rows turns attributes into observations, which is right when those attributes are repeated measurements or comparable treatments.

???+ example "Example: wide to long with `melt`"
    ```python
    import pandas as pd

    messydata1 = pd.DataFrame({
        "name": ["John", "Jane", "Mary"],
        "treatment1": [1, 4, 6],
        "treatment2": [18, 1, 7],
    })
    print(messydata1)
    print()

    print(messydata1.melt(id_vars=["name"]))
    print()
    print(messydata1.melt(id_vars=["name"],
                          var_name="treatment",
                          value_name="outcome"))
    ```

`treatment1` and `treatment2` were never two different *variables*; they were one variable measured twice. The long form says so, which is why every plotting and modelling library asks for data this way — and why `melt` is usually the first thing you run after loading a spreadsheet built for human eyes.

### 6.1.4 Alignment

Here is the rule that this chapter exists for. **pandas aligns indices and columns before performing any operation.** It never matches by position when labels are available; it matches by label, fills the gaps with `NaN`, and does not warn you.

That is the right default — it is what stops you accidentally adding 2019 revenue to 2020 revenue — but it means a mismatch produces a *result* rather than an error.

???+ example "Example: adding two frames that do not line up"
    ```python
    import pandas as pd

    df4 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}, index=['a', 'b', 'c'])
    df5 = pd.DataFrame({'B': [7, 8, 9], 'C': [10, 11, 12]}, index=['b', 'c', 'd'])

    print(df4, "\n")
    print(df5, "\n")
    print(df4 + df5)
    ```

The result is a 4×3 frame that is almost entirely `NaN`. Only `B` appears in both column sets, and only rows `b` and `c` appear in both indices, so only those four cells hold a number. Nothing went wrong — pandas did exactly what it promised — but if you expected a 3×2 frame of sums, you now have a table of missing values and no error message pointing at why. When you *want* positional behaviour, say so with `df4.add(df5.values)` or `.reset_index(drop=True)` first.

The same rule governs assignment, and here it gets less intuitive. Assigning through `.loc` with a label that does not exist does not fail — it **enlarges** the frame:

???+ example "Example: assignment that creates a column you did not ask for"
    ```python
    import pandas as pd

    df6 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}, index=['a', 'b', 'c'])
    print("Original DataFrame:")
    print(df6, "\n")

    df6.loc['b', ['A', 'C']] = [10, 30]

    print("After misaligned assignment:")
    print(df6)
    ```

A column `C` now exists, holding `30.0` in row `b` and `NaN` everywhere else — and column `A` has changed dtype from `int64` to `float64` to accommodate the `NaN`s in its new neighbour's world. Both are reasonable in isolation; together they are how a typo in a column name turns into a silently corrupted frame.

The last case is the strangest, and worth committing to memory because it looks like it must work:

???+ example "Example: the assignment that does nothing at all"
    ```python
    import pandas as pd

    data = {'A': ['foo', 'foo', 'bar', 'bar', 'baz'], 'B': [1, 2, 3, 4, 5]}
    df7 = pd.DataFrame(data)
    before = df7.copy()

    df7.loc[:, ['B', 'A']] = df7[['A', 'B']]     # "swap the two columns"

    print(df7)
    print("did anything change?", not df7.equals(before))   # False
    ```

You asked for `B` to take the values of `A` and vice versa. What happened is nothing: the right-hand side is a DataFrame with columns named `A` and `B`, so pandas **aligned it by label** before assigning — `A` went to `A`, `B` went to `B` — and the column order in your indexer was ignored entirely. Alignment beat position, as it always does.

To actually swap, strip the labels off the right-hand side so there is nothing to align:

```python
df7[['A', 'B']] = df7[['B', 'A']].to_numpy()   # or .values
```

???+ note "Key concept: the takehome"
    1. **Alignment happens first, on labels, silently.** Arithmetic, assignment, comparison — all of it.
    2. **A misaligned operation yields `NaN`, not an error.** Check `.shape` and `.isna().sum()` after any join-like step.
    3. **`.loc` assignment enlarges** rather than failing on an unknown label, and can change a column's dtype as a side effect.
    4. **To bypass alignment, drop the labels** with `.to_numpy()`.

### 6.1.5 WRDS connection

Most of the data you will actually use in this field comes from [WRDS](https://wrds-www.wharton.upenn.edu/), and it is reachable from Python directly rather than through the web interface — which matters, because a query in a script is a query you can re-run and a co-author can reproduce.

The [official introduction to `wrds_connection`](https://wrds-www.wharton.upenn.edu/documents/1443/wrds_connection.html) is the place to start. In outline:

```python
import wrds

db = wrds.Connection(wrds_username="your_username")   # prompts, then offers to
                                                      # save a .pgpass file
db.list_libraries()[:10]
db.list_tables(library="crsp")[:10]

df = db.raw_sql("""
    SELECT permno, date, ret
    FROM crsp.msf
    WHERE date BETWEEN '2015-01-01' AND '2015-12-31'
""", date_cols=['date'])

db.close()
```

Two practical notes. Create the `.pgpass` file once, so credentials never appear in a script you might commit — the same discipline as never putting an API key in a notebook. And pull only the columns and date range you need: `crsp.msf` is large enough that `SELECT *` will time out, and the SQL runs on their server, so filtering there rather than in pandas is the whole game.

## Summary

| | |
|---|---|
| **`stack` / `unstack`** | Move labels between index and columns. No value changes. |
| **`pivot_table` / `melt`** | Long ↔ wide. Contents become labels, so an aggregation is involved. |
| **`pivot` vs `pivot_table`** | `pivot` errors on duplicates; `pivot_table` averages them by default. |
| **Chains and `.assign`** | Use the `lambda df: ...` form so the chain stays correct when you insert a step. |
| **Alignment is by label** | Applied before every operation, silently, producing `NaN` rather than errors. |
| **`.loc` enlarges** | An unknown label creates the row or column instead of raising. |
| **`.to_numpy()` opts out** | Strip the labels when you genuinely want positional assignment. |
