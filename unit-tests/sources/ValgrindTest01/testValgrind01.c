#include <stdio.h>
#include <stdlib.h>


char* allocateString()
{
    char *leakString;
    leakString = malloc(3);
    return leakString;
}

int main()
{
    char *anotherString, *newString, *uninitialised;
    int p, *toWrite;
    //Memory leak
    newString = allocateString();
    //Invalid read
    printf("%c", newString[3]);
    //Invalid write
    newString[3] = 2;
    //Uninitialised pointer and invalid free
    free (uninitialised);
    //Opened file descriptor
    FILE* fileOpen = fopen("input.txt", "r");
    //INVALID FREE
    free(&p);
    return 0;
}
