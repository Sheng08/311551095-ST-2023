import angr
import claripy
import ctypes

main_addr = 0x4011a9
start_addr = 0x401286
find_addr = 0x401371
avoid_addr = 0x40134d

proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})

xs = [claripy.BVS('x_%d' % i, 32) for i in range(15)]
class my_scanf(angr.SimProcedure):
    def run(self, fmt, ptr):
        # self.state.mem[ptr].dword = xs[self.state.globals['scanf_count']]
        self.state.memory.store(ptr, xs[self.state.globals['scanf_count']], endness=proj.arch.memory_endness)
        self.state.globals['scanf_count'] += 1
        return 1 

class DoNothing(angr.SimProcedure):
    def run(self, fmt, *args):
        return

proj.hook_symbol("__isoc99_scanf", my_scanf() ,replace=True)
proj.hook_symbol('printf', DoNothing(), replace=True)

# state = proj.factory.entry_state()
state = proj.factory.blank_state(addr=main_addr)
simgr = proj.factory.simulation_manager(state)
simgr.one_active.globals['scanf_count'] = 0
# simgr.one_active.options.add(angr.options.LAZY_SOLVES)

simgr.explore(find=find_addr, avoid=avoid_addr)

if simgr.found:
    with open('solve_input', 'w') as f:
        for idx, c in enumerate(xs):
            x = simgr.found[0].solver.eval(c, cast_to=int)
            x_c_int = ctypes.c_int32(x).value
            print(f"Input x{idx}: {x_c_int}")
            # n = struct.unpack('<i', b)[0]
            f.write(str(x_c_int) + '\n')
else:
    print('Failed')