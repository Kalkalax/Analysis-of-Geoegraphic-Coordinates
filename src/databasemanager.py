import psycopg2
import pandas as pd
import numpy as np


class DatabaseManager:
    def __init__(self, configParameters):
        self.configParameters = configParameters
        self.connectionParametrs = {}
        self.dataFrame = pd.DataFrame

    def checkDatabaseExistence(self):

        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.configParameters["dbname"]}'")
            if cur.fetchone() is None:
                return False
            else: 
                return True
            
        except psycopg2.Error as e:
            print(f"Błąd podczas łączenia z bazą danych {self.configParameters["dbname"]}: {e}")
            return None
        
        finally:
            cur.close()
            conn.close()


    def createDatabase(self):
        
        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f'CREATE DATABASE "{self.configParameters["dbname"]}"')
            
        except psycopg2.Error as e:
            print(f"Błąd podczas łączenia z bazą danych {self.configParameters["dbname"]}: {e}")
        
        finally:
            cur.close()
            conn.close() 

    def checkDatabaseTableExistence(self):

        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "dbname": self.configParameters["dbname"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"SELECT 1 FROM pg_catalog.pg_tables WHERE tablename = '{self.configParameters["tbname"]}';")
            if cur.fetchone() is None:
                return False
            else:
                return True
            
        except psycopg2.Error as e:
            print(f"Błąd podczas łączenia z bazą danych {self.configParameters["dbname"]}: {e}")
            return None
        
        finally:
            cur.close()
            conn.close()

    def createDatabaseTable(self):

        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "dbname": self.configParameters["dbname"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f'''CREATE TABLE "{self.configParameters["tbname"]}"(
                               point_name CHARACTER VARYING,
                               coordinates CHARACTER VARYING,
                               altitude NUMERIC,
                               date_and_time TIMESTAMP,
                               metadata CHARACTER VARYING)
                            ''')
            
        except psycopg2.Error as e:
            print(f"Błąd podczas łączenia z bazą danych {self.configParameters["dbname"]}: {e}")
        
        finally:
            cur.close()
            conn.close() 
        
    def insertData(self, dataFrame):

        addedRow = 0
        self.dataFrame = dataFrame.replace({np.nan: ""}) 

        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "dbname": self.configParameters["dbname"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True
            cur = conn.cursor()

            for _, row in self.dataFrame.iterrows():
                cur.execute(f'SELECT 1 FROM "{self.configParameters["tbname"]}" WHERE point_name = %s AND coordinates = %s AND altitude = %s AND date_and_time = %s AND metadata = %s', tuple(row))
                
               
                if cur.fetchone() is None:
                    cur.execute(f'INSERT INTO "{self.configParameters["tbname"]}" VALUES (%s, %s, %s, %s, %s)', tuple(row))
                    addedRow += 1

            return addedRow
        
        except Exception as e:
            print(f"Błąd podczas wstawiania danych do bazy danych {self.configParameters['dbname']}: {e}")
            return None

        finally:
            cur.close()
            conn.close()
            
        
    def getData(self):

        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "dbname": self.configParameters["dbname"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM "{self.configParameters["tbname"]}";')
            
            data = cur.fetchall()
            columnNames = [desc[0] for desc in cur.description]
            dataFrame = pd.DataFrame(data, columns = columnNames)

            if data is None:
                return False
            else:
                return dataFrame

        except psycopg2.Error as e:
            print(f"Błąd podczas pobierania danych z bazą danych {self.configParameters["dbname"]}: {e}")
            return None
        
        finally:
            cur.close()
            conn.close()

