#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp;
    int c;               /* IMPORTANT: int, not char */

    fp = fopen("/tmp/file.log", "r");
    if (fp == NULL) {
        puts("Cannot find /tmp/file.log");
        return 1;
    }

    while ((c = fgetc(fp)) != EOF) {
        putchar(c);
    }

    fclose(fp);
    return 0;
}
