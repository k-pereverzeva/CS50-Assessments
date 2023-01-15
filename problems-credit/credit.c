#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
//Ask user for card number
{
    long credit;
    do
    {
        credit = get_long("Number: ");
    }
    while (credit < 0);

    int k;
    int mult;
    int sum;
    int i = 0;
    long credit2 = credit;
    
    while (credit2 > 0)   
    {
        //Separate digits
        k = credit2 % 10; 
        credit2 = credit2 / 10;
        i++;
        
        // Multiply by 2 every other digit, starting with the number’s second-to-last digit
        if (i % 2 == 0)
        {
            mult = k * 2;
            
            if (mult >= 10)
                
                // Sum every digit
            {
                sum = sum + (mult % 10) + 1;
            }
            
            else
            {
                sum = sum + mult;
            }
        }
        
        //Sum digits, starting with the number’s first-to-last digit
        else 
        {
            sum = sum + k;
        }
    }
    
    printf("sum: %i\n", sum);
    
    //Separate 2 first digits
    int a = credit / pow(10, i - 2);
    int b = credit / pow(10, i - 1);
    
    printf("i: %i\n", i);
    printf("a: %i\n", a);
    printf("b: %i\n", b);
    
    // Card check
    if (sum % 10 == 0)
    {
        if (i == 15 && (a == 34 || a == 37))
        {
            printf("AMEX\n");
        }
        
        else if (i == 16 && (a >= 51 && a <= 55))
        {
            printf("MASTERCARD\n");
        }
        
        else if (b == 4 && (i == 13 || i == 16))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    
    else
    {
        printf("INVALID\n");
    }
}