import os

import gdb

# Create a temporary file to provide input
input_file = "input.txt"

# Set up GDB commands
gdb.execute("file ./main")
gdb.execute("set environment LD_PRELOAD ./bypass.so")
gdb.execute("break *main+663")
gdb.execute("break *main+687")


def print_gdb_output(x):
    return gdb.execute(f"print {x}", to_string=True).split("= ")[1].strip()


flag = ["`" for _ in range(40)]
n = 0
is_break = False
while True:
    with open(input_file, "w") as f:
        f.write("".join(flag))
    # Execute GDB with input from the temporary file
    gdb.execute(f"r < {input_file}")

    # Skip through previous breakpoints
    gdb.execute("set logging off")
    for _ in range(n):
        gdb.execute("c")
        assert int(print_gdb_output("$rax")) == int(
            print_gdb_output("$rdx")
        ), f"Error, got {hex(int(print_gdb_output('$rax')))} and {hex(int(print_gdb_output('$rdx')))}"
        out = gdb.execute("c", to_string=True)
        if "Correct" in out:
            is_break = True
            break

    if is_break:
        break

    gdb.execute("set logging on")

    # Extract the value from memory and perform operations
    try:
        offset = int(print_gdb_output("$rax"))
    except:
        break
    print(f"offset = {offset}")
    gdb.execute("c")

    try:
        e = int(print_gdb_output("$rax"))
    except:
        break
    e = e ^ 0x1337

    # Check if the value is valid
    if (e // 16) * 16 != e:
        break

    # Append the character to the flag
    flag[offset] = chr(e // 16)
    print(f"flag = '" + "".join(flag) + "'")
    gdb.execute("c")
    n += 1

# Print the flag
print("flag =", "".join(flag).strip("`"))

# Clean up the temporary file
os.remove(input_file)
