import dis

with open("byteme.pyc", "rb") as f:
    code = f.read()

dis.dis(code)
