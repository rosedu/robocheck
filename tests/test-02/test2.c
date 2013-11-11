#include<stdio.h>
#include<stdlib.h>

void function2(){
    int x;
    x = x+2;
    FILE *f = fopen("date.in", "w");
}
void function(){
    function2();
}


int main(void){
    FILE *g = fopen("date.in", "r");
    int *x = malloc(4* sizeof(int));
    free(x);
    free(x);
    function();
    return 0;
}
