#include <stdio.h>

int main(void)
{
     int a,b;

     printf("Enter an integer:\n");
     scanf("%i",&a);
     printf("Enter second integer:\n");
     scanf("%i",&b);

     if(b%a==0)
    {
          printf("The first integer is a multiple of the second.\n");
     }
     else
     {
   printf("The first integer is not a multiple of the second.\n");
      }
 
      return 0;
}