TYPES = ["string", "integer"]

class Integer:
    MAXINTS = [0xff, 0xffff, 0xffffffff, 0xfffffffffffffff]
    MAXINTS_M1 = [i-1 for i in MAXINTS]
    MAXINTS_M2 = [i-2 for i in MAXINTS]
    MAXINTS_M3 = [i-3 for i in MAXINTS]
    MAXINTS_M4 = [i-4 for i in MAXINTS]


class String:
    FORMAT_STRINGS = ["%n"*20, "%s"*20]
    BIG_STRING = "B"*20000
    MULTIPLIERS = [10, 20, 50]
    PATH_TRAVERSAL = ["../", "/..\/"]

