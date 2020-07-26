#!/usr/bin/env pypy3
import angr
import analyse_util
import logging
import time

def run(filename):
    proj = angr.Project(filename, force_load_libs = analyse_util.rust_forced_load_libs)
    analyse_util.setAngrLogger(logging.INFO, False)
    #lang_start
    proj.hook_symbol('_ZN3std2rt10lang_start17ha4e0e87663c416e3E', analyse_util.lang_start())
    #print
    proj.hook_symbol('_ZN3std2io5stdio6_print17h29b5732a3c8e3feeE', angr.SIM_PROCEDURES['libc']['printf']())
    #panic
    proj.hook_symbol('_ZN3std9panicking11begin_panic17hbb16b07720ab8b7cE', analyse_util.rust_panic())
    
    state = proj.factory.entry_state()
    simgr = proj.factory.simulation_manager(state)
    simgr.run()
    print(simgr.deadended)
        
if __name__ == "__main__":
    filename = "../rust-examples/build/what_it_looks_like"
    begin_time = time.time()
    run(filename)
    end_time = time.time()
    total_time = end_time - begin_time
    print("total time = %.5f" % total_time)