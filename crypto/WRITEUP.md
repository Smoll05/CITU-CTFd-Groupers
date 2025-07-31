## Challenge Name: fibocrypt
Category: Cryptography

Challenge Description: 

The challenge gave a Python source code (fibonacci_crypt.py) that has the logic to encrypt and decrypt the flag and an output.txt file, which is the flag ciphertext. The goal is to check the source code used for encryption and decrypt the ciphertext inside the output.txt to reveal the flag.

**TL;DR:** The challenge gave a Python encryption script using a slow recursive Fibonacci-based key. The original code hit recursion and integer limits, so I refactored it with a fast Fibonacci algorithm and used sys.set_int_max_str_digits(0) to bypass conversion limits. By replicating the key generation and decrypt logic, I reversed the XOR encryption using the provided ciphertext and revealed the flag:
**CITU{Fasteist_Fib0Fib0_encrpyti0n}**

**fibonacci_crypt.py**
```python
import sys
from hashlib import sha512
from os import urandom

FLAG = b"CITU{????????????????????????????}"

def fib(k):
    if k == 0:
        return 0
    if k == 1:
        return 1
    return fib(k - 1) + fib(k - 2)


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
```

**output.txt**
```
3390560246ab6c5bbdbfa799623c467db08cd1a2fa67f1f29f67c203ab5eb6d30af4d6e19791b1f2887cb87889eb89e2
```

### Approach

**1. Will Running fibonacci_crypt.py Help Me?**

Inside the file is the logic used to encrypt the cipher text found in the output.txt. I tried to run the script thinking that I might uncover something, but all I found was an error.

```console
┌──(smoll㉿loki)-[~/ctf/crypto]
└─$ python fibonacci_crypt.py
Traceback (most recent call last):
  File "/home/smoll/ctf/crypto/fibonacci_crypt.py", line 37, in <module>
    key = gen_key(k)
  File "/home/smoll/ctf/crypto/fibonacci_crypt.py", line 16, in gen_key
    n = fib(k)
  File "/home/smoll/ctf/crypto/fibonacci_crypt.py", line 12, in fib
    return fib(k - 1) + fib(k - 2)
           ~~~^^^^^^^
  File "/home/smoll/ctf/crypto/fibonacci_crypt.py", line 12, in fib
    return fib(k - 1) + fib(k - 2)
           ~~~^^^^^^^
  File "/home/smoll/ctf/crypto/fibonacci_crypt.py", line 12, in fib
    return fib(k - 1) + fib(k - 2)
           ~~~^^^^^^^
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```
The hint gave us [different recursive fibonacci algorithms](https://www.nayuki.io/page/fast-fibonacci-algorithms) that are faster and borrowed the python source code. Here is what I refactored in the original source code.

```python
def _fib(n):
    if n == 0:
        return (0, 1)
    else:
        a, b = _fib(n // 2)
        c = a * (b * 2 - a)
        d = a * a + b * b
        if n % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)
        
def fib(n):
	if n < 0:
		raise ValueError("Negative arguments not implemented")
	return _fib(n)[0]
```

I ran the source code again and then another problem happened.

```console
    h = sha512(str(n).encode()).digest()
               ~~~^^^
ValueError: Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit
```

Another hint given is to use `sys.set_int_max_str_digits(0)` which sets no limit on the number of digits allowed when converting a string to an int in Python.

The source code then ran without errors and was able to encrypt and decrypt the dummy flag in the source code. Now I know it works.

**2. How Will I Abuse This Source Code To Decrypt The Cipher Text?**

These functions and variable from the source code given will be crucial for me to decrypt the ciphertext from the output.txt

```python
FLAG = b"CITU{????????????????????????????}"

def gen_key(k):
    n = fib(k)
    h = sha512(str(n).encode()).digest()
    return h

def unpad(m):
    return m[:len(FLAG)]

def decrypt(c, key):
    m = bytes([a ^ b for a, b in zip(c, key)])
    m = unpad(m)
    return m
```
We then take the ciphertext from the output.txt, convert it into bytes and pass it as argument in the `decrypt(c, key)` function. We then print the result.

```python
# Cipher text from the output.txt
ct = bytes.fromhex("3390560246d23217f6e5f1d5295c3f2bed83a8f4a76891a8ce3b8f4ced15e0dc5bf4c26b820b98eda80c3afd5790ba11")

k = 0xC0FFEE
key = gen_key(k)

hidden_flag = decrypt(ct, key)

print(hidden_flag)
```
**3. Getting The Flag🚩**

Now with all these script, I just need to run the program to get the flag. The flag is:
> CITU{Fasteist_Fib0Fib0_encrpyti0n}

### Full Solver Source Code

```python
import sys
from hashlib import sha512

FLAG = b"CITU{????????????????????????????}"

sys.set_int_max_str_digits(0)

def _fib(n):
    if n == 0:
        return (0, 1)
    else:
        a, b = _fib(n // 2)
        c = a * (b * 2 - a)
        d = a * a + b * b
        if n % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)

def fib(n):
  if n < 0:
    raise ValueError("Negative arguments not implemented")
  return _fib(n)[0]

def gen_key(k):
    n = fib(k)
    h = sha512(str(n).encode()).digest()
    return h

def unpad(m):
    return m[:len(FLAG)]

def decrypt(c, key):
    m = bytes([a ^ b for a, b in zip(c, key)])
    m = unpad(m)
    return m

# Cipher text from the output.txt
ct = bytes.fromhex("3390560246d23217f6e5f1d5295c3f2bed83a8f4a76891a8ce3b8f4ced15e0dc5bf4c26b820b98eda80c3afd5790ba11")

k = 0xC0FFEE
key = gen_key(k)

hidden_flag = decrypt(ct, key)

print(hidden_flag)
```

### Reflections
It really is important to understand and read the functionality of each line of code in the source code and analyze how to abuse it. And using Fibonacci in cryptology is new to me; what a time to be alive. 
  

---
[Back to home](<link>)
