
class Fuzzer:
    retcodes = {
        "132": "Illegal instruction",
        "134": "Abort",
        "139": "Segmentation fault"
    }

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
    def execute(self, **kwargs):
        raise NotImplementedError("Must override execute from child")

    def run(self, **kwargs):
        raise NotImplementedError("Must override execute from child")