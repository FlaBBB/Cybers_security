import numpy as np
from matplotlib import pyplot as plt
from pwn import remote

r = remote("13.201.224.182", 31816)

known_resps = ["You can't move there!", "Jumped over a wall!", "Moved!"]


def move(command: str):
    r.sendlineafter(b">", command.encode())
    resp = r.recvline().strip().decode()
    if resp not in known_resps:
        print("New response!")
        print(resp)
        r.interactive()
        exit()
    return "can't" not in resp


# 0 if can't do both
# 1 if moved only
# 2 if jumped
# 3 if moved THEN jumped
def move_or_jump(command: str):
    command = command.lower()
    can_move = move(command)
    a = 2 if can_jump else 0
    b = 0
    if not a:
        can_jump = move(command.upper())
        b = 1 if can_move else 0
    return a | b


def init():
    # going to upper left
    res = 3
    print("Going up")
    while res != 0:
        res = move_or_jump("w")
    res = 3
    print("Going left")
    while res != 0:
        res = move_or_jump("a")


print("Initializing")
init()
print("Done")
# draw the maze
maze = []
# start scanning left to right
to_right = True
go_down = True
try:
    while go_down:
        row = [False]
        # scan right
        hori_res = 3
        print(
            f"Starting to traverse row {len(maze) + 1}, going {'right' if to_right else 'left'}"
        )
        while hori_res != 0:
            command = "d" if to_right else "a"
            hori_res = move_or_jump(command)
            if hori_res == 1:
                row.extend([False])
            elif hori_res == 2:
                row.extend([True, False])
            elif hori_res == 3:
                row.extend([False, True, False])
        # store result
        if not to_right:
            row = row[::-1]
        maze.append(row)

        print(f"Row {len(maze)} finished with length {len(row)}!")
        # next iter
        to_right = not to_right
        go_down = move("s")

finally:
    max_len = 0
    for arr in maze:
        max_len = max(len(arr), max_len)

    norm_maze = []
    # maze length can be inconsistent, so we normalize
    for arr in maze:
        norm_maze.append(arr + [True for _ in range(max_len - len(arr))])
    binary = np.array(norm_maze)
    plt.imshow(binary)
    plt.show()
