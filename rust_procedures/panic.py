import logging
import angr
import pyvex

l = logging.getLogger(name=__name__)

######################################
# not finished
######################################
class lang_start(angr.SimProcedure):
    def run(self, main, argc, argv):
        self.call(main, (argc, argv), 'after_slingshot')

    def after_slingshot(self,  main, argc, argv, exit_addr=0):
        self.exit(0)
