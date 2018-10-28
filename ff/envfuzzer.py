#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules
import argparse
import subprocess
import os

from modules.fuzz import Connector
from modules.overflow import OverflowFuzzer
BORDER = "="*40

# MODULES DICTIONARY
# These are the modules that will be loaded
MODS = {"overflow": OverflowFuzzer}


class EnvConnector(Connector):
    '''
    Environment variable connector.
    Args: (target_bin, target_var)
    '''
    def __init__(self, target_bin, target_var):
        self.target = target_bin
        self.var = target_var
        self.module = None

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

    def load_module(self, module):
            self.module = MODS[module]()
            self.module.execute = self.execute

    def run(self):
        for module in MODS.keys():
            self.load_module(module)
            self.module.run(self.target)

def handle_args():
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
    return parser.parse_args()

if __name__ == "__main__":
    args = handle_args()
    fuzzer = EnvConnector(args.target, args.var)
    fuzzer.run()
