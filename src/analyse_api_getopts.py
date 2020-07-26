#!/usr/bin/env pypy3
import angr
import analyse_util
import logging
import time

def run(filename):
    proj = angr.Project(filename, force_load_libs = analyse_util.rust_forced_load_libs)
    analyse_util.setAngrLogger(logging.INFO, False)
    #lang_start
    proj.hook_symbol('_ZN3std2rt10lang_start17h11bd50e61fcdbe07E', analyse_util.lang_start())
    #print
    proj.hook_symbol('_ZN3std2io5stdio6_print17h29b5732a3c8e3feeE', angr.SIM_PROCEDURES['libc']['printf']())
    #panic
    proj.hook_symbol('_ZN3std9panicking11begin_panic17h2044ee2168208c27E', analyse_util.rust_panic())
    #std_env_args
    proj.hook_symbol('_ZN3std3env4args17h5c13af50c07c618eE', analyse_util.std_env_args())
    
    state = proj.factory.entry_state()
    simgr = proj.factory.simulation_manager(state)
    simgr.run()
    print(simgr.deadended)
        
if __name__ == "__main__":
    filename = "../rust-examples/build/api-getopts"
    begin_time = time.time()
    run(filename)
    end_time = time.time()
    total_time = end_time - begin_time
    print("total time = %.5f" % total_time)