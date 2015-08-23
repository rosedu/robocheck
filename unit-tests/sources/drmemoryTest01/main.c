#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void invalid_acces_function()
{
    //memory leak
    char *p = (char*)malloc(4*sizeof(char));
    //invalid access
    printf("%c", p[4]);
}

int uninitialized_variable_usage_function()
{
    int x;
    //uninitialized variable usage
    return x>9000;
}

int main()
{
    char *string = (char*)malloc(50*sizeof(char));
    //opened, but not closed file descriptor
    FILE *f = fopen("input.txt", "r");
    fgets(string, 20, f);
    free(string);

    // memory leak
    char *x = (char*)malloc(8*sizeof(char));
    //invalid access
    char c = *(x+8);
    //invalid free
    free(&c);

    invalid_acces_function();
    uninitialized_variable_usage_function();

    int *v;
    //invalid free and uninitialized variable usage
    free(v);

    return 0;
}
