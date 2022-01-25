"""
Ran into performance issues on the Feather while doing stuff with floats anddivision. 
I can use this code to benchmark all sorts of different comptuters, like the Feather,
Pi, and my desktop.
This code should be ran a few times to get an average

This will do floating point math, then division, then both.



"""

import time

benchmark_size = 10000

start = time.time_ns()

f = open("math_benchmark.csv", "a")
f.write("Math benchmark. Refer to the code for more into.")


def simple_division():
    for i in range(benchmark_size):
        simp_division = 100 / 10
        return simp_division
        

def complex_division():
    for i in range(benchmark_size):
        comp_division = 1300 / 700
        return comp_division
        

def float_division():
    for i in range(benchmark_size):
        flt_division = 1045254354354633565460454563063450304563045606350.02569 / 14514514514514154514514154514511451454511450.117521452451245145145145124154155587
        return flt_division
        






def addition():
    for i in range(benchmark_size):
        add = 100 + 10
        return add
        


def float_addition():
    for i in range(benchmark_size):
        flt_addition = 100.02569 + 10.15587
        return flt_addition
        


simple_division()
complex_division()
float_division()
addition()
float_addition()
end = time.time_ns()
print("done")



print(end-start)
























f.close()

