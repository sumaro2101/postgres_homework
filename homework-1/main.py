import os
from save_to_db import DataBase

def main(): 
    DataBase(db='north', path=os.path.join('homework-1', 'north_data', 'customers_data.csv'), cluster='customers').save_to_db()
    DataBase(db='north', path=os.path.join('homework-1', 'north_data', 'employees_data.csv'), cluster='employees').save_to_db()
    DataBase(db='north', path=os.path.join('homework-1', 'north_data', 'orders_data.csv'), cluster='orders').save_to_db()
    
    
if __name__ == '__main__':
    main()
    