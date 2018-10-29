from colorama import Fore, Style
from colorama import init

colormap = {"red": Fore.RED, "blue": Fore.BLUE, "yellow": Fore.YELLOW}

def color_string(color, string):
    return colormap[color] + string + Style.RESET_ALL

def reset():
    print(Style.RESET_ALL, end="")