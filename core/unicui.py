#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/skvozsneg/t_kbsp_schedule  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import csv
import json

from os.path import join
from rich.table import Table
from datetime import datetime
from rich.console import Console

def display_upd_file_status(d: dict):
    table = Table(title="Update status")
    table.add_column("File Name", style="yellow", no_wrap=True)
    table.add_column("Update status", style="green", no_wrap=True)

    for k, v in d.items():
        table.add_row(k, "Need update!" if v == 1 else "Don't need updating")
    
    console = Console()
    console.print(table)

    return True


def display_file_status(schedule_dir):
    """Visualize data from lmod.csv."""
    table = Table(title="Schedule status")
    table.add_column("Course", style="yellow", no_wrap=True)
    table.add_column("Link", style="cyan", no_wrap=True)
    table.add_column("Last Modified", style="green", no_wrap=True)
    table.add_column("Last Updated", style="magenta", no_wrap=True)

    with open(join(schedule_dir, 'lmod.csv'), encoding='utf-8') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
            table.add_row(row[0], row[1], row[2], row[3])

    console = Console()
    console.print(table)

    return True


def display_full_group_schedule(json_file_path, group_name):
    """Visualize schedule in readable form for current group."""
    codes = {
        1: '1 пара – 9:00-10:30',
        2: '2 пара – 10:40-12:10',
        3: '3 пара – 12:40-14:10',
        4: '4 пара – 14:20-15:50',
        5: '5 пара – 16:20-17:50',
        6: '6 пара – 18:00-19:30',
        11: 'Понедельник',
        12: 'Вторник',
        13: 'Среда',
        14: 'Четверг',
        15: 'Пятница',
        16: 'Суббота'
        # 111: 'Нечетная неделя',
        # 112: 'Четная неделя'
    }

    def dfgs_odd_even(odd: bool):
        title_week, oe = 'Четная', '112'
        if odd:
            title_week = 'Нечетная'
            oe = '111'
        table = Table(title=f"{group_name} {title_week} неделя")
        table.add_column("День недели", style="yellow", no_wrap=True)
        table.add_column("Пары и время", style="cyan", no_wrap=True)

        table.add_column("Предмет", style="magenta", no_wrap=True)
        table.add_column("Тип", style="green", no_wrap=True)
        table.add_column("Преподаватель", style="green", no_wrap=True)
        table.add_column("Аудитория", style="magenta", no_wrap=True)

        with open(json_file_path, 'r', encoding='utf-8') as rf:
            data = json.loads(rf.read())
            for week in range(11, 17):
                for lesson in range(1, 7):
                    table.add_row(
                        codes[week],
                        codes[lesson],
                        str(data[str(week)][str(lesson)][oe][0]),
                        str(data[str(week)][str(lesson)][oe][1]),
                        str(data[str(week)][str(lesson)][oe][2]),
                        str(data[str(week)][str(lesson)][oe][3]))
                    table.add_row(" ", " ", " ", " ", " ", " ")
                table.add_row("###\n", "###\n", "###\n", "###\n", "###\n", "###\n")

        console = Console()
        console.print(table)
    
    dfgs_odd_even(True)
    dfgs_odd_even(False)

    return True



def display_dx_group_schedule(json_file_path: str, group_name: str, dx=0):
    """Visualize todays schedule in readable form for current group."""
    codes = {
        1: '1 пара – 9:00-10:30',
        2: '2 пара – 10:40-12:10',
        3: '3 пара – 12:40-14:10',
        4: '4 пара – 14:20-15:50',
        5: '5 пара – 16:20-17:50',
        6: '6 пара – 18:00-19:30',
        11: 'Понедельник',
        12: 'Вторник',
        13: 'Среда',
        14: 'Четверг',
        15: 'Пятница',
        16: 'Суббота',
    }

    def ddgs_odd_even(odd: bool, week: int):
        title_week, oe = 'Четная', '112'
        if odd:
            title_week = 'Нечетная'
            oe = '111'
        table = Table(title=f"{codes[week]} - {group_name} {title_week} неделя")
        table.add_column("Пары и время", style="cyan", no_wrap=True)

        table.add_column("Предмет", style="magenta", no_wrap=True)
        table.add_column("Тип", style="green", no_wrap=True)
        table.add_column("Преподаватель", style="green", no_wrap=True)
        table.add_column("Аудитория", style="magenta", no_wrap=True)

        with open(json_file_path, 'r', encoding='utf-8') as rf:
            data = json.loads(rf.read())
            for lesson in range(1, 7):
                table.add_row(
                    codes[lesson],
                    str(data[str(week)][str(lesson)][oe][0]),
                    str(data[str(week)][str(lesson)][oe][1]),
                    str(data[str(week)][str(lesson)][oe][2]),
                    str(data[str(week)][str(lesson)][oe][3]))
                table.add_row(" ", " ", " ", " ", " ", " ")

        console = Console()
        console.print(table)

    week = 11 + (datetime.today().weekday() + dx) % 7
    if week > 16:
        console = Console()
        console.print("Воскресенье - Weekend!")
    else:
        ddgs_odd_even(True, week)
        ddgs_odd_even(False, week)

    return True
