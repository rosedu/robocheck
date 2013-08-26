#include<stdlib.h>
#include<stdio.h>
#include<string.h>
void function(char *something){
    char *x = strdup(something);
    char *y = malloc(4);
    free(y);
    y[3] = 'a';
}

int main(void) {
    FILE *f = fopen("date2.in", "r");
    int a=0;
    int b[10];
    int* x = malloc(4 * sizeof(int));
    free(x);
    x[2] = 3;
    function("hmm");
    b[10] = 4;
    return 0;
}
