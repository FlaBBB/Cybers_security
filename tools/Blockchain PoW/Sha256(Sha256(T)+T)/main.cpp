#include <iostream>
#include <ctime>
#include <chrono>
#include <cmath>
#include <random>
#include <string>
#include <thread>
#include <mutex>
#include <map>
#include <set>
#include <stack>
#include <iomanip>
#include <openssl/evp.h>
#include <openssl/sha.h>
#include <cstring>
#include <fstream>

#ifndef _WIN32
#include <ncurses.h>
#endif

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

size_t checkZeroPadding(unsigned char* sha) {
    size_t difficulty = 0;
    size_t cur_byte = 0;
    while (cur_byte < 32) {
        if (sha[cur_byte] != 0) {
            break;
        }
        difficulty += 2;
        cur_byte++;
    }

    if (sha[cur_byte] < 0x0F) {
        difficulty += 1;
    }

    return difficulty;
}

int main(int argc, char* argv[]) { // Number of zero before
    size_t threads_n = 2; // Concurrent threads
    int duration = std::stoi(argv[1]); // Duration of the program in seconds
    std::string filename = "result.txt"; // Name of the result file

    std::ofstream result_file(filename);
    if (!result_file.is_open()) { // Check if the file is open
        std::cerr << "Error opening result file." << std::endl;
        return 1;
    }
    result_file.close();

    srand((unsigned) time(NULL)); // Seed for random
    uint64_t ticket = 100000000 + rand() % 200000000000; // Initial ticket is equal to zero

    bool stop = false; // This is set by a thread if a correct a has been stop
    std::map<size_t, std::set<uint64_t>> result_tickets = std::map<size_t, std::set<uint64_t>>(); // The final ticket
    
    std::mutex result_mutex;
    std::mutex ticket_mutex;
    std::mutex stop_mutex;

#ifdef _WIN32
    std::thread** threads = reinterpret_cast<std::thread**>(malloc(threads_n * sizeof(std::thread*)));
#else
    std::thread** threads = reinterpret_cast<std::thread**>(malloc((threads_n + 1) * sizeof(std::thread*)));
#endif
    for (size_t i = 0; i < threads_n; ++i) {
        threads[i] = new std::thread([&ticket_mutex, &ticket, &stop_mutex, &stop, &result_mutex, &result_tickets]() {
            uint64_t thread_ticket = 0;
            int ticket_size = 0;
            char *ticket_str = reinterpret_cast<char*>(malloc(32));
            bool break_for = false;
            
            for (;;) {
                ticket_mutex.lock();
                if (stop) break_for = true;
                thread_ticket = ticket;
                ticket++;
                ticket_mutex.unlock();
                if (break_for) break;

                size_t size = int_to_str(thread_ticket, ticket_str);

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

                // Check if the hash is correct with the difficulty
                size_t cur_difficulty = checkZeroPadding(sha);
                if (cur_difficulty != 0) {
                    result_mutex.lock();
                    if (result_tickets.find(cur_difficulty) == result_tickets.end()) {
                        result_tickets[cur_difficulty] = std::set<uint64_t>();
                    }
                    if (result_tickets[cur_difficulty].size() < 10)
                    {
                        result_tickets[cur_difficulty].insert(thread_ticket);
                    }
                    result_mutex.unlock();
                }

                // free the allocated memory, avoid memory leaking.
                free(sha);
            }

            free(ticket_str);
        });
    }

#ifndef _WIN32
    bool show_remaining = false;
    std::mutex remaining_mutex;

    initscr(); // Start curses mode
    raw(); // Line buffering disabled
    keypad(stdscr, TRUE); // We get F1, F2 etc..
    noecho(); // Don't echo() while we do getch
    cbreak(); // Don't generate signals on ^C, ^Z

    threads[threads_n] = new std::thread([&remaining_mutex, &show_remaining]() {
        for (;;)
        {
            if (getch() == '\n'){
                remaining_mutex.lock();
                show_remaining = true;  
                remaining_mutex.unlock();
            }
        }
    });
#endif

    std::chrono::high_resolution_clock::time_point t_start = std::chrono::high_resolution_clock::now();

    for (;;) {
        std::chrono::high_resolution_clock::time_point t_current = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> time_span = t_current - t_start;

#ifndef _WIN32
        remaining_mutex.lock();
        if (show_remaining && time_span.count() > 2)
        {
            std::cout << "\r" << std::setw(60) << std::setfill(' ') << "";
            std::cout << "\rRemaining time: " << duration - time_span.count() << "s" << std::flush;
            show_remaining = false;
        }
        remaining_mutex.unlock();
#endif

        bool break_for = false;

        if (time_span.count() > duration) {
            std::cout << "Stopping..." << std::endl;
            stop_mutex.lock();
            stop = true;
            stop_mutex.unlock();

            result_file.open(filename, std::ios::trunc);
            result_mutex.lock();
            for (auto it = result_tickets.begin(); it != result_tickets.end(); ++it) {
                result_file << it->first << ":";
                for (auto it2 = it->second.begin(); it2 != it->second.end(); ++it2) {
                    result_file << " " << *it2;
                }
                result_file << std::endl;
            }
            result_mutex.unlock();

            // close the opened file.
            result_file.close();

            // free the allocated memory
#ifdef _WIN32
            for (size_t i = 0; i < threads_n; ++i)
#else
            for (size_t i = 0; i < (threads_n + 1); ++i)
#endif
            {
                free(threads[i]);
            }
            free(threads);

            // break the main loop.
            break_for = true;
        }
        if (break_for) break;

        using namespace std::chrono_literals;
        std::this_thread::sleep_for(1s);
    }
#ifndef _WIN32
    endwin();
#endif

    EVP_cleanup();

    return 0;
}