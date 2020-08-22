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
    #set argv symbolic
    argv_bytes = 12
    sym_argv = claripy.BVS("sym_argv", argv_bytes * 8)
    state = proj.factory.entry_state(args = [proj.filename, sym_argv])
    
    #添加约束，将输入限制到ascii码范围之内
    mask = claripy.BVV(0xff, argv_bytes * 8)
    for i in range(argv_bytes):
        least_bits = (sym_argv >> (i * 8)) & mask
        #print(least_bits)
        state.solver.add(least_bits >= 0)
        state.solver.add(least_bits <= 127)
    
    simgr = proj.factory.simulation_manager(state)
    simgr.run()
    print(simgr.deadended)

    for dd in simgr.deadended:
        res = dd.solver.eval(sym_argv)
        print('[+] New Input: ' + str(res) + ' |')
        argv_str = pass_int_to_ascii_string(res, argv_bytes)
        #貌似@是特殊字符?这一个判断也可以不加，这样solve的结果里会出现很多带有@的字符串
        if not argv_str.__contains__("@"):
            print("[solve string] argv = " + argv_str + ", strlen = " + str(len(argv_str)))
        #print(len(dd.solver.constraints))
        #print(dd.solver.constraints)
        

if __name__ == "__main__":
    filename = "../test/hello"
    begin_time = time.time()
    run_hello(filename)
    end_time = time.time()
    total_time = end_time - begin_time
    print("total time = %.5f" % total_time)