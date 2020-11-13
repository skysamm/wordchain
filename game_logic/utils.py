class bcolors:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def warning(text):
    """
        @input: string text
        @output: None
    """
    print(bcolors.FAIL + text + bcolors.ENDC)

def info(text):
    """
        @input: string text
        @output: None
    """
    print(bcolors.OKGREEN + text + bcolors.ENDC)

def server_print(text):
    """
        @input: string text
        @output: None
    """
    print(bcolors.OKCYAN + text + bcolors.ENDC)

def print_server_response(message):
    """
        @input: string message
        @output: None
    """
    if "1" in message:
        warning("Your word is not a valid word..")
    elif "2" in message:
        warning("Your word has already been used..")
    else:
        server_print(f"Server plays: {message}")