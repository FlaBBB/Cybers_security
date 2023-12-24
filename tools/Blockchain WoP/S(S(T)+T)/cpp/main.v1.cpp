#include <iostream>
#include <sstream>
#include <iomanip>
#include <thread>
#include <atomic>
#include <chrono>
#include <cryptopp/sha.h>
#include <cryptopp/filters.h>
#include <cryptopp/hex.h>
#include <cassert>

std::atomic<bool> found(false);
std::atomic<unsigned long long> total_count(0);
std::chrono::steady_clock::time_point start_time;

bool check_zero_padding(std::string digest, int difficulty) {
    for (int i = 0; i < difficulty / 2; i++) {
        if (((unsigned int)digest[i]) != 0) {
            return false;
        }
    }
    if (difficulty % 2 == 1) {
        return ((unsigned int) digest[difficulty / 2]) <= 0x0f;
    }
    return ((unsigned int) digest[difficulty / 2]) > 0x0f;
}

void worker(unsigned long long start, unsigned long long end, int difficulty, int id) {
    CryptoPP::SHA256 hash;
    std::string digest;

    for (unsigned long long i = start; i < end && !found; ++i) {
        std::stringstream m;
        m << i;

        digest.clear();
        CryptoPP::StringSource(m.str(), true, new CryptoPP::HashFilter(hash, new CryptoPP::StringSink(digest)));

        m.str("");
        m << digest << i;

        digest.clear();
        CryptoPP::StringSource(m.str(), true, new CryptoPP::HashFilter(hash, new CryptoPP::StringSink(digest)));

        if (check_zero_padding(digest, difficulty)) {
            std::cout << "\nThread " << id << " found the Ticket: " << i << std::endl;
            std::cout << "Average speed: " << static_cast<double>(total_count) / std::chrono::duration_cast<std::chrono::seconds>(std::chrono::steady_clock::now() - start_time).count() << " H/s" << std::endl;
            found = true;
        }

        ++total_count;
    }
}

void print_speed(unsigned long long range) {
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    unsigned long long last_count = total_count;

    while (!found) {
        std::chrono::steady_clock::time_point now = std::chrono::steady_clock::now();
        unsigned long long current_count = total_count;
        double speed = static_cast<double>(current_count - last_count) / std::chrono::duration_cast<std::chrono::seconds>(now - begin).count();
        double progress = static_cast<double>(current_count) / range * 100;
        std::cout << "\rProgress: " << current_count << "/" << range << "\t";
        std::cout << std::fixed << std::setprecision(2) << progress << "%\t";
        std::cout << "Total speed: " << speed << " H/s" << std::flush;
        begin = now;
        last_count = current_count;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

int main() {
    int difficulty;
    std::cout << "Difficulty: ";
    std::cin >> difficulty;

    assert(difficulty >= 1 && difficulty <= 32);

    srand((unsigned) time(NULL));
    unsigned long long x = 100000000 + rand() % 200000000000;
    unsigned long long range = 20000000000;
    int num_threads = std::thread::hardware_concurrency();
    std::cout << "Num Threads: " << num_threads << std::endl;

    start_time = std::chrono::steady_clock::now();
    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.push_back(std::thread(worker, x + i * range / num_threads, x + (i + 1) * range / num_threads, difficulty, i));
    }

    std::thread speed_thread(print_speed, range);

    for (auto& t : threads) {
        t.join();
    }

    speed_thread.join();

    return 0;
}
