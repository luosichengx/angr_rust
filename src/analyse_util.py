#!/usr/bin/env pypy3
import angr
import claripy
import logging
import time
import re

current_log_file = "../log/run_util.log"
angr_log_file = "../log/angr_run_util.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("../log/logging.log", mode='w', encoding="utf-8", delay=False)
logger.addHandler(fh)

rust_forced_load_libs = ["libmy_rust_std.so"]

class rust_util:
    ###function name
    std_rt_lang_start = "std::rt::lang_start"
    std_env_args = "std::env::args"
    std_io_stdio__print = "std::io::stdio::_print"
    std_panicking_begin_panic = "std::panicking::begin_panic"

    @staticmethod
    def get_function_sao(proj, state, shared_lib_name, function_name):
        shared_lib_object = proj.loader.shared_objects.get(shared_lib_name)
        function_addr = shared_lib_object.get_symbol(function_name).rebased_addr
        logger.debug("fucntion addr : 0x%x" % function_addr)
        function_bv = state.solver.BVV(function_addr, 64)
        return angr.state_plugins.sim_action_object.SimActionObject(function_bv)

    #objdump出来的地址需要为16位
    @staticmethod
    def get_all_symbols(filename, function_name):
        if not filename.endswith(".txt"):
            raise Exception("Invalid file type")
        res = set()
        with open(filename, "r") as fp:
            contents = fp.readlines()
            fp.close()
            function_symbols = function_name.split("::")
            #print(function_symbols)
            for line in contents:
                line = line.strip()
                #contain rust function name
                contain_all_flag = True
                for function_symbol in function_symbols:
                    if not line.__contains__(function_symbol):
                        contain_all_flag = False
                        break
                if not contain_all_flag:
                    continue
                #find function def pattern
                line_pattern = r'^([0-9]|[a-f]){16}\s+'
                function_name_pattern = r'<_ZN'
                for symbol in function_symbols:
                    function_name_pattern = function_name_pattern + r'\d+'
                    function_name_pattern = function_name_pattern + symbol
                function_name_pattern = function_name_pattern + r'([0-9]|[a-z]|[A-Z])+>'
                #print(function_name_pattern)

                if re.search(line_pattern, line) != None:
                    search_function_name_obj = re.search(function_name_pattern, line)
                    if search_function_name_obj != None:
                        #print(search_function_name_obj.span())
                        begin_index, end_index = search_function_name_obj.span()
                        one_res = line[begin_index+1:end_index-1]
                        #print(one_res)
                        res.add(one_res)
            return res

    @staticmethod
    def get_one_symbol(filename,function_name):
        all_symbols = list(rust_util.get_all_symbols(filename, function_name))
        if len(all_symbols) < 1:
            raise Exception("No symbol was found.")
        elif len(all_symbols) > 1:
            raise Exception("More than one symbol was found. Please call get_all_symbols.")
        else:
            return all_symbols[0]


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
    disassembly_filename = filename + ".txt"
    #std::rt::lang_start
    lang_start_symbol = rust_util.get_one_symbol(disassembly_filename,rust_util.std_rt_lang_start)
    proj.hook_symbol(lang_start_symbol, lang_start())
    #std::env::args()
    env_args_symbol = rust_util.get_one_symbol(disassembly_filename,rust_util.std_env_args)
    proj.hook_symbol(env_args_symbol, std_env_args())
    #print
    print_symbol = rust_util.get_one_symbol(disassembly_filename,rust_util.std_io_stdio__print)
    proj.hook_symbol(print_symbol, angr.SIM_PROCEDURES['libc']['printf']())
    #panic
    panic_symbol = rust_util.get_one_symbol(disassembly_filename,rust_util.std_panicking_begin_panic)
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


