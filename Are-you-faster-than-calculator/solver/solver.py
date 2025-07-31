from pwn import *

HOST, PORT = "103.252.117.81", 10010

io = remote(HOST, PORT)

io.recvline()
io.recvline()

for i in range(100):
    to_solve = io.recvline().decode().strip().split(' ')
    a = int(to_solve[0])
    op = to_solve[1]
    b = int(to_solve[2])

    if op == '+':
        io.sendline(str(a + b))
    elif op == '-':
        io.sendline(str(a - b))
    elif op == '*':
        io.sendline(str(a * b))
    elif op == '/':
        io.sendline(str(a // b))
    elif op == '^':
        io.sendline(str(a ** b))
    elif op == '%':
        io.sendline(str(a % b))
    elif op == '|':
        io.sendline(str(a | b))

print(io.recvline().decode().strip())
io.close()
    