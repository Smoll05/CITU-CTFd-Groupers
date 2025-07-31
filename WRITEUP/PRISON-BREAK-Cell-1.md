# Prison Break Level 1


## Problem
``` py
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
```

## Solution

The program accepts a user input. At the last line, it executes the user's input as a python script. In the confiscated tools, I saw that "flag" has been taken away as well. This means that there exists a file called flag that can be accessed and stores the flag value. Since the word flag has been confiscated, I had to take a different approach so that it can't be read as flag. I came up with "fl" + "ag". So, I used the open method to open this file, read the file, and printed its contents like so:

```py
print(open("fl" + "ag.txt").read())
```

I used this as the input and it showed the hidden flag:

```txt
CITU{th1s_1s_jus7_4n_ez_0n3_w4rd3n_1s_c4r3l3ss}
```