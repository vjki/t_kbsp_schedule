#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/skvozsneg/t_kbsp_schedule  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import re

from rich import print
from datetime import datetime
from os import path, mkdir, listdir
from kbsp_schedule import getting, parsing, updating
from core.ui import c_print, disp_greetings, user_input
from core.unicui import display_file_status, display_full_group_schedule, display_dx_group_schedule, display_upd_file_status


# -- globals --
version = 'v1.0'
current_datetime = datetime.now()
commands = {
    'group': 'Get schedule of current group.',
    'today': 'Get todays schedule of the week.',
    'tomorrow': 'Get tomorrow schedule of the week.',
    'get': 'Get all schedules files and file status from internet.',
    'update': 'Show which files need updating.',
    'view': 'Check a the file status',
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
            for sub_dir in range(1, 6):
                mkdir(path.join(self.schedule_dir, str(sub_dir)))
                mkdir(path.join(self.json_dir, str(sub_dir)))
        except FileExistsError:
            self.FIRST_TIME = False

        if self.FIRST_TIME:
            f = open(path.join(self.schedule_dir, 'lmod.csv'), 'w')
            f.close()
            self.com_get()

    def com_get(self):
        """Downloading last version of files and pars them into jsons."""
        assert getting.get_schedule(
            self.schedule_dir), "Cannot download the files..."
        for d in parsing.pars_for_cells(self.schedule_dir):
            parsing.pars_main(d, self.json_dir)
        getting.check_schedule(self.schedule_dir)

    def com_upd(self):
        """Smart Updating files."""
        return updating.update(self.schedule_dir)

    def com_group(self, group_name: str):
        """Get json file groups"""
        self.file_name, self.course = self.get_file_name_by_group(group_name)
        self.path_to_file = path.join(
            self.json_dir, str(self.course), self.file_name)

        assert display_full_group_schedule(
            self.path_to_file, group_name), "Cannot display full group schedule..."

    def com_tt(self, group_name: str, dx=0):
        """Display schdule for today + dx & for current group"""
        self.file_name, self.course = self.get_file_name_by_group(group_name)
        self.path_to_file = path.join(
            self.json_dir, str(self.course), self.file_name)

        assert display_dx_group_schedule(
            self.path_to_file, group_name, dx=dx), "Cannot display schedule for group..."

    def com_view(self):
        """Display lmod.csv"""
        assert display_file_status(
            schdeule.schedule_dir), "Cannot display the file status..."

    # TECHNICAL TOOLS

    def get_file_name_by_group(self, group_name: str):
        course = int(current_datetime.year) % 100 - \
            int(group_name.split('-')[-1])
        for myfile in listdir(path.join(self.json_dir, str(course))):
            if group_name.upper() == myfile.split()[0].upper():
                return myfile, course


# -- launching --
disp_greetings(version)
schdeule = KbspSchedule()
display_file_status(schdeule.schedule_dir)
if schdeule.FIRST_TIME:
    c_print("[bold]Hello and welcome![/bold] Type [bold green]> [/bold green]help comand to see what i can.")

while True:
    command = user_input()

    if command == 'group':
        c_print("Please enter the name of youre group (example: БИСО-02-16)")
        group_name = user_input()
        try:
            schdeule.com_group(group_name)
        except AssertionError as e:
            c_print(f"[bold red]Fail.[/bold red] {e}", border='red')

    if command == 'today':
        c_print("Please enter the name of youre group (example: БИСО-02-16)")
        group_name = user_input()
        try:
            schdeule.com_tt(group_name)
        except AssertionError as e:
            c_print(f"[bold red]Fail.[/bold red] {e}", border='red')

    if command == 'tomorrow':
        c_print("Please enter the name of youre group (example: БИСО-02-16)")
        group_name = user_input()
        try:
            schdeule.com_tt(group_name, dx=1)
        except AssertionError as e:
            c_print(f"[bold red]Fail.[/bold red] {e}", border='red')

    if command == 'get':
        try:
            schdeule.com_get()
            c_print("[bold green]OK.[/bold green] New schedules was up to date. New status of files will be displayed...", border="green")
            display_file_status(schdeule.schedule_dir)
        except AssertionError as e:
            c_print(f"[bold red]Fail.[/bold red] {e}", border='red')
    
    if command == 'update':
        try:
            d_upd_file_status = schdeule.com_upd()
            c_print("[bold green]OK.[/bold green] The file update status will be displayed...",  border="green")
            display_upd_file_status(d_upd_file_status)
        except AssertionError as e:
            c_print(f"[bold red]Fail.[/bold red] {e}", border='red')

    if command == 'view':
        schdeule.com_view()

    if command == 'help':
        res = []
        for k, v in commands.items():
            res.append(f"[bold]{k}[/bold] - {v}")
        c_print('\n'.join(res))

    if command == 'exit':
        c_print("[bold]Bye![/bold]")
        break

    if command not in commands:
        c_print(
            f'I don not know [bold green]> [/bold green]{command} command :( Type [bold]help[/bold] for commands list')
