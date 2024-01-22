// Differential Cryptanalysis of FEAL-4
// Uses a chosen-plaintext attack to fully recover the key
// For use with tutorial at http://theamazingking.com/crypto-feal.php

#include <stdio.h>
#include <math.h>

#define MAX_CHOSEN_PAIRS 10000
#define ROTATE_LEFT(x, n) (((x) << (n)) | ((x) >> (32 - (n))))

int winner = 0;
int loser = 0;

unsigned long subkey[6];

unsigned char rotl2(unsigned char a) { return ((a << 2) | (a >> 6)); }
unsigned char swap(unsigned char a) { return (((a << 4) | (a >> 4)) & 0xFF); }

unsigned long leftHalf(unsigned long long a) { return (a >> 32LL); }
unsigned long rightHalf(unsigned long long a) { return a; }
unsigned char sepByte(unsigned long a, unsigned char index) { return a >> (8 * index); }
unsigned long combineBytes(unsigned char b3, unsigned char b2, unsigned char b1, unsigned char b0)
{
    return b3 << 24L | (b2 << 16L) | (b1 << 8L) | b0;
}
unsigned long long combineHalves(unsigned long leftHalf, unsigned long rightHalf)
{
    return (((unsigned long long)(leftHalf)) << 32LL) | (((unsigned long long)(rightHalf)) & 0xFFFFFFFFLL);
}

unsigned char gBox(unsigned char a, unsigned char b, unsigned char mode)
{
    return swap((3 * a) + (5 * b) + (7 * mode));
}

unsigned long fBox(unsigned long plain)
{
    unsigned char x0 = sepByte(plain, 0);
    unsigned char x1 = sepByte(plain, 1);
    unsigned char x2 = sepByte(plain, 2);
    unsigned char x3 = sepByte(plain, 3);

    unsigned char y0 = gBox(x0, x1, 0);
    unsigned char y1 = gBox(x2, x1 ^ y0, 1);
    unsigned char y2 = gBox(x2 ^ y1, x3, 0);
    unsigned char y3 = gBox(x3, x3, 1);

    return combineBytes(y3, y2, y1, y0);
}

unsigned long long encrypt(unsigned long long plain)
{
    unsigned long left = leftHalf(plain);
    unsigned long right = rightHalf(plain);

    unsigned long round2Left = left ^ right;
    unsigned long round2Right = left ^ fBox(right ^ subkey[0]);

    unsigned long round3Left = round2Right;
    unsigned long round3Right = round2Left ^ fBox(round2Right ^ subkey[1]);

    unsigned long round4Left = round3Right;
    unsigned long round4Right = round3Left ^ fBox(round3Right ^ subkey[2]);

    unsigned long cipherLeft = round4Left ^ fBox(round4Right ^ subkey[3]);
    unsigned long cipherRight = cipherLeft ^ round4Right;

    return combineHalves(cipherLeft, cipherRight);
}

void generateSubkeys(int seed)
{
    srand(seed);

    int c;
    for (c = 0; c < 6; c++)
        subkey[c] = (rand() << 16L) | (rand() & 0xFFFFL);
}

int numPlain;
unsigned long long plain0[MAX_CHOSEN_PAIRS];
unsigned long long cipher0[MAX_CHOSEN_PAIRS];
unsigned long long plain1[MAX_CHOSEN_PAIRS];
unsigned long long cipher1[MAX_CHOSEN_PAIRS];

void undoFinalOperation()
{
    int c;
    for (c = 0; c < numPlain; c++)
    {
        unsigned long cipherLeft0 = leftHalf(cipher0[c]);
        unsigned long cipherRight0 = rightHalf(cipher0[c]) ^ cipherLeft0;
        unsigned long cipherLeft1 = leftHalf(cipher1[c]);
        unsigned long cipherRight1 = rightHalf(cipher1[c]) ^ cipherLeft1;

        cipher0[c] = combineHalves(cipherLeft0, cipherRight0);
        cipher1[c] = combineHalves(cipherLeft1, cipherRight1);
    }
}

unsigned long crackLastRound(unsigned long outdiff)
{
    printf("  Using output differential of 0x%08x\n", outdiff);
    printf("  Cracking...");

    unsigned long fakeK;
    for (fakeK = 0x00000000L; fakeK < 0xFFFFFFFFL; fakeK++)
    {
        int score = 0;

        int c;
        for (c = 0; c < numPlain; c++)
        {
            unsigned long cipherLeft = (cipher0[c] >> 32LL);
            cipherLeft ^= (cipher1[c] >> 32LL);

            unsigned long Z = cipherLeft ^ outdiff;

            unsigned long fakeRight = cipher0[c] & 0xFFFFFFFFLL;
            unsigned long fakeRight2 = cipher1[c] & 0xFFFFFFFFLL;

            unsigned long Y0 = fakeRight;
            unsigned long Y1 = fakeRight2;

            unsigned long fakeInput0 = Y0 ^ fakeK;
            unsigned long fakeInput1 = Y1 ^ fakeK;
            unsigned long fakeOut0 = fBox(fakeInput0);
            unsigned long fakeOut1 = fBox(fakeInput1);
            unsigned long fakeDiff = fakeOut0 ^ fakeOut1;

            if (fakeDiff == Z)
                score++;
            else
                break;
        }

        if (score == numPlain)
        {
            printf("found subkey : 0x%08lx\n", fakeK);
            return fakeK;
        }
    }

    printf("failed\n");
    return 0;
}

void chosenPlaintext(unsigned long long diff)
{
    printf("  Generating %i chosen-plaintext pairs\n", numPlain);
    printf("  Using input differential of 0x%016llx\n", diff);

    srand(time(NULL));

    int c;
    for (c = 0; c < numPlain; c++)
    {
        plain0[c] = (rand() & 0xFFFFLL) << 48LL;
        plain0[c] += (rand() & 0xFFFFLL) << 32LL;
        plain0[c] += (rand() & 0xFFFFLL) << 16LL;
        plain0[c] += (rand() & 0xFFFFLL);

        cipher0[c] = encrypt(plain0[c]);
        plain1[c] = plain0[c] ^ diff;
        cipher1[c] = encrypt(plain1[c]);
    }
}

void undoLastRound(unsigned long crackedSubkey)
{
    int c;
    for (c = 0; c < numPlain; c++)
    {
        unsigned long cipherLeft0 = leftHalf(cipher0[c]);
        unsigned long cipherRight0 = rightHalf(cipher0[c]);
        unsigned long cipherLeft1 = leftHalf(cipher1[c]);
        unsigned long cipherRight1 = rightHalf(cipher1[c]);

        cipherLeft0 = cipherRight0;
        cipherLeft1 = cipherRight1;
        cipherRight0 = fBox(cipherLeft0 ^ crackedSubkey) ^ (cipher0[c] >> 32LL);
        cipherRight1 = fBox(cipherLeft1 ^ crackedSubkey) ^ (cipher1[c] >> 32LL);

        cipher0[c] = combineHalves(cipherLeft0, cipherRight0);
        cipher1[c] = combineHalves(cipherLeft1, cipherRight1);
    }
}

void prepForCrackingK0()
{
    int c;
    for (c = 0; c < numPlain; c++)
    {
        unsigned long cipherLeft0 = leftHalf(cipher0[c]);
        unsigned long cipherRight0 = rightHalf(cipher0[c]);
        unsigned long cipherLeft1 = leftHalf(cipher1[c]);
        unsigned long cipherRight1 = rightHalf(cipher1[c]);

        unsigned long tempLeft0 = cipherLeft0;
        unsigned long tempLeft1 = cipherLeft1;
        cipherLeft0 = cipherRight0;
        cipherLeft1 = cipherRight1;
        cipherRight0 = tempLeft0;
        cipherRight1 = tempLeft1;

        cipher0[c] = combineHalves(cipherLeft0, cipherRight0);
        cipher1[c] = combineHalves(cipherLeft1, cipherRight1);
    }
}

int main()
{

    printf("JK'S FEAL-4 DIFFERENTIAL CRYPTANALYSIS DEMO\n");
    printf("-------------------------------------------\n");
    printf("\n");

    int graphData[20];

    int c;

    generateSubkeys(time(NULL));
    numPlain = 12;
    unsigned long long inputDiff1 = 0x0080808000808080LL;
    unsigned long long inputDiff2 = 0x0000000080800000LL;
    unsigned long long inputDiff3 = 0x0000000002000000LL;
    unsigned long outDiff = 0x02000000L;

    unsigned long fullStartTime = time(NULL);

    // CRACKING ROUND 4
    printf("ROUND 4\n");
    chosenPlaintext(inputDiff1);
    undoFinalOperation();
    unsigned long startTime = time(NULL);
    unsigned long crackedSubkey3 = crackLastRound(outDiff);
    unsigned long endTime = time(NULL);
    printf("  Time to crack round #4 = %i seconds\n", (endTime - startTime));

    // CRACKING ROUND 3
    printf("ROUND 3\n");
    chosenPlaintext(inputDiff2);
    undoFinalOperation();
    undoLastRound(crackedSubkey3);
    startTime = time(NULL);
    unsigned long crackedSubkey2 = crackLastRound(outDiff);
    endTime = time(NULL);
    printf("  Time to crack round #3 = %i seconds\n", (endTime - startTime));

    // CRACKING ROUND 2
    printf("ROUND 2\n");
    chosenPlaintext(inputDiff3);
    undoFinalOperation();
    undoLastRound(crackedSubkey3);
    undoLastRound(crackedSubkey2);
    startTime = time(NULL);
    unsigned long crackedSubkey1 = crackLastRound(outDiff);
    endTime = time(NULL);
    printf("  Time to crack round #2 = %i seconds\n", (endTime - startTime));

    // CRACK ROUND 1
    printf("ROUND 1\n");
    undoLastRound(crackedSubkey1);
    unsigned long crackedSubkey0 = 0;
    unsigned long crackedSubkey4 = 0;
    unsigned long crackedSubkey5 = 0;

    printf("  Cracking...");

    startTime = time(NULL);
    unsigned long guessK0;
    for (guessK0 = 0; guessK0 < 0xFFFFFFFFL; guessK0++)
    {
        unsigned long guessK4 = 0;
        unsigned long guessK5 = 0;
        int c;
        for (c = 0; c < numPlain; c++)
        {
            unsigned long plainLeft0 = leftHalf(plain0[c]);
            unsigned long plainRight0 = rightHalf(plain0[c]);
            unsigned long cipherLeft0 = leftHalf(cipher0[c]);
            unsigned long cipherRight0 = rightHalf(cipher0[c]);

            unsigned long tempy0 = fBox(cipherRight0 ^ guessK0) ^ cipherLeft0;
            if (guessK4 == 0)
            {
                guessK4 = tempy0 ^ plainLeft0;
                guessK5 = tempy0 ^ cipherRight0 ^ plainRight0;
            }
            else if (((tempy0 ^ plainLeft0) != guessK4) || ((tempy0 ^ cipherRight0 ^ plainRight0) != guessK5))
            {
                guessK4 = 0;
                guessK5 = 0;
                break;
            }
        }
        if (guessK4 != 0)
        {

            crackedSubkey0 = guessK0;
            crackedSubkey4 = guessK4;
            crackedSubkey5 = guessK5;
            endTime = time(NULL);

            printf("found subkeys : 0x%08lx  0x%08lx  0x%08lx\n", guessK0, guessK4, guessK5);
            printf("  Time to crack round #1 = %i seconds\n", (endTime - startTime));
            break;
        }
    }

    printf("\n\n");
    printf("0x%08lx - ", crackedSubkey0);
    if (crackedSubkey0 == subkey[0])
        printf("Subkey 0 : GOOD!\n");
    else
        printf("Subkey 0 : BAD\n");
    printf("0x%08lx - ", crackedSubkey1);
    if (crackedSubkey1 == subkey[1])
        printf("Subkey 1 : GOOD!\n");
    else
        printf("Subkey 1 : BAD\n");
    printf("0x%08lx - ", crackedSubkey2);
    if (crackedSubkey2 == subkey[2])
        printf("Subkey 2 : GOOD!\n");
    else
        printf("Subkey 2 : BAD\n");
    printf("0x%08lx - ", crackedSubkey3);
    if (crackedSubkey3 == subkey[3])
        printf("Subkey 3 : GOOD!\n");
    else
        printf("Subkey 3 : BAD\n");
    printf("0x%08lx - ", crackedSubkey4);
    if (crackedSubkey4 == subkey[4])
        printf("Subkey 4 : GOOD!\n");
    else
        printf("Subkey 4 : BAD\n");
    printf("0x%08lx - ", crackedSubkey5);
    if (crackedSubkey5 == subkey[5])
        printf("Subkey 5 : GOOD!\n");
    else
        printf("Subkey 5 : BAD\n");
    printf("\n");

    unsigned long fullEndTime = time(NULL);
    printf("Total crack time = %i seconds\n", (fullEndTime - fullStartTime));

    printf("FINISHED\n");
    while (1)
    {
    }

    return 0;
}