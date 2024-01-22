int printf(const char *format, ...);
int open(const char *pathname, int flags);
int close(int fd);
int read(int fd, void *buf, unsigned int count);
char *strcpy(char *dest, const char *src);
char *strncpy(char *dest, const char *src, unsigned int n);
char *strstr(const char *s1, const char *s2);
unsigned int strlen(const char *s);
int scanf(const char *format, ...);

unsigned int crc32(unsigned char *m)
{
    int i, j;
    unsigned int b, c, mk;

    i = 0;
    c = 0xFFFFFFFF;
    while (m[i] != 0)
    {
        b = m[i];
        c = c ^ b;
        for (j = 7; j >= 0; j--)
        {
            mk = -(c & 1);
            c = (c >> 1) ^ (0xEDB88320 & mk);
        }
        i = i + 1;
    }
    return ~c;
}

int main(int argc, char *argv[])
{
    const char *lslash = strrchr(argv[0], '/');

    if (lslash == 0)
    {
        printf("No '/' found in the path.\n");
        return 1;
    }
    unsigned int subLen = lslash - argv[0];

    char path[subLen + 1];

    strncpy(path, argv[0], subLen);
    path[subLen] = '\0';

    printf("Substring: %s\n", path);

    // int fd = open(resStr, 'r');
    // if (fd == -1)
    // {
    //     printf("Error opening file\n");
    //     return 1;
    // }

    // int bufLen = read(fd, buff, 2048);
    // if (bufLen == -1)
    // {
    //     printf("Error reading file\n");
    //     return 1;
    // }

    // close(fd);

    // printf("%d\n", strlen(buff));

    // char inp[2048];
    // gets(inp);

    // int i = 0;
    // while (buff[i] != 0 && inp[i] != 0)
    // {
    //     buff[i] = buff[i] ^ inp[i];
    //     i = i + 1;
    // }
    // if (inp[i] != buff[i])
    // {
    //     printf("inp = %c \n", inp[i]);
    //     printf("buff = %c \n", buff[i]);
    //     printf("Error incorrect input\\n");
    //     return 0;
    // }

    // printf("%d\\n", crc32(buff));

    return 0;
}