#!/usr/local/bin/python

import os
import sys
import string

print("="*40)
print("Welcome to the prison break level 3")
print("="*40)
print("Warden: Ohoy!! you are being caught again.")
print("Warden: I found out that you escaped at level 2, now I will confiscate all your tools here.")
print("Warden: I will also make sure that you won't be able to escape again. BWAHAHA!!")
print("="*40)
print("---- TIPS from 'ret' who escaped and now he is in katipwnan ----")
print("1. Steal back the tools from the prison's server.")
print("2. Warden is careless, your tools are still in the prison.")
print("----------------------------------------------------------------")
hax = input("> ")
sys.stdin.close()

if len(hax) > 256 or any(x not in string.printable for x in hax):
    print("In here your tools was replaced...")
    exit(1)

code = f"""
import sys
import os
import inspect

if "_posixsubprocess" in sys.modules:
    print("nope 2")
    os._exit(1)

for k in list(sys.modules):
    del sys.modules[k]

f = inspect.currentframe()

for k in f.f_builtins:
    if k == "print":
        continue
    if k == "dir":
        continue
    if k == "Exception":
        continue
    f.f_builtins[k] = None

for k in f.f_globals:
    if k != "f":
        f.f_globals[k] = None
for k in f.f_locals:
    # print(k, f.f_locals[k])
    f.f_locals[k] = None

{hax}
""".strip()

os.execv(sys.executable, [sys.executable, "-c", code])