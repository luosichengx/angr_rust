#!/usr/bin/env pypy3
import angr
import analyse_util
import logging
import time

def run(filename):
    proj = angr.Project(filename, force_load_libs = analyse_util.rust_forced_load_libs)
    analyse_util.setAngrLogger(logging.DEBUG, False)
    #lang_start
    proj.hook_symbol('_ZN2rt10lang_start20h58cfae38546804729kxE', analyse_util.lang_start())
    #print
    proj.hook_symbol('_ZN2io5stdio6_print20h47445faa595ef503E6gE', angr.SIM_PROCEDURES['libc']['printf']())
    #panic
    proj.hook_symbol('_ZN9panicking5panic20hb8a57f0c8013c90awDKE', analyse_util.rust_panic())
    proj.hook_symbol('_ZN10sys_common6unwind3imp5panic17exception_cleanup20h1b826c82bc5cdd67jasE', 
                        analyse_util.empty_procedure())
    proj.hook_symbol('rust_panic', analyse_util.rust_panic())
    proj.hook_symbol('_ZN9panicking9panic_fmt20h4c8d12e3c05f3b8cZEKE', analyse_util.empty_procedure())
    proj.hook_symbol('_ZN9panicking9log_panic20hffc6d029fed602571nxE', analyse_util.rust_panic())
    proj.hook_symbol('_ZN9panicking18panic_bounds_check20h2c011cc7c407798b5DKE', 
                        analyse_util.empty_procedure())
    

    state = proj.factory.entry_state()
    simgr = proj.factory.simulation_manager(state)
    simgr.run()
    print(simgr.deadended)
        
if __name__ == "__main__":
    filename = "../rust_example/what_it_looks_like2"
    begin_time = time.time()
    run(filename)
    end_time = time.time()
    total_time = end_time - begin_time
    print("total time = %.5f" % total_time)