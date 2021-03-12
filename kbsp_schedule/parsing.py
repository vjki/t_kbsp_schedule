#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Source: https://github.com/skvozsneg/t_kbsp_schedule  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import openpyxl
import json 
from os import path, listdir


# --- Functions ---
def write_in_json(json_dir, schedule_d, course):
    """Write groups schedule in json file

    • json_dir - string which contain way to json dir

    • schedule_d - dictionary with groups schedule data

    • course - group number of the course
    """
    json_dir_full = path.join(json_dir, str(course))
    json_name = schedule_d['Group'] + '.json'
    with open(path.join(json_dir_full, json_name), 'w', encoding='utf-8') as f:
        json.dump(schedule_d, f, ensure_ascii=False, indent=4)


def pars_for_cells(schedule_dir):
    """GENERATOR. Gets cells with group name.
    Go throw th 2-nd row in xlsx and catch cells with group names. Yield
    dictionary (d) with file name and cells.
        view(d): (file name): list(cells)

    • schedule_dir - string which contain way to schedule dir

    """
    for sub_dir in range(1, 6):
        current_dir = path.join(schedule_dir, str(sub_dir))
        for file_name in listdir(current_dir):
            full_path = path.join(current_dir, file_name)
            d = {'full_path': full_path, 'course': sub_dir, 'cells': []}
            wb = openpyxl.load_workbook(full_path)
            sheet = wb.active
            for row in sheet.iter_rows(2):
                for cell in row:
                    if cell.value is not None and '-' in str(cell.value):
                        d['cells'].append(cell.coordinate)
                break
            yield d


def pars_main(d_cells, json_dir):
    """Parsing Excel.
    Function collects data from .xlsx file and return it as a list of dictionary.

    • d_cells - dictionary with full path to file and its cells with group name

    • res - list with dictionaries.
            view: [dict, dict, dict, ..., dict]

    • d - dictionary with group schedule data's. Every list there collect four type of information.
        1: Subject name;
        2: Subject type;
        3: Professor name;
        4: Audience;
            view: {'Group'(group name): str,
                    11(monday):{
                        1(first lesson): {
                            111(odd week): list,
                            112(even week): list
                        },
                        2(second lesson): {
                            111(odd week): list,
                            112(even week): list
                        },
                                ...
                        6(sixth lesson): {
                            111(odd week): list,
                            112(even week): list
                        },
                    }
                    12(tuesday):{...}
                    13(wednesday):{...}
                            ...
                    16(saturday):{...}
            }
    """
    full_path = d_cells['full_path']
    cell_coordinate = d_cells['cells']
    course = d_cells['course']
    wb = openpyxl.load_workbook(full_path)
    sheet = wb.active
    for el in cell_coordinate:
        d = {'Group': None,
             11: {
                 1: {111: [],
                     112: []},
                 2: {111: [],
                     112: []},
                 3: {111: [],
                     112: []},
                 4: {111: [],
                     112: []},
                 5: {111: [],
                     112: []},
                 6: {111: [],
                     112: []}},
             12: {
                 1: {111: [],
                     112: []},
                 2: {111: [],
                     112: []},
                 3: {111: [],
                     112: []},
                 4: {111: [],
                     112: []},
                 5: {111: [],
                     112: []},
                 6: {111: [],
                     112: []}},
             13: {
                 1: {111: [],
                     112: []},
                 2: {111: [],
                     112: []},
                 3: {111: [],
                     112: []},
                 4: {111: [],
                     112: []},
                 5: {111: [],
                     112: []},
                 6: {111: [],
                     112: []}},
             14: {
                 1: {111: [],
                     112: []},
                 2: {111: [],
                     112: []},
                 3: {111: [],
                     112: []},
                 4: {111: [],
                     112: []},
                 5: {111: [],
                     112: []},
                 6: {111: [],
                     112: []}},
             15: {
                 1: {111: [],
                     112: []},
                 2: {111: [],
                     112: []},
                 3: {111: [],
                     112: []},
                 4: {111: [],
                     112: []},
                 5: {111: [],
                     112: []},
                 6: {111: [],
                     112: []}},
             16: {
                 1: {111: [],
                     112: []},
                 2: {111: [],
                     112: []},
                 3: {111: [],
                     112: []},
                 4: {111: [],
                     112: []},
                 5: {111: [],
                     112: []},
                 6: {111: [],
                     112: []}},
             }
        count_nmb_weeks, count_weeks, count_lessons = 111, 11, 1
        try:
            xy = openpyxl.utils.coordinate_to_tuple(el)
            d['Group'] = sheet[el].value
            for row in sheet[
                       openpyxl.utils.get_column_letter(xy[1]) + str(xy[0] + 2):
                       openpyxl.utils.get_column_letter(xy[1] + 3) + str(xy[0] + 73)]:
                for cell in row:
                    if cell.value == None:
                        d[count_weeks][count_lessons][count_nmb_weeks].append('-')
                    else:
                         d[count_weeks][count_lessons][count_nmb_weeks].append(cell.value)
                if count_nmb_weeks == 111:
                    count_nmb_weeks += 1
                else:
                    count_nmb_weeks -= 1
                    count_lessons += 1
                if count_lessons > 6:
                    count_weeks += 1
                    count_lessons = 1
            write_in_json(json_dir, d, course)
        except:
            return False
        else:
            pass
