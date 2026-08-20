# 1. Style and Error Messages

```motto
Code is read far more often than it is written — including by you, six months from now.
```

## Introduction

We open the two days with the two things that cost graduate students the most time and get taught the least: **how your code should look**, and **what to do when it stops**. Neither is glamorous. Both compound. A project written in a consistent style is one you can still read after a semester away; a traceback you can read is a bug fixed in two minutes instead of an afternoon of `print` statements.

The chapter has three parts. §1.1 is the community's style agreement, PEP 8, in the five points that actually come up. §1.2 is the anatomy of a traceback and the machinery of `try`/`except`. §1.3 — new since the course was first taught — is the part that makes §1.1 nearly free: modern tooling that formats your code for you, so style stops being something you remember and becomes something that just happens.

## 1.1 The PEP 8 style guide

PEP stands for **Python Enhancement Proposal**, the numbered documents in which changes to Python are proposed, argued over, and recorded. Most PEPs are about the language itself. [PEP 8](https://peps.python.org/pep-0008/) is different: it proposes nothing about how Python *works* and everything about how Python should be *written*. It is the reason code from a stranger's repository looks like code from yours.

It is a long document. Five points cover most of what you will meet.

1. **Use four spaces per indentation level.** ([🐍](https://peps.python.org/pep-0008/#indentation)) Not two, not a tab. Indentation is syntax in Python, so this is not merely cosmetic.
2. **Never mix tabs and spaces for indentation.** ([🐍](https://peps.python.org/pep-0008/#tabs-or-spaces)) Python 3 refuses to guess: inconsistent indentation raises `TabError` before your program runs a single line. Configure your editor to insert spaces when you press Tab and this problem disappears permanently.
3. **Use blank lines sparingly — no more than two.** ([🐍](https://peps.python.org/pep-0008/#blank-lines)) Two blank lines between top-level functions and classes, one between methods inside a class, and single blank lines inside a function only to separate logical steps.
4. **Mind your whitespace.** ([🐍](https://peps.python.org/pep-0008/#pet-peeves)) No space just inside brackets, none before a comma or colon, one on each side of a binary operator. `f(x[1], {"a": 2})`, not `f( x[ 1 ] , { "a" : 2 } )`.
5. **Follow the naming conventions.** ([🐍](https://peps.python.org/pep-0008/#naming-conventions)) `lower_snake_case` for functions, variables, and modules; `CapWords` for classes; `UPPER_SNAKE_CASE` for constants. A leading underscore marks something as internal — a convention we return to in [5.1.1](camp_ch5_oop.md#511-naming-conventions-private-names-and-name-mangling), where the *double* underscore turns out to do something the interpreter actually enforces.

Line length is the sixth point, and the one people argue about. PEP 8 says 79 characters, a number inherited from terminals that no longer exist. Most modern projects settle at 88 (the default of the `black` formatter) or 100. Pick one, put it in your project's configuration, and stop thinking about it.

???+ warning "Pitfall: style is a convention, not a rule the interpreter checks"
    Almost nothing in PEP 8 is enforced by Python. Name a class `my_class` and it runs
    fine. The cost is paid later and by people — the reader who has to work out
    whether `my_class` is a class, a function, or a dictionary. The one exception is
    indentation, which *is* syntax: get that wrong and nothing runs at all.

## 1.2 Reading and handling error messages

Style is about the code that works. This section is about the code that does not — which, in practice, is most of the code most of the time. Being fluent in tracebacks is not a debugging tip; it is the difference between reading what Python already told you and guessing.

Suppose you write this in a file called `exception_example.py`. There is a deliberate typo in it — the last line of the function returns `next_sum1`, a name that is never defined:

```python
def print_sum(x):
    print(x)
    def next_sum(y):
        return print_sum(x + y)
    return next_sum1


print_sum(1)(3)(5)
```

Run it and Python prints this before stopping:

```pytb
1
Traceback (most recent call last):
  File "exception_example.py", line 8, in <module>
    print_sum(1)(3)(5)
    ~~~~~~~~~^^^
  File "exception_example.py", line 5, in print_sum
    return next_sum1
           ^^^^^^^^^
NameError: name 'next_sum1' is not defined. Did you mean: 'next_sum'?
```

Read it from the **bottom up**, because that is where the answer is. The last line names the exception type (`NameError`) and describes it in plain English; since Python 3.12 it will even suggest the name you probably meant. Above that, the stack is printed **oldest call first**, so the *last* frame listed is where the error actually happened — line 5, inside `print_sum`. The frames above it tell you how you got there: line 8 of the module called `print_sum(1)`.

The `~~~^^^` markers under each line are worth knowing. Python 3.11 and later highlight the exact sub-expression at fault, which matters enormously on a dense line: in the module frame the tildes mark the callable and the carets mark the call that failed, so on a line like `a[i] + b[j] * c[k]` you are told *which* subscript blew up rather than being left to work it out.

!!! tip "One line of advice worth more than the rest of this section"
    Read [Understanding the Python Traceback](https://realpython.com/python-traceback/)
    once, properly, and the next hundred error messages will cost you seconds each.

### `try`, `except`, and the order of handlers

Once you can read an exception, the next question is what to do about it. The `try` statement lets you attempt something and take a different path when it fails. What catches most people out is that when several `except` clauses could match, **the first matching clause wins** — not the most specific one. Handlers are tested top to bottom, and a class matches if the raised exception is that class *or a subclass of it*.

The example below defines three unrelated exception classes and raises each in turn, with the handlers listed in reverse order. Because the three classes are siblings rather than ancestors of one another, each `raise` finds exactly one match and the ordering makes no difference — which is the controlled case to have in mind before we break it.

???+ example "Example 1.1: which `except` clause runs"
    ```python
    class Exception1(Exception):
        pass

    class Exception2(Exception):
        pass

    class Exception3(Exception):
        pass

    for cls in [Exception1, Exception2, Exception3]:
        try:
            raise cls()
        except Exception3:
            print("Exception 3 occurred! What'd I do???")
        except Exception2:
            print("Exception 2 occurred! What'd I do???")
        except Exception1:
            print("Exception 1 occurred! What'd I do???")
    ```

Now change one line and the lesson arrives. Make the classes a chain — `class Exception2(Exception1)` and `class Exception3(Exception2)` — and put the broad handler first. Every raise is caught by `except Exception1`, because every one of them *is* an `Exception1`, and the two clauses below it become unreachable code that Python will never warn you about.

???+ example "Example 1.2: a broad handler first swallows everything"
    ```python
    class Exception1(Exception):
        pass

    class Exception2(Exception1):   # now a subclass
        pass

    class Exception3(Exception2):   # and a sub-subclass
        pass

    for cls in [Exception1, Exception2, Exception3]:
        try:
            raise cls()
        except Exception1:          # matches all three!
            print("caught as Exception1:", cls.__name__)
        except Exception2:
            print("never reached")
        except Exception3:
            print("never reached")
    ```

???+ warning "Pitfall: `except Exception` at the top of the list"
    The same trap, one level up: `except Exception:` catches essentially everything,
    so any handler after it is dead. Order your clauses **most specific first**, and
    reach for a bare `except Exception:` only when you genuinely mean "whatever went
    wrong, keep going" — and even then, log the exception rather than discarding it.

We come back to the rest of the `try` statement — the lifetime of the `as` name, and the fact that `finally` runs even after a `return` — in [3.3.6](camp_ch3_names.md#336-the-try-statement), once we have the vocabulary of names and namespaces to describe it precisely. The main course covers the same ground more gently in [2.4 §5](ch2_4_use_cases.md).

## 1.3 Let a tool do it for you

The section above describes how your code should look. Nothing in it is worth a minute of your attention while you are writing, because a formatter will do all of it for you, correctly, every time you save.

The tool to learn is [**Ruff**](https://docs.astral.sh/ruff/): a single, very fast program that both *checks* your code against PEP 8 (and several hundred other rules) and *reformats* it. It has replaced the older stack of `flake8` + `black` + `isort` in most new projects.

```powershell
pip install ruff
ruff format .    # rewrite every file in this folder to a consistent style
ruff check .     # report the problems formatting cannot fix
```

`ruff format` handles indentation, blank lines, whitespace, quote style, and line breaking. `ruff check` is the interesting half — it catches unused imports, shadowed built-ins, mutable default arguments (a bug we will meet properly in [Example 4.2](camp_ch4_functions.md#41-simple-functions)), and comparisons to `None` with `==`. Configure it once, in the `pyproject.toml` at the root of your project:

```toml
[tool.ruff]
line-length = 88
```

Better still, have your editor run it on save; every editor discussed in [2.4](camp_ch2_environments.md#24-writing-code) can. Style then costs you nothing at all, and the review conversation moves on from where the spaces go to whether the code is right.

## Summary

| | |
|---|---|
| **PEP 8 in one line** | Four spaces, no tabs, sparing blank lines, careful whitespace, conventional names. |
| **Read tracebacks bottom-up** | The exception type and message are last; the deepest frame is directly above them. |
| **Trust the `^^^` markers** | Python 3.11+ points at the exact failing sub-expression. |
| **Order `except` clauses specific first** | The *first* match wins, not the closest one; a broad handler makes the rest dead code. |
| **Automate the style** | `ruff format` and `ruff check` on save; put `line-length` in `pyproject.toml`. |
