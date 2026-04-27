#!/bin/python

import ast
import numpy as np
import matplotlib.pyplot as plt

with open('../time_fft_singlecalcs.out', 'r') as f:
    content = f.read().strip()
    fft_naive = ast.literal_eval(content)
    
with open('../time_fft_singlecalcs_opt.out', 'r') as f:
    content = f.read().strip()
    fft_opt = ast.literal_eval(content)
    
with open('../fft_np_times.out', 'r') as f:
    content = f.read().strip()
    fft_np = ast.literal_eval(content)
    
# reshape lists
fft_naive_array = np.array(fft_naive).reshape(1000, 10000)
fft_opt_array = np.array(fft_opt).reshape(1000, 10000)
fft_np_array = np.array(fft_np).reshape(1000, 10000)

i_values_to_plot = [10, 100, 500, 999]  

plt.figure(figsize=(12, 6))
for i_val in i_values_to_plot:
    plt.plot(range(10000), fft_naive_array[i_val, :], label=f'i={i_val}', alpha=0.7, linewidth=1, color='magenta')
    
for i_val in i_values_to_plot:
    plt.plot(range(10000), fft_opt_array[i_val, :], label=f'i={i_val}', alpha=0.7, linewidth=1, color='lightpink')
    
for i_val in i_values_to_plot:
    plt.plot(range(10000), fft_np_array[i_val, :], label=f'i={i_val}', alpha=0.7, linewidth=1, color='lightskyblue')

plt.xlabel('integer 1')
plt.ylabel('Time (seconds)')
plt.title('Multiplication Time vs j*i')
plt.legend()
plt.savefig('fft_results.png')


