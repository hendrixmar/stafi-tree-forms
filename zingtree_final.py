import csv
from collections import defaultdict


def get_columns(csv_data: list[list[str]]) -> dict[str, list[int]]:
    column_iterator = enumerate(csv_data[0])
    columns_map = defaultdict(list)

    while True:

        try:
            index, column = next(column_iterator)
        except StopIteration:
            break


        columns_map[column].append(index)
        while index + 1 < len(csv_data[0]) and csv_data[0][index + 1] == '':
            try:
                index, _ = next(column_iterator)
            except StopIteration:
                break
        columns_map[column].append(index)

        print(index, column)

    for e in columns_map.items():
        print(e)

    return columns_map

import itertools

def batched(iterable, n):
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch

with open('complete.csv', 'r') as fp:

    result = list(csv.reader(fp))

    temp = get_columns(result)

    for key, indexes in temp.items():

        for index in batched(indexes,  n=2):
            print(index)

            if index[0] == index[1]:
                print()








