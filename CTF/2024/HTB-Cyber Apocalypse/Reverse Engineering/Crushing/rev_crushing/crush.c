#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void add_char_to_map(char *cipher, unsigned char character, long long index) {
    long long *entry = (long long *)(8LL * character + (long long)cipher);
    long long *new_entry = malloc(sizeof(long long) * 2);
    if (!new_entry) {
        // Handle allocation failure
        exit(EXIT_FAILURE);
    }
    new_entry[0] = index;
    new_entry[1] = 0LL;

    if (*entry) {
        long long *ptr = (long long *)*entry;
        while (ptr[1])
            ptr = (long long *)ptr[1];
        ptr[1] = (long long)new_entry;
    } else {
        *entry = (long long)new_entry;
    }
}

long long list_length(void *list) {
    long long length = 0;
    if (list) {
        length = 1;
        long long *ptr = (long long *)list;
        while (ptr[1]) {
            ptr = (long long *)ptr[1];
            ++length;
        }
    }
    return length;
}

void serialize_and_output(char *cipher) {
    FILE *output_file = stdout;

    for (int i = 0; i <= 254; ++i) {
        long long **entry = (long long **)(8LL * i + (long long)cipher);
        long long length = list_length(*entry);
        // printf("%x: %lld\n", i, length);
        fwrite(&length, 8, 1, output_file);
        for (long long *ptr = *entry; ptr; ptr = (long long *)ptr[1])
            fwrite(ptr, 8, 1, output_file);
    }
}

int main(int argc, const char **argv, const char **envp) {
    char cipher[2052];
    memset(cipher, 0, sizeof(cipher));
    
    for (long long i = 0; ; ++i) {
        int character = getchar();
        if (character == EOF)
            break;
        add_char_to_map(cipher, (unsigned char)character, i);
    }

    serialize_and_output(cipher);
    return 0;
}
