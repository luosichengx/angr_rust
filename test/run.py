#!/usr/bin/env python3
import angr

class lang_start(angr.SimProcedure):
    def run(self, main, argc, argv):
        self.call(main, (argc, argv), 'after_slingshot')

    def after_slingshot(self,  main, argc, argv, exit_addr=0):
        self.exit(0)

proj = angr.Project("hello")

#objs = proj.loader.main_object
#lang_start_addr = objs.get_symbol('_ZN3std2rt10lang_start17ha0e013fbbe2d5e95E').rebased_addr
#print("lang_start_addr:" + str(lang_start_addr))
#print_addr = objs.get_symbol('_ZN3std2io5stdio6_print17h67d3962635b60ab5E').rebased_addr
#print("print_addr:" + str(lang_start_addr))


proj.hook_symbol('_ZN3std2rt10lang_start17ha0e013fbbe2d5e95E', lang_start())
proj.hook_symbol('_ZN3std2io5stdio6_print17h67d3962635b60ab5E', angr.SIM_PROCEDURES['libc']['printf']())

state = proj.factory.entry_state()
simgr = proj.factory.simulation_manager(state)
#print(simgr.active)

print(simgr.explore(find=lambda s: b"Hello" in s.posix.dumps(1)))
s = simgr.found[0]
print(s.posix.dumps(1))
#simgr.run()
#print(simgr.deadended)
#print(simgr.deadended[0].posix.dumps(0))
