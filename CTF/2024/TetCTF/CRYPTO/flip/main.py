# Please ensure that you solved the challenge properly at the local.
# If things do not run smoothly, you generally won't be allowed to make another attempt.
import os
import subprocess
import sys
import tempfile

# from secret.network_util import ban_client, check_client

OFFSET_PLAINTEXT = 0x4010
OFFSET_KEY = 0x4020

replacement = 0x11be + 3


def main():
    # if not check_client():
    #     return

    key = os.urandom(16)
    with open("encrypt", "rb") as f:
        content = bytearray(f.read())

    print(content[replacement : replacement + 16])

    # input format: hex(plaintext) i j
    try:
        # plaintext_hex, i_str, j_str = input().split()
        plaintext_hex, i_str, j_str = "00" * 16, f"{replacement}", "4"
        pt = bytes.fromhex(plaintext_hex)
        assert len(pt) == 16
        i = int(i_str)
        assert 0 <= i < len(content)
        j = int(j_str)
        assert 0 <= j < 8
    except Exception as err:
        print(err, file=sys.stderr)
        # ban_client()
        return

    # update key, plaintext, and inject the fault
    content[OFFSET_KEY : OFFSET_KEY + 16] = key
    content[OFFSET_PLAINTEXT : OFFSET_PLAINTEXT + 16] = pt
    content[i] ^= 1 << j

    # tmpfile = tempfile.NamedTemporaryFile(delete=True)
    with open("generated", "wb") as f:
        f.write(content)
    # os.chmod(tmpfile.name, 0o775)
    # tmpfile.file.close()

    # # execute the modified binary
    # try:
    #     ciphertext = subprocess.check_output(tmpfile.name, timeout=1.0)
    #     print(ciphertext.hex())
    # except Exception as err:
    #     print(err, file=sys.stderr)
    #     # ban_client()
    #     return

    # # please guess the AES key
    # if bytes.fromhex(input()) == key:
    #     with open("secret/flag.txt") as f:
    #         print(f.read())
    #     from datetime import datetime

    #     print(datetime.now(), plaintext_hex, i, j, file=sys.stderr)


main()
