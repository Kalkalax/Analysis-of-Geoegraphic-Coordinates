import psycopg2


class DatabaseManager:
    def __init__(self, configParameters):
        self.configParameters = configParameters
        self.connectionParametrs = {}

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

        