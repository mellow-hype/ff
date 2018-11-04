#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules
import subprocess
import os

from utils import colors
from utils import message
from utils.overflow import overflow_locator
from utils.fault_detector import FaultCatcher
from generators.payload import PayloadGen
from config import BORDER, TYPES
from config import Config


PAYLOADS = {
    "string": PayloadGen.strings,
    "integer": PayloadGen.integer
}

class EnvConnector:
    '''
    Environment variable connector.
    '''
    def __init__(self, binary, variables):
        self.vars = variables
        self.bin = binary
        self.payloads = {}
        self.catcher = FaultCatcher()
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

    
    def execute(self, target_var, payload):
        self.current_payload = payload
        env = os.environ.copy()
        env[target_var] = payload

        try:
            proc = subprocess.Popen(
                [self.bin],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                env=env,
                shell=True
            )
            proc.wait()
            return proc.returncode
        except subprocess.CalledProcessError as exc:
            print("Error: {}".format(exc.output))

    def generate_payloads(self):
        for target in self.vars:
            self.payloads[target.NAME] = PAYLOADS[target.TYPE]()

    def launch(self, target, payload):
        ret = self.execute(target, payload)
        
        if len(payload) > 100:
            payload_msg = "'{}...' (truncated, {} bytes).".format(
                payload[:3], 
                len(payload)
                )
        
        elif "%n" or "%s" in payload:
            payload_msg = "'{}...' (truncated). Format string error.".format(
                payload[:5]
                ) 

        if self.catcher.check_fault(ret):
            message.alert("Fault detected using payload {}".format(payload_msg))
            message.alert("Buffer overflow detected. Finding the faulting size now...")
            overflow_locator(self.execute, target, 0, len(payload))

    def fuzz(self):
        for target in self.vars:
            for payload in self.payloads[target.NAME]:
                self.launch(target.NAME, payload)
                    
            
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
