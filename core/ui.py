#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/vjki/t_kbsp_schedule #
# # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import os
from rich import print


# -- Functions --
def disp_greetings(version):
    """Print the intro.

    • version: str - version of program
    """
    with open(os.path.join('core', 'static', 'logo'), 'r') as fr:
        print('\n')
        for line in fr:
            print("[bold red]" + line + "[/bold red]", end="")
        print('\n')



