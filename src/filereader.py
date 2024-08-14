import pandas as pd

#Klasa obsługująca wczytanie pliku CSV i zwrócenie zawartości w dataFrame
class FileReader:
    def __init__(self, filePath):   
        self.filePath = f"{filePath}"
        self.dataFrame = pd.DataFrame

    #Metoda wczytująca zawartość pliku CSV do dataframe
    def readFile(self):

        try:
            self.dataFrame = pd.read_csv(self.filePath, sep=';')
            return True
        except FileNotFoundError:
            print(f"# Error: The file at {self.filePath} was not found.")
            return False
        except pd.errors.ParserError:
            print("# Error: There was an issue with parsing the CSV file.")   
            return False 
        except Exception as e:
             print(f"# Error: An unexpected error occurred: {e}")
             return False
        
    #Metoda zwracająca dane odczytane z pliku CSV w dataframe
    def getData(self):
        
        return self.dataFrame