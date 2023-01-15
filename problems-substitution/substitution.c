#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdlib.h>

bool is_string_unique(string str);

int main(int argc, string argv[])
{
    string text;
    string key = "";

    if (argc > 1 && argc <= 2)
    {
        int n = strlen(argv[1]);

        if (n == 26)
        {
            for (int i = 0; i < n; i++)
            {
                if (isalpha(argv[1][i]))
                {
                    key = argv[1];
                }

                else
                {
                    printf("Key must only contain alphabetic characters.\n");
                    return 1;
                }
            }
        }

        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }

        if (is_string_unique(key) == false)
        {
            printf("Key must not contain repeated characters.\n");
            return 1;
        }
    }

    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }


    text = get_string("plaintext: ");


    int l = strlen(text);
    int cip;
    char result[l];

    for (int i = 0; i < l; i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                cip = toupper(key[text[i] - 65]);
                
            }

            if (islower(text[i]))
            {
                cip = tolower(key[text[i] - 97]);
            }
        }

        else
        {
            cip = text[i];
        }

        char ch = cip;
        result[i] = ch;
        result[i + 1] = '\0';
    }
    printf("ciphertext: %s\n", result);

    return 0;
}


bool is_string_unique(string str)
{

    // If at any time we encounter 2
    // same characters, return false
    for (int i = 0, n = strlen(str); i < n - 1; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (str[i] == str[j])
            {
                return false;
            }
        }
    }

    // If no duplicate characters encountered,
    // return true
    return true;
}
