# %%
import c_fibonacci
print(c_fibonacci.fibonacci(70))
%timeit c_fibonacci.fibonacci(50)

# %%
import time

def timer(func):
    def wrapper(*args, **kwargs):
        stime = time.perf_counter()
        res = func(*args, **kwargs)
        etime = time.perf_counter()
        print(f"time elapsed: {etime - stime}")
        return res
    return wrapper

@timer
def p_fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a
# %%
print(p_fibonacci(70))


# %%
%timeit p_fibonacci(50)

# %%
