import angr
import claripy

FLAG_LEN = 25
STDIN_FD = 0

base_addr = 0x140000000  # To match addresses to Ghidra

proj = angr.Project(".\\LughTuathaDe.exe", main_opts={"base_addr": base_addr})

flag_chars = [claripy.BVS("flag_%d" % i, 8) for i in range(FLAG_LEN)]
flag = claripy.Concat(
    *flag_chars + [claripy.BVV(b"\n")]
)  # Add \n for scanf() to accept the input

state = proj.factory.full_init_state(
    args=[".\\LughTuathaDe.exe"],
    add_options=angr.options.unicorn,
    stdin=flag,
)

# Add constraints that all characters are printable
for k in flag_chars:
    state.solver.add(k >= ord("!"))
    state.solver.add(k <= ord("~"))

simgr = proj.factory.simulation_manager(state)
find_addr = 0x140006737  # The address of "call puts" for SUCCESS
avoid_addr = 0x140024724  # The address of "call puts" for FAILURE
simgr.explore(find=find_addr, avoid=avoid_addr)

if len(simgr.found) > 0:
    for found in simgr.found:
        print(found.posix.dumps(STDIN_FD))