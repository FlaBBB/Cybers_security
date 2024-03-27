#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

int n = 13003401;
int x = 0;
char gathered[36] = {0};
int gathered_len = 0;
int function_id = 0;
int checked = 0;

void shift()
{
    for (int i = 0; i < gathered_len; ++i)
        gathered[i] = ((char)gathered[i] - 96) % 26 + 97;
}

int check_1(char a1)
{
    if (checked || function_id != 0)
    {
        shift();
        return 1;
    }
    if (a1 <= 96 || a1 > 122)
        return 0;
    gathered[gathered_len++] = a1;
    printf("access function check_1 with %d, %d\n", a1, x);
    if ((a1 == 98 || a1 == 99 || a1 == 104 || a1 == 115 || a1 == 116) &&
        ++x != 2 && x != 8 && x != 9 && x != 12)
        function_id = 1;
    if (a1 == 100)
        function_id = 2;
    checked = 1;
    return 1;
}

int check_2(char a1)
{
    if (checked || function_id != 1)
    {
        shift();
        return 1;
    }
    if (a1 <= 47 || a1 > 57)
        return 0;
    if (a1 - 48 != n % 10)
        return 0;
    n /= 10;
    if (x == 3)
        function_id = 2;
    else
        function_id = 0;
    checked = 1;
    printf("access function check_2 with %d, %d\n", a1, x);
    return 1;
}

int check_3(char a1)
{
    if (checked || function_id != 2)
    {
        shift();
        return 1;
    }
    if (!(a1 * a1 % 9024))
        return 0;
    function_id = 0;
    checked = 1;
    printf("access function check_3 with %d, %d\n", a1, x);
    return 1;
}

int check_input(char *input)
{
    if (strlen(input) != 35)
    {
        return 0;
    }
    if (strncmp(input, "lactf{", 6) != 0)
    {
        return 0;
    }
    if (input[34] != 125)
    {
        return 0;
    }
    for (int m = 6; m <= 33; ++m)
    {
        checked = 0;
        if (!check_1(input[m]) || !check_2(input[m]) || !check_3(input[m]))
        {
            printf("wrong in: %d\n", m);
            return 0;
        }
    }
    printf("gathered: %s\n", gathered);

    return strcmp(gathered, "vwbowpcjrhpkobfryu") == 0;
}

int main(int argc, char **argv, char **envp)
{
    char input[70] = {0};
    printf("she r on my b till I p > ");
    fgets(input, 69, stdin);
    strtok(input, "\n");
    if (check_input(input))
        printf("omg how did u guess\n");
    else
        printf("extremely loud incorrect buzzer\n");

    return 0;
}