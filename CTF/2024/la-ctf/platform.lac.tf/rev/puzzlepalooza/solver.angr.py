from itertools import chain

import angr
import claripy

flaglen = 54
p = angr.Project("./puzzlepalooza", main_opts={"base_addr": 0})
flag = claripy.BVS("flag", flaglen * 8)
init_st = p.factory.entry_state(
    stdin=claripy.Concat(flag, claripy.BVV(b"\0")),
    add_options={
        angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY,
        angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS,
    },
)

sm = p.factory.simulation_manager(init_st)
sm.use_technique(angr.exploration_techniques.DFS())
sm.explore(find=0x123A, avoid={0x1173, 0x1302, 0x130F})
st = sm.found[0]

for i, ch in enumerate(b"lactf{"):
    st.solver.add(flag.chop(8)[i] == ch)
st.solver.add(flag.chop(8)[flaglen - 1] == ord("}"))

for i in range(6, flaglen - 1):
    ch = flag.chop(8)[i]
    st.solver.add(claripy.ULT(ch, 127))
    st.solver.add(claripy.UGT(ch, 0x20))
    for b in b"|^`{}[]\\~":
        st.solver.add(ch != b)


full = st.memory.load(st.regs.rsp, 48)

# endianess fix
nibbles = list(chain.from_iterable(by.chop(4)[::-1] for by in full.chop(8)))

for i in range(9):
    a, b, c = 0, 0, 0
    k = i
    for j in range(9):
        b ^= 1 << nibbles[j + 9 * i].zero_extend(28)
        a ^= 1 << nibbles[k].zero_extend(28)
        k += 9
        c ^= 1 << nibbles[9 * ((j // 3) + 3 * (i // 3)) + 3 * (i % 3) + (j % 3)]
    st.solver.add(a == 511, b == 511, c == 511)
    print(st.solver.eval(flag, bytes))
