# fuzzy-framework

## Overview
This is meant to be a framework of sorts. 

Different fuzzing modules are defined as `Fuzzer` subclasses that live in the `ff/modules/` directory. These modules perform different types of fuzzing. 
Modules are meant to be loaded and called from user-defined `Connector` subclasses. Connectors define the input vector that will be targeted. For example, the `EnvConnector` subclass targets environment variables. 

The `Connector` base class is defined below. New Connector subclasses should implement `handle_args`, `print_head`, and 
`execute`. 

```py
class Connector:
    def __init__(self, modules):
        self.target = ""
        self.mods = modules
        self.module = None
        self.handle_args()
        self.print_head()
        self.run()
    
    def execute(self, **kwargs):
        raise NotImplementedError("Must override execute from child")

    def print_head(self, **kwargs):
        raise NotImplementedError("Must override execute from child")

    def handle_args(self, **kwargs):
        raise NotImplementedError("Must override execute from child")

    def load_module(self, target_mod):
        self.module = self.mods[target_mod]()
        self.module.execute = self.execute

    def run(self):
        for mod in self.mods.keys():
            print("== {} ==".format(str(mod).upper()))
            self.load_module(mod)
            self.module.run(self.target)
            print()
```

The `EnvConnector` should serve as a model for how to implement new Connectors. The `execute` method in particular will be unique to the input vector the Connector targets.


Combining `Connectors` with available `Fuzzer` modules lets us mix-and-match inputs and fuzzing methods. 


## Connector Modules
These are the available `Connector` modules.

### `EnvConnector`
This Connector targets environment variables.

```
usage: envfuzzer.py [-h] VAR target

environment variable fuzzer

positional arguments:
  VAR         the target environment variable
  target      the target binary

optional arguments:
  -h, --help  show this help message and exit
```

Here is how this Connector is implemented:

```py
from modules.fuzz import Connector
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
      ...

    def handle_args(self):
      ...
```

## Fuzzer Modules
These are the available `Fuzzer` modules. Modules are configured in the `MODS` dictionary in `ff/config.py`

### `OverflowFuzzer`
This module tests for overflow conditions. It begins by performing a fast sweep with predefined values. If it detects a crash in the target application, it then drills down to find 
the exact size that triggers the crash.

### `Naughty`
This module tests uses predefined lists of strings that are likely to cause issues. These are split into different types. Currently, only format strings are checked.


## Examples

Below are examples of running the `OverflowFuzzer` and `Naughty` moduled through the `EnvConnector`. 

*The vulnerable binaries used for these examples are available under `ff/tests/envconnector`.*

```
$ ./envfuzzer.py DUMMY tests/bin/envsmash2 
----------------------------------------
MODULES             : overflow, naughty
TARGET FILE         : tests/bin/envsmash2
TARGET VARIABLE     : DUMMY           
----------------------------------------

== OVERFLOW ==
[+] Fast overflow check starting...
[!] Fault detected: 0-1000 bytes
[+] Pinpointing the faulting buffer size...
> Executing with buffer size: 500
> Executing with buffer size: 250
> Executing with buffer size: 375
> Executing with buffer size: 437
> Executing with buffer size: 406
> Executing with buffer size: 421
> Executing with buffer size: 413
> Executing with buffer size: 409
> Executing with buffer size: 407
> Executing with buffer size: 408
[!] Overflow occurs at: 409 bytes

== NAUGHTY ==
[+] Naughty - Format strings fuzz starting...
[!] Fault detected with payload: %s%s%s%s%s%s%s%s%s%s
[!] Fault detected with payload: %n%n%n%n%n%n%n%n%n%n

```

```
$ ./envfuzzer.py DUMMY tests/bin/envsmash 
----------------------------------------
MODULES             : overflow, naughty
TARGET FILE         : tests/bin/envsmash
TARGET VARIABLE     : DUMMY           
----------------------------------------

== OVERFLOW ==
[+] Fast overflow check starting...
[!] Fault detected: 1000-5000 bytes
[+] Pinpointing the faulting buffer size...
> Executing with buffer size: 3000
> Executing with buffer size: 2000
> Executing with buffer size: 1500
> Executing with buffer size: 1250
> Executing with buffer size: 1125
> Executing with buffer size: 1062
> Executing with buffer size: 1031
> Executing with buffer size: 1015
> Executing with buffer size: 1007
> Executing with buffer size: 1003
> Executing with buffer size: 1001
[!] Overflow occurs at: 1001 bytes

== NAUGHTY ==
[+] Naughty - Format strings fuzz starting...
[!] No faults detected using Naughty module
```