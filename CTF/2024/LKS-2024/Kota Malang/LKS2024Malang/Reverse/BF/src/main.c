#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

uint32_t crc32(const uint8_t *data, size_t len) {
    uint32_t crc_table[256];
    uint32_t crc;
    for (int i = 0; i < 256; i++) {
        crc = i;
        for (int j = 0; j < 8; j++) {
            crc = crc & 1 ? (crc >> 1) ^ 0xEDB88320UL : crc >> 1;
        }
        crc_table[i] = crc;
    }

    crc = 0xFFFFFFFFUL;
    while (len--) {
        crc = crc_table[(crc ^ *data++) & 0xFF] ^ (crc >> 8);
    }
    return crc ^ 0xFFFFFFFFUL;
}

uint32_t tables[] = {
    0xad68e236,
    0x330c7795,
    0x2060efc3,
    0x1ad5be0d,
    0xf4dbdf21,
    0x1ad5be0d,
    0xf3b61b38,
    0xda6fd2a0,
    0xd3d99e8b,
    0xad68e236,
    0xd3d99e8b,
    0x4366831a,
    0x3aba3bbe,
    0x15d54739,
    0x4ad0cf31,
    0x6c09ff9d,
    0xf26d6a3e,
    0x856a5aa8,
    0x6dd28e9b,
    0x76d32be0,
    0xf4dbdf21,
    0x6c09ff9d,
    0x06b9df6f,
    0x6dd28e9b,
    0x29d6a3e8,
    0xdd0216b9,
    0x84b12bae,
    0x29d6a3e8,
    0xa3b36a04,
    0xf3b61b38,
    0x29d6a3e8,
    0xf4dbdf21,
    0x4366831a,
    0x9606c2fe,
    0xc0b506dd,
    0x29d6a3e8,
    0x270d2bda,
    0xf3b61b38,
    0xfbdb2615,
    0xfcb6e20c,
};

int main(int argc, char **argv) {
    // const char *flag = "LKS2024MALANG{Brut3f0rc3_I5_D4_0NlY_W4y}";
    // for (int i = 0; i < strlen(flag); i++) {
    //     printf("%08x\n", crc32((uint8_t *)&flag[i], 1));
    // }
    char flag[100];
    printf("Enter the flag: ");
    scanf("%s", flag);
    
    for (int i = 0; i < sizeof(tables) / sizeof(tables[0]); i++) {
        if (crc32((uint8_t *)&flag[i], 1) != tables[i]) {
            printf("Wrong!\n");
            return 0;
        }
    }
    printf("Correct!\n");
    return 0;
}