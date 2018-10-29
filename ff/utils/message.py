from utils import colors
BORDER = "-"*40

def alert(message):
    prompt = "[!] "
    msg = colors.color_string("red", prompt+message)
    print(msg)

def status(message):
    prompt = "[+] "
    msg = prompt + message
    print(msg)
