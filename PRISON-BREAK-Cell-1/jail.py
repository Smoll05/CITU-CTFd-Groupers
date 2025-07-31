#!/usr/local/bin/python

import os
import sys
import string

print("="*40)
print("Welcome to the prison break level 1")
print("="*40)
print("Warden: if any of you will try to escape, I will meet you in level 2 to level 3.")
print("Warden: I will also make sure that you won't be able to escape since ret was trying to escape and was caught in level 2.")
print("="*40)
hax = input("> ")
sys.stdin.close()

confiscated_tools = ['os', 'import', 'flag', 'system']

if len(hax) > 1024:
    print("Few of ret tools was confiscated only, try to find the other tools.")
    exit(1)

for tool in confiscated_tools:
    if tool in hax:
        print("Few of ret tools was confiscated only try to find the other tools.")
        exit(1)

code = f"""
{hax}
""".strip()

os.execv(sys.executable, [sys.executable, "-c", code])