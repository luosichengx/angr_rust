#!/usr/bin/env pypy3
import angr
import claripy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("minimal_hook.log", mode='w', encoding="utf-8", delay=False)
logger.addHandler(fh)


class lang_start(angr.SimProcedure):
    def run(self, main, argc, argv):
        logger.debug("main")
        self.call(main, (argc, argv), 'after_slingshot')


    def after_slingshot(self,  main, argc, argv, exit_addr=0):
        logger.debug("after_slingshot")
        self.exit(0)



class rust_panic(angr.SimProcedure):
    def run(self, exit_addr=0):
        self.exit(101)

class empty_procedure(angr.SimProcedure):
    def run(self):
        self.ret()

def setAngrLogger(level, need_file_handler):
    angr_logger = logging.getLogger('angr')
    angr_logger.setLevel(level)
    if need_file_handler:
        fileHandler = logging.FileHandler("angr_log.log", mode='w', encoding="utf-8", delay=False)
        fileHandler.setFormatter(logging.Formatter('%(levelname)-7s | %(asctime)-23s | %(name)-8s | %(message)s'))
        angr_logger.addHandler(fileHandler)
        

if __name__ == "__main__":
    proj = angr.Project("rust_example/minimal_hook")
    setAngrLogger(logging.DEBUG, False)
    #proj.hook_symbol('_ZN3std2rt10lang_start17hf3c239e75c0091e5E', lang_start())
    #proj.hook_symbol('_ZN3std2rt10lang_start17ha0e013fbbe2d5e95E', lang_start())
    #proj.hook_symbol('_ZN3std3env4args17h3d221e79ea653f05E', std_env_args())
    #proj.hook_symbol('_ZN3std2io5stdio6_print17h67d3962635b60ab5E', angr.SIM_PROCEDURES['libc']['printf']())
    proj.hook_symbol('_ZN3std9panicking11begin_panic17h650ba46693a559d5E', rust_panic())

    state = proj.factory.entry_state()
    simgr = proj.factory.simulation_manager(state)
    simgr.run()
    print(simgr.deadended)
