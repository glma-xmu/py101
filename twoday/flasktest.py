#%%
import inspect
import objgraph

def gen_foo():
    for _ in range(10):
        yield inspect.currentframe()

import objgraph
import inspect

# Define a custom filter function
def custom_filter(obj):
    return isinstance(obj, (type(lambda: None), type(sample_function.__code__))) or \
           (hasattr(obj, 'f_code') and isinstance(obj.f_code, type(sample_function.__code__)))

# Show references
# objgraph.show_refs(
#     [sample_function, code_obj, frame],
#     filename='filtered_refs.png',
#     filter=custom_filter
# )
# objgraph.show_refs(gen_foo,
#                 filter=custom_filter)    
gf = gen_foo()
objgraph.show_refs(gf,
                   filter=custom_filter)

print(f'{id(gf.gi_frame):02x}')

gi_frame = gf.gi_frame

frames = list(gf)

print(gf.gi_frame)

for f in frames:
    print(f is gi_frame)
# %%

def corout_avg():
    count = 0
    total = 0
    avg = None
    while True:
        try:
            val = yield avg
        except GeneratorExit:
            return total, count, avg
        else:
            total += val
            count += 1
            avg = total / count

coro = corout_avg()
next(coro)
# %%
coro.send(10)
# %%
coro.send(20)
# %%
coro.send(30)
# %%
try:
    coro.throw(GeneratorExit, "out")
except GeneratorExit as e:
    final_values = e.value
    print(final_values)

# %%
def countdown(n):
    print("Counting down from", n)
    while n >= 0:
        newvalue = (yield n)
        if newvalue is not None:
            n = newvalue
        else:
            n -= -1
            
c = countdown(5)
for n in c:
    print(n)
    if n == 5:
        c.send(1)

# %%
import time
def g():
    for i in range(5):
        time.sleep(2)
        x = yield i
        time.sleep(2)
        yield i

g1 = g()

# %%
id(g1.gi_frame)
# %%
next(g1)
id(g1.gi_frame)
# %%
def my_generator():
    print(f"Before first yield, .gi_running: {gen.gi_running}")
    yield 1  # First yield
    print(f"Between yields, .gi_running: {gen.gi_running}")
    yield 2  # Second yield

# Create the generator
gen = my_generator()

# Check .gi_running before any execution
print(f"Before starting, .gi_running: {gen.gi_running}")

# Start the generator and see the .gi_running status during execution
print(next(gen))  # Executes until the first yield
print(f"After first yield, .gi_running: {gen.gi_running}")

print(next(gen))  # Executes until the second yield
print(f"After second yield, .gi_running: {gen.gi_running}")

# Trying to run again will raise StopIteration, as the generator is exhausted
try:
    print(next(gen))
except StopIteration:
    print(f"Generator finished, .gi_running: {gen.gi_running}")

# %%
def do_twice(func):
    def wrapper():
        func()
        func()
    return wrapper

@do_twice
def func():
    print(1)
    
func()

# %%
def do_twice(func):
    def wrapper():
        func()
        func()
        func()
    return wrapper

func()
# %%
