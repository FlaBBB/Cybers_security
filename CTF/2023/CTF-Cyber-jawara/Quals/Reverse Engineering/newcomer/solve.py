        # 00203b90 d2              ??         D2h
        # 00203b91 95              ??         95h
        # 00203b92 c2              ??         C2h
        # 00203b93 70              ??         70h    p
        # 00203b94 a4              ??         A4h
        # 00203b95 53              ??         53h    S
        # 00203b96 d5              ??         D5h
        # 00203b97 4a              ??         4Ah    J
        # 00203b98 3d              ??         3Dh    =
        # 00203b99 c0              ??         C0h
        # 00203b9a 9a              ??         9Ah
        # 00203b9b 3c              ??         3Ch    <
        # 00203b9c 62              ??         62h    b
        # 00203b9d 0d              ??         0Dh
        # 00203b9e a7              ??         A7h
        # 00203b9f 41              ??         41h    A
        # 00203ba0 ea              ??         EAh
        # 00203ba1 2a              ??         2Ah    *
        # 00203ba2 3c              ??         3Ch    <
        # 00203ba3 85              ??         85h
        # 00203ba4 73              ??         73h    s
        # 00203ba5 c6              ??         C6h
        # 00203ba6 ac              ??         ACh
        # 00203ba7 47              ??         47h    G
        # 00203ba8 ee              ??         EEh
        # 00203ba9 87              ??         87h
        # 00203baa 0d              ??         0Dh
        # 00203bab 64              ??         64h    d
        # 00203bac b8              ??         B8h
        # 00203bad 5e              ??         5Eh    ^
        # 00203bae a9              ??         A9h
        # 00203baf 5a              ??         5Ah    Z
        # 00203bb0 0d              ??         0Dh
        # 00203bb1 47              ??         47h    G
        # 00203bb2 8d              ??         8Dh
        # 00203bb3 3b              ??         3Bh    ;
        # 00203bb4 8a              ??         8Ah
        # 00203bb5 58              ??         58h    X
        # 00203bb6 8a              ??         8Ah
        # 00203bb7 00              ??         00h
        # 00203bb8 05              ??         05h
        # 00203bb9 da              ??         DAh
        # 00203bba 81              ??         81h
        # 00203bbb 44              ??         44h    D
        # 00203bbc ab              ??         ABh
        # 00203bbd 2e              ??         2Eh    .
        # 00203bbe 96              ??         96h
        # 00203bbf 93              ??         93h
        # 00203bc0 6e              ??         6Eh    n
        # 00203bc1 43              ??         43h    C
        # 00203bc2 56              ??         56h    V
        # 00203bc3 1b              ??         1Bh
        # 00203bc4 9d              ??         9Dh
        # 00203bc5 51              ??         51h    Q
        # 00203bc6 89              ??         89h
        # 00203bc7 60              ??         60h    `
        # 00203bc8 29              ??         29h    )
        # 00203bc9 ae              ??         AEh
        # 00203bca 09              ??         09h
        # 00203bcb 54              ??         54h    T
        # 00203bcc 4e              ??         4Eh    N
        # 00203bcd 7f              ??         7Fh    
        # 00203bce d3              ??         D3h
        # 00203bcf c0              ??         C0h
        # 00203bd0 82              ??         82h
        # 00203bd1 e8              ??         E8h
        # 00203bd2 0d              ??         0Dh
        # 00203bd3 a3              ??         A3h
        # 00203bd4 33              ??         33h    3
        # 00203bd5 52              ??         52h    R
        # 00203bd6 ac              ??         ACh
        # 00203bd7 20              ??         20h     
        # 00203bd8 bd              ??         BDh
        
from randomgen.xoshiro256 import Xoshiro256
from numpy.random import Generator

DAT_00203b90 = [
    0xd2, 0x95, 0xc2, 0x70, 0xa4, 0x53, 0xd5, 0x4a, 0x3d, 0xc0, 0x9a, 0x3c, 0x62, 0x0d, 0xa7, 0x41, 0xea, 0x2a, 0x3c, 0x85, 0x73, 0xc6, 0xac, 0x47, 0xee, 0x87, 0x0d, 0x64, 0xb8, 0x5e, 0xa9, 0x5a, 0x0d, 0x47, 0x8d, 0x3b, 0x8a, 0x58, 0x8a, 0x00, 0x05, 0xda, 0x81, 0x44, 0xab, 0x2e, 0x96, 0x93, 0x6e, 0x43, 0x56, 0x1b, 0x9d, 0x51, 0x89, 0x60, 0x29, 0xae, 0x09, 0x54, 0x4e, 0x7f, 0xd3, 0xc0, 0x82, 0xe8, 0x0d, 0xa3, 0x33, 0x52, 0xac, 0x20, 0xbd
]

seed = 0x1a4

rand = Generator(Xoshiro256(seed))

print(rand.bit_generator.jump(0).state["s"])
print(hex(18442901823787151761))
print(hex(DAT_00203b90[0] ^ ord("C")))
# print(hex(DAT_00203b90[1] ^ ord("J")))
# print(hex(DAT_00203b90[2] ^ ord("2")))
# print(hex(DAT_00203b90[3] ^ ord("0")))
# print(hex(DAT_00203b90[4] ^ ord("2")))
# print(hex(DAT_00203b90[5] ^ ord("3")))
# print(hex(DAT_00203b90[6] ^ ord("{")))
# print(hex(DAT_00203b90[6] ^ ord("{")))
# print(chr(DAT_00203b90[7] ^ ord("t")))
