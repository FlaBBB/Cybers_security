import types
from random import randint


class Riddler:

    max_int: int
    min_int: int
    co_code_start: bytes
    co_code_end: bytes
    num_list: list[int]

    def __init__(self) -> None:
        self.max_int = 1000
        self.min_int = -1000
        self.co_code_start = b"d\x01}\x01d\x02}\x02"
        self.co_code_end = b"|\x01|\x02f\x02S\x00"
        self.num_list = [randint(self.min_int, self.max_int) for _ in range(10)]

    def ask_riddle(self) -> str:
        return """ 'In arrays deep, where numbers sprawl,
        I lurk unseen, both short and tall.
        Seek me out, in ranks I stand,
        The lowest low, the highest grand.
        
        What am i?'
        """

    def check_answer(self, answer: bytes) -> bool:
        _answer_func: types.FunctionType = types.FunctionType(
            self._construct_answer(answer), {}
        )
        return _answer_func(self.num_list) == (min(self.num_list), max(self.num_list))

    def _construct_answer(self, answer: bytes) -> types.CodeType:
        co_code: bytearray = bytearray(self.co_code_start)
        co_code.extend(answer)
        co_code.extend(self.co_code_end)

        code_obj: types.CodeType = types.CodeType(
            1,
            0,
            0,
            4,
            3,
            3,
            bytes(co_code),
            (None, self.max_int, self.min_int),
            (),
            ("num_list", "min", "max", "num"),
            __file__,
            "_answer_func",
            "_answer_func",
            1,
            b"",
            b"",
            (),
            (),
        )
        return code_obj


def format_answer(answer: str) -> bytearray:
    try:
        return bytes([int(b) for b in answer.strip().split(",")])
    except Exception:
        raise Exception(
            "\nFormat should be like: int_value1,int_value2,int_value3...\nExample answer: 1, 25, 121...\n"
        )


riddler = Riddler()
payload = b"|\x00D\x00]\x12}\x03|\x03|\x01k\x00\x00\x00\x00\x00r\x02|\x03}\x01|\x03|\x02k\x04\x00\x00\x00\x00r\x02|\x03}\x02\x8c\x13"
print(types.FunctionType(riddler._construct_answer(payload), {})(riddler.num_list))
# payload = "124,0,68,0,93,17,0,0,125,3,124,3,124,1,107,2,0,0,114,2,124,3,125,1,124,3,124,2,107,68,0,0,115,1,140,16,124,3,125,2,140,19,4,0"
# print(riddler.check_answer(format_answer(payload)))
