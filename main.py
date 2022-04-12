from PersistenceLayer import *
import sqlite3
import os
import sys

from PersistenceLayer import _Repository


def parseConfig(repo):
    configFile = open(sys.argv[1], "r")  
    lines = configFile.readlines()
    firstLine = lines[0].split(',')
    numHats = int(firstLine[0])  # parses the first line
    numSuppliers = int(firstLine[1])
    for line in lines[1:numHats + 1]:  # parses the hats
        if line:
            hatTxt = line.split(',')
            repo.hats.insert(Hat(*hatTxt))
    for line in lines[numHats + 1:len(lines)]:  # parses the suppleirs
        if line:
            supplierTxt = line.replace("\n", "").split(',')
            repo.suppliers.insert(Supplier(*supplierTxt))
    configFile.close()


def placeOrders(repo):
    orderFile = open(sys.argv[2], "r")  
    outputFile = open(sys.argv[3], "w")  
    
    orders = orderFile.readlines()
    orderId = 1
    for order in orders:
        to_order = order.replace("\n", "").split(',')
        location = to_order[0]
        topping = to_order[1]
        hatsWithTopping = repo.hats.find_by_topping(topping)
        minIdSupplierHat = hatsWithTopping[0]
        for hat in hatsWithTopping[1:]:
            if hat.supplier < minIdSupplierHat.supplier and hat.quantity > 0:
                minIdSupplierHat = hat
        repo.orders.insert(Order(orderId, location, minIdSupplierHat.id))
        supplierName = repo.suppliers.find(minIdSupplierHat.supplier).name
        outputFile.write(topping + "," + supplierName + "," + location + "\n")
        orderId += 1
        minIdSupplierHat.quantity -= 1
        if minIdSupplierHat.quantity == 0:  # Hat is out of quantity, deleting it from database
            repo.hats.delete_hat(minIdSupplierHat.id)
        else:  # decreasing quantity of hat by 1
            repo.hats.place_order_update(minIdSupplierHat.id, minIdSupplierHat.quantity)
    orderFile.close()
    repo.return_conn().commit()
    


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    repo = _Repository(sys.argv[4])
    repo.create_tables()
    parseConfig(repo)
    placeOrders(repo)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
