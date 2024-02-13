#include <stdio.h>

unsigned long key[] = {0x1234567, 0x89ABCDEF, 0x0FEDCBA98, 0x76543210};

void encrypt_token(unsigned long *token1, unsigned long *token2) {
    int i = 0;
    for (int _ = 0; _ < 32; _++) {
        *token1 += (*token2 + i) ^ (16 * *token2 + key[0]) ^ ((*token2 >> 5) + key[1]);
        i -= 0x61C88647;
        *token2 += ((*token1 >> 5) + key[3]) ^ (*token1 + i) ^ (16 * *token1 + key[2]);
    }
}

void decrypt_token(unsigned long *token1, unsigned long *token2) {
    int i = 0xc6ef3720;
    for (int _ = 0; _ < 32; _++) {
        *token2 -= ((*token1 >> 5) + key[3]) ^ (*token1 + i) ^ (16 * *token1 + key[2]);
        i += 0x61C88647;
        *token1 -= (*token2 + i) ^ (16 * *token2 + key[0]) ^ ((*token2 >> 5) + key[1]);
    }
}

int main() {
    unsigned long token1 = 4068142527;
    unsigned long token2 = 3976246892;
    decrypt_token(&token1, &token2);
    printf("Token: %u_%u\n", token1, token2);
}