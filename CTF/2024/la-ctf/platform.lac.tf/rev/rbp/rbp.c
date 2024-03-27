#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <signal.h>
#include <stdlib.h>
#include <errno.h>
#include <stdint.h>

int dword_70824 = 13003401;
int dword_70AE4 = 0;
int dword_70AE8 = 0;
int dword_70AEC = 0;
char byte_70B00[36] = {0};
char byte_70AC0 = 0;

__attribute__((section("p"))) int check_1(char a1)
{
    if (a1 <= 96 || a1 > 122)
        return 0;
    byte_70B00[dword_70AE4++] = a1;
    if ((a1 == 98 || a1 == 99 || a1 == 104 || a1 == 115 || a1 == 116) && ++dword_70AEC != 2 && dword_70AEC != 8 && dword_70AEC != 9 && dword_70AEC != 12)
        dword_70AE8 = 1;
    if (a1 == 100)
        dword_70AE8 = 2;
    return 1;
}

__attribute__((section("b"))) int check_2(char a1)
{
    if (a1 <= 47 || a1 > 57)
        return 0;
    if (a1 - 48 != dword_70824 % 10)
        return 0;
    dword_70824 /= 10;
    if (dword_70AEC == 3)
        dword_70AE8 = 2;
    else
        dword_70AE8 = 0;
    return 1;
}

__attribute__((section("r"))) int check_3(char a1)
{
    if (!(a1 * a1 % 9024))
        return 0;
    dword_70AE8 = 0;
    return 1;
}

void protecting(int function_got_protect)
{
    long page_size = sysconf(_SC_PAGE_SIZE);

    void *check_1_addr = (void *)((long)check_1 & ~(page_size - 1));
    void *check_2_addr = (void *)((long)check_2 & ~(page_size - 1));
    void *check_3_addr = (void *)((long)check_3 & ~(page_size - 1));

    int prot;
    if (function_got_protect)
        prot = PROT_READ | PROT_WRITE;
    else
        prot = PROT_READ | PROT_WRITE | PROT_EXEC;
    if (mprotect(check_1_addr, 0xb8, prot) == -1)
    {
        printf("mprotect failed: %s\n", strerror(errno));
        abort();
    }
    if (function_got_protect == 1)
        prot = PROT_READ | PROT_WRITE | PROT_EXEC;
    else
        prot = PROT_READ | PROT_WRITE;
    if (mprotect(check_2_addr, 0xaa, prot) == -1)
    {
        printf("mprotect failed: %s\n", strerror(errno));
        abort();
    }
    if (function_got_protect == 2)
        prot = PROT_READ | PROT_WRITE | PROT_EXEC;
    else
        prot = PROT_READ | PROT_WRITE;
    if (mprotect(check_3_addr, 0x52, prot) == -1)
    {
        printf("mprotect failed: %s\n", strerror(errno));
        abort();
    }
}

int check_input(char *input)
{
    int prime_sequence[10]; // {3, 5, 7, 11, 13, 17, 19, 23, 29, 31}
    int v15[36] = {0, 0xD, 0xF, 0x18, 0xA, 0x17, 0xD, 0, 2, 0x15, 7, 26, 15, 2, 0, 23, 5, 24, 24, 21, 23, 0, 18, 15, 10, 7, 5, 18, 0, 29, 23, 26, 24, 15, 29, 0};
    long long prod_input = 1LL;
    int itr, v5, i, v7, j, k, m;
    unsigned long len_input = strlen(input) - 1;

    for (itr = 0, v5 = 2; itr <= 9;)
    {
        ++v5;
        for (i = 2; i < v5; ++i)
        {
            if (v5 % i == 0)
                goto next_itr;
        }
        prime_sequence[itr++] = v5;
    next_itr:;
    }

    if (len_input != prime_sequence[1] * prime_sequence[2])
    {
        return 0;
    }
    for (j = 0, v7 = 0; j <= 5; ++j)
    {
        for (k = 0; k <= 5; ++k)
        {
            if ((char)(input[j] ^ input[k]) != v15[v7++])
                return 0;
        }
        prod_input *= input[j];
    }

    if (prod_input != 1509363893664LL)
    {
        return 0;
    }

    if (input[34] != 125)
    {
        return 0;
    }

    for (m = 6; m <= 33; ++m)
    {
        if (dword_70AE8 != -1)
        {
            protecting(dword_70AE8);
            dword_70AE8 = -1;
        }
        if (!check_1(input[m]) || !check_2(input[m]) || !check_3(input[m]))
        {
            printf("wrong in: %d\n", m);
            return 0;
        }
    }

    return strcmp(byte_70B00, "vwbowpcjrhpkobfryu") == 0;
}

int64_t sub_710F9(int64_t a1, int64_t a2, int64_t a3)
{
    int64_t result; // rax
    int i;

    for (i = 0; i < dword_70AE4; ++i)
        byte_70B00[i] = ((char)byte_70B00[i] - 96) % 26 + 97;
    *(unsigned int *)(a3 + 144) = 1LL;
    result = a3;
    *(unsigned int *)(a3 + 168) = **(unsigned int **)(a3 + 160);
    return result;
}

int main(int argc, char **argv, char **envp)
{
    struct sigaction act;
    memset(&act, 0, sizeof(act));
    act.sa_handler = (void (*)(int))sub_710F9;
    sigemptyset(&act.sa_mask);
    act.sa_flags = 4;
    if (sigaction(SIGSEGV, &act, 0) == -1)
    {
        printf("sigaction failed: %s\n", strerror(errno));
        abort();
    }

    char input[70] = {0};
    printf("she r on my b till I p > ");
    fgets(input, 69, stdin);

    if (check_input(input))
        printf("omg how did u guess\n");
    else
        printf("extremely loud incorrect buzzer\n");

    return 0;
}
