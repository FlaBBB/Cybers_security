#include <iostream>
#include <ctime>
#include <chrono>
#include <cmath>
#include <random>
#include <string>
#include <thread>
#include <mutex>
#include <map>
#include <stack>
#include <iomanip>
#include <openssl/evp.h>
#include <openssl/sha.h>
#include <cstring>

// Prints a 32 bytes sha256 to the hexadecimal form filled with zeroes
void print_hex(const unsigned char* inp, size_t size) {
    for (size_t i = 0; i < size; ++i) {
        std::cout << std::hex << std::setfill('0') << std::setw(2) << static_cast<int>(inp[i]);
    }
    std::cout << std::dec << std::endl;
}

size_t int_to_str(uint64_t inp, char* out) {
    uint64_t result = inp;
    uint8_t remainder;
    size_t inp_size = inp == 0 ? 1 : floor(log10(inp)) + 1;
    size_t i = inp_size;
    while (result >= 10) {
        remainder = result % 10;
        result /= 10;
        out[--i] = remainder + '0';
    }

    out[0] = result + '0';
    out[inp_size] = 0;
    return inp_size;
}

bool checkZeroPadding(unsigned char* sha, size_t difficulty) {

    for (size_t cur_byte = 0; cur_byte < difficulty / 2; ++cur_byte) {
        if (sha[cur_byte] != 0) {
            return false;
        }
    }

    bool isOdd = difficulty % 2 != 0;
    size_t last_byte_check = static_cast<size_t>(difficulty / 2);
    if (isOdd) {
        if (sha[last_byte_check] > 0x0F || sha[last_byte_check] == 0) {
            return false;
        }
    }
    else if (sha[last_byte_check] < 0x0F) return false;

    return true;
}

int main() {
    unsigned difficulty = 1; // Number of zero before
    size_t threads_n = 2; // Concurrent threads
    srand((unsigned) time(NULL));
    uint64_t ticket = 100000000 + rand() % 200000000000; // Initial ticket is equal to zero
    uint64_t range = 20000000000;

    uint64_t calculated_hashes = 0; // Total number of hashes calculated in the program

    std::cout << "Difficulty : ";
    std::cin >> difficulty;
    std::cout << std::endl;

    
    bool found = false; // This is set by a thread if a correct a has been found
    unsigned char* found_hash = reinterpret_cast<unsigned char*>(malloc(32)); // The final hash
    uint64_t found_ticket = 0; // The final ticket
    
    std::mutex nonce_mutex;
    std::mutex found_mutex;
    std::mutex calculated_hashes_mutex;
        
    std::thread** threads = reinterpret_cast<std::thread**>(malloc(threads_n * sizeof(std::thread*)));
    for (size_t i = 0; i < threads_n; ++i) {
        threads[i] = new std::thread([&nonce_mutex, &ticket, &range, &calculated_hashes_mutex, &calculated_hashes, &found_mutex, &found, &difficulty, found_hash, &found_ticket]() {
            uint64_t thread_nonce = 0;
            int ticket_size = 0;
            char *ticket_str = reinterpret_cast<char*>(malloc(32));
            bool break_for = false;
            
            for (;calculated_hashes < range;) {
                nonce_mutex.lock();
                if (found) break_for = true;
                thread_nonce = ticket;
                ticket++;
                nonce_mutex.unlock();
                if (break_for) break;

                size_t size = int_to_str(thread_nonce, ticket_str);

                // Calculate the hash Sha256(Sha256(ticket) + ticket)
                unsigned char* sha = reinterpret_cast<unsigned char*>(malloc(32));
                SHA256_CTX sha256;

                // First hash: res = Sha256(ticket)
                SHA256_Init(&sha256);
                SHA256_Update(&sha256, ticket_str, size);
                SHA256_Final(sha, &sha256);

                // Second hash: res = Sha256(res + ticket)
                SHA256_Init(&sha256);
                SHA256_Update(&sha256, sha, 32);
                SHA256_Update(&sha256, ticket_str, size);
                SHA256_Final(sha, &sha256);

                // Increment gloal hashes count
                calculated_hashes_mutex.lock();
                calculated_hashes++;
                calculated_hashes_mutex.unlock();

                // Check if the hash is correct with the difficulty
                if (checkZeroPadding(sha, difficulty)) {
                    found_mutex.lock();
                    found_ticket = thread_nonce;
                    memcpy(found_hash, sha, 32);
                    found = true;
                    found_mutex.unlock();
                    break;
                }

                free(sha);
            }

            free(ticket_str);
        });
    }

    std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();
    std::chrono::high_resolution_clock::time_point t_last_updated = std::chrono::high_resolution_clock::now();

    for (;;) {
        std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();

        std::chrono::duration<double, std::milli> last_show_interval = t2 - t_last_updated;
        if (last_show_interval.count() > 2000) {
            t_last_updated = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double, std::milli> span = t2 - t1;
            float ratio = span.count() / 1000;

            calculated_hashes_mutex.lock();
            std::cout << std::fixed << "Progress: " << static_cast<int>(calculated_hashes) << "/" << range << "\t";
            std::cout << std::fixed << std::setprecision(2) << static_cast<double>(calculated_hashes) / range * 100 << "%\t";
            std::cout << std::fixed << static_cast<int>(calculated_hashes / ratio) << " hash(es)/s" << std::endl;
            calculated_hashes_mutex.unlock();

            bool break_for = false;

            found_mutex.lock();
            if (found) {
                std::cout << "\n[#] hash found --" << std::endl;
                std::cout << "Ticket: " << std::to_string(found_ticket) << std::endl;
                calculated_hashes_mutex.lock();
                std::cout << "Average: " << static_cast<double>(calculated_hashes) / ratio << " H/s" << std::endl;
                calculated_hashes_mutex.unlock();
                std::cout << "Hash: "; print_hex(found_hash, 32);
                for (size_t i = 0; i < threads_n; ++i) {
                    free(threads[i]);
                }
                free(threads);
                break_for = true;
            }
            found_mutex.unlock();
            if (break_for) break;

        }

        using namespace std::chrono_literals;
        std::this_thread::sleep_for(1s);
    }

    EVP_cleanup();

    return 0;
}