#%%
import time
from time import sleep
def one_task():
    print(f'begin task')
    ...
    print(f'  begin big_step:')
    big_corout = big_step()
    while 1:
        try:
            x = big_corout.send(None)
        except StopIteration as e:
                big_result = e.value
                break
        else:
            func, arg = x
            func(arg)

    print(f'  end big_step with {big_result}  ')
    ...
    print(f'end task')
    
def big_step():
    ...
    print(f'    begin small step:')
    
    # small_coroutine = yield from small_step()
    small_coroutine = small_step()
    while True:
        try:
            x = small_coroutine.send(None)
        except StopIteration as e:
            small_result = e.value
            break
        else:
            yield x        
        
    print(f'    end small_step with {small_result}')
    ...
    return small_result * 1000

def small_step():
    print('      rest...')
    t1 = time.time()
    yield sleep, 20
    assert time.time() - t1 > 20, 'sleeping'
    print('      working...')
    return 123

one_task()
# %%
# module.py
# define several algorithms and call them with a common function
def algo1(x):
	print("algorithm 1 computing")
	if x == 1:
		yhat = 1.1
	else:
		yhat = 1.2
	print("yhat1=", yhat)
	return
    
def algo2(x):
	print("algorithm 1 computing")
	if x == 1:
		yhat = 2.1
	else:
		yhat = 2.2
	print("yhat1=", yhat)
	return
    
def algo3(x):
    print("algorithm 1 computing")
    if x == 1:
    	yhat = 3.1
    else:
    	yhat = 3.2
    print("yhat1=", yhat)
    return

# main.py
x = 0
def ml(f):
	print(f"{f.__name__} invoked")
	ans = f(x)
	print("answer is", ans)
	return f
    
ml(algo1)
# %%
@ml
def algo3(x):
    print("algorithm 1 computing")
    if x == 1:
    	yhat = 3.1
    else:
    	yhat = 3.2
    print("yhat1=", yhat)
    return
# %%
algo3(2)
# %%
