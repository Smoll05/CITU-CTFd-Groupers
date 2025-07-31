#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

#define FLAGSIZE_MAX 64

char flag[FLAGSIZE_MAX];

void sigsegv_handler(int sig) {
  printf("%s\n", flag);
  fflush(stdout);
  exit(1);
}

void vuln(char *input){
  char buf2[16];
  strcpy(buf2, input);
}

int main(int argc, char **argv){
  setbuf(stdout, NULL);
  
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }
  
  fgets(flag,FLAGSIZE_MAX,f);
  signal(SIGSEGV, sigsegv_handler); // Set up signal handler
  
  gid_t gid = getegid();
  setresgid(gid, gid, gid);


    int choice;
    printf("Menu:\n");
    printf("1. Flag\n");
    printf("2. Command prompt\n");
    printf("Choose an option: ");
    scanf("%d", &choice);
    getchar();

    if (choice == 1) {
        printf("CCSLynx{@r3_u_sure}\n");
    } else if (choice == 2) {
        printf("Input: ");
        fflush(stdout);
        char buf1[100];
        fgets(buf1, sizeof(buf1), stdin);

        if (strstr(buf1, "max verstappen") != NULL || strstr(buf1, "formula 1") != NULL) {
            printf("CCSLynx{DU_DU_DU_DU...MAX_VERSTAPPEN}\n");
        } else {
            vuln(buf1);
        }
    } else {
        printf("Command Not Found\n");
    }

    return 0;
}
