import csv
import psycopg2
import os
from abc import ABC, abstractmethod


class AbstractSaveDb(ABC):
    
    @abstractmethod
    def save_to_db(self):
        pass
   
 
class DataBase(AbstractSaveDb):
    """Класс подключения к базе данных
    """    
    
    __slots__ = ('path', 'db', 'cluster')
    
    def __init__(self, db, cluster, path) -> None:
        self.path = path
        self.db = db
        self.cluster = cluster
        
    @classmethod
    def _make_correct_tuple(cls, row: dict) -> tuple:
        """Класс метод сбора корректного кортежа для запроса в БД
        """        
        correct_row = []
        
        for elem in row:
                                    
            if elem.isdigit():
                elem = int(elem)
                correct_row.append(elem)

            elif "'" in str(elem):
                correct_row.append(''.join([item for item in elem if "'" != item]))

            else:
                correct_row.append(elem)
                
        return tuple(correct_row)

            
    def save_to_db(self) -> None:
        """Метод сохранения из файла в базу данных
        """        
        
        try:
            with open(self.path) as file:
                read_file = csv.DictReader(f=file, fieldnames=None)
                
                try:
                    with psycopg2.connect(database=self.db,
                                        user='postgres',
                                        password=os.getenv('PASSWORD_POSTGRES')) as db:
                        
                        with db.cursor() as cur:
                            header = read_file.fieldnames
                            
                            for row in read_file.reader:
                                cur.execute(f'INSERT INTO {self.cluster}\
                                    VALUES {self._make_correct_tuple(row)}')
                finally:
                    db.close()
                    
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл {self.path} не был найден')
        