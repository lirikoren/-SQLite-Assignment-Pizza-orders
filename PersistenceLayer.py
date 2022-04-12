import atexit
import os
import sqlite3
# Repository


class _Repository:
    def __init__(self,db):
        self._conn = sqlite3.connect(db)
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)

    def return_conn(self):
        return self._conn

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE hats (
        id INTEGER PRIMARY KEY,
        topping STRING NOT NULL,
        supplier INTEGER REFERENCES Supplier(id),
        quantity INTEGER NOT NULL
        );
        
        CREATE TABLE suppliers (
        id INTEGER PRIMARY KEY,
        name STRING NOT NULL
        );
        
        CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        location STRING NOT NULL,
        hat INTEGER REFERENCES hats(id)
        );
        """)

# atexit.register(repo._close)


# DTO - data transfer objects
class Hat:
    def __init__(self, id, topping, supplier, quantity):
        self.id = id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity



class Supplier:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Order:
    def __init__(self, id, location, hat):
        self.id = id
        self.location = location
        self.hat = hat


# DAO - data access objects
class _Hats:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, hat):
        self._conn.execute("""
        INSERT INTO Hats (id,topping,supplier,quantity) VALUES(?,?,?,?)
        """, [hat.id, hat.topping, hat.supplier, hat.quantity])

    def find_by_supplier(self, topping, supplier):  # FIND HAT BY TOPPING And supplier
        c = self._conn.cursor()
        c.execute("""
        SELECT id, topping, supplier, quantity FROM hats WHERE topping = ? AND supplier = ? 
        """, [topping], [supplier])
        return Hat(*c.fetchone())

    def find_by_topping(self, topping):
        c = self._conn.cursor()
        all_hats = c.execute("""
        SELECT id, topping, supplier, quantity FROM hats WHERE topping = ?
        """, [topping]).fetchall()
        return [Hat(*row) for row in all_hats]

    def find_first_supplier(self,topping):
        c = self._conn.cursor()
        all_suppliers= c.execute("""
        SELECT id, topping, supplier, quantity FROM hats WHERE topping = ?
        JOIN """, [topping]).featchall()

    def place_order_update(self, id, quantity):
        c = self._conn.cursor()
        c.execute("""
                   UPDATE hats SET quantity = ? WHERE id= ?
                   """, [quantity,id])

    def delete_hat(self,id):
        c = self._conn.cursor()
        c.execute("""
                           DELETE FROM hats WHERE id= ?
                           """, [id])

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers (id, name) VALUES (?, ?)
        """, [supplier.id, supplier.name])

    def find(self, supplier_id):  # FIND SUPPLIER BY ID
        c = self._conn.cursor()
        c.execute("""
                SELECT id, name FROM suppliers WHERE id = ?
            """, [supplier_id])

        return Supplier(*c.fetchone())


class _Orders:
    def __init__(self, conn):
        self._conn = conn

    def insert(self,order):
        self._conn.execute("""
        INSERT INTO orders (id, location, hat) VALUES (?, ?, ?)
        """, [order.id, order.location, order.hat])

    def find(self, id):
        c = self._conn.cursor()
        found_order = c.execute("""
        SELECT id, location, hat FROM hats WHERE id = ?
        """, [id]).fetchone()
        return Order(*found_order)
