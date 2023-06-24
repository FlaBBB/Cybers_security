"""
just learned python and i can't
find builtin hashing functions -
so, i tried to make one myself.
not sure whether it is a hashing
or not because it produces diff-
erent length for different inpu-
ts. but, who cares?
"""


def my_hash_function(c):
    chunks = [c[i:i + 2] for i in range(0, len(c), 2)]
    rv = [hex(len(c))[2:]]
    for ck in chunks:
        if len(ck) < 2:
            rv.append(hex(ck[0]**2)[2:])
            break
        rv.append(hex((ck[0]**3 - ck[1]**3) * ck[1])[2:])
    return 'g'.join(rv)


flag_hash = ('1dg0gx1acf64ga8d80ga8d80g63082b6g2b76d77gx1fe00e6g169b0fcg78c092gx3ab29dcgx347d21g1767ba7g1080168gx24090e8g3d09')

# if __name__ == '__main__' \
#         and my_hash_function(input('Validate your Flag = ').encode()) == flag_hash:
#     print('congrats!')

print(my_hash_function("Ca)EW(JG2i0msBe2ig20W)Ge9j023gmke)".encode()))