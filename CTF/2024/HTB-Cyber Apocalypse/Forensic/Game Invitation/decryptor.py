def xor(given_string, length):
    xor_key = 45
    for i in range(length):
        given_string[i] ^= xor_key
        xor_key = (xor_key ^ 99) ^ (i % 254)
    return given_string


def decryptor(input_filename, output_filename):
    with open(input_filename, "rb") as f:
        filename_content = bytearray(f.read())
        filename_content = filename_content.decode("utf-8", "ignore")
        if (
            "sWcDWp36x5oIe2hJGnRy1iC92AcdQgO8RLioVZWlhCKJXHRSqO450AiqLZyLFeXYilCtorg0p3RdaoPa"
            not in filename_content
        ):
            return
        idx = filename_content.rfind(
            "sWcDWp36x5oIe2hJGnRy1iC92AcdQgO8RLioVZWlhCKJXHRSqO450AiqLZyLFeXYilCtorg0p3RdaoPa"
        )
        print(idx)

        res_file_len = 13082
        f.seek(idx + 81)
        res_file = f.read(res_file_len)
        res_file = xor(res_file, res_file_len)

    with open(output_filename, "wb") as f:
        f.write(res_file)


decryptor("invitation.docm", "malware.js")
