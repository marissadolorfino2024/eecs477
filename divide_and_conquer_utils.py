#!/bin/python

# util functions for divide and conquer: integer mult, fft, convolutions

def fft(polyA: list[float], wn: float):
    ''' function for fft on coefficient list of size n for polynomial A
    polyA (list): list of coefficients of polynomial A
    wn: primitive nth root of unity
    '''

    if len(polyA) == 1: # evaluate A(1) = a0
        return polyA[0]

    d = fft([polyA[i] for i in range(len(polyA)) if i%2 == 0], (wn ** 2)) # fft on the even coefficients of polyA
    e = fft([polyA[i] for i in range(len(polyA)) if i%2 != 0], (wn ** 2)) # fft on the odd coefficients of polyA

    return 




# class invFFT()

