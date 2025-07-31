import sys
from hashlib import sha512
from os import urandom

FLAG = b"CITU{???????????????????????????????}"

# def fib(k):
#     if k == 0:
#         return 0
#     if k == 1:
#         return 1
#     return fib(k - 1) + fib(k - 2)

# Fibonacci number in O(log(n))
# n = 12648430
# ETA: 116s
def fib(n):
    if n == 0: 
        return 0

    if n == 1: 
        return 1

    def matmul(M1, M2):
        a11 = M1[0][0]*M2[0][0] + M1[0][1]*M2[1][0]
        a12 = M1[0][0]*M2[0][1] + M1[0][1]*M2[1][1]
        a21 = M1[1][0]*M2[0][0] + M1[1][1]*M2[1][0]
        a22 = M1[1][0]*M2[0][1] + M1[1][1]*M2[1][1]
        return [[a11, a12], [a21, a22]]

    def matPower(mat, p):
        if p == 1: 
            return mat

        m2 = matPower(mat, p//2)
        if p % 2 == 0:
            return matmul(m2, m2)
        else: 
            return matmul(matmul(m2, m2),mat)



def gen_key(k):
    n = fib(k)
    h = sha512(str(n).encode()).digest()
    return h

def pad(m):
    return m + b"".join([urandom(1) for _ in range(16 - (len(m) % 16))])

def unpad(m):
    return m[:len(FLAG)]

def encrypt(m, key):
    m = pad(m)
    c = bytes([a ^ b for a, b in zip(m, key)])
    return c

def decrypt(c, key):
    m = bytes([a ^ b for a, b in zip(c, key)])
    m = unpad(m)
    return m
    
k = 0xC0FFEE
key = gen_key(k)
ct = encrypt(FLAG, key)
with open("output.txt", "w") as f:
    f.write(ct.hex())
    
pt = decrypt(ct, key)
assert pt == FLAG