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

def std_err(err_message):
    formatted_msg = ""
    multiline_msg = str(err_message).split("\n")
    for line in multiline_msg:
        formatted_msg += "\t|"+line+"\n"
    print(formatted_msg)
    

