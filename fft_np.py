#!/bin/python

import numpy as np

def fft_multiply(a_int, b_int):
    # get binary
    a_digits = [int(d) for d in str(a_int)][::-1]
    b_digits = [int(d) for d in str(b_int)][::-1]
    
    # pad to next power of 2
    n = len(a_digits) + len(b_digits)
    size = 2**int(np.ceil(np.log2(n)))
    
    # fft and multiplication of polys
    fft_a = np.fft.fft(a_digits, n=size)
    fft_b = np.fft.fft(b_digits, n=size)
    product_fft = fft_a * fft_b
    
    # inverse fft on product of ffta and fftb 
    res_raw = np.round(np.fft.ifft(product_fft).real).astype(int)
    
    # convert to base 10
    carry = 0
    final_digits = []
    for digit in res_raw:
        total = digit + carry
        final_digits.append(total % 10)
        carry = total // 10
    
    # get integer
    return int("".join(map(str, final_digits[::-1])))