import struct
import sys


def add_char_to_map(cipher, character, index):
    entry = cipher[8 * character : 8 * (character + 1)]
    new_entry = [index, 0]

    if entry[0]:
        ptr = entry[0]
        while ptr[1]:
            ptr = ptr[1]
        ptr[1] = new_entry
    else:
        entry[0] = new_entry


def list_length(lst):
    length = 0
    if lst:
        length = 1
        ptr = lst
        while ptr[1]:
            ptr = ptr[1]
            length += 1
    return length


def serialize_and_output(cipher):
    output_file = sys.stdout.buffer

    for i in range(255):
        print(f"\n{i} ", end=" ")
        entry = cipher[8 * i : 8 * (i + 1)]
        length = list_length(entry[0])
        output_file.write(struct.pack("q", length))
        ptr = entry[0]
        while ptr:
            output_file.write(struct.pack("qq", ptr[0], ptr[1]))
            ptr = ptr[1]


def main():
    cipher = [[0, 0] for _ in range(256)]

    index = 0
    while True:
        character = sys.stdin.buffer.read(1)
        if not character:
            break
        add_char_to_map(cipher, character[0], index)
        index += 1

    print(cipher)
    serialize_and_output(cipher)


if __name__ == "__main__":
    main()
