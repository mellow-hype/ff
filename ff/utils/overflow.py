#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules
from utils import message
from utils.fault_detector import FaultCatcher

def overflow_locator(execute_func, target, low, high):
    '''
    The function was called with low/high boundaries, meaning a fault was detected.
    Drill down to find the exact size that causes a crash:
    '''
    # - if the difference between low and high is >1:
    #   1. execute payload that is of size halfway between low and high boundaries
    #       - if a fault occurs: fault size is below midpoint, mid point becomes the new high
    #       - if no fault occurs: fault size is above midpoint, midpoint becomes thew new low
    #   2. call this function recursively with new low/high boundaries 
    execute = execute_func
    catcher = FaultCatcher()

    if high-low > 1:
        mid_size = ((high - low) // 2) + low
        payload = "B"*mid_size
        
        print("> Executing with buffer size: {}".format(mid_size))
        if catcher.check_fault(execute(target, payload)):
            # use the mid_size as the new max
            overflow_locator(execute, target, low, mid_size)
        else:
            # use the mid_size as the new low
            overflow_locator(execute, target, mid_size, high)
    else:
        message.alert("Overflow size found: {} bytes".format(high))
