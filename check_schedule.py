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
from rich.panel import Panel
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


# -- class --
class KbspSchedule:
    def __init__(self):
        """Creating environment.

        """
        self.FIRST_TIME = True
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

    def display_status(self):
        """Visualize data from lmod.csv.

        """
        table = Table(title="Schedule status")
        table.add_column("Course", style="yellow", no_wrap=True)
        table.add_column("File", style="cyan", no_wrap=True)
        table.add_column("Last Modified", style="green", no_wrap=True)
        table.add_column("Last Updated", style="magenta", no_wrap=True)

        with open(path.join(self.schedule_dir, 'lmod.csv'), encoding='utf-8') as rf:
            reader = csv.reader(rf, delimiter=',')
            for row in reader:
                table.add_row(row[0], row[1], row[2], row[3])

        console = Console()
        console.print(table)


# -- functions --
def c_print(message, border='white', end='\n\n'):
    print(Panel(message, border_style=border, expand=False), end=end)


# -- launching --
ui.disp_greetings(version)
schdeule = KbspSchedule()
if schdeule.display_status():
    c_print("[bold red]Fail.[/bold red] Something went wrong... (in ui.py)", border='red')
if schdeule.FIRST_TIME:
    c_print("[bold]Hello and welcome![/bold] Type |[bold green]> [/bold green]help| comand to see what i can.")

while True:
    print("[bold green]> [/bold green]", end='')
    command = input().strip()
    if command == 'get':
        if not schdeule.com_get():
            c_print(
                "[bold red]Fail.[/bold red] Something went wrong... (in getting.py)", border='red')
        else:
            c_print(
                "[bold green]OK.[/bold green] New schedules was up to date. Type check to see last modified time of files.", border="green")

    if command == 'check':
        if not schdeule.com_check():
            c_print(
                "[bold red]Fail.[/bold red] Something went wrong... (in getting.py)", border='red')
        else:
            c_print(
                "[bold green]OK.[/bold green] New status of files will be displayed...", border='green')
            schdeule.display_status()

    if command == 'exit':
        c_print("[bold]Bye![/bold]")
        break

    if command == 'help':
        for k, v in commands.items():
            c_print(f"[bold]{k}[/bold] - {v}")

    if command not in commands:
        c_print(
            f'I don not know |[bold green]> [/bold green]{command}| command :( Type [bold]help[/bold] for commands list')
