import angr
import claripy
from rust_procedures import *


def run_symexe(path):
    sym_argv = claripy.BVS('sym_argv', 64)
    p = angr.Project(path, load_options={"auto_load_libs": False})
    main_obj = p.loader.main_object.get_symbol('main')
    # state = p.factory.entry_state(args=[p.filename, sym_argv])
    state = p.factory.entry_state(addr=main_obj.rebased_addr, args=[p.filename, sym_argv])
    pg = p.factory.simgr(state)
    add_rust_support(p)
    pg.run()
    for dd in pg.deadended:
        res = dd.solver.eval(sym_argv, cast_to=bytes)
        print(b'[+] New Input: ' + res + b' |')
        print(str(dd.solver.constraints))


def add_rust_support(p):
    if "rust" in p.filename:
        # for obj in p.loader.initial_load_objects:
        #     for reloc in obj.imports.values():
        #         if reloc.resolvedby is not None:
        #             print(reloc.resolvedby.name, hex(reloc.resolvedby.rebased_addr))
        #         else:
        #             print(reloc)
        objs = p.loader.main_object
        # lang_start_addr = objs.get_symbol('_ZN2rt10lang_start20h58cfae38546804729kxE').rebased_addr
        p.hook_symbol('_ZN2rt10lang_start20h58cfae38546804729kxE', lang_start())
        # print_addr = objs.get_symbol('_ZN2io5stdio6_print20h47445faa595ef503E6gE').rebased_addr
        p.hook_symbol('_ZN2io5stdio6_print20h47445faa595ef503E6gE', angr.SIM_PROCEDURES['libc']['printf']())
        # p.hook_symbol('_ZN6string13_$LT$impl$GT$9to_string9to_string21h12836934065809422381E', to_string())
        # p.hook_symbol('_ZN9panicking9panic_fmt20h4c8d12e3c05f3b8cZEKE', angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained']())

run_symexe("old_rust_example/what_it_looks_like")