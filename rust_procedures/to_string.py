import logging

import pyvex
import angr

l = logging.getLogger(name=__name__)

######################################
# lang_start
######################################
class to_string(angr.SimProcedure):
    def run(self, object):
        return object.__str__();
