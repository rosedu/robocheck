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
    function();
    return 0;
}
