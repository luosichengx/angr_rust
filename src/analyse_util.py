#!/usr/bin/env pypy3
import angr
import claripy
import logging
import time

current_log_file = "../log/run_util.log"
angr_log_file = "../log/angr_run_util.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("../log/logging.log", mode='w', encoding="utf-8", delay=False)
logger.addHandler(fh)

rust_forced_load_libs = ["libmy_rust_std.so"]

class rust_util:
    @staticmethod
    def get_function_sao(proj, state, shared_lib_name, function_name):
        shared_lib_object = proj.loader.shared_objects.get(shared_lib_name)
        function_addr = shared_lib_object.get_symbol(function_name).rebased_addr
        logger.debug("fucntion addr : 0x%x" % function_addr)
        function_bv = state.solver.BVV(function_addr, 64)
        return angr.state_plugins.sim_action_object.SimActionObject(function_bv)


class lang_start(angr.SimProcedure):
    def run(self, main, argc, argv):
        test_func_name = "add_one_test"
        rust_init_func_name = "rust_init"
        logger.debug("lang_start")
        rust_init_sao = rust_util.get_function_sao(self.project, self.state, 
                    "libmy_rust_std.so", rust_init_func_name)
        logger.debug(rust_init_sao)
        self.call(rust_init_sao, (argc, argv), 'run_main')

    def run_main(self, main, argc, argv):
        logger.debug("run_main")
        self.call(main, (), "after_slingshot")        

    def after_slingshot(self,  main, argc, argv, exit_addr=0):
        logger.debug("after_slingshot")
        self.exit(0)

class std_env_args(angr.SimProcedure):
    def run(self):
        logger.debug("std_env_args")
        rust_std_env_args_func_name = "std_args"
        rust_std_env_args_sao = rust_util.get_function_sao(self.project, 
                    self.state, "libmy_rust_std.so", rust_std_env_args_func_name)
        self.call(rust_std_env_args_sao, (), "jump_back")
    
    def jump_back(self):
        logger.debug("jump_back")
        self.ret()

class rust_panic(angr.SimProcedure):
    def run(self, exit_addr=0):
        self.exit(101)

class empty_procedure(angr.SimProcedure):
    def run(self):
        self.ret()

def setAngrLogger(level, need_file_handler, logfilename = angr_log_file):
    angr_logger = logging.getLogger('angr')
    angr_logger.setLevel(level)
    if need_file_handler:
        fileHandler = logging.FileHandler(logfilename, mode='w', encoding="utf-8", delay=False)
        fileHandler.setFormatter(logging.Formatter('%(levelname)-7s | %(asctime)-23s | %(name)-8s | %(message)s'))
        angr_logger.addHandler(fileHandler)

def run_hello(filename):
    setAngrLogger(logging.INFO, False)
    proj = angr.Project(filename, force_load_libs = rust_forced_load_libs)
    #lang_start
    proj.hook_symbol('_ZN3std2rt10lang_start17ha0e013fbbe2d5e95E', lang_start())
    #std::env::args()
    proj.hook_symbol('_ZN3std3env4args17h3d221e79ea653f05E', std_env_args())
    #print
    proj.hook_symbol('_ZN3std2io5stdio6_print17h67d3962635b60ab5E', angr.SIM_PROCEDURES['libc']['printf']())
    #panic
    proj.hook_symbol('_ZN3std9panicking11begin_panic17h650ba46693a559d5E', rust_panic())
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


