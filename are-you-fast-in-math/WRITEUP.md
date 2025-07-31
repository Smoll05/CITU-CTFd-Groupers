## Challenge Name: Are You Fast In Math
**Category:** Problem Solving

**Challenge Description:** 

Given a remote challenge endpoint, users need to solve the math equations as fast as they can to reveal the flag. Making an incorrect answer of not responding fast enough will lead to failing the challenge. 

**TL;DR:** Solved a timed math challenge by automating responses using Python and `pwntools`. Used regex  to parse equations, computed results with conditionals, and looped until the flag was revealed: **CITU{0k_y0u_4r3_f4st_m4th_w1z4rd!}.**

### Approach

**1. How can I rapidly answer the equations?**

A human being cannot answer math equations very fast, thus my approach is to create a program that would answer the math equations for me. 

A day before answering this challenge, I faced an interesting problem while practicing in picoGym called **Easy Peasy**. I looked a [writeup](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Easy_Peasy.md) for it and learned that you can break into remote servers and enables you to write scripts in it. It used the python library called `pwntools`. With that, I thought to myself that using **pwn** to connect to the remote challenge server, then add scripts that would answer the equations rapidly would work.

```python
from pwn import *
r = remote(HOST, PORT)
```

**2. How do I take the questions?**

To take the questions I used `recvlineS()` function to 	receive the question and decode it to a string.
```python
question = r.recvlineS(timeout=2)
```
I used regex to take the operands and the operator, and since the questions are just simple math equations with two operands and one operator in between, I created this
```python
match = re.match(r"(\d+)\s*([+\-*/%^|])\s*(\d+)\s*=", question.strip())
if match:
    a, op, b = match.groups()
    a, b = int(a), int(b)
```
Alternatively, since the math equestions consists of `operand + ' ' + operation + ' ' + operand`, it is much easier to use  `split(' ')`

**3. How do I return the answer?**

Since I now have the operands and the operators, I can now use if-elif statements to solve the equation and use `sendline()` to return the answer.
```python
if op == '+':
	answer = str(a + b)
elif op == '-':
	answer = str(a - b)
elif op == '*':
	answer = str(a * b)
elif op == '/':
	answer = str(a // b)
elif op == '%':
	answer = str(a % b)
elif op == '^':
	answer = str(a ** b)
elif op == "|":
	answer = str(a | b)
else:
	log.error(f"Unknown operator: {op}")
	answer = ""
	
r.sendline(answer)
log.info(f"Sent answer: {answer}")
```

**4. Getting The Flag🚩**
Now with those logic, I just need to loop the logic until I get the final answer. The flag is:
> You are fast in math! Here is your flag: CITU{0k_y0u_4r3_f4st_m4th_w1z4rd!}

### Full Source Code
```python
from pwn import *
import re

r = remote("192.168.8.136", 10010)
r.recvuntil("Are you fast in math? Let's see!\n\n")

while True:
    try:
        question = r.recvlineS(timeout=2)
        if not question:
            log.info("No more questions received. Exiting.")
            break
        log.info(f"Question: {question}")

        match = re.match(r"(\d+)\s*([+\-*/%^|])\s*(\d+)\s*=", question.strip())

        if match:
            a, op, b = match.groups()
            a, b = int(a), int(b)
            log.info(f"Parsed: {a} {op} {b}")
            if op == '+':
                answer = str(a + b)
            elif op == '-':
                answer = str(a - b)
            elif op == '*':
                answer = str(a * b)
            elif op == '/':
                answer = str(a // b)
            elif op == '%':
                answer = str(a % b)
            elif op == '^':
                answer = str(a ** b)
            elif op == "|":
                answer = str(a | b)
            else:
                log.error(f"Unknown operator: {op}")
                answer = ""
            r.sendline(answer)
            log.info(f"Sent answer: {answer}")
        else:
            log.error("Could not parse the question.")
            break
    except EOFError:
        log.info("No more questions. Exiting.")
        break
```

### Reflections
**pwn** is scary and useful, I wonder what other things it can do.
  

---
[Back to home](/)
