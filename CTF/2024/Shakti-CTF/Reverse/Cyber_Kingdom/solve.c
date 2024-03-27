#include <stdio.h>

int main() {
    char flag[35];
    flag[0] = 114;
    flag[1] = 109;
    flag[2] = 96;
    flag[3] = 101;
    flag[4] = 115;
    flag[5] = 98;
    flag[6] = 104;
    flag[7] = 122;
    flag[8] = 108;
    flag[9] = 122;
    flag[10] = 119;
    flag[11] = 100;
    flag[12] = 49;
    flag[13] = 84;
    flag[14] = 119;
    flag[15] = 49;
    flag[16] = 108;
    flag[17] = 99;
    flag[18] = 89;
    flag[19] = 103;
    flag[20] = 98;
    flag[21] = 49;
    flag[22] = 108;
    flag[23] = 88;
    flag[24] = 49;
    flag[25] = 125;
    flag[26] = 83;
    flag[27] = 126;
    flag[28] = 59;
    flag[29] = 98;
    flag[30] = 105;
    flag[31] = 48;
    flag[32] = 108;
    flag[33] = 49;
    flag[34] = 114;
    srand(123);
    for (int i = 0; i < 35; i++) {
        flag[i] = flag[i] ^ (rand() & 0xf);
    }
    printf("%s\n", flag);
}