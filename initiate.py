import os
import sys

if os.path.exists('moncafe.db'):
    os.remove('moncafe.db')

from Repository import *


def initiate(args):
    repo.create_tables()

    filename = args[1]
    with open(filename, "r") as fp:
        lines = fp.readlines()
        for line in lines:
            words = line.split(", ")
            words = [word.strip() for word in words]
            if words[0] == "E":
                repo.dao_employees.insert(dto_employee(*(words[1:])))
            elif words[0] == "S":
                repo.dao_suppliers.insert(dto_supplier(*(words[1:])))
            elif words[0] == "P":
                repo.dao_products.insert(dto_product(*(words[1:])))
            elif words[0] == "C":
                repo.dao_stands.insert(dto_stand(*(words[1:])))


if __name__ == '__main__':
    initiate(sys.argv)
