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
from os import path, mkdir

# -- globals --
version = 'v1.0'
commands = {
    'help': 'Get list of all commands.',
    'get': 'Get all schedules files. To check int go [program folder]/schedule.',
    'check': 'Get time last modified and update schedule.',
    'exit': 'Exit program.'
}


# -- classes --
class KbspSchedule:
    def __init__(self):
        """Creating environment.

        """
        try:
            mkdir('schedule')
            mkdir('json')
            for subdir in range(1, 6):
                mkdir(path.join('.', 'schedule', str(subdir)))
                mkdir(path.join('.', 'json', str(subdir)))
        except FileExistsError:
            pass
        f = open(path.join('.', 'schedule', 'lmod.csv'), 'w')
        f.close()


# -- functions --
def com_check():
    getting.check_schedule(path.join(".", "schedule"))


def com_get():
    getting.get_schedule(path.join(".", "schedule"))
    getting.check_schedule(path.join(".", "schedule"))


# -- launching --
if __name__ == "__main__":
    launch = KbspSchedule()
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

        if command == 'help':
            for k, v in commands.items():
                print(f'{k} - {v}')

        if command not in commands:
            ui.print_line(f'I don not know {command} command :(Type \'help\' for commands list', end='\n\n')
