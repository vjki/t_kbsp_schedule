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
from datetime import datetime


# -- Functions --
def disp_greetings(version):
    """Print the intro.

    • version: str - version of program
    """
    dt = datetime.now()
    try:
        with open(os.path.join('core', 'static', 'logo'), 'r') as fr:
            rich.print('\n')
            print(f"<-- IKBSP -->\t\t\t\t\t\t\t{version}")
            for line in fr:
                rich.print(f"[bold red]" + line + "[/bold red]", end="")
            rich.print('\n')
        rich.print(f"[bold]Starts at:[/bold] [bold yellow]{dt.strftime('%d-%m-%Y %H:%M:%S')}[/bold yellow]\n")
        return True
    except:
        return False




