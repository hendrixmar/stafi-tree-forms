import csv

with open('nuevo_csv.csv', 'r') as fp:
    reader = [list(row)[3:] for row in csv.reader(fp)]

    print(dict(zip(reader[0], reader[2])))

