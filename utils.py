#!/bin/python

import math 
import numpy as np

# util functions for divide and conquer: integer mult, fft, convolutions

# fft function (forward and inverse)
def fft(polyA: list[float], n: int, wn: float, inverse=False):
    ''' function for fft on coefficient list of size n for polynomial A
    polyA (list): list of coefficients of polynomial A
    n (int): specifies the degree of the polynomial A
    wn (float): unit nth root of unity
    '''
    
    # bitwise and to ensure n is a power of 2
    if n & (n - 1) != 0: 
        print('the degree of polyA must be a power of 2')
        return 'error'

    polyA_n = len(polyA) # get length of poly (n)
    if polyA_n == 1:
        return [polyA[0]] # return a0
    
    A_even = [polyA[i] for i in range(polyA_n) if i % 2 == 0]
    A_odd = [polyA[i] for i in range(polyA_n) if i % 2 != 0]
    
    even_evals = fft(A_even, len(A_even), wn**2)
    odd_evals = fft(A_odd, len(A_odd), wn**2)

    yk = []
    yk_n2 = []
    
    # get the values of A from Aeven and Aodd
    for i in range(int(polyA_n/2)):
        factor = wn ** i
        y = even_evals[i] + factor * odd_evals[i]
        yk.append(y)
        
        yn2 = even_evals[i] - factor * odd_evals[i]
        yk_n2.append(yn2)

    # if inverse, divide outputs by n
    if inverse == True:
        ytotal = [a/n for a in yk] + [a/n for a in yk_n2]
        return ytotal

    ytotal = yk + yk_n2        
    return ytotal 

def pad_polys(poly: list[float]):
    n = len(poly)
    if n <= 1:
        return poly
    
    next_pow2 = 1 << (n - 1).bit_length()
    
    return poly + [0.0] * (next_pow2 - n)

def ensure_poly_n(polya: list[float], polyb: list[float]):
    max_len = max(len(polya), len(polyb))
    polya = polya + [0.0] * (max_len - len(polya))
    polyb = polyb + [0.0] * (max_len - len(polyb))
    
    # double pad length
    result_len = 2 * max_len
    polya = polya + [0.0] * (result_len - len(polya))
    polyb = polyb + [0.0] * (result_len - len(polyb))
    
    return pad_polys(polya), pad_polys(polyb)

def multiply_polys(polya: list[float], polyb: list[float]):
    # naive implementation of polynomial multiplication
    result = [0.0] * len(polya)
    for i in range(len(polya)):
        result[i] = polya[i] * polyb[i]
    return result
    
def ints2polys(int1: int, int2: int):
    # convert integers to polynomials
    polya = [float(bit) for bit in reversed(bin(int1)[2:])] 
    polyb = [float(bit) for bit in reversed(bin(int2)[2:])] 
    
    # pad lower degree polynomial with 0s
    if len(polya) > len(polyb):
        for i in range(len(polya) - len(polyb)):
            polyb.append(0.0)
        return polya, polyb
        
    elif len(polyb) > len(polya):
        for i in range(len(polyb) - len(polya)):
            polya.append(0.0)
        return polya, polyb
    
    else:
        return polya, polyb
    
def poly_evaluation(poly: list[float]):
    result = 0
    for i in range(len(poly)):
        pow = i
        result += poly[i] * (2 ** i) 
    return result
    
def pattern_matching():
    return 0
    
def fft_tests(int1: int, int2: int):

    polya, polyb = ints2polys(int1, int2)
    
    polya = pad_polys(polya)
    polyb = pad_polys(polyb)
    
    polya, polyb = ensure_poly_n(polya, polyb)
    
    unit_unity = (math.e) ** ((2j * math.pi) / len(polya))
    unit_unity_inv = (math.e) ** ((-2j * math.pi) / len(polya))

    # fft on polya (first integer)
    outpa = fft(polya, len(polya), unit_unity)
    
    # fft on polyb (second integer)
    outpb = fft(polyb, len(polyb), unit_unity)
    
    resultc = multiply_polys(outpa, outpb)
    
    resultc = fft(resultc, len(resultc), unit_unity_inv, inverse=True)
    
    resultint = 0
    for i, coeff in enumerate(resultc):
        resultint += round(coeff.real) * (2 ** i)
        
    true_result = int1 * int2
    
    if true_result != resultint:
        print(f'true result ({true_result}) does not match fft result ({resultint})')
    
    return resultint




