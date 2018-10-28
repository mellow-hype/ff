# fuzzy-framework

## Overview
This is meant to be a framework of sorts. 

Different fuzzing modules are defined as `Fuzzer` subclasses that live in the `modules` directory. These modules perform different types of fuzzing. 
Modules are meant to be loaded and called from user-defined `Connector` subclasses. Connectors define the input vector that will be targeted. For example, 
the `EnvConnector` subclass targets environment variables. 

The `Connector` base class is defined below. New Connectors should implement argument handlers using `argparse`. The `EnvConnector` should serve as a model for how to implement new
Connectors.
```py
class Connector:
    def execute(self, **kwargs):
        raise NotImplementedError("Must override execute from child")

    def run(self, **kwargs):
        raise NotImplementedError("Must override execute from child")
```

Combining `Connectors` with available `Fuzzer` modules lets us mix-and-match inputs and fuzzing methods. 


## Fuzzer Modules
These are the available `Fuzzer` modules.

### `OverflowFuzzer`
This module tests for overflow conditions. It begins by performing a fast sweep with predefined values. If it detects a crash in the target application, it then drills down to find 
the exact size that triggers the crash.

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


## Examples

Below are examples of running the `OverflowFuzzer` module through the `EnvConnector` to detect buffer overflows in environment variables. The vulnerable binaries
used for these examples are available under `ff/tests/envconnector`.

```
(venv) [ff] ./envfuzzer.py DUMMY tests/envfuzzer/bin/envsmash2
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
> Done.

[+] Overfow occurs at: 409 bytes
```

```
(venv) [ff] ./envfuzzer.py DUMMY tests/envfuzzer/bin/envsmash
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
> Done.

[+] Overfow occurs at: 1001 bytes

```