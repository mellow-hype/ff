#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules
import subprocess
import os

from utils import colors
from utils import message
from modules.fuzz import Fuzzer
from generators.payload import PayloadGen
from config import BORDER, TYPES
from config import Config


PAYLOADS = {
    "string": PayloadGen.strings,
    "integer": PayloadGen.integer
}

class EnvConnector(Fuzzer):
    '''
    Environment variable connector.
    '''
    def __init__(self, binary, variables):
        self.vars = variables
        self.bin = binary
        self.payloads = {}
        self.validate()
        self.generate_payloads()
        self.print_head()
        self.fuzz()

    def validate(self):
        for var in self.vars:
            if var.TYPE not in TYPES:
                message.alert("{} is not a valid type. Valid types are '{}'".format(var.TYPE, TYPES))
                exit()
        
        if not os.path.exists(self.bin):
            message.alert("{} is not a valid path".format(self.bin))
            exit()
        elif not os.access(self.bin, os.X_OK):
            message.alert("{} is not executable".format(self.bin))
            exit()

    
    def execute(self, target_var, payload_list):
        for payload in payload_list:
            env = os.environ.copy()
            env[target_var] = payload
            fault_detected = False

            try:
                proc = subprocess.Popen(
                    [self.bin],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    env=env,
                    shell=True
                )
                err = proc.communicate()
                err_message = err[1].decode()
                proc.wait()
                
                if self.check_fault(proc.returncode):
                    fault = True
                    if len(payload) > 100:
                        payload = "'{}...' (truncated, {} bytes). Potential buffer overflow.".format(payload[:3], len(payload))
                    elif "%n" or "%s" in payload:
                        payload = "'{}...' (truncated). Potential format string bug.".format(payload[:5]) 
                    message.alert("Fault detected using payload {}".format(payload))
                    message.std_err(err_message)
            except subprocess.CalledProcessError as exc:
                print("Error: {}".format(exc.output))
        if not fault_detected:
            message.status("No faults detected.")

    def generate_payloads(self):
        for target in self.vars:
            self.payloads[target.NAME] = PAYLOADS[target.TYPE]()

    def fuzz(self):
        for target in self.vars:
            self.execute(target.NAME, self.payloads[target.NAME])
            
    def print_head(self):
        target = colors.color_string("red", self.bin)
        target_var = ""
        for var in self.vars:
            target_var += "{} ({}) ".format(var.NAME, var.TYPE)
            
        head = {
            "TARGET FILE": target,
            "TARGET VARIABLE": target_var
        }

        print(BORDER)
        for key in head.keys():
            print("{:<20}: {:<25}".format(key, head[key]))
        print(BORDER)
        print()


if __name__ == "__main__":
    config = Config()
    EnvConnector(config.TARGET_BINARY, config.TARGET_VARIABLES)
