# import string

# def generator():
#     for i in range(100):
#         yield i

# print({}.setdefault)
# f = open("flag.txt", "r")
# dic = {"a":1}

# print([p:=[a:=[],a.append(b.gi_frame.f_back for b in a),*a[0]][2], p.f_globals[p.f_code.co_filename[-8]]][1].read())
# print([a:=[],a.append(b.gi_frame.f_back for b in a),*a[0]])


# exp = "[p:=[a:=[],a.append(b.gi_frame.f_back.f_globals for b in a),*a[0]][2], list(p.values())][1][-4]"
# if any([c not in string.printable for c in exp]) or any([c in exp for c in ["__", "'", "\""]]) or len(exp) > 120:
#     print("admin I'm sorry, I'm afraid I can't let you do that!")
# else :
#     print(eval(exp, {'__builtins__': None}, {'__builtins__': None}))

import dis

def regenerate():
    a = []
    a.append(b.gi_frame.f_back.f_back for b in a)
    # for b in a:
    #     a.append(b.gi_frame.f_back)
    return [*a[0]][0]

print(regenerate().f_locals)