# pandas: Reshaping and Grouping

```motto
Every table has a shape that makes your question easy to ask.
```

## Introduction

In [3.2](ch3_2_pandas.md) we reached the end of what you can do to a table while leaving its contents where they are. `stack` and `unstack` moved *labels* between the index and the columns, but never touched a single number: an 8×2 table became a 16-element series holding the same sixteen values.

This page crosses that line. The operations here **move data between the contents and the labels** — a value that was sitting in a cell becomes a column *name*, or a column name becomes a value in a cell. That sounds like vandalism the first time you meet it, and it is the single most useful thing pandas does. A table you cannot analyse in one shape becomes obvious in another.

Three tools, in order of how often you will reach for them. **`pivot_table`** turns a long table into a wide one, summarising as it goes. **`melt`** turns a wide table into a long one, which is how you tidy a messy file. And **`groupby`** splits a table into groups and applies something to each — the workhorse of nearly every real analysis. We close with the three cleaning methods you will need constantly and which nobody bothers to teach: `dropna`, `drop_duplicates`, and `reset_index`.

As in 3.2, the examples are small tables built in the page so you can run them. The exercises point at the real files, which you get in class.

## 1. Long and wide: two shapes of the same information

The vocabulary first, because it is relative and people use it as though it were absolute.

A table is **long** when it has more rows than you want, and **wide** when it has more columns than you want. Neither is right. What is right depends on the question you are about to ask, and the whole skill is noticing which shape your question needs.

Consider twelve exam scores: four grade groups observed on three dates. Here is the **long** version — one row per observation, twelve rows, and the identifying information repeated down the columns:

| score | grades | date |
|---|---|---|
| 90 | A | 2020-01-03 |
| 91 | A | 2020-01-04 |
| 92 | A | 2020-01-05 |
| 80 | B | 2020-01-03 |
| … | … | … |

And the **wide** version — one row per date, one column per grade group, three rows:

| date | A | B | C | D |
|---|---|---|---|---|
| 2020-01-03 | 90 | 80 | 60 | 50 |
| 2020-01-04 | 91 | 81 | 61 | 51 |
| 2020-01-05 | 92 | 82 | 62 | 52 |

Identical information. But look at what changed structurally: in the long table, `A` was a **value** sitting in the `grades` column; in the wide table, `A` is a **column name**. Data became a label. That is the move `stack` could never make.

Each shape suits different work. Long tables are what databases produce, what statistical models want, and what survives adding a new grade group without changing the table's structure. Wide tables are what humans read, what you put in a paper, and what makes "compare A against B on the same date" a matter of looking sideways.

???+ note "Key concept: pivot and melt"
    **Pivoting** goes long → wide: the values of one column are spread out to become
    new columns. **Melting** goes wide → long: a set of columns is gathered back into
    two columns, one holding the old column *names* and one holding the values.
    They are inverses, and you will use both on the same dataset in the same hour.

## 2. `pivot_table`: from long to wide

`pivot_table` has three parameters that do the real work, and it helps enormously to read them as three questions about the table you *want*:

- **`index`** — whose values become the row labels?
- **`columns`** — whose values become the column names?
- **`values`** — whose values fill the cells?

???+ example "Example: pivoting the scores table"
    ```python
    import pandas as pd

    data = {
        "score": [90, 91, 92, 80, 81, 82, 60, 61, 62, 50, 51, 52],
        "grades": ["A"] * 3 + ["B"] * 3 + ["C"] * 3 + ["D"] * 3,
        "date": pd.to_datetime(["2020-01-03", "2020-01-04", "2020-01-05"] * 4),
    }
    df = pd.DataFrame(data)
    print(df.head(4))
    print()

    pivoted = df.pivot_table(
        index="date",       # whose values become the row labels?
        columns="grades",   # whose values become the column names?
        values="score",     # whose values fill the cells?
    )
    print(pivoted)
    ```

Twelve rows became three. Nothing was lost, because each (date, grade) pair occurred exactly once and had exactly one cell to land in.

### 2.1 Pivoting is aggregating

Now the part that makes `pivot_table` more than a rearrangement. Ask yourself what happens when a (date, grade) pair occurs **twice**. There is one cell and two numbers competing for it. Something has to combine them — and that something is the **`aggfunc`** parameter.

Its default is `"mean"`. That is worth saying loudly, because it means **`pivot_table` silently averaged something for you** in every example above; you just did not notice, since each cell had one value and the mean of one number is itself.

???+ example "Example: `aggfunc` decides what a cell means"
    ```python
    import pandas as pd

    # note: five A's and only two D's -- the groups are now uneven
    data = {
        "value": range(13),
        "variable": ["A"] * 5 + ["B"] * 3 + ["C"] * 3 + ["D"] * 2,
        "date": pd.to_datetime(["2020-01-03"] * 5 + ["2020-01-04"] * 4
                               + ["2020-01-05"] * 4),
    }
    df = pd.DataFrame(data)

    print(df.pivot_table(index="date", columns="variable", values="value"))
    print()
    print(df.pivot_table(index="date", columns="variable", values="value",
                         aggfunc="sum"))
    print()
    print(df.pivot_table(index="date", columns="variable", values="value",
                         aggfunc="count"))    # how many went into each cell?
    ```

Run all three and compare. Where a cell drew on one observation the three agree; where it drew on several they diverge, and the `count` version tells you which cells those were. Get into the habit of pivoting with `aggfunc="count"` once before trusting any pivot — it is the cheapest way to discover that your data is not shaped the way you assumed.

The `NaN`s are meaningful too: they mark combinations that never occurred. A `NaN` here is not missing data, it is *absent* data — nobody in group D was observed on 2020-01-03.

???+ warning "Pitfall: the default `aggfunc` is `mean`"
    If your table has duplicate (index, column) pairs and you do not say otherwise,
    `pivot_table` averages them and tells you nothing. Silently averaging a duplicate
    row is a genuinely bad thing to do to financial data. Either state `aggfunc`
    explicitly every time, or check for duplicates first (§5.2).

You can also pass **several** aggregation functions, and nest labels by handing `index` or `columns` a *list*:

???+ example "Example: several statistics, and nested columns"
    ```python
    import pandas as pd

    sales = pd.DataFrame({
        "Year":     [2015, 2015, 2016, 2016, 2016, 2017, 2017],
        "Category": ["Clothing", "Components", "Accessories", "Bikes",
                     "Clothing", "Clothing", "Components"],
        "Product":  ["Socks", "Chains", "Helmets", "Road-150",
                     "Bib-Shorts", "Jerseys", "Cranks"],
        "Sales":    [3700, 2300, 68400, 6300, 2300, 40000, 25400],
    })

    print(sales.pivot_table(index="Year", columns="Category", values="Sales",
                            aggfunc="sum"))
    print()
    print(sales.pivot_table(index="Year", columns="Category", values="Sales",
                            aggfunc=["sum", "mean"]))
    print()
    print(sales.pivot_table(index="Year", columns=["Category", "Product"],
                            values="Sales", aggfunc="sum"))
    ```

### 2.2 Cleaning a column before you can aggregate it

Real spreadsheets do not hold numbers. They hold things that *look* like numbers to a human: `"$20,000 "` with a currency symbol, a thousands separator, and a trailing space; `"75%"` with a percent sign. pandas reads those as text, `.describe()` ignores them, and `aggfunc="sum"` either fails or — worse — concatenates the strings.

The fix is the **`.str` accessor**. Every string method you know from Chapter 1 is available on a whole column through `.str`, applied element by element.

???+ example "Example: from a currency string to an integer"
    ```python
    import pandas as pd

    sales = pd.DataFrame({
        "Year":   [2015, 2016, 2017],
        "Sales":  ["$3,700 ", "$68,400 ", "$40,000 "],
        "Rating": ["22%", "75%", "22%"],
    })
    print(sales.dtypes)          # Sales and Rating are 'object' -- i.e. text
    print()

    # ' hello '.strip() works on ONE string; .str.strip() works on the whole column
    print(sales["Sales"].str.strip().str.strip("$").str.replace(",", ""))
    print()

    sales["Sales"] = (sales["Sales"]
                      .str.strip()            # drop the trailing space
                      .str.strip("$")         # drop the currency symbol
                      .str.replace(",", "")   # drop the thousands separator
                      .astype(int))           # finally: text -> integer
    sales["Rating"] = sales["Rating"].str.strip("%").astype(int)

    print(sales)
    print()
    print(sales.dtypes)
    ```

Two things to take from this beyond the cleaning itself.

First, **`.str` is the bridge** between one string and a column of them. Writing `sales["Sales"].strip()` fails — a `Series` has no `.strip`; only the strings *inside* it do. `.str` hands the method down to each element.

Second, notice the shape of that assignment. Each step is a small, obvious transformation, and they are stacked one per line inside parentheses. This is the **chained style**, and it is how idiomatic pandas is written: wrap the whole expression in `(` … `)`, put each link of the chain on its own line, and read it top to bottom as a sequence of verbs — strip, strip, replace, convert. The alternative is four intermediate variables named `sales2`, `sales3`, and by `sales4` nobody knows which is current.

```recall
Every table has a shape that makes your question easy to ask — but first the cells have to hold what they claim to. A column of `"$20,000 "` is a column of *text*, and no reshaping will make it add up.
```

???+ question "In-class exercise: Mall sales"
    Read in `MallSales.csv`, then:

    1. Pivot the table to compute the **sum** of `Sales` by `Year` and `Category`. What issue do you hit?
    2. Fix it, then pivot to compute the **average** `Sales` by `Year`.
    3. Pivot to see the average `Rating` by `Product`. (`.str` again — remove the trailing character with `rstrip`.)
    4. Pivot to show **both** the sum and the mean of `Sales` by `Year` and `Category`.
    5. Nest `Product` under `Category` and redo question 4.

## 3. `melt`: from wide to long

`melt` runs the other way, and its main use is not analysis but **tidying**. A file with too many columns is hard to work with — useful information hides in the header, and every operation needs you to name columns individually.

The parameter that matters is **`id_vars`**: the columns that *identify* a row and should be left alone. Everything else gets gathered into two new columns — one holding the old column names, one holding the values.

???+ example "Example: melting a wide, messy table"
    ```python
    import pandas as pd

    messy = pd.DataFrame({
        "Name":       ["Alice Smith", "Bob Johnson"],
        "ID":         [1, 2],
        "Age":        [30, 45],
        "Gender":     ["Female", "Male"],
        "Occupation": ["Data Scientist", "Project Manager"],
        "Salary":     [90000, 120000],
    })
    print(messy)
    print()

    long_messy = messy.melt(id_vars=["Name"])
    print(long_messy)
    print()

    # now pull out one neat table per attribute
    ages = long_messy.loc[lambda df: df["variable"] == "Age", :]
    print(ages)
    ```

The two new columns are called `variable` and `value` by default. Those names are rarely what you mean, and `melt` lets you say so with **`var_name`** and **`value_name`** — always worth doing, because `value` is a uselessly generic name three lines later.

???+ example "Example: naming the melted columns"
    ```python
    import pandas as pd

    # a taste-testing panel: four sensory scales measured per session
    ff = pd.DataFrame({
        "time": [1, 1, 1], "treatment": [1, 1, 1],
        "subject": [3, 3, 10], "rep": [1, 2, 1],
        "potato":  [2.9, 14.0, 11.0],
        "buttery": [0.0, 0.0, 6.4],
        "grassy":  [0.0, 0.0, 0.0],
        "rancid":  [0.0, 1.1, 0.0],
    })

    tidy = ff.melt(
        id_vars=["time", "treatment", "subject", "rep"],
        var_name="scale",     # what the old column names describe
        value_name="score",   # what the numbers are
    )
    print(tidy.head(8))
    print()
    print("shape:", ff.shape, "->", tidy.shape)
    ```

Four identifier columns plus four measurement columns became four identifiers plus two — and the row count multiplied by four. That is the trade `melt` always makes: fewer columns, more rows, and a table where `scale` is now something you can `groupby`.

???+ question "In-class exercise: the cake data"
    `cake.dat` records ratings of cakes by four bakers and four judges, identified by
    `cr` and `fr`. It is **tab**-separated, so `pd.read_csv` needs
    `delimiter="\t"` — try it with `delimiter=" "` first and look at what you get, so
    you recognise the symptom later.

    Melt it into a long table with columns `cr`, `fr`, `variable`, `value`. The file
    is mostly empty cells, so finish with `.dropna()` (§5.1) and check the row count
    is what you expect.

## 4. `groupby`: split, apply, combine

Reshaping changes how a table looks. **`groupby`** changes what a question applies to: instead of asking something of the whole table, you ask it of every group separately and collect the answers.

Every use of `groupby` follows the same three beats, and naming them makes the API obvious:

1. **Split** the rows into groups by the value of one or more columns.
2. **Apply** something to each group independently.
3. **Combine** the results back into one table, one row per group.

### 4.1 The group object holds no data

Calling `.groupby()` on its own computes almost nothing. It hands back a `DataFrameGroupBy` object, which is best understood as **a note of which rows belong to which group** — not a set of new tables.

???+ example "Example: what `groupby` actually returns"
    ```python
    import pandas as pd

    iris = pd.DataFrame({
        "type": ["setosa"] * 3 + ["versicolor"] * 3 + ["virginica"] * 2,
        "sepal_length": [5.1, 4.9, 4.7, 7.0, 6.4, 6.9, 6.3, 5.8],
        "petal_width":  [0.2, 0.2, 0.2, 1.4, 1.5, 1.5, 2.5, 1.9],
    })

    grouped = iris.groupby("type")
    print(grouped)               # just an object -- nothing computed yet
    print()
    print(grouped.size())        # how many rows in each group
    print()
    print(grouped.mean())        # the split-apply-combine, in one call
    ```

`.size()` and `.mean()` are where the work happens. Between them they cover most of what you will ever need: **how many** and **how much**.

### 4.2 Aggregating within groups

Anything that reduces a column to one number works per group — `mean`, `sum`, `count`, `min`, `max`, `std`, `median` — and `.agg` takes the same string names, lists, and dicts it did in [3.2 §5](ch3_2_pandas.md#5-aggregating-the-birds-eye-view).

Grouping by **several** columns gives you a group per combination, and a `MultiIndex` on the result:

???+ example "Example: counting by two keys at once"
    ```python
    import pandas as pd

    course_form = pd.DataFrame({
        "name":  [1, 2, 2, 3, 4, 5],
        "class": [1, 1, 1, 1, 2, 2],
        "form":  ["online", "onsite", "onsite", "online", "online", "onsite"],
    })

    print(course_form.groupby("form").count())
    print()
    print(course_form.groupby(["class", "form"]).count())
    ```

Look closely at what `.count()` counted. It reports a number **for every remaining column**, and those numbers can differ — because `count` counts *non-missing* values, column by column. That is a feature: a column whose count is lower than its neighbours' is a column with missing data, and this is often how you first find out.

### 4.3 Picking rows out of each group

Aggregating gives you a summary per group. Sometimes you want an actual **row** from each — the fastest animal, the largest firm, the most recent observation. Four methods do this, and they differ in ways worth knowing.

???+ example "Example: `first`, `nth`, `idxmax`, and `get_group`"
    ```python
    import pandas as pd

    animal = pd.DataFrame({
        "class":     ["bird", "bird", "mammal", "mammal", "mammal"],
        "animal":    ["eagle", "slowbird", "tiger", "sloth", "tiger"],
        "max_speed": [389.0, 24.0, 80.2, None, 58.0],
    })
    print(animal)
    print()

    print(animal.groupby("class").first())        # first row of each group
    print()
    print(animal.groupby("class").nth([0, 1]))    # the first TWO rows of each
    print()
    print(animal.groupby("class")["max_speed"].idxmax())   # LABEL of the max row
    print()
    print(animal.groupby("class").get_group("bird"))       # one group, as a table
    ```

Three traps live in that example, and all three are worth meeting now.

**`.first()` means "first *row*", not "largest".** It obeys the order the rows happen to be in. If you want the fastest animal, you must `sort_values("max_speed", ascending=False)` *first* — otherwise you get whichever row was typed in first. The same applies to `.nth()`.

**`.first()` also skips missing values, column by column.** In the example, `mammal`'s first row is sloth for `animal` but `80.2` for `max_speed` — because sloth's speed is `NaN` and `first` reached past it to the next non-null. The row it returns may not correspond to any row that exists in your data. `.nth(0)` returns a genuine row and does not do this.

**`.idxmax()` returns an index label, not a value.** It answers "*where* is the maximum", which you then feed to `.loc`. And notice we selected `["max_speed"]` before calling it: run `.idxmax()` on the whole frame and it happily computes a maximum for the *text* column too, comparing strings alphabetically, so `slowbird` beats `eagle`.

???+ warning "Pitfall: passing a column name to `.idxmax` does not select it"
    Reaching for `animal.groupby("class").idxmax("max_speed")` is natural and wrong:
    the first positional parameter of `idxmax` is **`axis`**, so pandas replies
    `ValueError: No axis named max_speed for object type DataFrame`. Select the column
    before you aggregate — `groupby("class")["max_speed"].idxmax()` — which is the
    general rule for every reduction, not just this one.

???+ question "In-class exercise: animals and race times"
    Using `animal.csv`:

    1. Find the fastest animal in each `class` with `.first`. Is the answer right? What must you do to the table first?
    2. Find the fastest **and second fastest** in each class with `.nth`.
    3. Find the **index** of the fastest animal in each class with `.idxmax`.
    4. Get just the bird group as a table, using `.get_group`.

    Then, using `race.csv` — where `id` is an athlete and `time` is one of several
    attempts — find each athlete's average time.

## 5. Three methods you will use constantly

These get one slide in most courses and cause a disproportionate share of wrong answers. Read the documentation for each; here is what they are for and where they bite.

### 5.1 `dropna` — remove missing values

Real files have holes: a blank cell, an `NA`, a footnote row at the bottom that pandas read as data. `.dropna()` removes rows containing missing values.

The parameter to know is **`subset`**. Bare `.dropna()` drops a row if *any* column is missing, which on a wide table can silently delete most of your data. Almost always you mean "drop rows where *this particular* column is missing":

```python
df.dropna()                       # any column missing -> row goes
df.dropna(subset=["max_speed"])   # only this column matters
df.dropna(how="all")              # only if the ENTIRE row is empty
```

Check `len(df)` before and after, every time. A `dropna` that removes more than you expected is one of the easiest ways to publish a wrong number.

### 5.2 `drop_duplicates` — remove repeated rows

Duplicates arrive from merged exports, double-submitted forms, and files that were appended to twice. They inflate counts and quietly bias means.

```python
df.drop_duplicates()                    # rows identical in every column
df.drop_duplicates(subset=["animal"])   # rows repeating this key
df.duplicated().sum()                   # how many are there? -- check first
```

In the animal table above, `tiger` appears twice with different speeds. Whether that is a duplicate to remove or two genuine observations is a question about the data, not about pandas — which is exactly why the check comes before the drop.

### 5.3 `reset_index` — turn the index back into a column

After a `groupby` or a `sort_values`, your index is often no longer a plain `0, 1, 2, …`. `reset_index` restores it, and its **`drop`** parameter decides what happens to the old one:

```python
df.reset_index()              # old index becomes a new COLUMN
df.reset_index(drop=True)     # old index is thrown away
```

Use `drop=True` when the old index was just row numbers left over from sorting. Leave it off after a `groupby`, when the index holds the group keys and is real information you want as a column.

This matters more than it looks, because **assigning a column aligns on the index** ([3.2 §7](ch3_2_pandas.md#7-new-columns-arithmetic-across-a-table)). Sort two tables the same way, forget to reset their indices, then assign a column from one to the other, and pandas will line the values up by the *old* scrambled labels rather than by position. The numbers land in the wrong rows and nothing warns you.

???+ example "Example: why `reset_index` matters before combining"
    ```python
    import pandas as pd

    a = pd.DataFrame({"region": ["X", "Y", "Z"], "gdp": [10, 30, 20]})
    b = pd.DataFrame({"region": ["X", "Y", "Z"], "pop": [1, 3, 2]})

    a = a.sort_values("gdp")            # index is now 0, 2, 1
    b = b.sort_values("pop")            # index is now 0, 2, 1
    print(a, "\n")

    a["pop_wrong"] = b["pop"]           # aligned by INDEX, not by position
    print(a, "\n")

    a2 = a.reset_index(drop=True)
    b2 = b.reset_index(drop=True)
    a2["pop_right"] = b2["pop"]
    print(a2)
    ```

Here the two tables happened to sort into the same order, so the result looks fine — which is precisely the danger. Change one number so the orders differ and the same code returns nonsense, silently. The habit that saves you: **after sorting, reset; before assigning across tables, check that the indices match.**

## 6. Putting it together: provincial savings

The exercises so far each used one method. Real work chains them, and this one is worth doing slowly because the pattern recurs in every panel dataset you will ever meet.

???+ question "In-class exercise: real savings by province"
    You have four files — `consumption.csv`, `cpi.csv`, `gdp.csv`, and
    `population.csv` — each **wide**: one row per province, one column per year
    (`2014年` … `2023年`).

    1. Read them in and reshape so that all the information sits in **one** table. Think before you type: they are wide, you want them long, and once long they must be lined up. *Hint: `melt` each one with `id_vars="地区"`, then `sort_values` on the same keys in every table, then `reset_index(drop=True)` — §5.3 explains why that last step is not optional.*
    2. Compute the **total savings** of each province in each year, storing the result in long format. (Savings is the part of income not consumed; both figures are *per capita*, so population is involved.)
    3. `cpi.csv` gives a price index relative to 2013. Deflate the total savings by it to get **real savings**, in 2013 yuan.
    4. What is the average real savings of each province across the years?
    5. Which province saves the most on average?

    Two warnings from experience. The files do not all have the same number of rows —
    check `.shape` on each after loading and use `dropna` where a file has trailing
    blank rows. And step 2 says *long* format for a reason: the wide version invites
    exactly the misaligned-assignment bug from §5.3.

??? info "Deep dive: extended exercises on market data"
    These use the larger files distributed in class and are closer to what a research
    task actually looks like. They need everything on this page plus `shift` and
    `rolling` from [3.2 §10](ch3_2_pandas.md#10-lead-lag-and-rolling-windows).

    **Individual stock returns.** `stock_utf.csv` holds daily records for ten listed
    stocks over 1990–2000, in 75 columns. Work out what the variables are, then build
    a `DataFrame` with only what you need — `PrevClPr` and `Clpr`. Construct the daily
    return from those two, then the cumulative return over every 5 days, per stock.

    **Market return.** `Chinese_market.csv` has `stkcd` (stock code), `trdmnt`
    (trading month), `mclsprc` (closing price), and `msmvttl` (total market value).
    Compute the market-value-weighted average closing price across all firms in each
    month — that series is how the market as a whole performed.

    **Index return.** `FT50.xlsx` lists the constituents of the FT50 index. Take the
    subset of `Chinese_market` matching them and compute their weighted average.

    **Portfolio returns.** Hardest, and the most realistic. Each month, sort the stock
    universe by the log of market value and cut it into ten equal parts. The largest
    10% form one portfolio, the next 10% another, and so on. Compute each portfolio's
    simple average return in each month, then the average return of each portfolio
    series over time. You are building the size-sorted portfolios that underpin a
    large part of the asset-pricing literature.

## Summary

| | |
|---|---|
| **Long vs. wide** | Relative, not absolute. Long = more rows than you want; wide = more columns. |
| **`pivot_table`** | Long → wide. `index` / `columns` / `values` = row labels / column names / cell contents. |
| **`aggfunc`** | Defaults to **`"mean"`** — it silently averages duplicates. Pivot with `"count"` once to check. |
| **`.str`** | Applies string methods down a column. The bridge from `"$20,000 "` to `20000`. |
| **Chained style** | Wrap in parentheses, one link per line. Beats `df2`, `df3`, `df4`. |
| **`melt`** | Wide → long. `id_vars` are kept; everything else becomes `variable` / `value`. Name them. |
| **`groupby`** | Split, apply, combine. The object itself holds no data, just group membership. |
| **`first` / `nth`** | Positional, not "largest" — **sort first**. `first` also skips `NaN` per column. |
| **`idxmax`** | Returns a *label*. Select the column before calling it, or it compares strings too. |
| **`dropna`** | Use `subset=`; check `len()` before and after. |
| **`drop_duplicates`** | Count with `.duplicated().sum()` before you drop. |
| **`reset_index`** | `drop=True` after sorting. Forgetting it misaligns cross-table assignment, silently. |

Everything so far has been one table. [3.4](ch3_4_merge.md) is about combining several — which is where the index alignment we keep warning about finally gets a tool built for it.
