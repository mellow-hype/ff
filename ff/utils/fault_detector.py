#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules

class FaultCatcher:
    retcodes = {
        "132": "Illegal instruction",
        "134": "Abort",
        "139": "Segmentation fault"
    }


    def check_fault(self, rcode):
        '''
        Detect a fault in the fuzzed application. Returns True or False.
        '''
        if str(rcode) in self.retcodes.keys():
            return True
        else:
            return False