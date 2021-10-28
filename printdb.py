import sys

from Repository import *


def dto_print(row):
    print(tuple(row.__dict__.values()))


def rows_print(rows, as_tuple=True):
    for row in rows:
        if as_tuple:
            dto_print(row)
        else:
            print(*row.__dict__.values(), sep=" ")


def dao_print(tbl, as_tuple=True):
    print(tbl.name.replace("_", " "))
    rows_print(tbl.get_rows(), as_tuple)


class dto_report_employ:
    def __init__(self, name, salary, location):
        self.name = name
        self.salary = salary
        self.location = location
        self.sales = 0


class dto_act_action:
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


class dao_report_employees:
    def __init__(self, conn):
        self.conn = conn
        self.name = "Employees report"

    def get_rows(self):
        sql_emps = self.conn.execute("""
                                        SELECT Employees.id, Employees.name, Employees.salary, Coffee_stands.location 
                                        FROM Employees
                                        INNER JOIN Coffee_stands 
                                        WHERE Employees.coffee_stand = Coffee_stands.id
                                        ORDER BY Employees.id
               """).fetchall()
        emps = {row[0]: dto_report_employ(*tuple(list(row)[1:]))
                for row in sql_emps}

        sql_acts = self.conn.execute("""
                                        SELECT product_id, SUM(-1*quantity), activator_id, date
                                        FROM Activities
                                        WHERE quantity < 0
                                        GROUP BY product_id, activator_id
                                        ORDER BY product_id
                """).fetchall()

        actions = {row[0]: 0 for row in sql_acts}
        for prod_id in actions.keys():
            actions[prod_id] = [dto_activity(*row) for row in sql_acts if row[0] == prod_id]

        for prod_id, curr_actions in actions.items():
            product = repo.dao_products.find(prod_id)
            for curr_act in curr_actions:
                emps[curr_act.activator_id].sales += product.price * curr_act.quantity
        return list(emps.values())


class dao_report_activities:
    def __init__(self, conn):
        self.conn = conn
        self.name = "Activities"

    def get_rows(self):
        all_of_it = self.conn.execute("""
                    SELECT Activities.date, Products.description, Activities.quantity, Employees.name, Suppliers.name 
                    FROM Activities
                    LEFT JOIN Products 
                        ON Activities.product_id = Products.id
                    LEFT JOIN Employees
                        ON Activities.activator_id = Employees.id
                    LEFT JOIN Suppliers
                        ON Activities.activator_id = Suppliers.id
                    ORDER BY Activities.date
                """).fetchall()

        return [dto_act_action(*row) for row in all_of_it]


class reports_manager:
    def __init__(self):
        self.dao_employees = dao_report_employees(repo.conn)
        self.dao_activities = dao_report_activities(repo.conn)


rep_manger = reports_manager()


def printdb():
    dao_print(repo.dao_activities)
    dao_print(repo.dao_stands)
    dao_print(repo.dao_employees)
    dao_print(repo.dao_products)
    dao_print(repo.dao_suppliers)
    print()
    dao_print(rep_manger.dao_employees, False)
    if len(rep_manger.dao_activities.get_rows()):
        print()
        dao_print(rep_manger.dao_activities)


if __name__ == '__main__':
    printdb()
