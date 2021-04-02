#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/skvozsneg/t_kbsp_schedule  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import csv
import shutil
import requests

from os import mkdir, path
from datetime import datetime
from openpyxl import load_workbook

# -- globals --
temp_dir_name = 'temp'

# -- functions --
def get_file_links(schedule_dir: str) -> tuple:
    """Generator."""
    lmod_dir = path.join(schedule_dir, 'lmod.csv')
    with open(lmod_dir, encoding='utf-8') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
            yield row[0], row[1] 


def get_file_lenght(link: str):
    responce = requests.head(link, allow_redirects=True)
    size = responce.headers['Content-Length']
    return int(size)


def update_status(schedule_dir: str) -> dict:
    d = {}
    for cource, link in get_file_links(schedule_dir):
        file_name = link.split('/')[-1]
        full_path = path.join(schedule_dir, cource, file_name)
        if path.getsize(full_path) != get_file_lenght(link):
            d.update({file_name: 1})
        else:
            d.update({file_name: 0})
    return d


def update(schedule_dir: str, d: dict):
    try:
        for cource, link in get_file_links(schedule_dir):
            file_name = link.split('/')[-1]
            if d[file_name] == 1:
                full_path = path.join(schedule_dir, cource, file_name)
                with open(full_path, 'wb') as f:
                    urf = requests.get(link)
                    f.write(urf.content)
        return True
    except:
        return False



if __name__ == "__main__":
    print(update_status(path.join('schedule')))
