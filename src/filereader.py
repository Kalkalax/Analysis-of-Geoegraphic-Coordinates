import pandas as pd
import re

#Klasa obsługująca wczytanie i weryfikacje pliku CSV
class FileReader:
    def __init__(self, filePath):
        self.filePath = filePath
        self.dataFrame = None

    #Metoda wczytująca zawartość pliku CSV do dataframe
    def readFile(self):
        self.dataFrame = pd.read_csv(self.filePath, sep=';')

        print(self.dataFrame)
        return self.dataFrame
    
    #Metoda weryfikująca czy nazwa punktu nie zawiera niedozwolonych znaków
    def checkPointName(self):
        
        firstColumn = self.dataFrame.iloc[:,0]

        print(firstColumn)

        for value in firstColumn:
            if not re.match("^[A-Za-z ]+$", str(value)):
                return False
            
        return True
    
    #Metoda weryfikujaca czy współrzędne nie zawierają niedozwolonych znaków
    def checkCoordinates(self):

        secondColumn = self.dataFrame.iloc[:,1]

        print(secondColumn)

        for value in secondColumn:
            if not re.match("^[0-9NESW.,\"'° -]+$", str(value)):
                return False
        
        return True

        
    #Metoda zwracająca dane odczytane z pliku CSV w dataframe
    def getData(self):
        return self.dataFrame