#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules
import argparse
import subprocess
import os

from colorama import Fore, Style
from modules.fuzz import Connector
from utils import colors
from utils import message

from config import MODS, BORDER

class EnvConnector(Connector):
    '''
    Environment variable connector.
    '''
    def __init__(self):
        self.var = ""
        Connector.__init__(self, MODS)
    
    def execute(self, target, payload):
        env = os.environ.copy()
        env[self.var] = payload

        try:
            proc = subprocess.Popen(
                [target],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                shell=True
            )
            proc.wait()
            
            return proc.returncode
        except subprocess.CalledProcessError as exc:
            print("Error: {}".format(exc.output))

    def print_head(self):
        modules = [x for x in MODS.keys()]
        modules = colors.color_string("red", ', '.join(modules))
        target = colors.color_string("red", self.target)
        target_var = colors.color_string("red", self.var)

        head = {
            "MODULES": modules,
            "TARGET FILE": target,
            "TARGET VARIABLE": target_var
        }

        print(BORDER)
        for key in head.keys():
            print("{:<20}: {:<25}".format(key, head[key]))
        print(BORDER)
        print()

    def handle_args(self):
        parser = argparse.ArgumentParser(description="environment variable fuzzer")
        parser.add_argument(
            "var", 
            metavar="VAR",
            help="the target environment variable"
        )
        parser.add_argument(
            "target", 
            help="the target binary"
        )
        args = parser.parse_args()
        self.target = args.target
        self.var = args.var


if __name__ == "__main__":
    EnvConnector()
