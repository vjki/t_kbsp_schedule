#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/skvozsneg/t_kbsp_schedule  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import re
import csv
import time
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from openpyxl import load_workbook
from os import path, listdir, remove


# --- globals ---
url = 'https://www.mirea.ru/schedule/'


# --- function ---
def check_schedule(schedule_dir: str) -> bool:
    """Write in lmod.csv.
    Check last modified and last update of all files and write it into lmod.csv.
        view(lmod.csv): (course),(file name),(last modified),(last update)

    • schedule_dir - string which contain way to schedule dir

    """
    try:
        remove(path.join(schedule_dir, 'lmod.csv'))
        for sub_dir in range(1, 6):
            current_dir = path.join(schedule_dir, str(sub_dir))
            for file_name in listdir(current_dir):
                full_path = path.join(current_dir, file_name)
                wb = load_workbook(full_path, read_only=True)
                last_modified = wb.properties.modified
                last_update = datetime.fromtimestamp(path.getmtime(full_path))
                with open(path.join(schedule_dir, 'lmod.csv'), 'a', encoding='utf-8') as f:
                    file_writer = csv.writer(f, lineterminator="\r")
                    file_writer.writerow([sub_dir, file_name, last_modified, last_update])
        wb.close()
        return True
    except:
        return False


def get_schedule(schedule_dir: str) -> bool:
    """Downloading schedules.
    Download kbsp schedules from site mirea and put them into
    directories.
        View: schedule -> 1(number of semester)

    • schedule_dir - string which contain way to schedule dir

    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features="html.parser")
        links = soup.find_all(href=re.compile(r"КБиСП.*xlsx"))
        for link in links:
            file_name = link.get('href').split('/')[-1]
            with open(path.join(schedule_dir, file_name.split()[1], file_name), 'wb') as f:
                urf = requests.get(link.get('href'))
                f.write(urf.content)
        return True
    except:
        return False
