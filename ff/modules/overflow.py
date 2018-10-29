#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules
from utils.generators import PayloadGenerator
from .fuzz import Fuzzer
from utils.message import status, alert

class OverflowFuzzer(Fuzzer):
    def fast_sweep(self, target):
        '''
        Do a fast check to find overflows using pre-defined sizes. Keeps
        track of the current and previous size to define low/high boundaries 
        for deep sweep in case a fault is detected.
        '''
        fault_size, prev_size = 0,0
        steps = [0, 1000, 5000, 10000, 25000, 50000]
        
        status("Fast overflow check starting...")
        for size in steps:
            payload = PayloadGenerator.abuff(size)
            if self.check_fault(self.execute(target, payload)):
                alert("Fault detected: {}-{} bytes".format(prev_size, size))
                fault_size = size
                break
            prev_size = size

        if fault_size == 0:
            status("No buffer overflows detected")
        else:
            status("Pinpointing the faulting buffer size...")
            self.deep_sweep(target, prev_size, fault_size)

    def deep_sweep(self, target, low, high):
        '''
        The function was called with low/high boundaries, meaning a fault was detected.
        Drill down to find the exact size that causes a crash:
        '''
        # - if the difference between low and high is >1:
        #   1. execute payload that is of size halfway between low and high boundaries
        #       - if a fault occurs: fault size is below midpoint, mid point becomes the new high
        #       - if no fault occurs: fault size is above midpoint, midpoint becomes thew new low
        #   2. call this function recursively with new low/high boundaries 
        if high-low > 1:
            mid_size = ((high - low) // 2) + low
            payload = PayloadGenerator.abuff(mid_size)
            
            print("> Executing with buffer size: {}".format(mid_size))
            if self.check_fault(self.execute(target, payload)) == True:
                # use the mid_size as the new max
                self.deep_sweep(target, low, mid_size)
            else:
                # use the mid_size as the new low
                self.deep_sweep(target, mid_size, high)
        else:
            alert("Overflow occurs at: {} bytes".format(high))

    def run(self, target):
        self.fast_sweep(target)

