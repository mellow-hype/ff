#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules
import os
from utils import primitives

class PayloadGen:
    @staticmethod
    def strings():
        payloads = []
        payloads.append(primitives.String.BIG_STRING)
        
        for p in primitives.String.FORMAT_STRINGS:
            payloads.append(p)
        
        return payloads

    @staticmethod
    def integer():
        payloads = [str(x) for x in primitives.Integer.MAXINTS]
        return payloads


    @staticmethod
    def random(size):
        '''Generates a buffer of the requested size filled with random data'''
        return os.urandom(size)

