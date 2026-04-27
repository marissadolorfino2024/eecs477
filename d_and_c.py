#!/bin/python

# from dc_utils import *
# import time

# times = []
# # divide and conquer FFT for integer multiplication, convolutions
# for i in range(1000):
#     for j in range(10000):
#         starttime = time.perf_counter()
#         fft_tests(i, j)
#         endtime = time.perf_counter()
#         times.append(endtime-starttime)

# print(times)

# from dc_opt_utils import *
# import time

# times = []
# # divide and conquer FFT for integer multiplication, convolutions
# for i in range(1000):
#     for j in range(10000):
#         starttime = time.perf_counter()
#         fft_tests(i, j)
#         endtime = time.perf_counter()
#         times.append(endtime-starttime)
        
# print(times)

from fft_np import *
import time

times = []
# numpy fft
for i in range(1000):
    for j in range(10000):
        starttime = time.perf_counter()
        fft_multiply(i, j)
        endtime = time.perf_counter()
        times.append(endtime-starttime)
        
print(times)