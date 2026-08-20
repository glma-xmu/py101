#%%
def simple_gen():
    yield 1
    yield 2
import dis

def simple_gen():
    yield 1
    yield 2

dis.dis(simple_gen)

# %%
import time

def timeit():
    start_time = time.time()
    print(start_time)
    yield
    elapsed_time = time.time() - start_time
    print(f'{elapsed_time} has passed since {start_time}')
    
t1 = timeit()
next(t1)
# %%
try:
    next(t1)
except StopIteration as e:
    pass

# %%
#some languages compile directly to CPU instructions
#some interpret source code directly while running
#some compile to an intermediate set of instructions and implement a virtual machine that turns those into CPU instructions while running: BYTECODE
#James Bennett
def outer(nums):
    def repeat(func):
        def wrapper(*args, **kwargs):
            for _ in range(nums):
                value = func(*args, **kwargs)
            return value
        return wrapper
    return repeat

@outer(2)
def func1(x):
    print(x)
    return 3
# %%
func1(4)
# %%
