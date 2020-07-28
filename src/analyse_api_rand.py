#!/usr/bin/env pypy3
import angr
from analyse_util import *
import logging
import time

def run(filename):
    disassembly_filename = filename + ".txt"
    proj = angr.Project(filename, force_load_libs = rust_forced_load_libs)
    setAngrLogger(logging.INFO, False)
    #lang_start
    lang_start_symbol = rust_util.get_one_symbol(disassembly_filename,rust_util.std_rt_lang_start)
    proj.hook_symbol(lang_start_symbol, lang_start())
    #print
    print_symbol = rust_util.get_one_symbol(disassembly_filename, rust_util.std_io_stdio__print)
    proj.hook_symbol(print_symbol, angr.SIM_PROCEDURES['libc']['printf']())
    #panic
    panic_symbols = rust_util.get_all_symbols(disassembly_filename, rust_util.std_panicking_begin_panic)
    for panic_symbol in panic_symbols:
        proj.hook_symbol(panic_symbol, rust_panic())
    
    state = proj.factory.entry_state()
    simgr = proj.factory.simulation_manager(state)
    simgr.run()
    print(simgr.deadended)
        
if __name__ == "__main__":
    filename = "../rust-examples/build/api-rand"
    begin_time = time.time()
    run(filename)
    end_time = time.time()
    total_time = end_time - begin_time
    print("total time = %.5f" % total_time)