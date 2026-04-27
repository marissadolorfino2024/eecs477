#!/bin/python

import math
import numpy as np

# pad to power of 2 and extend to double max length in one step
def ensure_poly_n(polya, polyb):
    max_len = max(len(polya), len(polyb))
    
    # pad to power of 2 and double length in one step instead of 2
    result_len = 1 << (2 * max_len - 1).bit_length()
    
    # allocate arrays instead of appending later
    result_a = [0.0] * result_len
    result_b = [0.0] * result_len
    
    # copy and extend instead of appending
    result_a[:len(polya)] = polya
    result_b[:len(polyb)] = polyb
    
    return result_a, result_b

def multiply_polys(polya, polyb):
    # list comprehension in stead of for loop
    return [a * b for a, b in zip(polya, polyb)]

def ints2polys(int1, int2):
    # convert integers to polys
    
   # represetn bits as strings (faster than list of ints)
    bits1 = bin(int1)[2:][::-1] # reverse
    bits2 = bin(int2)[2:][::-1] # reverse
    
    # convert bits to floats in one list comprehension each
    polya = [float(b) for b in bits1]
    polyb = [float(b) for b in bits2]
    
    # pad to equal length
    max_len = max(len(polya), len(polyb))
    polya.extend([0.0] * (max_len - len(polya)))
    polyb.extend([0.0] * (max_len - len(polyb)))
    
    return polya, polyb

def fft(polyA, wn: float, inverse=False):
    polyA_n = len(polyA)
    
    if polyA_n & (polyA_n - 1) != 0:
        print('the degree of polyA must be a power of 2')
        return 'error'
    
    if polyA_n == 1:
        return [polyA[0]]
    
    # split instead of list comprehension
    A_even = polyA[0::2]  
    A_odd = polyA[1::2]
    
    # Recursive calls with wnsquared
    even_evals = fft(A_even, wn * wn)
    odd_evals = fft(A_odd, wn * wn)
    
    # pre allocate instead of appending
    half_n = int(polyA_n /  2)
    result = [0] * polyA_n
    
    # current power of wn
    factor = 1.0
    
    # fill both halves at the same time instead of double loop
    for i in range(half_n):
        t = factor * odd_evals[i] # precompute to not compute again
        result[i] = even_evals[i] + t
        result[i + half_n] = even_evals[i] - t
        factor *= wn  
        
    if inverse:
        inv_n = 1.0 / polyA_n # only compute this once
        # list comprehensions
        result = [x * inv_n for x in result]
    
    return result

def fft_tests(int1: int, int2: int):

    polya, polyb = ints2polys(int1, int2)
    
    polya, polyb = ensure_poly_n(polya, polyb)
    
    unit_unity = (math.e) ** ((2j * math.pi) / len(polya))
    unit_unity_inv = (math.e) ** ((-2j * math.pi) / len(polya))

    # fft on polya (first integer)
    outpa = fft(polya , unit_unity)
    
    # fft on polyb (second integer)
    outpb = fft(polyb, unit_unity)
    
    resultc = multiply_polys(outpa, outpb)
    
    resultc = fft(resultc, unit_unity_inv, inverse=True)
    
    resultint = 0
    for i, coeff in enumerate(resultc):
        resultint += round(coeff.real) * (2 ** i)
        
    true_result = int1 * int2
    
    if true_result != resultint:
        print(f'true result ({true_result}) does not match fft result ({resultint})')
    
    return resultint
