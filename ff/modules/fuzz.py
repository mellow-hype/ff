
class Fuzzer:
    retcodes = {
        "132": "Illegal instruction",
        "134": "Abort",
        "139": "Segmentation fault"
    }

    def run(self, **kwargs):
        raise NotImplementedError("Must override execute from child")

    def execute(self, **kwargs):
        raise NotImplementedError("Must override execute from child")

    def check_fault(self, rcode):
        '''
        Detect a fault in the fuzzed application. Returns True or False.
        '''
        if str(rcode) in self.retcodes.keys():
            return True
        else:
            return False

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
