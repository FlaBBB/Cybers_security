import hashlib
import random
import threading
import time

found = False
total_count = 0
start_time = time.time()


def check_zero_padding(digest, difficulty):
    for i in range(difficulty // 2):
        if digest[i] != 0:
            return False
    if difficulty % 2 == 1:
        return digest[difficulty // 2] <= 0x0F
    return digest[difficulty // 2] > 0x0F


def worker(start, end, difficulty, id):
    global found
    global total_count

    for i in range(start, end):
        if found:
            break

        m = hashlib.sha256()
        m.update(str(i).encode("utf-8"))
        digest = m.digest()

        m = hashlib.sha256()
        m.update(digest + str(i).encode("utf-8"))
        digest = m.digest()

        if check_zero_padding(digest, difficulty):
            print(f"\nThread {id} found the Ticket: {i}")
            print(
                f"Average speed: {(total_count / (time.time() - start_time)):.2f} H/s"
            )
            found = True

        total_count += 1


def print_speed(range_):
    global found
    global total_count

    begin = time.time()
    last_count = total_count

    while not found:
        now = time.time()
        current_count = total_count
        speed = (current_count - last_count) / (now - begin)
        progress = (current_count / range_) * 100
        print(
            f"\rProgress: {current_count}/{range_}\t{progress:.2f}%\tTotal speed: {speed:.2f} H/s",
            end="",
        )
        begin = now
        last_count = current_count
        time.sleep(1)


def main():
    difficulty = int(input("Difficulty: "))
    assert 1 <= difficulty <= 32

    x = 100000000 + random.randint(0, 200000000000)
    range_ = 20000000000
    num_threads = threading.active_count()
    print(f"Num Threads: {num_threads}")

    threads = []
    for i in range(num_threads):
        t = threading.Thread(
            target=worker,
            args=(
                x + i * range_ // num_threads,
                x + (i + 1) * range_ // num_threads,
                difficulty,
                i,
            ),
        )
        t.start()
        threads.append(t)

    speed_thread = threading.Thread(target=print_speed, args=(range_,))
    speed_thread.start()

    for t in threads:
        t.join()

    speed_thread.join()


if __name__ == "__main__":
    main()
