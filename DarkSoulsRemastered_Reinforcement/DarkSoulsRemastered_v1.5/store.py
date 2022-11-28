import csv


def store(name, data):
    with open(name, 'w', newline = '') as file:
        wr = csv.writer(file)
        wr.writerows(data)


def load():
    pass
