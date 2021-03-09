#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/skvozsneg/t_kbsp_schedule  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import csv
from os.path import join
from rich.table import Table
from rich.console import Console

def display_file_status(schedule_dir):
    """Visualize data from lmod.csv."""
    table = Table(title="Schedule status")
    table.add_column("Course", style="yellow", no_wrap=True)
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Last Modified", style="green", no_wrap=True)
    table.add_column("Last Updated", style="magenta", no_wrap=True)

    with open(join(schedule_dir, 'lmod.csv'), encoding='utf-8') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
            table.add_row(row[0], row[1], row[2], row[3])

    console = Console()
    console.print(table)
