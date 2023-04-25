#include <stdio.h>

int main(){
    int a[8];
    int b[8];
    a[8+8] = 1;   // Cross!
    a[8+100] = 1; // Cross!

    return 0;
}