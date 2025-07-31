
## Challenge Name: Baby Binary
**Category:** Binary
**Points:** 200

**Challenge Description:**

The problem was given with the vuln.c and a description that said something like "You should know stackoverflow. Or maybe bufferoverflow..." The task is to inspect the code and find its vulnerable points and exploit it to reveal the flag.

### Approach

**1. How did I find the weak point of the code?**

Since the code was already given, I just opened it and looked for the functions in there and I found one function that prints the flag.

```
void sigsegv_handler(int sig) {
  printf("%s\n", flag);
  fflush(stdout);
  exit(1);
} 
```

The next step I did was to find the callers of the ```sigsegv_handler(int sig)``` and conveniently it's inside the main. Indeed a very vulnerable position to be placed.

```
main {
    ...

    signal(SIGSEGV, sigsegv_handler); // Set up signal handler

    ...
}
```

**2. How did I make the program call the ```sigsegv_handler(int sig)```**

I looked into the signal function because the ```sigsegv_handler(int sig)``` was passed as parameter and I found out that signal function sends a signal XD.

Since the program asks for an input and passes it to the function:
```
void vuln(char *input){
  char buf2[16];
  strcpy(buf2, input);
}
```
I surmised that inputting more than 16 characters/bytes will cause the buf2 to overflow (hence the title **baby-overflow**) with a hope that it leads to an undefined behavior, which might send some signal that will call the ```sigsegv_handler(int sig)``` to reveal the flag. 

So I spammed random keys in my keyboard up to more than 16 characters. Upon pressing enter the program printed the flag:
> CITU{ur_1rst_Pwn}

### Reflections
This challenge reminded me how fragile memory handling in C can be. I thought I had a decent grasp of C, but this showed me how much more there is to learn — especially when it comes to low-level memory and security. Even a small oversight like using strcpy on a fixed-size buffer can lead to critical vulnerabilities.

---
[**Back to Home**](/)


