import pandas as pd # Library for data analysis and operations on data frames

# Class that supports loading a CSV file and returning the contents as a DataFrame
class FileReader:
    def __init__(self, filePath):   
        self.filePath = f"{filePath}"  
        self.dataFrame = pd.DataFrame  

    # Method that loads the contents of a CSV file into a DataFrame object
    def readFile(self):

        # Trying to load a CSV file with separators into a DataFrame
        try:
            self.dataFrame = pd.read_csv(self.filePath, sep=';')
            return True
        except FileNotFoundError:
            print(f"# The file under the path {self.filePath} was not found.")
            return False
        except pd.errors.ParserError:
            print("# There was a problem parsing the CSV file.")   
            return False
        except Exception as e:
            print(f"# An unexpected error occurred: {e}.")
            return False
        
    # Method that returns data read from a CSV file in the form of a DataFrame
    def getData(self):
        return self.dataFrame 
