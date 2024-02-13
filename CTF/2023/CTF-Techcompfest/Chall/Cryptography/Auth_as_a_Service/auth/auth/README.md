# Auth as a Service - User - Kernel

## TL;DR

**Auth as a Service - User**
- `interface.c`

**Auth as a Kernel**
- `char.c`
- `char.h`
- `aes.c`
- `aes.h`

## Folder Structure

```
.
├── Dockerfile
├── README.md
├── bin
│   ├── auth.ko
│   ├── interface
│   ├── ld-linux-x86-64.so.2
│   └── libc.so.6
├── docker-compose.yml
├── qemu
│   ├── bzImage
│   ├── rootfs.cpio.gz
│   └── run.sh
└── src
    ├── Makefile
    ├── aes.c
    ├── aes.h
    ├── char.c
    ├── char.h
    └── interface.c

3 directories, 16 files
```

## Detail Source

- `Dockerfile`, `docker-compose.yml` ~ Config docker images and container to host this challenge
- `bin` ~ Binary of a challenge and mostly important for debugging process
- `qemu` ~ All the challenge files in here
- `src` ~ Source of a challenge

#### `ls bin/`
- `auth.ko` ~ The kernel module for **Auth as a Kernel**
- `interface` ~ The auth interface binary for **Auth as a Service** and **Auth as a User**
- `libc.so.6` ~ The libc for `interface` binary
- `ld-linux-x86-64.so.2` ~ The ld for `interface` binary

#### `ls qemu/`
- `bzImage` ~ Compressed linux kernel image
- `rootfs.cpio.gz` ~ Initial root filesystem
- `run.sh` ~ Qemu run script

#### `ls src/`
- `Makefile` ~ Build script for kernel and interface
- `aes.c` ~ AES module
- `aes.h` ~ Header file `aes.c` 
- `char.c` ~ Main character device module
- `char.h` ~ Header file `char.c` 
- `interface.c` ~ Auth interface source
