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