#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/vjki/t_kbsp_schedule #
# # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import csv
from core import ui
from rich import print
from rich.table import Table
from rich.console import Console
from kbsp_schedule import getting
from os import path, mkdir

# -- globals --
version = 'v1.0'
commands = {
    'help': 'Get list of all commands.',
    'get': 'Get all schedules files. To check int go [home folder]/schedule.',
    'check': 'Get time last modified and update schedule.',
    'exit': 'Exit program.'
}
FIRST_TIME = True


# -- classes --
class KbspSchedule:
    def __init__(self):
        """Creating environment.

        """
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
            FIRST_TIME = False
        if FIRST_TIME:
            self.com_get()
            self.com_check()

    def com_check(self):
        """Update lmode.csv file.


        """
        return getting.check_schedule(self.schedule_dir)

    def com_get(self):
        """Downloading last version of files.

        """
        return getting.get_schedule(self.schedule_dir)


# -- functions --
def display_status():
    """Visualize data from lmod.csv.

    """
    table = Table(title="Schedule status")
    table.add_column("Course", style="yellow", no_wrap=True)
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Last Modified", style="green", no_wrap=True)
    table.add_column("Last Updated", style="magenta", no_wrap=True)

    with open(path.join('.', 'schedule', 'lmod.csv'), encoding='utf-8') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
            table.add_row(row[0], row[1], row[2], row[3])

    console = Console()
    console.print(table)


# -- launching --
if __name__ == "__main__":
    ui.disp_greetings(version)
    schdeule = KbspSchedule()
    display_status()

    while True:
        print("[bold green]> [/bold green]", end='')
        command = input().strip()
        if command == 'get':
            if not schdeule.com_get():
                print("\t[bold red]Fail.[/bold red] Something went wrong... (in getting.py)")
            print("\t[bold green]OK.[/bold green] New schedules was up to date. Type check to see last modified time of files.")

        if command == 'check':
            if not schdeule.com_check():
                print("\t[bold red]Fail.[/bold red] Something went wrong... (in getting.py)")
                print("\tOld status of files will be displayed...")
            print("\t[bold green]OK.[/bold green] New status of files will be displayed...", end="\n\n")
            display_status()

        if command == 'exit':
            print("\t[bold red]Bye![/bold red]")
            break

        if command == 'help':
            for k, v in commands.items():
                print(f"\t'{k}' - {v}")

        if command not in commands:
            print(
                f'\tI don not know {command} command :( Type \'help\' for commands list', end='\n\n')
