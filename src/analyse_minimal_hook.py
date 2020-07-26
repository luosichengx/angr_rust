#!/usr/bin/env pypy3
import angr
import analyse_util
import logging

def run(filename):
    proj = angr.Project(filename, force_load_libs = analyse_util.rust_forced_load_libs)
    analyse_util.setAngrLogger(logging.INFO, False)
    proj.hook_symbol('_ZN3std2rt10lang_start17hf3c239e75c0091e5E', analyse_util.lang_start())
    #proj.hook_symbol('_ZN3std9panicking11begin_panic17h650ba46693a559d5E', analyse_util.rust_panic())

    state = proj.factory.entry_state()
    simgr = proj.factory.simulation_manager(state)
    simgr.run()
    print(simgr.deadended)
        

if __name__ == "__main__":
    filename = "../old_rust_example/minimal_hook"
    run(filename)
