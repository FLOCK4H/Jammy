RED = "\033[31m"
GREEN = '\033[32m'
BLUE = '\033[34m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = "\033[0m"
BRIGHT = '\033[1m'
YELLOW = '\033[33m'
MAGENTA = '\033[35m'
LIGHT_GREEN = '\033[92m'
LIGHT_BLUE = '\033[94m'
LIGHT_CYAN = '\033[96m'
LIGHT_RED = '\033[91m'
LIGHT_MAGENTA = '\033[95m'
LIGHT_YELLOW = '\033[93m'
LIGHT_WHITE = '\033[97m'
BLACK = '\033[30m'

def cprint(string):
    print(f'{RESET}{CYAN}[+]{RESET}' + ' ' + f'{BRIGHT}{BLUE}{string}{RESET}')

def wprint(string):
    print(f'{WHITE}[+]{RESET}' + ' ' + f'{RED}{string}{RESET}')

def iprint(string):
    print(f'{GREEN}[{RED}JAMMY{GREEN}]{RESET}' + ' ' + f'{WHITE}{BRIGHT}{string}{BRIGHT}{RESET} ')

def cinput(string):
    r = input(f'{GREEN}[>]{RESET}' + ' ' + f'{CYAN}{string}:{BRIGHT}{RESET} ')
    return r