

#include <stdio.h>

int fib(int n){
    if (n <= 1)
        return n;
    return fib(n-1) + fib(n-2);
}


int main(int argc, char* argv[])
{

    int n = 18 ;
    int f ; 

    printf("Hello world!\n");
    printf("This program will print %d fibonacci numbers.\n\n" , n+1);

    for (int i = 0 ; i<=n ; i++){

        f = fib(i) ; 
        printf("Fibonacci term %d , is %d!\n" , i , f);

    }

    printf("Bye world!\n");

    return 0 ; 
}
