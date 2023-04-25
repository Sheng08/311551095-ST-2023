#include <stdio.h>
#include <stdlib.h>

int main(){
    int *a = malloc(4 * sizeof(int));
    free(a);
    printf("%d\n", a[1]);
    
    return 0;
}