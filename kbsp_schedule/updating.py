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
import shutil
import requests

from os import mkdir, path
from bs4 import BeautifulSoup
from datetime import datetime
from openpyxl import load_workbook

# -- globals --
temp_dir_name = 'temp'
url = 'https://www.mirea.ru/schedule/'


# -- functions --
def get_file_links(schedule_dir: str) -> tuple:
    """Generator."""
    lmod_dir = path.join(schedule_dir, 'lmod.csv')
    with open(lmod_dir, encoding='utf-8') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
            yield row[0], row[1] 


def get_file_status(link: str):
    responce = requests.head(link, allow_redirects=True)
    status = responce.status_code
    return status


def update_status(schedule_dir: str) -> dict:
    d = {}
    for course_link in get_file_links(schedule_dir):
        link = course_link[1]
        file_name = link.split('/')[-1]
        link_status = get_file_status(link)
        if link_status == 404:
            d.update({file_name: 1})
        elif link_status == 200:
            d.update({file_name: 0})
    return d


def update(schedule_dir: str, d: dict):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features="html.parser")
        links = soup.find_all(href=re.compile(r"КБиСП.*xlsx"))
        for link in links:
            file_name = link.get('href').split('/')[-1]
            if d[file_name] == 1:
                with open(path.join(schedule_dir, file_name.split()[1], file_name), 'wb') as f:
                    urf = requests.get(link.get('href'))
                    f.write(urf.content)

        # for cource, link in get_file_links(schedule_dir):
        #     file_name = link.split('/')[-1]
        #     if d[file_name] == 1:
        #         full_path = path.join(schedule_dir, cource, file_name)
        #         with open(full_path, 'wb') as f:
        #             urf = requests.get(link)
        #             f.write(urf.content)
        return True
    except:
        return False



if __name__ == "__main__":
    print(update_status(path.join('schedule')))
