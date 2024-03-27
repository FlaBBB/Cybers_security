import os

from aes import AES

# A function that does nothing
no_op = lambda *x: None


def main():
    k = os.urandom(16)
    c = AES(k)
    s = b"".join(k[i : i + 1] * 4 for i in range(16))

    flag = os.environ.get(
        "FLAG", "LKS2024Malang{***********************MISSING*************************}"
    ).encode()
    assert len(flag) == 64

    flag = b"".join([c.encrypt(flag[i : i + 16]) for i in range(0, 64, 16)])
    print(f"Here is encrypted flag: {flag.hex()}.")

    opts = ["sb", "sr", "mc", "ark"]
    sopts = ["data", "secret"]

    for _ in range(128):
        [opt, suboption, *more] = input("> ").split(" ")
        if opt not in opts:
            raise Exception("invalid option!")
        if suboption not in sopts:
            raise Exception("invalid suboption!")

        if suboption == "secret":
            opts.remove(opt)
            msg = s
        else:
            msg = bytes.fromhex(more[0])
            if len(msg) != 16:
                raise Exception("invalid length!")
            msg = msg * 4

        if opt == "sb":
            c = AES(k)
            c._sub_bytes = no_op
            ct = c.encrypt(msg[0:16])

        elif opt == "sr":
            c = AES(k)
            c._shift_rows = no_op
            ct = c.encrypt(msg[16:32])

        elif opt == "mc":
            c = AES(k)
            c._mix_columns = no_op
            ct = c.encrypt(msg[32:48])

        elif opt == "ark":
            c = AES(k)
            c._add_round_key = no_op
            ct = c.encrypt(msg[48:64])

        print(ct.hex())


if __name__ == "__main__":
    main()
