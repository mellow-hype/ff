BORDER = "-"*40
TYPES = ["string", "integer"]

class EnvironmentVariable:
    def __init__(self, name, var_type):
        self.NAME = name
        self.TYPE = var_type

class Config:
    TARGET_BINARY="tests/bin/envsmash2"
    TARGET_VARIABLES = [EnvironmentVariable("DUMMY", "string")]