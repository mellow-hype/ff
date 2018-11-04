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
        for multi in primitives.String.MULTIPLIERS:
            payloads.append("B"*multi)
        
        for p in primitives.String.FORMAT_STRINGS:
            payloads.append(p)
        
        return payloads

    @staticmethod
    def integer():
        edge_range = 5

        edge_values = []
        final_values = []
        for i in range(1, edge_range):
            edge_values.append([x-i for x in self.MAXINTS])
        for edges in edge_values:
            final_values.append([x for x in edges])
        return final_values

    @staticmethod
    def random(size):
        '''Generates a buffer of the requested size filled with random data'''
        return os.urandom(size)

