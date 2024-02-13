from typing import List, Tuple


class Paper:
    decoder_board: List[Tuple[int, int]] = [
        (0, 0),
        (2, 1),
        (5, 0),
        (7, 1),
        (10, 0),
        (12, 1),
        (15, 0),
        (17, 1),
        (0, 10),
        (3, 9),
        (6, 10),
        (9, 9),
        (11, 10),
        (14, 9),
        (17, 10),
    ]
    max_x = 17
    max_y = 10

    def __init__(self, metrix: List[List[str]]):
        assert (
            len(metrix) >= Paper.max_y + 1 and len(metrix[0]) >= Paper.max_x + 1
        ), "Invalid metrix size"
        self.metrix = metrix
        self.size_x_metrix = len(metrix[0])
        self.size_y_metrix = len(metrix)
        for y in range(self.size_y_metrix):
            assert (
                len(metrix[y]) == self.size_x_metrix
            ), "All lines must have the same length"

    @staticmethod
    def fromString(string: str) -> "Paper":
        metrix = []
        for line in string.split("\n"):
            metrix.append(list(line))
        return Paper(metrix)

    def decodeMessage(self, x: int, y: int) -> str:
        assert (
            0 <= x < self.size_x_metrix and 0 <= y < self.size_y_metrix
        ), "Invalid x or y"
        assert (
            x + self.max_x < self.size_x_metrix and y + self.max_y < self.size_y_metrix
        ), "Invalid x or y"
        message = ""
        for board_x, board_y in Paper.decoder_board:
            message += self.metrix[y + board_y][x + board_x]
        return message

    def searchAllDecodedMessage(
        self, search_msg: str
    ) -> List[Tuple[Tuple[int, int], str]]:
        all_messages = []
        for y in range(self.size_y_metrix - self.max_y - 1):
            if search_msg[0] not in self.metrix[y][: -(self.max_x + 1)]:
                continue
            x = self.metrix[y][: -(self.max_x + 1)].index(search_msg[0])
            msg = self.decodeMessage(x, y)
            if search_msg in msg:
                all_messages.append(((x, y), msg))
        return all_messages

    def getAllDecodedMessage(self) -> List[str]:
        all_messages = []
        for y in range(self.size_y_metrix - self.max_y - 1):
            for x in range(self.size_x_metrix - self.max_x - 1):
                msg = self.decodeMessage(x, y)
                all_messages.append(msg)
        return all_messages


note = open("note.txt").read()
p = Paper.fromString(note)
print(p.getAllDecodedMessage())
