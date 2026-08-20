import time

def timer(func):
    def wrapper(*args, **kwargs):
        stime = time.perf_counter()
        res = func(*args, **kwargs)
        etime = time.perf_counter()
        print(f"time elapsed: {etime - stime}")
        return res
    return wrapper
    
cpdef unsigned long long int fibonacci(int n):
    cdef unsigned long long int a = 0, b = 1, i
    for i in range(n):
        a, b = b, a + b
    return a

fibonacci = timer(fibonacci)