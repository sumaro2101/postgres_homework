import json
import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
from config import config


def main():
    script_file = os.path.join('homework-5', 'fill_db.sql')
    json_file = os.path.join('homework-5', 'suppliers.json')
    db_name = 'orders_db'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    
    try:
        
        connection = psycopg2.connect(**params)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        curr = connection.cursor()
        sql_create_database = f'CREATE DATABASE {db_name}'
        curr.execute(sql_create_database)
        
    except (Exception, Error) as error:
        print('База данных с таким именем уже существует', error)   
        
    finally:
        curr.close()
        connection.close()
    
    
def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    with open(script_file) as file:
        cur.execute(file.read())


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    table = 'DROP TABLE IF EXISTS suppliers;\
        CREATE TABLE suppliers\
        (   supplier_id  serial NOT NULL,\
            company_name varchar( 100 ) NOT NULL,\
            contact      varchar( 100 ) NOT NULL,\
            address      varchar( 100 ) NOT NULL,\
            phone        varchar( 20 ) NOT NULL,\
            fax          varchar( 20 ),\
            homepage     text,\
            products     text[] NOT NULL,\
            CONSTRAINT pk_suppliers_company_name PRIMARY KEY ( supplier_id )\
        );'
               
    cur.execute(table)


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    with open(json_file) as file:
        result = json.load(file)
        
    return result


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    for item in suppliers:
        
        value = tuple(item.values())
        
        cur.execute(f'INSERT INTO suppliers ( company_name, contact, address, phone, fax, homepage, products )\
            VALUES (%s,%s,%s,%s,%s,%s,%s::text[]);', value)


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    
    cur.execute('ALTER TABLE products ADD COLUMN supplier_id integer;')
    
    cur.execute('ALTER TABLE products ADD CONSTRAINT fk_supplier_id_products\
                FOREIGN KEY ( supplier_id ) REFERENCES suppliers( supplier_id )\
                ON DELETE CASCADE;')
    
    cur.execute('UPDATE products\
                SET supplier_id =\
                ( SELECT supplier_id FROM suppliers\
                WHERE products.product_name = ANY( suppliers.products ));')


if __name__ == '__main__':
    main()
