from itertools import product
from typing import Dict, List

from pwn import *


class Node:
    def __init__(self, value):
        self.value: str = value
        self.parent: List[NodeParent] = []

    def __repr__(self):
        return f"<Node {self.value}>"

    def delete(self):
        for p in self.parent:
            p.remove(self)
            if len(p.child_node) == 0:
                p.delete()

        del self


class NodeParent:
    def __init__(self, parent: Node, value: str):
        self.parent: Dict[str, NodeParent] = parent
        self.value: str = value
        self.child_node: List[Node] = []

    def delete(self):
        self.parent.pop(self.value)
        del self

    def remove(self, node: Node):
        self.child_node.remove(node)

    def append(self, node: Node):
        self.child_node.append(node)

    def pop(self, idx=-1):
        return self.child_node.pop(idx)


class GenText:
    def __init__(self, dictionary, length):
        self.dictionary = dictionary
        self.length = length
        self.l: List[Dict[str, NodeParent]] = [dict() for _ in range(length - 1)]
        for text in product(dictionary, repeat=length):
            text = "".join(text)
            node = Node(text)
            for i in range(length - 1):
                d = self.l[i]
                t = text[: i + 1]
                if d.get(t, None) is None:
                    d[t] = NodeParent(d, t)
                node.parent.append(d[t])
                d[t].append(node)
        self.num_l = len(dictionary) ** length

        self.text = dictionary[0] * (length - 1)
        self.counter = 3

    def get_char_candidate(self):
        for i in range(self.length - 1, 0, -1):
            d = self.l[i - 1]
            text = self.text[-i:]
            if d.get(text, None) is not None:
                node = d[text].child_node[0]
                res = node.value[i:]
                node.delete()
                self.counter += len(res)
                self.num_l -= 1
                return res
        exit(-1)

    def gen(self, send_per=16):
        while self.num_l > 0:
            self.text += self.get_char_candidate()

            if self.counter >= send_per or self.num_l == 0:
                yield self.text[-self.counter :]
                self.counter = 0

    def get_all(self):
        while self.num_l > 0:
            self.text += self.get_char_candidate()
        return self.text


# nc accessible-sesasum-indicum.chal.irisc.tf 10104
HOST = "accessible-sesasum-indicum.chal.irisc.tf"
PORT = 10104

io = remote(HOST, PORT)

dictionary = "0123456789abcdef"
length = 4

t = GenText(dictionary, length).get_all().encode()
print(t)

for i in range(16):
    io.recvuntil(b"Attempt>")
    # print()
    io.sendline(t)
    recv = b""
    while recv == b"":
        recv = io.recv(27).strip()
    assert b"Attempt>" not in recv
    print(recv)
    print(f"vault {i + 1} break")

io.interactive()
