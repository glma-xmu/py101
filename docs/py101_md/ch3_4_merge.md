# pandas: Combining Tables

```motto
Two tables about the same things can be made one — if you can say what "the same" means.
```

## Introduction

Think back to your high-school grades. Your Chinese teacher recorded the Chinese scores, your maths teacher the maths scores, your English teacher the English scores. Three tables, three separate sources of truth. Yet at the parent–teacher meeting the class teacher had *all* of them, on one sheet, one row per student — because somebody combined them.

That is this page. Research data arrives the same way and almost never in one file: prices come from an exchange, accounting figures from financial reports, GDP from one government table, population from another. Nothing interesting happens until they are one table.

The tool is **`merge`**, and the whole difficulty is in a single question: *how does a row in one table correspond to a row in the other?* Get that right and merging is a one-liner. Get it wrong and you produce a table that looks perfectly reasonable and is silently wrong — which is why this page spends most of its length on the ways it goes wrong.

We work with two tables throughout. Three or more is just two, repeated.

pandas also offers `concat`, `join`, and `update`, which are worth reading about; `merge` is the general one and the only one you truly need.

## 1. Why you cannot just assign a column

Start with the mistake, because it is the one everybody makes and it is a direct consequence of [3.2 §7](ch3_2_pandas.md#7-new-columns-arithmetic-across-a-table).

Each teacher sorted their own list differently — one alphabetically, one by score. The names are the same three students in a different order.

???+ example "Example: the obvious approach, and why it fails"
    ```python
    import pandas as pd

    C_score = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"],
                            "Chinese": [90, 85, 70]})
    m_score = pd.DataFrame({"name": ["Bob", "Charlie", "Alice"],
                            "math": [95, 86, 77]})
    print(C_score, "\n")
    print(m_score, "\n")

    wrong = C_score.copy()
    wrong["math"] = m_score["math"]     # looks reasonable. it is not.
    print(wrong)
    ```

Alice gets 95. Alice sat in row 0 of the first table, and row 0 of the second table belongs to Bob.

Assigning a column aligns on the **index** — the row labels `0, 1, 2` — and both tables have those labels, so pandas matched them happily and reported nothing. The index encoded *position in this particular file*, which is not a fact about the student.

What you needed was to match on **`name`**. That is exactly what `merge` does.

???+ note "Key concept: the merge key"
    A **key** is the column (or columns) whose values identify the same real-world
    entity in both tables. Merging matches rows by comparing keys, not positions. The
    hardest part of any merge is deciding what the key is — and confirming it really
    does identify one thing.

## 2. `merge` and the `on` parameter

`pd.merge(left, right, on=...)` matches rows whose key values are equal.

???+ example "Example: merging on a shared key"
    ```python
    import pandas as pd

    C_score = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"],
                            "Chinese": [90, 85, 70]})
    m_score = pd.DataFrame({"name": ["Bob", "Charlie", "Alice"],
                            "math": [95, 86, 77]})

    print(pd.merge(C_score, m_score, on="name"))
    ```

Alice now has 90 and 77. The row order of either input stopped mattering the moment we named a key.

Merging on **several** columns at once is just as common, and you do it by passing a list. In panel data the key is almost always an entity *and* a time period:

```python
pd.merge(prices, accounts, on=["firm_id", "year"])
```

Getting that wrong is a classic error. Merge firm-year data on `firm_id` alone and every year of one table matches every year of the other — nine rows become eighty-one, and you may not notice until a mean looks strange. **Check `.shape` before and after every merge.**

## 3. The five modes of `how`

Now the second question. What should happen to a row that has **no match** in the other table?

Suppose David was ill for the Chinese exam but sat the maths one, and Eve did the reverse. Whether they belong in the combined table is not a pandas question — it is a question about your rules. If the rule is "only students who sat both exams," you keep neither. If it is "anyone who sat at least one," you keep both.

That choice is the **`how`** parameter, and there are five values:

| `how` | Which rows survive |
|---|---|
| `"inner"` *(default)* | only keys present in **both** — the intersection |
| `"outer"` | every key from **either** — the union, with `NaN` where a side is missing |
| `"left"` | every key from the **left** table; matching info pulled in from the right |
| `"right"` | every key from the **right** table |
| `"cross"` | every row paired with every row. Rarely what you want |

"Left" and "right" mean literally the first and second arguments you passed.

???+ example "Example: the four modes that matter, side by side"
    ```python
    import pandas as pd

    C_score = pd.DataFrame({"name": ["Alice", "Bob", "Charlie", "Eve"],
                            "Chinese": [90, 85, 70, 70]})
    m_score = pd.DataFrame({"name": ["Bob", "Charlie", "Alice", "David"],
                            "math": [95, 86, 77, 60]})

    for how in ["inner", "outer", "left", "right"]:
        out = pd.merge(C_score, m_score, on="name", how=how)
        print(f"--- how={how!r}  ({out.shape[0]} rows) ---")
        print(out)
        print()
    ```

Read the four results against each other. `inner` drops both David and Eve. `outer` keeps both and fills the gaps with `NaN`. `left` keeps Eve but not David; `right` the reverse. Nobody's *scores* changed — only who is on the sheet.

Think of `how` as choosing an **anchor**: which table's list of entities defines the rows of the result.

???+ warning "Pitfall: the default is `inner`, and it deletes rows quietly"
    Omit `how` and you get `inner`, which silently discards every unmatched row. On a
    merge where the keys do not line up as well as you assumed — a mistyped country
    name, a year stored as text in one file and a number in the other — you can lose
    most of your sample and get back a small, clean, entirely misleading table.

    Guard against it by counting:

    ```python
    print(len(left), len(right))
    merged = pd.merge(left, right, on="id", how="inner")
    print(len(merged))          # did this collapse?
    ```

    When you are unsure, merge with `how="outer"` and `indicator=True`. That adds a
    `_merge` column saying `left_only`, `right_only`, or `both` for each row, and
    `merged["_merge"].value_counts()` tells you immediately how well the keys matched.

???+ question "In-class exercise: feeding the zoo"
    Two companies jointly run a zoo. Company A weighs the animals; Company B sets a
    feeding standard for each. If an animal is **heavier** than its standard it gets
    the smaller ration, otherwise the larger one.

    The tables are `zooA.csv` (`animal`, `weight`) and `zooB.csv`
    (`animal`, `standard`, `less`, `more`). Produce a table giving the amount of food
    for each animal.

    Watch the row counts: the two files do not list the same animals. Decide which
    `how` your answer needs, and be able to justify what should happen to an animal
    that appears in only one of them.

## 4. Different key names: `left_on` and `right_on`

Two tables often identify the same thing under different column names — `permno` in one, `gvkey` in another; `date` here, `trdmnt` there. Then `on=` cannot work, since it needs one name that exists on both sides.

Before the fix, look carefully at what pandas does when you leave `on` out entirely. It falls back to merging on **all column names the two tables share**:

???+ example "Example: an empty result means the wrong key"
    ```python
    import pandas as pd

    Ultramen = pd.DataFrame({
        "name": ["Ultraman", "Ultraseven", "UltraReturn"],
        "time": [1967, 1968, 1972],
    })
    Monster = pd.DataFrame({
        "name": ["Bemular", "Eleking", "Bemstar"],
        "year": [1967, 1968, 1972],
    })

    oops = pd.merge(Ultramen, Monster, how="inner")
    print(oops)
    print("shape:", oops.shape)      # (0, 3) -- no rows at all!
    ```

The only shared column name is `name`, so pandas matched heroes against monsters by name, found no hero called Bemular, and returned an empty table. No error, no warning — an empty `DataFrame` is a perfectly valid result.

**An empty merge almost always means you merged on the wrong key.** Learn to recognise it.

The years *do* correspond; they are simply called `time` on one side and `year` on the other. Say so:

???+ example "Example: `left_on`, `right_on`, and `suffixes`"
    ```python
    import pandas as pd

    Ultramen = pd.DataFrame({
        "name": ["Ultraman", "Ultraseven", "UltraReturn"],
        "time": [1967, 1968, 1972],
    })
    Monster = pd.DataFrame({
        "name": ["Bemular", "Eleking", "Bemstar"],
        "year": [1967, 1968, 1972],
    })

    print(pd.merge(Ultramen, Monster, how="inner",
                   left_on="time", right_on="year"))
    print()
    print(pd.merge(Ultramen, Monster, how="inner",
                   left_on="time", right_on="year",
                   suffixes=["_ultraman", "_monster"]))
    ```

Now look at the column names in the first result: `name_x` and `name_y`. Both tables had a column called `name`, and since it was not the key, pandas had to keep both and disambiguate them. `_x` and `_y` are the defaults, and three lines later you will not remember which was which. **`suffixes` is worth setting on every merge where the inputs share column names.**

Note also that `left_on`/`right_on` keeps *both* key columns — `time` and `year` — where `on` would have kept one. Drop the redundant one if it bothers you.

???+ question "In-class exercise: self-reported versus UN figures"
    `country_self.csv` holds values each country reports about itself;
    `country_UN.csv` holds the UN's figures for the same countries and years. Merge
    them so the two sources sit side by side, then compute the difference for each
    country in each year.

    Look at both files before writing any code. The country identifiers are not in
    the same form, and no `how=` will fix that — it is a problem you must solve
    *before* merging. What do you have to do to one of the columns first?

## 5. `validate`: catching a merge that multiplies rows

Here is the failure that costs people the most time, because the output looks entirely normal.

A merge does not just match rows — where a key appears several times, it matches **every** combination. Merge a table of 3 advisors with a table of 7 advisees on the advisor's name and you get 7 rows, which is right. But merge two tables that you *believed* had unique keys and one of them secretly does not, and your row count multiplies. Every subsequent mean, sum, and regression is then computed over duplicated observations.

The **`validate`** parameter makes pandas check your assumption and raise an error if it is false.

- `"one_to_one"` — keys unique on both sides
- `"one_to_many"` — unique on the left, repeated on the right
- `"many_to_one"` — repeated on the left, unique on the right
- `"many_to_many"` — no check (the default behaviour)

???+ example "Example: `validate` turns a silent bug into an error"
    ```python
    import pandas as pd

    advisor = pd.DataFrame({"name": ["Zhao", "Qian", "Sun"],
                            "age": [37, 45, 68]})
    advisee = pd.DataFrame({"name": ["Alice", "Bob", "Charlie", "David", "Emma"],
                            "advisor": ["Zhao", "Qian", "Qian", "Sun", "Qian"]})

    ok = pd.merge(advisor, advisee, how="outer",
                  left_on="name", right_on="advisor",
                  validate="one_to_many")          # true: one advisor, many advisees
    print(ok, "\n")

    try:
        pd.merge(advisor, advisee, how="outer",
                 left_on="name", right_on="advisor",
                 validate="one_to_one")            # false -- and pandas says so
    except Exception as e:
        print(type(e).__name__, ":", e)
    ```

The second call raises `MergeError: Merge keys are not unique in right dataset; not a one-to-one merge`. Without `validate` it would have returned the same 7-row table as the first, and you would have had no way to know whether that was intended.

Write down what you expect the relationship to be, then make `validate` enforce it. It costs one argument and catches a whole class of error that is otherwise invisible.

???+ question "In-class exercise: linking CRSP and Compustat"
    This is a genuine piece of empirical finance plumbing, and it is fiddly on purpose.

    - `permno.csv` — from the exchanges. `permno` is a firm's permanent number; `year` the observation year; `price` the end-of-year price.
    - `gvkey.csv` — from financial reports. `gvkey` is S&P's identifier for a firm; `year` and `size` as before.
    - `linktable.csv` — how the two identifiers correspond: `permno`, `gvkey`, `stime`, `etime`.

    Exchanges use `permno`; S&P uses `gvkey`. The same firm has both, so you must go
    through the link table to bring `size` and `price` into one table.

    Two things make this real work rather than a one-liner. First it takes **two**
    merges, not one — through the link table. Second, look hard at `stime` and
    `etime`: `permno` 100000 maps to `gvkey` 237816 for 2000–2002 and to a *different*
    `gvkey` from 2003. **The mapping changes over time.** A merge on the identifiers
    alone will attach the wrong years to each other and hand you more rows than you
    started with — so check `.shape` at every step, and think about where `year`
    belongs in your keys.

???+ question "In-class exercise: two exams, one class ranking"
    University X lets students sit either exam A or exam B. To be fair, each score is
    standardised within its own exam: a student scoring $x$ on exam A is reported as
    $(x - \mu_A) / \sigma_A$, where $\mu_A$ and $\sigma_A$ are the mean and standard
    deviation among students who sat exam A. Exam B is adjusted the same way against
    its own mean and standard deviation.

    The scores are in `scoreA.csv` and `scoreB.csv`. Produce one table reporting the
    adjusted score for the whole class.

    Think first about whether this is really a `merge` at all. Each student appears in
    exactly one file, and both files have the same columns — so are you matching rows
    *across* tables, or stacking them on top of each other? Look up `pd.concat`, and
    be ready to say why it, and not `merge`, is the right tool here.

## 6. A full analysis: China's provincial GDP

This last exercise uses everything from 3.2, 3.3, and this page. It is the shape of a real empirical project: several official files, none in the form you need, and a question that only makes sense after they are one table.

???+ question "In-class exercise: real GDP per worker by region"
    The files come from the National Bureau of Statistics: `GDP_by_province.csv`
    (31 provinces, one column per year), `pop_by_province.csv`,
    `unemp_by_province.csv` (urban unemployment, used as a proxy for the total rate),
    `CPI_by_province.csv`, and `region.csv` for geography.

    1. Combine GDP and population so that each province in each year has both. They arrive **wide**, one column per year — so reshape before you merge ([3.3 §3](ch3_3_reshape_group.md#3-melt-from-wide-to-long)), and think about what the key must be.
    2. Compute average GDP per person for each province and year. Then, using the unemployment rate, compute GDP per *working* person.
    3. The CPI file gives each year's price index **relative to the previous year** — Beijing's 2022 figure of 101.8 means prices rose 1.8% over 2021. Convert these into indices relative to a 2014 base, so every figure is in 2014 yuan, and deflate GDP to get **real** GDP. *Hint: relative-to-previous-year indices chain by multiplication, which means a cumulative product within each province — look up `cumprod`, and mind the order of the years.*
    4. Compute each province's average population, then the median of those averages (`np.median`). Provinces above it count as large-population. Use `region.csv` to attach geography, then compute average real regional GDP by year.
    5. For each region and year, what share of the region's total do the large-population provinces contribute? Explain what you find.

    Step 3 is where most people go wrong, and the error is silent: the year columns
    are in **descending** order in these files, so a cumulative product computed
    left to right chains the wrong way. Sort first, and sanity-check that the 2014
    index comes out as 100.

## Summary

| | |
|---|---|
| **Why `merge`** | Assigning a column aligns on the **index** (position); merging aligns on a **key** (identity). |
| **`on`** | The shared key column. Pass a **list** for panel data — usually entity *and* period. |
| **`how="inner"`** | The default. Keeps only keys in both, and drops the rest **silently**. |
| **`how="outer"`** | Keeps every key from either side, `NaN` where missing. |
| **`how="left"` / `"right"`** | Anchor on the first / second argument's list of entities. |
| **No `on` given** | pandas merges on *all* shared column names — a frequent cause of an empty result. |
| **`left_on` / `right_on`** | When the key is called something different on each side. Keeps both columns. |
| **`suffixes`** | Set it whenever the inputs share non-key column names, or you get `_x` and `_y`. |
| **`validate`** | `"one_to_one"`, `"one_to_many"`, `"many_to_one"`. Turns a silent row explosion into an error. |
| **`indicator=True`** | Adds a `_merge` column; `value_counts()` on it shows how well the keys matched. |
| **Always** | Print `.shape` before and after. A merge that changes the row count unexpectedly is a bug. |

That completes Chapter 3. You can now load data from a file, inspect and clean it, reshape it into whatever form your question needs, split it into groups, and combine it with other sources — which is, in practice, the great majority of what applied empirical work consists of.
