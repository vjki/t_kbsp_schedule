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
from core.unicui import display_file_status, display_full_group_schedule, display_today_group_schedule
from rich import print
from kbsp_schedule import getting, parsing
from os import path, mkdir, listdir

# -- globals --
version = 'v1.0'
current_datetime = datetime.now()
commands = {
    # TODO: Создать кнопки:
    # [DONE]            "Сегодня" - расписание на текущий день недели для определеннной группы.
    # [...]             "Завтра" - тоже самое, что и "Сегодня", но на день вперед.
    # [DONE]            "Группа" - полное расписание для определенной группы.
    # [NO TERMINAL]     "Файл" - скчаивается(ются) файл(ы) конкретного курса.
    # [DONE]            "Обновление" - обновления файлов с раписанием + lmod.csv (в чатах релизовать по расписанию).
    'group': 'Get schedule of current group.',
    'today': 'Get todays schedule of the week.',
    'tomorrow': 'Get tomorrow schedule of the week.',
    'update': 'Update all schedules files and file status.',
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

    def com_udate(self):
        """Downloading last version of files and pars them into jsons."""
        if not getting.get_schedule(self.schedule_dir):
            return False
        for d in parsing.pars_for_cells(self.schedule_dir):
            parsing.pars_main(d, self.json_dir)
        if not getting.check_schedule(self.schedule_dir):
            return False
        return True

    def com_group(self, group_name: str):
        """Get json file groups"""
        try:
            self.file_name = self.get_file_name_by_group(group_name)
            display_full_group_schedule(
                path.join(self.json_dir, str(self.course), self.file_name), group_name)
            return True
        except:
            return False

    def com_today(self, group_name: str):
        """Get schedule for today from json"""
        try:
            self.file_name = self.get_file_name_by_group(group_name)
            display_today_group_schedule(
                path.join(self.json_dir, str(self.course), self.file_name), group_name)
            return True
        except:
            return False

    def com_tomorrow(self, group_name: str):
        """Get schedule for today from json"""
        try:
            self.file_name = self.get_file_name_by_group(group_name)
            display_today_group_schedule(
                path.join(self.json_dir, str(self.course), self.file_name), group_name, dx=1)
            return True
        except:
            return False

    # TECHNICAL TOOLS

    def get_file_name_by_group(self, group_name: str) -> str:
        self.course = int(current_datetime.year) % 100 - \
            int(group_name.split('-')[-1])
        for file in listdir(path.join(self.json_dir, str(self.course))):
            if group_name == file.split()[0].upper():
                return file


# -- launching --
disp_greetings(version)
schdeule = KbspSchedule()
display_file_status(schdeule.schedule_dir)
if schdeule.FIRST_TIME:
    c_print("[bold]Hello and welcome![/bold] Type [bold green]> [/bold green]help comand to see what i can.")

while True:
    print("[bold green]> [/bold green]", end='')
    command = input().strip().lower()

    if command == 'group':
        c_print("Please enter the name of youre group (example: БИСО-02-16)")
        print("[bold green]> [/bold green]", end='')
        group_name = input().strip().upper()
        if not schdeule.com_group(group_name):
            c_print(
                f"[bold red]Fail.[/bold red] Can not find the {group_name} group... ", border='red')
        

    if command == 'today':
        c_print("Please enter the name of youre group (example: БИСО-02-16)")
        print("[bold green]> [/bold green]", end='')
        group_name = input().strip().upper()
        if not schdeule.com_today(group_name):
            c_print(
                f"[bold red]Fail.[/bold red] Can not find the {group_name} group... ", border='red')

    if command == 'tomorrow':
        c_print("Please enter the name of youre group (example: БИСО-02-16)")
        print("[bold green]> [/bold green]", end='')
        group_name = input().strip().upper()
        if not schdeule.com_tomorrow(group_name):
            c_print(
                f"[bold red]Fail.[/bold red] Can not find the {group_name} group... ", border='red')

    if command == 'update':
        if not schdeule.com_udate():
            c_print(
                "[bold red]Fail.[/bold red] Something went wrong... ", border='red')
        else:
            c_print(
                "[bold green]OK.[/bold green] New schedules was up to date. New status of files will be displayed...", border="green")
            display_file_status(schdeule.schedule_dir)

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
