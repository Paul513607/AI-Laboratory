import csv
import numpy as np


def parse_data(file_name):
    attributes_arr = []
    classes_arr = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) == 0:
                break
            attributes_arr += [[row[0], row[1], row[2], row[3]]]
            classes_arr += [row[4]]
    return np.array(attributes_arr), np.array(classes_arr)