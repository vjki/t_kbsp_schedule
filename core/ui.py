#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/vjki/t_kbsp_schedule #
# # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import os
from colorama import init, Fore, Back, Style

init()


# -- Functions --
def greetings(version):
    with open(os.path.join('core', 'static', 'logo'), 'r') as fr:
        print('\n')
        for line in fr:
            print(Fore.BLUE + line, end="")
        print('\n')
    print(Fore.WHITE + Style.DIM + "             by" + Style.RESET_ALL + Style.BRIGHT + Fore.WHITE + " vjki " + Style.RESET_ALL + Style.DIM + Fore.WHITE + "(@ikjvvjki)" + Style.RESET_ALL, end="\n")
    print(Fore.CYAN + "  ---------------------------------------")
    print(Fore.CYAN + f"  | {version} | ", end="")
    print(Fore.CYAN + Style.DIM + "Monitors the schedule change" + Style.RESET_ALL + Fore.CYAN + " |")
    print(Fore.CYAN + "  ---------------------------------------")
