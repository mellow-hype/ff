#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules
import os

class PayloadGenerator:
    @staticmethod
    def abuff(size):
        '''Generates a buffer of the requested size with the value "A"''' 
        return "A"*size

    @staticmethod
    def random(size):
        '''Generates a buffer of the requested size filled with random data'''
        return os.urandom(size)

