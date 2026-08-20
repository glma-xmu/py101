'''
Contents:
    1. memory layout model
    2. function call routine
    3. miscellaneous
'''
#%%
def gf(f, *args):
    return f(*args) + 1

def base(x, y):
    return x + y

# %%
gf(base, 1, 2)

# %%
def print_sum(x):
    print(x)
    def next_sum(y):
        return print_sum(x+y)
    return next_sum

print_sum(1)(3)(5)

# %%
nums = [1, 2, 3]
print(id(nums))

nums.append(4)
print(nums, id(nums))

nums = nums + [5]
print(id(nums))
# %%
nums = [1, 2, 3]
for x in nums:
    x = x * 10
print(nums)

# %%
class PBR:
    def __inint__(self):
        self.variable = 'Original'
        self.change(self.variable)
        print(self.variable)
        
    def change(self, var):
        self.variable = 'Changed'
        
pbr = PBR()
pbr

# %%
# put to chapter 4
outer_list = ['a', 'b', 'c']
def func(lst):
    print(id(lst))
    lst.append('d')
    print(id(lst))
    
print(outer_list, id(outer_list))
func(outer_list)
print(outer_list, id(outer_list))
# %%
outer_list = ['a', 'b', 'c']
def func(lst):
    print(id(lst))
    lst= [1, 2, 3]
    print(id(lst))
    
print(outer_list, id(outer_list))
func(outer_list)
print(outer_list, id(outer_list))
# %%
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-command', methods=['POST'])
def run_command():
    command = request.json.get('command')
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return jsonify({"output": result})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e.output)}), 400

if __name__ == '__main__':
    app.run(debug=True)

# %% example 3.2
x, y = 1, 2
x.__radd__(1)

x, y, = [1], [2]
x.__iadd__(y)

x = 1
print(id(x))
x = x + 1
print(id(x))
y = 300
print(id(y))
y += 1
print(id(y))

a = b = []
a += [5]
a
b
a = a + [5]
a
b

# %% example 3.3
from pandas import DataFrame

# %% example 3.3
# If I want to use a for loop to change the values of a list, ...
nums = [1, 2, 3]
for x in nums:
    x += 1
print(nums)

nums = [[1], [2], [3]]
for x in nums:
    x += [1]
print(nums)

# We will talk more about function arguments assignment.
def gotcha(lst, val):
    lst.append(val)
    return
nums = [1, 2, 3]
gotcha(nums, 4)
print(nums)
gotcha(nums, 4)
print(nums)
# what is a best way to write the function
# void swap(int a, int b)
# # what happens from within the function is within the function scope
# {
#     int tmp;
#     tmp = a;
#     a = b;
#     b = tmp;
#     return;
# }

# %%
nums = [[0] * 3 for _ in range(3)]
nums[0][1] = 1
nums

# %%
x = 23
y = 23
print(id(x), id(y))
id(x) == id(y)

# %%
x = 257
y = 257
id(x) == id(y)
# %%
x = 1000
y = x
id(x), id(y)

# %%
import sys
sys.getsizeof(1)
x=1
sys.getsizeof(x)
# https://stackoverflow.com/questions/10365624/sys-getsizeofint-returns-an-unreasonably-large-value

# %%
def grep(pattern):
    print("Looking for %s" % pattern)
    while True:
        line = (yield)
        if pattern in line:
            print(line)
# %%
g = grep("python")
next(g)

# %%
import inspect
import objgraph
def foo():
    return inspect.currentframe()

def bar():
    return foo()

b1 = bar()
objgraph.show_refs(b1,
                   filter=lambda x: not isinstance(x, (type, type(lambda: None), type(objgraph))))
# %%
def gen_foo():
    for _ in range(3):
        yield inspect.currentframe()
        
class A:
    def __init__(self, a):
        self.a = a
   
a1 = A(1)
        
gf = gen_foo()
objgraph.show_refs(a1,
                   extra_ignore=[id(globals()),
                                 id(locals())])
# %%
x = [1,2,3]
if len(x) == 3:
    print(x)
    
# %%
def high_order_function(f, x):
    return f(x)

def square(n):
    return n * n

result = high_order_function(square, 10)

# %%
import inspect

def high_order_function(f, x):
    frame = inspect.currentframe()  # Get the current frame
    call_frame = inspect.getouterframes(frame)[1]  # Get the caller's frame

    print("Current frame details:")
    print(f"  Function: {frame.f_code.co_name}")
    print(f"  File: {frame.f_code.co_filename}")
    print(f"  Line number: {frame.f_lineno}")
    print(f"  Local variables: {frame.f_locals}")

    print("\nCaller frame details:")
    print(f"  Function: {call_frame.function}")
    print(f"  File: {call_frame.filename}")
    print(f"  Line number: {call_frame.lineno}")
    print(f"  Local variables: {call_frame.frame.f_locals}")

    return f(x)

def square(n):
    return n * n

result = high_order_function(square, 10)

# %%
# Inspect function arguments
args_info = inspect.getargvalues(inspect.currentframe)
print("Function arguments:", args_info)

# Inspect the code object
code_obj = frame.f_code
print("Code object details:")
print(f"  Number of arguments: {code_obj.co_argcount}")
print(f"  Local variable names: {code_obj.co_varnames}")

# Inspect global variables
globals_info = frame.f_globals
print("Global variables:", globals_info)

# %%
stack = inspect.stack()
for frame_info in stack:
    print(f"Function: {frame_info.function}")
    print(f"File: {frame_info.filename}")
    print(f"Line number: {frame_info.lineno}")
    print(f"Local variables: {frame_info.frame.f_locals}")
    print("-" * 40)

# %%
class Student: 
    def __init__(self, name): 
        self.__name = name 
  
s1 = Student("Santhosh") 
s1.__name = "see"
s1.age = 20
print(s1.__name, s1._Student__name, s1.age)

# %%
import types
types.FrameType

def foo():
    x = 1
    print(locals())
    def bar():
        y = 2
        # print(x)
        print(locals())
    bar()

foo()
foo.__name__

# %%
globals() == locals()

# %%
a = [5]
class A:
    # a = 42
    a += [3]
    a = a + [4]
    print(a)
    # c = [a + i for i in range(3)]
    # print(b)
    
print(a)
    
    
# %%
class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update   # private copy of original update() method

class MappingSubclass(Mapping):

    def update(self, keys, values):
        # provides new signature for update()
        # but does not break __init__()
        for item in zip(keys, values):
            self.items_list.append(item)
            
    # __update = update
    
# %%
m1 = Mapping(range(5))
m1.update(range(6))
m1.items_list
m2 = MappingSubclass(range(5))
m2.update(range(5), range(5))
m2.items_list

# %%
# %%
import numpy as np

# %%
lst = [1,2,3,4,5]
lst[1:3]
# %%
a, b, c = 1, 2, 1
a<b>c
# %%
x = None
x!=x

# %%
x = float('NaN')
x !=x
# %%
class Foo():
    def __eq__(self, other):
        return True
    
f = Foo()
f == None

# %%
lst = []
tgt = 1, 2, 3
lst = *tgt

# %%
*a, b, c = 1, 2, 3
a, b, c

# %%
class A:
    x = 3
    def __init__(self, x):
        self.y = x
        
inst = A(1)
inst.x = inst.x + 1
A.x += 1
print(inst.x, A.x)




# %%
x = 1
assert None is not None, x

# %%
f = min
f = max
g, h = min, max
max = g
print(max(f(2, g(h(1, 5), 3)), 4))
print(f == g == h == min == builtins.max)
import builtins
builtins.max

# %%
# how yield works
import inspect
frame = None
def add(x, y):
    global frame
    s = x + y
    frame = inspect.currentframe()
    return s

def outer(f):
    return f

outer(add)(1, 2)
print(frame)
print(frame.f_trace)

# %%
glb = globals().items()
for k, v in glb:
    if not k.startswith("_"):
        print(k, ":", v)
# %%
import dis
def gen_add(x, y):
    s = x + y
    yield s

dis.show_code(gen_add(x=1, y=2))

# %%
def gen_two(x, y):
    print('x ready')
    yield x
    print('y ready')
    yield y

g = gen_two(1, 2)

print('last Instruction Pointer:', g.gi_frame.f_lasti)
dis.disco(g.gi_code, g.gi_frame.f_lasti)
# %%
next(g)
# %%
print('last Instruction Pointer:', g.gi_frame.f_lasti)
dis.disco(g.gi_code, g.gi_frame.f_lasti)
# %%
next(g)
# %%
print('last Instruction Pointer:', g.gi_frame.f_lasti)
dis.disco(g.gi_code, g.gi_frame.f_lasti)
# %%
next(g)
# %%
from typing import NamedTuple
class Result(NamedTuple):
    count: int
    average: float

class Sentinel:
    def __repr__(self):
        return f'<Sentinel>'

STOP = Sentinel()

def average2():
    total = 0.0
    count = 0
    average = 0.0
    while True:
        try:
            term = yield average
        except Exception:
            pass
        print('received', term)
        if isinstance(term, Sentinel):
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)
# %%
coro_avg = average2()
# %%
next(coro_avg)
# %%
coro_avg.send(10)
coro_avg.send(20)
coro_avg.send(30)
# %%
coro_avg.close()
# %%
try:
    coro_avg.send(STOP)
except StopIteration as e:
    result = e.value
# %%
result
# %%
