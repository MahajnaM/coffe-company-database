import sqlite3
import atexit

# region DTO
# Data Transfer Objects:
class dto_product(object):
    def __init__(self, id, description, price, quantity=0):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class dto_supplier(object):
    def __init__(self, id, name, contact):
        self.id = id
        self.name = name
        self.contact = contact


class dto_employee(object):
    def __init__(self, id, name, salary, stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.stand = stand


class dto_stand(object):
    def __init__(self, id, location, num):
        self.id = id
        self.location = location
        self.num = num


class dto_activity(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


# endregion
# region DAO
# Data Access Objects:
# All of these are meant to be singletons
class generic_table:
    def __init__(self, conn, table_name, pri_key):
        self.conn = conn
        self.name = table_name
        self.pri_key = pri_key

    def insert(self, dto):
        self.conn.execute(
            "INSERT INTO " + self.name + " VALUES " +
            str(tuple(['?'] * len(dto.__dict__.values()))).replace("'", ""),
            list(dto.__dict__.values()))
        self.conn.commit()

    def find(self, num):
        c = self.conn.cursor()
        c.execute("SELECT * FROM " + self.name + " WHERE " + self.pri_key + " = ?", [num])

        return dto_product(*c.fetchone())

    def get_rows(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM " + self.name + " ORDER BY " + self.pri_key)
        all_rows = c.fetchall()
        return [dto_product(*row) for row in all_rows]

    def update(self, curr_id, col_name, val):
        self.conn.execute("UPDATE " + self.name + " SET " + col_name + " = (?) WHERE id = (?)", [val, curr_id])
        self.conn.commit()


class dao_Products(generic_table):
    def __init__(self, conn):
        super().__init__(conn, "Products", "id")


class dao_Suppliers(generic_table):
    def __init__(self, conn):
        super().__init__(conn, "Suppliers", "id")


class dao_Employees(generic_table):
    def __init__(self, conn):
        super().__init__(conn, "Employees", "id")


class dao_Activities(generic_table):
    def __init__(self, conn):
        super().__init__(conn, "Activities", "date")


class dao_Coffee_stands(generic_table):
    def __init__(self, conn):
        super().__init__(conn, "Coffee_stands", "id")


# endregion
# The Repository
class _Repository:
    def __init__(self):
        self.conn = sqlite3.connect('moncafe.db')
        self.dao_products = dao_Products(self.conn)
        self.dao_suppliers = dao_Suppliers(self.conn)
        self.dao_employees = dao_Employees(self.conn)
        self.dao_activities = dao_Activities(self.conn)
        self.dao_stands = dao_Coffee_stands(self.conn)

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.executescript("""
                        CREATE TABLE Suppliers (id INTEGER PRIMARY KEY,
                                                name TEXT NOT NULL,
                                                contact_information TEXT
                        );

                        CREATE TABLE Products (id INTEGER PRIMARY KEY,
                                                description TEXT NOT NULL,
                                                price REAL NOT NULL,
                                                quantity INTEGER NOT NULL
                        );

                        CREATE TABLE Coffee_stands (id INTEGER PRIMARY KEY,
                                                    location TEXT NOT NULL,
                                                    number_of_employees INTEGER
                        );

                        CREATE TABLE Employees (id INTEGER PRIMARY KEY,
                                               name TEXT  NOT NULL,
                                               salary REAL NOT NULL,
                                               coffee_stand INTEGER REFERENCES Coffee_stands
                        );
                        
                        CREATE TABLE Activities (product_id INTEGER REFERENCES Products,
                                                quantity INTEGER NOT NULL,
                                                activator_id INTEGER NOT NULL,
                                                date DATE NOT NULL
                        );
                """)


repo = _Repository()
atexit.register(repo.close)
