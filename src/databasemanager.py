import psycopg2 # Library for working with PostgreSQL databases
import pandas as pd # Library for data analysis and operations on data frames
import numpy as np # Library for efficient calculation on multidimensional arrays

# Class that manages connection to PostgreSQL database
class DatabaseManager:
    def __init__(self, configParameters):
        self.configParameters = configParameters
        self.connectionParametrs = {}
        self.dataFrame = pd.DataFrame

    # Method responsible for checking the existence of a database
    def checkDatabaseExistence(self):

        # Prepares the connection parameters for the database
        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            # Establishes connection to database and sets automatic transaction validation mode
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True

            # Creates a cursor and executes a query to check the existence of a database
            cur = conn.cursor()
            cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.configParameters["dbname"]}'")
            
            # Checks whether the query result is empty
            if cur.fetchone() is None:
                return False
            else: 
                return True
            
        except psycopg2.Error as e:
            # Displays a message if an error occurs
            print(f"# Error while connecting to database {self.configParameters["dbname"]}: {e}")
            return None
        
        finally:
            # Closes cursor and database connection
            cur.close()
            conn.close()

    # Method responsible for the creation of the database
    def createDatabase(self):
        
        # Prepares the connection parameters for the database
        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            # Establishes connection to database and sets automatic transaction validation mode
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True

            # Creates a cursor and executes a query to create a new database
            cur = conn.cursor()
            cur.execute(f'CREATE DATABASE "{self.configParameters["dbname"]}"')
            
        except psycopg2.Error as e:
            # Displays a message if an error occurs
            print(f"# Error while connecting to database {self.configParameters["dbname"]}: {e}")
        
        finally:
            # Closes cursor and database connection
            cur.close()
            conn.close() 

    # Method responsible for checking the existence of a data table in the database 
    def checkDatabaseTableExistence(self):

        # Przygotowuje parametry połączenia dla bazy danych
        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "dbname": self.configParameters["dbname"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            # Establishes connection to database and sets automatic transaction validation mode
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True

            # Creates a cursor and executes a query to check the existence of a specific table in the database
            cur = conn.cursor()
            cur.execute(f"SELECT 1 FROM pg_catalog.pg_tables WHERE tablename = '{self.configParameters["tbname"]}';")
            
            # Checks whether the query result is empty
            if cur.fetchone() is None:
                return False
            else:
                return True
            
        except psycopg2.Error as e:
            # Displays a message if an error occurs
            print(f"# Error while connecting to database {self.configParameters["dbname"]}: {e}.")
            return None
        
        finally:
            # Closes cursor and database connection
            cur.close()
            conn.close()

    # Method responsible for creating a data table in the database
    def createDatabaseTable(self):

        # Prepares the connection parameters for the database
        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "dbname": self.configParameters["dbname"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            # Establishes connection to database and sets automatic transaction validation mode
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True
            
            # Creates a cursor and executes a query to create a new table in the database
            cur = conn.cursor()
            cur.execute(f'''CREATE TABLE "{self.configParameters["tbname"]}"(
                               point_name CHARACTER VARYING,
                               coordinates CHARACTER VARYING,
                               altitude NUMERIC,
                               date_and_time TIMESTAMP,
                               metadata CHARACTER VARYING)
                            ''')
            
        except psycopg2.Error as e:
            # Displays a message if an error occurs
            print(f"# Error while connecting to database {self.configParameters["dbname"]}: {e}.")
        
        finally:
            # Closes cursor and database connection
            cur.close()
            conn.close() 
    
    # Method responsible for inserting data from a DataFrame into a database table
    def insertData(self, dataFrame):

        addedRow = 0

        # Replaces NaN with empty strings in the DataFrame
        self.dataFrame = dataFrame.replace({np.nan: ""}) 

        # Prepares the connection parameters for the database
        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "dbname": self.configParameters["dbname"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            # Establishes connection to database and sets automatic transaction validation mode
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True

            # Creates a cursor and iterates through the DataFrames rows
            cur = conn.cursor()
            for _, row in self.dataFrame.iterrows():
                cur.execute(f'SELECT 1 FROM "{self.configParameters["tbname"]}" WHERE point_name = %s AND coordinates = %s AND altitude = %s AND date_and_time = %s AND metadata = %s', tuple(row))
                
                # If the row does not exist, adds it to the table
                if cur.fetchone() is None:
                    cur.execute(f'INSERT INTO "{self.configParameters["tbname"]}" VALUES (%s, %s, %s, %s, %s)', tuple(row))
                    addedRow += 1

            return addedRow
        
        except Exception as e:
            # Displays a message if an error occurs
            print(f"Error when inserting data into database {self.configParameters['dbname']}: {e}")
            return None

        finally:
            # Closes cursor and database connection
            cur.close()
            conn.close()
            
    # Method responsible for retrieving data from a database table and returning it as a DataFrame  
    def getData(self):

        # Prepares connection parameters for the database
        self.connectionParametrs = {
            "host": self.configParameters["host"],
            "port": self.configParameters["port"],
            "dbname": self.configParameters["dbname"],
            "user": self.configParameters["user"],
            "password": self.configParameters["password"]
        }

        try:
            # Establishes connection to database and sets automatic transaction validation mode
            conn = psycopg2.connect(**self.connectionParametrs)
            conn.autocommit = True

            # Creates a cursor and # Performs a query to retrieve all the data from the table
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM "{self.configParameters["tbname"]}";')
            
            # Retrieves all result rows and creates a DataFrame from the retrieved data
            data = cur.fetchall()
            columnNames = [desc[0] for desc in cur.description]
            dataFrame = pd.DataFrame(data, columns = columnNames)

            #Check if any data has been returned
            if data is None:
                return False
            else:
                return dataFrame

        except psycopg2.Error as e:
            # Displays a message if an error occurs
            print(f"Error while retrieving data from database {self.configParameters["dbname"]}: {e}")
            return None
        
        finally:
            # Closes cursor and database connection
            cur.close()
            conn.close()

