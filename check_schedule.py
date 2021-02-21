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
commands = [
    'get',
    'check',
    'exit'
]


# -- classes --
class KbspSchedule:
    def __init__(self):
        pass


# -- functions --
def com_check():
    getting.check_schedule(path.join(".", "schedule"))


def com_get():
        getting.get_schedule(path.join(".", "schedule"))
        getting.check_schedule(path.join(".", "schedule"))


# -- launching --
if __name__ == "__main__":
    ui.greetings(version)
    while True:
        command = ui.get_line()
        if command == 'get':
            com_get()

        if command == 'check':
            com_check()
        
        if command == 'exit':
            ui.print_line("Bye!")
            break
        
        if command not in commands:
            ui.print_line(f'I don not know {command} command :(', end='\n\n')
