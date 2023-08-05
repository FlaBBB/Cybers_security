cbc_cipher = bytes.fromhex("19705ef0a67b6368140ec9da440ace0230f99927fa3d05e11a92055509ee2df24fc8f41de018162c781cdd159a149f39")
ecb_plain  = bytes.fromhex("8e7a8f91646b23d5938713236e1b0ae27a022780d214185b776c96ef3169a5376fcdef17cb595ad02dcd247428cf0c8f")

plain = bytes([a ^ b for a, b in zip(cbc_cipher[:-16], ecb_plain[16:])])
    
print(plain)