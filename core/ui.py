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
    """Print the intro.

    • version: str - version of program
    """
    with open(os.path.join('core', 'static', 'logo'), 'r') as fr:
        print('\n')
        for line in fr:
            print(Fore.BLUE + line, end="")
        print('\n')
    print(
        Fore.WHITE + Style.DIM + "             by" + Style.RESET_ALL + Style.BRIGHT + Fore.WHITE + " vjki " + Style.RESET_ALL + Style.DIM + Fore.WHITE + "(@ikjvvjki)" + Style.RESET_ALL,
        end="\n")
    print(Fore.CYAN + "  ---------------------------------------")
    print(Fore.CYAN + f"  | {version} | ", end="")
    print(Fore.CYAN + Style.DIM + "Monitors the schedule change" + Style.RESET_ALL + Fore.CYAN + " |")
    print(Fore.CYAN + "  ---------------------------------------", end="\n\n")


def print_line(message, status='info'):
    """Print text message in console.

    """
    if status == 'info':
        print(Style.DIM + Fore.WHITE + '  [' + Fore.BLUE + 'i' + Fore.WHITE + ']: ' + Style.RESET_ALL + message)
    elif status == 'warning':
        print(Style.DIM + Fore.WHITE + '  [' + Fore.RED + '!' + Fore.WHITE + ']: ' + Style.RESET_ALL + message)


def get_line(message=""):
    x = input(Style.DIM + Fore.WHITE + '  [' + Fore.GREEN + '>' + Fore.WHITE + '] ' + Style.RESET_ALL + message)
    return x
