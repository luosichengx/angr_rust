#!/usr/bin/env pypy3
import angr
import claripy
import logging
import time
from analyse_util import *

def run_hello(filename):
    setAngrLogger(logging.INFO, False)
    proj = angr.Project(filename, force_load_libs = rust_forced_load_libs)
    disassembly_filename = filename + ".txt"
    #std::rt::lang_start
    lang_start_symbol = rust_util.get_one_symbol(disassembly_filename,
                        rust_util.std_rt_lang_start)
    proj.hook_symbol(lang_start_symbol, lang_start())
    #std::env::args()
    env_args_symbol = rust_util.get_one_symbol(disassembly_filename, 
                        rust_util.std_env_args)
    proj.hook_symbol(env_args_symbol, std_env_args())
    #print
    print_symbol = rust_util.get_one_symbol(disassembly_filename,
                        rust_util.std_io_stdio__print)
    proj.hook_symbol(print_symbol, angr.SIM_PROCEDURES['libc']['printf']())
    #panic
    panic_symbol = rust_util.get_one_symbol(disassembly_filename,
                        rust_util.std_panicking_begin_panic)
    proj.hook_symbol(panic_symbol, rust_panic())
    #set argc symbolic
    sym_argc = claripy.BVS("sym_argc", 64)
    state = proj.factory.entry_state(argc = sym_argc, args = [proj.filename, "1", "2", "3"])
    #print(state.posix.argc)
    #print(state.posix.argv)
    state.solver.add(sym_argc < 5)
    state.solver.add(sym_argc > 0)
    simgr = proj.factory.simulation_manager(state)
    simgr.run()
    print(simgr.deadended)

    for dd in simgr.deadended:
        res = dd.solver.eval(sym_argc)
        print('[+] New Input: ' + str(res) + ' |')
        print(len(dd.solver.constraints))
        

if __name__ == "__main__":
    filename = "../old_rust_example/hello"
    begin_time = time.time()
    run_hello(filename)
    end_time = time.time()
    total_time = end_time - begin_time
    print("total time = %.5f" % total_time)


