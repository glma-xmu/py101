# Exercises — Chapter 3: NumPy and pandas

A set of practice problems, grouped by the section they exercise. Try them on your own; where a problem shows code, treat it as the given data or a starting point. Each problem shows a **sample output** so you know what to aim for. Solutions are not provided here.

Every problem builds its own data, so nothing here depends on a file you have to download. Where a problem uses random numbers it sets a seed first, so your answer should match the sample output exactly.

## 1. NumPy

???+ question "Exercise 1.1 — array vs list"
    Build `nums = [1, 2, 3, 4]` and `arr = np.array(nums)`. Print `nums * 2` and `arr * 2`. Explain in one sentence why they differ.

    **Sample output**
    ```text
    [1, 2, 3, 4, 1, 2, 3, 4]
    [2 4 6 8]
    ```

???+ question "Exercise 1.2 — dtype is decided once, for the whole array"
    Create arrays from `[1, 2, 3]`, `[1, 2, 3.0]`, and `[1, 2, "3"]`. Print each array's `dtype`. Why does adding one float, or one string, change the type of *every* element?

???+ question "Exercise 1.3 — the cost of a Python object"
    Compare `sys.getsizeof(10**9)` with `np.int64().nbytes`. Then build `np.arange(1_000_000)` and print its `nbytes`. Roughly how much memory would a Python list of the same million integers need, and why?

???+ question "Exercise 1.4 — vectorise a loop"
    Given `prices = np.array([100.0, 102.5, 101.0, 105.5, 104.0])`, compute the simple return from each day to the next **without writing a loop**. You should get four numbers.

    **Hint:** slice the array twice, offset by one.

    **Sample output**
    ```text
    [ 0.025      -0.01463415  0.04455446 -0.01421801]
    ```

???+ question "Exercise 1.5 — boolean masks"
    Using `prices` from 1.4, print the prices above their own mean, and count how many there are. Do it with a boolean mask, not a loop.

???+ question "Exercise 1.6 — where"
    With the returns from 1.4, use `np.where` to build an array of the strings `"up"` and `"down"`. Then count the `"up"` days.

???+ question "Exercise 1.7 — broadcasting a row"
    Build `m = np.arange(12).reshape(3, 4)` and `row = np.array([100, 200, 300, 400])`. Print `m + row`. Then try `m + np.array([1, 2, 3])` and explain the error in terms of shapes.

???+ question "Exercise 1.8 — demeaning by column"
    With `m` from 1.7, subtract each column's mean from that column, so every column of the result has mean zero. Verify with `.mean(axis=0)`.

    **Hint:** `m.mean(axis=0)` has shape `(4,)`, which broadcasts against `(3, 4)`.

???+ question "Exercise 1.9 — axis discipline"
    For `m = np.arange(12).reshape(3, 4)`, predict *before running* what `m.sum()`, `m.sum(axis=0)` and `m.sum(axis=1)` each give, including their shapes. Then check.

???+ question "Exercise 1.10 — reshape and transpose are different"
    Take `a = np.arange(6)`. Print `a.reshape(2, 3)` and `a.reshape(2, 3).T`. Then print `a.reshape(3, 2)`. Are `reshape(3, 2)` and `reshape(2, 3).T` the same array? Explain.

???+ question "Exercise 1.11 — a slice is a view"
    Build `a = np.arange(10)`, take `b = a[2:5]`, then set `b[0] = 999`. Print `a`. Now repeat with `c = a[2:5].copy()`. Explain the difference, and check both with `np.shares_memory`.

    **Sample output**
    ```text
    [  0   1 999   3   4   5   6   7   8   9]
    ```

???+ question "Exercise 1.12 — a simulated portfolio"
    Set `rng = np.random.default_rng(2026)` and draw `returns = rng.normal(0.0005, 0.02, size=(252, 4))` — one year of daily returns for four assets. Report each asset's mean daily return, its annualised volatility (daily standard deviation times $\sqrt{252}$), and which asset had the single worst day.

## 2. pandas: one table

???+ question "Exercise 2.1 — Series carries an index"
    Build `costs = pd.Series([1300, 2500, 90, 870], index=["rent", "tuition", "coffee", "books"])`. Print the Series, then `costs["tuition"]`, then `costs.index`. How does this differ from a NumPy array holding the same four numbers?

???+ question "Exercise 2.2 — alignment happens on the index, not position"
    Build two Series with *different* index orders:

    ```python
    a = pd.Series([1, 2, 3], index=["x", "y", "z"])
    b = pd.Series([10, 20, 30], index=["z", "y", "x"])
    ```

    Predict `a + b` before running it. Why is this behaviour a feature rather than a nuisance?

    **Sample output**
    ```text
    x    31
    y    22
    z    13
    dtype: int64
    ```

???+ question "Exercise 2.3 — build a DataFrame"
    Create this table as a `DataFrame` called `staff`, then print `.shape`, `.dtypes`, and `.info()`.

    | name | dept | salary | years |
    |---|---|---|---|
    | Alice | Econ | 95000 | 6 |
    | Bob | Finance | 105000 | 3 |
    | Chen | Econ | 88000 | 9 |
    | Dara | Marketing | 76000 | 2 |
    | Elif | Finance | 120000 | 11 |

???+ question "Exercise 2.4 — one column, two ways"
    From `staff`, get the `salary` column using both `staff["salary"]` and `staff.salary`. Then get a *DataFrame* containing only `salary` — note the double brackets. Print `type()` for all three.

???+ question "Exercise 2.5 — sorting"
    Sort `staff` by `salary` descending. Then sort by `dept` ascending and, within each department, `salary` descending. Print both.

???+ question "Exercise 2.6 — describe, and what it silently skips"
    Call `staff.describe()`. Which columns appear, and which are missing? Now call `staff.describe(include="all")` and explain what changed.

???+ question "Exercise 2.7 — a new column"
    Add a column `monthly` equal to `salary / 12`, rounded to whole currency units. Then add `senior`, a boolean that is `True` when `years >= 5`. Print the table.

???+ question "Exercise 2.8 — `.loc` vs `.iloc`"
    Set `name` as the index of `staff`. Then, using the right one of `.loc` / `.iloc` for each:

    1. the row for `"Chen"`
    2. the first two rows
    3. `salary` and `years` for `"Alice"` and `"Elif"`
    4. the value in the third row, second column

    State for each which you used and why.

???+ question "Exercise 2.9 — filtering"
    From `staff`, select everyone in `Finance` earning more than 100000. Then select everyone *not* in `Econ`. Then select those with `years` between 3 and 9 inclusive.

    **Hint:** combine conditions with `&` and `|`, and parenthesise each one.

???+ question "Exercise 2.10 — the chained-assignment trap"
    Run the following and explain what goes wrong:

    ```python
    econ = staff[staff.dept == "Econ"]
    econ["bonus"] = econ.salary * 0.1
    ```

    Then rewrite it so the intent is unambiguous and no warning appears.

???+ question "Exercise 2.11 — reading a file you do not have"
    Write — but do not run — the code to read `staff.csv` into a DataFrame, where the file sits in a `data/` folder beside your notebook. Then write the variant for a file whose first line is *not* a header. Finally, write the line that would save `staff` back out without its index.

???+ question "Exercise 2.12 — stack and unstack"
    Build a two-level column index:

    ```python
    scores = pd.DataFrame(
        [[85, 90, 88, 91], [78, 82, 80, 85], [92, 89, 94, 90]],
        index=["Alice", "Bob", "Chen"],
        columns=pd.MultiIndex.from_product([["Exam1", "Exam2"], ["Math", "English"]]),
    )
    ```

    Print `scores`, then `scores.stack()`, then `scores.stack().unstack()`. Does the last one return you to exactly where you started?

???+ question "Exercise 2.13 — lag with `shift`"
    Build a small annual series and add a `last_gdp` column using `shift(1)`, then a `growth` column from the two.

    ```python
    gdp = pd.DataFrame({
        "year": [2019, 2020, 2021, 2022, 2023],
        "gdp":  [21.4, 21.0, 23.3, 25.7, 27.4],
    })
    ```

???+ question "Exercise 2.14 — two traps in `shift`"
    This is the exercise most worth doing carefully. In each case, `shift(1)` gives a *wrong* answer. Say why, then fix it.

    **Trap 1 — the rows are not in order.**

    ```python
    ages1 = pd.DataFrame({
        "id":   [1, 1, 1, 1, 1],
        "year": [2002, 2004, 2003, 2005, 2006],
        "age":  [23, 25, 24, 26, 27],
    })
    ages1["last_age"] = ages1.age.shift(1)
    ```

    **Trap 2 — there is more than one person.**

    ```python
    ages2 = pd.DataFrame({
        "id":   [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
        "year": [2002, 2004, 2003, 2005, 2006, 2002, 2004, 2003, 2005, 2006],
        "age":  [23, 25, 24, 26, 27, 17, 19, 18, 20, 21],
    })
    ages2["last_age"] = ages2.age.shift(1)
    ```

    For Trap 2, which row is most obviously wrong, and what should it contain instead?

???+ question "Exercise 2.15 — rolling windows"
    Using the daily prices below, add a 3-day rolling mean and a 3-day rolling standard deviation. Why are the first two rows `NaN`, and what would `min_periods=1` change?

    ```python
    px = pd.Series([100, 102, 101, 105, 104, 108, 107])
    ```

## 3. Reshaping and grouping

???+ question "Exercise 3.1 — name the shape"
    For each table, say whether it is cross-sectional, a time series, or a panel, and give the column(s) that identify one observation.

    1. GDP of 31 provinces, 2023 only
    2. One country's quarterly inflation, 1990–2024
    3. GDP of 31 provinces, each year 2014–2023
    4. Closing price of 500 stocks on one trading day

???+ question "Exercise 3.2 — wide to long"
    Convert this wide table to long form, so that each province-year pair is one row with columns `province`, `year`, `gdp`.

    ```python
    wide = pd.DataFrame({
        "province": ["Beijing", "Shanghai", "Guangdong"],
        "2021": [4.03, 4.32, 12.44],
        "2022": [4.16, 4.47, 12.91],
        "2023": [4.38, 4.72, 13.57],
    })
    ```

    **Sample output** (first three rows)
    ```text
        province  year    gdp
    0    Beijing  2021   4.03
    1   Shanghai  2021   4.32
    2  Guangdong  2021  12.44
    ```

???+ question "Exercise 3.3 — long back to wide"
    Take your long table from 3.2 and pivot it back so the years are columns again. Confirm you recover the original. Which method did you use, and why not the other one?

???+ question "Exercise 3.4 — groupby basics"
    Using `staff` from §2, compute the mean salary by department, the headcount by department, and the highest-paid person's salary in each department.

???+ question "Exercise 3.5 — agg with several statistics"
    In one call, produce the count, mean, and standard deviation of `salary` by `dept`, and the maximum of `years` by `dept`. Name the resulting columns sensibly.

???+ question "Exercise 3.6 — transform keeps the shape"
    Add a column `dept_mean` to `staff` giving each person's departmental average salary, then a column `above_dept` showing how far above or below that average they are. Note that `transform` returns one value per *row*, not per group — explain why that matters here.

???+ question "Exercise 3.7 — shares that sum to one"
    Compute each person's share of their own department's total salary. Verify by grouping the shares by department and summing — every group must give `1.0`.

???+ question "Exercise 3.8 — a two-way table"
    Build a `pivot_table` of average salary with `dept` as rows and `senior` (from 2.7) as columns. Add row and column totals with `margins=True`. Where do `NaN`s appear, and what do they mean here?

???+ question "Exercise 3.9 — group, then rank"
    Within each department, rank people by salary from highest to lowest, and add the rank as a column. Then keep only the top earner in each department.

## 4. Combining tables

???+ question "Exercise 4.1 — why not just assign"
    You have two tables in different row orders:

    ```python
    left  = pd.DataFrame({"id": [1, 2, 3], "score": [90, 80, 70]})
    right = pd.DataFrame({"id": [3, 1, 2], "grade": ["C", "A", "B"]})
    ```

    Show what goes wrong with `left["grade"] = right["grade"]`, then do it correctly with `merge`.

???+ question "Exercise 4.2 — the five modes of `how`"
    With these tables, run `merge` with each of `inner`, `left`, `right`, `outer`, and `cross`, and describe in one sentence each what you get and how many rows.

    ```python
    a = pd.DataFrame({"key": ["w", "x", "y"], "v1": [1, 2, 3]})
    b = pd.DataFrame({"key": ["x", "y", "z"], "v2": [40, 50, 60]})
    ```

???+ question "Exercise 4.3 — different key names"
    Merge these on the student identifier, which is named differently on each side. Then tidy the result so only one identifier column remains.

    ```python
    students = pd.DataFrame({"sid": [1, 2, 3], "name": ["Alice", "Bob", "Chen"]})
    marks    = pd.DataFrame({"student_id": [1, 2, 3], "mark": [88, 75, 91]})
    ```

???+ question "Exercise 4.4 — the merge that multiplies rows"
    Merge these and count the rows. You start with 3 orders and end with more — explain exactly why.

    ```python
    orders = pd.DataFrame({"cust": ["A", "B", "C"], "amount": [10, 20, 30]})
    contacts = pd.DataFrame({
        "cust":  ["A", "A", "B", "C", "C"],
        "email": ["a1@x", "a2@x", "b@x", "c1@x", "c2@x"],
    })
    ```

    Now re-run with `validate="one_to_one"`. What happens, and why is being told about this early a good thing?

???+ question "Exercise 4.5 — `indicator` tells you what matched"
    Merge `a` and `b` from 4.2 with `how="outer", indicator=True`. Use the resulting column to count how many keys were in the left only, the right only, and both. Why is this the first thing to check after any merge of real data?

???+ question "Exercise 4.6 — merge, then aggregate"
    Combine these, then report total revenue by category.

    ```python
    sales = pd.DataFrame({
        "sku":   ["p1", "p2", "p3", "p1", "p3"],
        "units": [3, 1, 5, 2, 4],
    })
    products = pd.DataFrame({
        "sku":      ["p1", "p2", "p3"],
        "category": ["Food", "Toys", "Food"],
        "price":    [2.50, 12.00, 4.25],
    })
    ```

    **Sample output**
    ```text
    category
    Food    50.75
    Toys    12.00
    Name: revenue, dtype: float64
    ```

???+ question "Exercise 4.7 — concat is not merge"
    Stack these two tables into one, then explain when you would reach for `concat` rather than `merge`.

    ```python
    q1 = pd.DataFrame({"month": ["Jan", "Feb", "Mar"], "sales": [10, 12, 9]})
    q2 = pd.DataFrame({"month": ["Apr", "May", "Jun"], "sales": [14, 15, 13]})
    ```

    What does `ignore_index=True` change, and why does it usually matter?

???+ question "Exercise 4.8 — a link table"
    Firms are identified by `gvkey` in accounting data and `permno` in price data, and the mapping changes over time.

    ```python
    acct  = pd.DataFrame({"gvkey": [1001, 1001, 1002], "year": [2020, 2021, 2020], "assets": [50, 55, 80]})
    price = pd.DataFrame({"permno": [10, 10, 20], "year": [2020, 2021, 2020], "px": [12.0, 13.5, 40.0]})
    link  = pd.DataFrame({"permno": [10, 20], "gvkey": [1001, 1002], "start": [2019, 2019], "end": [2022, 2022]})
    ```

    Join accounting data to prices through the link table, keeping only rows whose `year` falls between `start` and `end`. Report assets and price side by side for each firm-year.

## 5. Applied: a sequential analysis

The questions in this section run **in order** on one DataFrame. Each step updates it, and later steps assume the earlier ones have been done. Do not rebuild the data part-way through. Run this cell first:

```python
import pandas as pd
import numpy as np

rng = np.random.default_rng(2026)
n = 400

orders = pd.DataFrame({
    "order_id":  np.arange(1, n + 1),
    "customer":  rng.choice([f"C{i:03d}" for i in range(1, 61)], n),
    "date":      pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
    "category":  rng.choice(["Food", "Toys", "Books", "Home"], n, p=[0.4, 0.2, 0.25, 0.15]),
    "units":     rng.integers(1, 6, n),
    "unit_cost": rng.uniform(2.0, 40.0, n).round(2),
    "margin":    rng.uniform(0.10, 0.45, n).round(3),
})
print(orders.shape)
orders.head()
```

???+ question "Exercise 5.1 — revenue and profit"
    Add `revenue` (`units × unit_cost`) and `profit` (`revenue × margin`), both rounded to 2 decimals. Report total revenue and total profit, printed as currency with thousands separators.

???+ question "Exercise 5.2 — by category"
    Group by `category` and report order count, total revenue, total profit, and mean margin. Sort by total profit, highest first. Which category earns the most profit, and is it the same one with the most orders?

???+ question "Exercise 5.3 — a calendar dimension"
    Add a `month` column from `date` (as a monthly period or as a year-month string). Then build a pivot table of total revenue with `month` as rows and `category` as columns. Which month was strongest overall?

???+ question "Exercise 5.4 — customers"
    For each customer compute the number of orders, total revenue, and the date of their most recent order. How many customers ordered only once? Print the top 5 customers by revenue.

???+ question "Exercise 5.5 — a customer's share"
    Add a column giving each order's share of that customer's total revenue. Verify the shares sum to 1 within every customer.

???+ question "Exercise 5.6 — bands"
    Classify each order into `"small"`, `"medium"` or `"large"` by revenue, using the 33rd and 67th percentiles as cut-points. Count the orders in each band, and report mean profit per band.

    **Hint:** `pd.qcut` will do the whole thing in one call.

???+ question "Exercise 5.7 — a running total"
    Sort by `date` and add a cumulative revenue column. Then, for each category separately, add a cumulative revenue column that restarts for each category. Explain which of `groupby(...).cumsum()` and a plain `cumsum()` you needed, and why.

???+ question "Exercise 5.8 — month over month"
    From the monthly totals in 5.3, compute each category's month-on-month revenue growth. State clearly what you had to do about the first month, and why sorting matters before you shift.

???+ question "Exercise 5.9 — write it out and read it back"
    Save the final table to `orders_final.csv` without the index, read it back into a new DataFrame, and confirm the shapes match. Then check the `date` column's dtype in the new frame — is it still a datetime? Explain what you would add to `read_csv` to fix it.
