/* this is implementation for calculation PoW Sha256(Sha256(ticket) + ticket) */
/* that using sha-intrinsics https://github.com/noloader/SHA-Intrinsics */

/* gcc -DTEST_MAIN -msse4.1 -msha -O3 main.c -o main */

#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/time.h>
#include <signal.h>
#include "sha256.h"

#define NUM_THREADS 2  // Change this to the desired number of threads

struct ThreadData {
    unsigned int id;  // Thread ID
    struct init_sha256_state state;
    unsigned long long start;
    unsigned long long end;
    unsigned long long hashes;  // Number of hashes processed by the thread
    unsigned int difficulty;
    volatile int* stopFlag;     // Pointer to the shared stop flag
};

void handleSignal(int sig) {
    if (sig == SIGINT) {
        printf("Received SIGINT. Stopping all threads.\n");
        exit(0);
    }
}

void* workerThread(void* arg) {
    struct ThreadData* threadData = (struct ThreadData*)arg;
    unsigned long long nonce = threadData->start;

    uint8_t hash[32];
    uint8_t ticket[64];

    // ticket = nonce (big-endian)
    // Convert an unsigned integer to a big-endian byte array with range 48(0) - 57(9)
    unsigned int idx = 0;
    while (threadData->start > 0)
    {
        ticket[idx] = (threadData->start % 10) + 48;
        threadData->start /= 10;
        idx++;
    }
    unsigned int ticket_size = idx; // ticket size

    do {
        // Check the stop flag
        if (*(threadData->stopFlag) != 0) {
            return NULL;
        }
        
        // 1. sha256(ticket)
        init_sha256(&threadData->state);
        update_sha256(&threadData->state, ticket, ticket_size);
        finish_sha256(&threadData->state, hash);

        // 2. sha256(sha256(ticket) + ticket)
        init_sha256(&threadData->state);
        update_sha256(&threadData->state, hash, 32);
        update_sha256(&threadData->state, ticket, ticket_size);
        finish_sha256(&threadData->state, hash);

        // 3. check difficulty
        for (idx = 0; idx < threadData->difficulty / 2; idx++) {
            if (hash[idx] != 0) {
                goto ncorrect;
            }
        }
        if (threadData->difficulty % 2 == 1) {
            if (hash[idx] >= 0x10) {
                goto ncorrect;
            }
        }

        printf("Thread %u Ticket: %s\n", threadData->id, (char*)ticket);
        for (int i = 0; i < 32; i++) {
            printf("%02x", hash[i]);
        }
        printf("\n");

        // Signal all threads to stop
        *(threadData->stopFlag) = 1;
        return NULL;

ncorrect:

        // Increment the number of hashes processed by the thread
        threadData->hashes++;

        // increment nonce and update message
        nonce++;
        idx = 0;
        for (;;){
            if (idx == ticket_size) {
                ticket[idx] = 48;
                ticket_size++;
                break;
            }
            ticket[idx] += 1;
            if (ticket[idx] == 58) {
                ticket[idx] = 48;
                idx++;
                continue;
            }
            break;
        }
        
    } while (nonce < threadData->end);
    

    return NULL;
}

unsigned long long getCurrentTimeInMilliseconds() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (unsigned long long)tv.tv_sec * 1000 + (unsigned long long)tv.tv_usec / 1000;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <difficulty>\n", argv[0]);
        return 1;
    }

    unsigned int difficulty = 0;
    sscanf(argv[1], "%u", &difficulty);
    printf("Difficulty: %u\n", difficulty);

    // set
    srand(time(NULL));
    unsigned long long start = 100000000 + rand() % 200000000000;
    unsigned long long range = 20000000000 / NUM_THREADS;

    // Set up signal handler
    signal(SIGINT, handleSignal);

    // Set up thread data
    pthread_t threads[NUM_THREADS];
    struct ThreadData threadData[NUM_THREADS];

    // Set up stop flag
    int stopFlag = 0;

    for (int i = 0; i < NUM_THREADS; i++) {
        threadData[i].id = i;   
        threadData[i].start = start + (i * range);  // Start each thread with a different nonce
        threadData[i].end = start + ((i + 1) * range);
        threadData[i].difficulty = difficulty;
        threadData[i].hashes = 0;
        threadData[i].stopFlag = &stopFlag;
    }

    unsigned long long startTime = getCurrentTimeInMilliseconds();

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, workerThread, &threadData[i]);
    }

    // Wait for threads to finish
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    unsigned long long endTime = getCurrentTimeInMilliseconds();
    unsigned long long totalTime = endTime - startTime;
    unsigned long long totalHashes = 0;

    // Calculate total hashes processed by all threads
    for (int i = 0; i < NUM_THREADS; i++) {
        totalHashes += threadData[i].hashes;
    }

    // Display results
    printf("\n=== statistics ===\nTotal Hashes: %llu\n", totalHashes);
    printf("Total Time: %llu ms\n", totalTime);
    printf("Hashing Speed: %llu H/s\n", totalHashes * 1000 / totalTime);

    return 0;
}