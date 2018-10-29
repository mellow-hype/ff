#!/usr/bin/env python
# Author:   hyperlogic
# Date:     11/2018
# Project:  fuzzy-framework
# A collection of fuzzing modules
from colorama import Fore, Style
from utils.generators import PayloadGenerator
from modules.fuzz import Fuzzer
import os.path

class Naughty(Fuzzer):
    def load_values_from_file(self, filename):
        vals = []
        filepath = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(filepath, filename)
        data = open(path, "r")
        for entry in data.readlines():
            vals.append(entry)
        return vals

    def format_string(self, target, input_file="format.txt"):
        format_strs = self.load_values_from_file(input_file)
        fault = False

        print("[+] Naughty - Format strings fuzz starting...")
        for entry in format_strs:
            payload = entry.strip("\n")
            if self.check_fault(self.execute(target, payload)):
                print(Fore.RED, end="")
                print("[!] Fault detected with payload: {}".format(payload))
                print(Style.RESET_ALL, end="")
                fault = True
        if not fault:
            print("[!] No faults detected using Naughty module")

    def run(self, target):
        self.format_string(target)
