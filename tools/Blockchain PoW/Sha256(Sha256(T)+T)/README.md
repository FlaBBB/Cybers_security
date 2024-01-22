# Calculate WoP Speed Comparison

Compare Ticket Calculation speed of WoP (Work of Proof).

$WoP = Sha256(Sha256(Ticket) + Ticket)$

## Test Environment

- **Operating System**: Windows 11 (WSL2 Ubuntu 22.04)
- **Processor**: AMD Athlon silver 3050U with Radeon Graphics 2.30 GHz
- **Memory**: 16 GB

- **Difficulty**: 7
- **Number Threads**: 2

## C Results

- **Code Version**: 1.0.0
- **Compiler Version**: 11.4.0 (Ubuntu 11.4.0-1ubuntu1~22.04)
- **Compile Flags**: -msse4.1 -msha -O3
- **Average Speed**: 11,008,056.00 H/s

## C++ Results

- **Code Version**: 1.0.0
- **Compiler Version**: 11.4.0 (Ubuntu 11.4.0-1ubuntu1~22.04)
- **Compile Flags**: -O3 -march=native -flto -lcryptopp
- **Average Speed**: 653,901.00 H/s 
</br>

- **Code Version**: 2.0.0
- **Compiler Version**: 11.4.0 (Ubuntu 11.4.0-1ubuntu1~22.04)
- **Compile Flags**: -O3 -march=native -flto -lssl -lcrypto
- **Average Speed**: 5,409,386.00 H/s

## Go Results

- **Code Version**: 1.0.0
- **Go Version**: go1.21.4 linux/amd64
- **Compile Flags**: -
- **Average Speed**: 2,427,995.58 H/s
</br>

- **Code Version**: 2.0.0
- **Go Version**: go1.21.4 linux/amd64
- **Compile Flags**: -
- **Average Speed**: 4,492,402.90 H/s

## Python Results

- **Code Version**: 1.0.0
- **Python Version**: 3.10.12
- **Compile Flags**: -
- **Average Speed**: 217,106.84 H/s