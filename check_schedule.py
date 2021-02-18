#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/vjki/t_kbsp_schedule #
# # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
from core import ui
from kbsp_schedule import getting, parsing
from os import path

# -- globals --
version = 'v1.0'


# -- classes --
class KbspSchedule:
    def __init__(self):
        pass


# -- functions --


# -- launching --
if __name__ == "__main__":
    ui.greetings(version)
    x = ui.get_line("Get it?: ")
    ui.print_line(x)
