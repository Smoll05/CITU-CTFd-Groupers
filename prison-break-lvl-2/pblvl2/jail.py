#!/usr/local/bin/python

import os
import sys

print("="*40)
print("Welcome to the prison break level 2")
print("="*40)
print("Warden: I found out that you escaped at level 1, and now I will confiscate your tools.")
print("Warden: I will also make sure that you won't be able to escape again. BWAHAHA!!")
print("="*40)
print("---- TIPS from 'ret' who escaped and now he is in lvl 3 ----")
print("I love decorating texts in my house.")
print("------------------------------------------------------------")
hax = input("> ")
sys.stdin.close()

confiscated_tools = ['sys', 'import', 'flag', 'open', '/', "sh", "bin", 'eval', 'exec', 'os', 'read', 'system', 'builtins', '__builtins__']

if len(hax) > 512:
    print("In here your tools was replaced...")
    exit(1)

for tool in confiscated_tools:
    if tool in hax:
        print("In here your tools was replaced...")
        exit(1)

code = f"""
import os

{hax}

""".strip()

os.execv(sys.executable, [sys.executable, "-c", code])