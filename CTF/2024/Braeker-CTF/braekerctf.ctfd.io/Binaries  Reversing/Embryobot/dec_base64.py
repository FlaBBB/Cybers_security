from base64 import b64decode

c = b"f0VMRgEBAbADWTDJshLNgAIAAwABAAAAI4AECCwAAAAAAADo3////zQAIAABAAAAAAAAAACABAgAgAQITAAAAEwAAAAHAAAAABAAAA=="

with open("embryobot.bin", "wb") as f:
    f.write(b64decode(c))