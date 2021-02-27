#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/vjki/t_kbsp_schedule #
# # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import os
import rich


# -- Functions --
def disp_greetings(version):
    """Print the intro.

    • version: str - version of program
    """
    with open(os.path.join('core', 'static', 'logo'), 'r') as fr:
        rich.print('\n')
        print(f"<-- IKBSP -->\t\t\t\t\t\t\t{version}")
        for line in fr:
            rich.print(f"[bold red]" + line + "[/bold red]", end="")
        rich.print('\n')



