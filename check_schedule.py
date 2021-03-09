#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/skvozsneg/t_kbsp_schedule  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import re
from datetime import datetime
from core.ui import c_print, disp_greetings
from core.unicui import display_file_status
from rich import print
from kbsp_schedule import getting, parsing
from os import path, mkdir, listdir

# -- globals --
version = 'v1.0'
current_datetime = datetime.now()
commands = {
    'group': 'Get schedule of current group.',
    'update': 'Update all schedules files. To check int go [home folder]/schedule.',
    'check': 'Get time last modified and update schedule.',
    'help': 'Get list of all commands.',
    'exit': 'Exit program.'
}


# -- class --
class KbspSchedule:
    def __init__(self):
        """Creating environment."""
        self.FIRST_TIME = True
        # Paths
        self.abs_path = path.abspath('.')
        self.schedule_dir = path.join(self.abs_path, 'schedule')
        self.json_dir = path.join(self.abs_path, 'json')
        try:
            mkdir('schedule')
            mkdir('json')
            for subdir in range(1, 6):
                mkdir(path.join(self.schedule_dir, str(subdir)))
                mkdir(path.join(self.json_dir, str(subdir)))
        except FileExistsError:
            self.FIRST_TIME = False
        if self.FIRST_TIME:
            f = open(path.join(self.schedule_dir, 'lmod.csv'), 'w')
            f.close()
            self.com_udate()
            self.com_check()

    def com_check(self):
        """Update lmode.csv file."""
        return getting.check_schedule(self.schedule_dir)

    def com_udate(self):
        """Downloading last version of files and pars them into jsons."""
        if not getting.get_schedule(self.schedule_dir):
            return False
        for d in parsing.pars_for_cells(self.schedule_dir):
            parsing.pars_main(d, self.json_dir)
        return True

    def schedule_by_group(self, group_name):
        """Get json file groups"""
        self.course = int(current_datetime.year) % 100 - \
            int(group_name.split('-')[-1])
        for file in listdir(path.join(self.json_dir, str(self.course))):
            if group_name == file.split()[0].upper():
                self.file_name = file
                break
        return path.join(self.json_dir, str(self.course), self.file_name)


# -- launching --
disp_greetings(version)
schdeule = KbspSchedule()
display_file_status(schdeule.schedule_dir)
if schdeule.FIRST_TIME:
    c_print("[bold]Hello and welcome![/bold] Type |[bold green]> [/bold green]help| comand to see what i can.")

while True:
    print("[bold green]> [/bold green]", end='')
    command = input().strip().lower()

    if command == 'group':
        c_print("Please enter the name of youre group (example: БИСО-02-16)")
        print("[bold green]> [/bold green]", end='')
        c_print(
            f"OUTPUT {schdeule.schedule_by_group(input().strip().upper())}")

    if command == 'update':
        if not schdeule.com_udate():
            c_print(
                "[bold red]Fail.[/bold red] Something went wrong... ", border='red')
        else:
            c_print(
                "[bold green]OK.[/bold green] New schedules was up to date. Type |[bold green]> [/bold green]group| to see the current group schedule.", border="green")

    if command == 'check':
        if not schdeule.com_check():
            c_print(
                "[bold red]Fail.[/bold red] Something went wrong... (in getting.py)", border='red')
        else:
            c_print(
                "[bold green]OK.[/bold green] New status of files will be displayed...", border='green')
            display_file_status(schdeule.schedule_dir)

    if command == 'exit':
        c_print("[bold]Bye![/bold]")
        break

    if command == 'help':
        res = []
        for k, v in commands.items():
            res.append(f"[bold]{k}[/bold] - {v}")
        c_print('\n'.join(res))

    if command not in commands:
        c_print(
            f'I don not know |[bold green]> [/bold green]{command}| command :( Type [bold]help[/bold] for commands list')
