#%%
import traceback
import sys

def call1(f):
    for i in range(3):
        print(f'1 calls 2: {i}')
        call2(f)
        yield i
    
def call2(f):
    print('2 calls f')
    f()
    
def f():
    summary = traceback.StackSummary.extract(traceback.walk_stack(None))
    print(''.join(summary.format()))

c1 = call1(f)
print(c1.__next__())
print(c1.__next__())
    

# %%
def gen_func():
    for i in range(5):
        yield i
        
g = gen_func()

# %%
# importing the modules 
import traceback 
import sys 
  
def call1(f):
    call2(f) 
  
def call2(f):
    f() 
      
template = ( 
    '{frame.filename}:{frame.lineno}:{frame.name}:\n'
    '    {frame.line}'
) 
  
def f(): 
    summary = traceback.StackSummary.extract( 
        traceback.walk_stack(None) 
    ) 
    for frame in summary: 
        print(template.format(frame=frame)) 

call1(f) 
# %%
