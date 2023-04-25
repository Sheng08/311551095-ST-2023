#include <stdlib.h>
#include <stdio.h>

int main(){
    int length = 4;
    int *p = (int*) malloc(length * sizeof(int));
    
    p[4] = 4;
    printf("%d", p[4]);
    
    return 0;
}