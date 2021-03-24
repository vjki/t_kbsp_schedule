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

# TODO: Необходимо сделать "умное" обновление.
# Скачивание файлов во временное хранилище и сравнение
# их последней даты изменения с той, что хранится в lmod.
# Если даты на файлах различаются ->
#       обновляем этот файл в основном хранилище;
#       обновляем все jsonы тех групп, которые были в файлах;
#       выводим сообщения об обновленных файлах.
# Иначе ->
#       выводим сообщение о том, что все файлы свежие.

# -- globals --
temp_dir_name = 'temp'

# -- functions --
def get_file_links(lmod_dir: str) -> str:
    """Generator."""
    with open(lmod_dir, encoding='utf-8') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
            yield row[1]


def download_tempfiles(link: str) -> str:
    file_name = link.split('/')[-1]
    try:
        with open(path.join(temp_dir_name, file_name), 'wb') as f:
            urf = requests.get(link)
            f.write(urf.content)
        return file_name
    except:
        return None


def get_last_time_modified(full_path: str) -> datetime:
    wb = load_workbook(full_path, read_only=True)
    last_modified = wb.properties.modified
    wb.close()
    return last_modified


# -- launch --
def update(schedule_dir: str) -> dict:
    d = dict()
    lmod_dir = path.join(schedule_dir, 'lmod.csv')
    mkdir(temp_dir_name)
    for file_link in get_file_links(lmod_dir):
        file_name = download_tempfiles(file_link)
        if file_name is None:
            shutil.rmtree('temp')
            raise AssertionError("Error downloading files...")
        else:
            temp_to_file = path.join(temp_dir_name, file_name)
            sched_to_file = path.join(schedule_dir, file_name.split()[1], file_name)
            if get_last_time_modified(temp_to_file) > get_last_time_modified(sched_to_file):
                d.update({file_name: 1})
            else:
                d.update({file_name: 0})
    shutil.rmtree('temp')
    return d


if __name__ == "__main__":
    print(update(path.join('schedule')))
