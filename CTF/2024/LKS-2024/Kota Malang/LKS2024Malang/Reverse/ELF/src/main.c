#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <elf.h>
#include <sys/ptrace.h>
#include <stdlib.h>

#ifdef __LP64__
#define Elf_Ehdr Elf64_Ehdr
#define Elf_Shdr Elf64_Shdr
#define Elf_Sym  Elf64_Sym
#else
#define Elf_Ehdr Elf32_Ehdr
#define Elf_Shdr Elf32_Shdr
#define Elf_Sym  Elf32_Sym
#endif

#define Section(name) __attribute__((section(name)))

Section("f16") int _f16 = 5143;
Section("f25") int _f25 = 5831;
Section("f30") int _f30 = 5495;
Section("f28") int _f28 = 5543;
Section("f17") int _f17 = 5831;
Section("f4") int _f4 = 5831;
Section("f27") int _f27 = 4103;
Section("f19") int _f19 = 5735;
Section("f3") int _f3 = 5127;
Section("f6") int _f6 = 5623;
Section("f13") int _f13 = 5383;
Section("f5") int _f5 = 5975;
Section("f24") int _f24 = 5639;
Section("f1") int _f1 = 6071;
Section("f8") int _f8 = 5447;
Section("f20") int _f20 = 5143;
Section("f22") int _f22 = 5831;
Section("f9") int _f9 = 5831;
Section("f23") int _f23 = 4135;
Section("f10") int _f10 = 5895;
Section("f0") int _f0 = 5239;
Section("f29") int _f29 = 5655;
Section("f18") int _f18 = 5127;
Section("f12") int _f12 = 4103;
Section("f2") int _f2 = 4135;
Section("f21") int _f21 = 4103;
Section("f15") int _f15 = 5991;
Section("f26") int _f26 = 5703;
Section("f14") int _f14 = 5511;
Section("f11") int _f11 = 5559;
Section("f7") int _f7 = 4215;

__attribute__((constructor)) void init0() {
    if (ptrace(PTRACE_TRACEME, 0, 0, 0) == -1) {
        int status = 0;
        asm volatile (
            "movl $60, %%eax\n"
            "movl %0, %%edi\n"
            "syscall"
            :
            : "r" (status)
            : "eax", "edi"
        );
    }
}

__attribute__((constructor)) void init1() {
    int isDebugged = 0;

    // /proc/self/status
    char gxAeVE[] = { 0x56, 0x0A, 0x13, 0x11, 0x16, 0x5B, 0x10, 0x1B, 0x1F, 0x14, 0x58, 0x0D, 0x0B, 0x19, 0x09, 0x03, 0x1A, 0x00 };
    for (int kos = 0; kos < 17; kos++) {
        gxAeVE[kos] += kos;
        gxAeVE[kos]--;
        gxAeVE[kos] ^= 0x7A;
        gxAeVE[kos] += kos;
        gxAeVE[kos] ^= kos;
    }

    // r
    char UrjsXv[] = { 0x97, 0x00 };
    for (int ZtQ = 0; ZtQ < 1; ZtQ++) {
        UrjsXv[ZtQ]++;
        UrjsXv[ZtQ] ^= 0x15;
        UrjsXv[ZtQ] += 0x79;
        UrjsXv[ZtQ]--;
        UrjsXv[ZtQ] += 0x6D;
    }

    // TracerPid:
    char vepIDx[] = { 0xAA, 0x8D, 0x9F, 0x96, 0x9D, 0x81, 0xA4, 0x8C, 0x82, 0xCD, 0x00 };
    for (int Ynr = 0; Ynr < 10; Ynr++) {
        vepIDx[Ynr] ^= Ynr;
        vepIDx[Ynr] += Ynr;
        vepIDx[Ynr] ^= Ynr;
        vepIDx[Ynr]++;
        vepIDx[Ynr] = ~vepIDx[Ynr];
    }

    // TracerPid:\t%d
    char swjapB[] = { 0xB3, 0x5C, 0xAE, 0xAF, 0xAC, 0x58, 0x85, 0xAD, 0xAB, 0x9C, 0xBD, 0xA4, 0xF4, 0xB6, 0x00 };
    for (int GkB = 0; GkB < 14; GkB++) {
        swjapB[GkB] ^= 0x25;
        swjapB[GkB] -= GkB;
        swjapB[GkB] += 0x14;
        swjapB[GkB] = ~swjapB[GkB];
        swjapB[GkB]--;
    }


    FILE* f = fopen(gxAeVE, UrjsXv);
    if (!f) {
        return;
    }

    char line[128];
    while (fgets(line, sizeof(line), f)) {
        if (strstr(line, vepIDx) == line) {
            int tracerPid;
            if (sscanf(line, swjapB, &tracerPid) == 1 && tracerPid != 0) {
                isDebugged = 1;
                break;
            }
        }
    }

    fclose(f);

    if (isDebugged) {
        int status = 0;
        asm volatile (
            "movl $60, %%eax\n"
            "movl %0, %%edi\n"
            "syscall"
            :
            : "r" (status)
            : "eax", "edi"
        );
    }
}

int main(int argc, char **argv) {
    char input[33];
    printf("Enter the flag: ");
    scanf("%s", input);
    
    FILE *f = fopen(argv[0], "rb");
    if (f == NULL) {
        perror("fopen");
        return 1;
    }

    Elf_Ehdr ehdr;
    fread(&ehdr, sizeof(ehdr), 1, f);

    Elf_Shdr shdr;
    fseek(f, ehdr.e_shoff + ehdr.e_shstrndx * sizeof(shdr), SEEK_SET);
    fread(&shdr, sizeof(shdr), 1, f);

    char *shstrtab = malloc(sizeof(char) * shdr.sh_size);
    fseek(f, shdr.sh_offset, SEEK_SET);
    fread(shstrtab, sizeof(char), shdr.sh_size, f);

    fseek(f, ehdr.e_shoff, SEEK_SET);
    for (int i = 0; i < ehdr.e_shnum; i++) {
        fread(&shdr, sizeof(shdr), 1, f);
        char *name = shstrtab + shdr.sh_name;
        // printf("%s\n", name);

        if (name && strlen(name) > 1) {
            if (name[0] != '.') {
                int idx = atoi(name + 1);

                int val;
                size_t pos = ftell(f);
                fseek(f, shdr.sh_offset, SEEK_SET);
                fread(&val, sizeof(val), 1, f);
                fseek(f, pos, SEEK_SET);

                // printf("%d: %d\n", idx, val);
                if (((input[idx] << 4) ^ 0x1337) != val) {
                    printf("Wrong!\n");
                    return 1;
                }
            }
        }
    }
    fclose(f);

    printf("Correct!\n");
    return 0;
}
