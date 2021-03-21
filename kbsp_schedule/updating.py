#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/skvozsneg/t_kbsp_schedule  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import csv

from os import mkdir, path

# TODO: Необходимо сделать "умное" обновление.
# Скачивание файлов во временное хранилище и сравнение
# их последней даты изменения с той, что хранится в lmod.
# Если даты на файлах различаются ->
#       обновляем этот файл в основном хранилище;
#       обновляем все jsonы тех групп, которые были в файлах;
#       выводим сообщения об обновленных файлах.
# Иначе ->
#       выводим сообщение о том, что все файлы свежие.

# -- class ---
class UpdatingFiles():
    def __init__(self):
        self.links = []
        mkdir('temp')


    def csv_read(self):
        with open(path.join('schedule', 'lmod.csv'), encoding='utf-8') as rf:
            reader = csv.reader(rf, delimiter=',')
            for row in reader:
                self.links.append(row[1])

    
    def download(self, links):
        for link in links:
            with open('temp', 'wb') as f:
                urf = requests.get(link.get('href'))
                f.write(urf.content)
        
