import pandas as pd
import re

#Klasa obsługująca wczytanie i weryfikacje pliku CSV
class FileReader:
    def __init__(self, filePath):
        self.filePath = filePath
        self.dataFrame = None

    #Metoda wczytująca zawartość pliku CSV do dataframe
    def readFile(self):

        try:
            self.dataFrame = pd.read_csv(self.filePath, sep=';')

        except FileNotFoundError:
            print(f"Error: The file at {self.filePath} was not found.")
        except pd.errors.ParserError:
            print("Error: There was an issue with parsing the CSV file.")    
        except Exception as e:
             print(f"Error: An unexpected error occurred: {e}")

        return self.dataFrame
    
    #Metoda weryfikująca czy nazwa punktu posiada odpowiedni format
    def checkPointName(self):
        
        firstColumn = self.dataFrame.iloc[:,0]

        for value in firstColumn:
            if not re.match("^[A-Z][a-z]*(\s[a-zA-Z][a-z]*)*$", str(value)):
                return False
    
        return True
    
    #Metoda weryfikujaca czy współrzędne posiadają odpowiedni format
    def checkCoordinates(self):

        secondColumn = self.dataFrame.iloc[:,1]

        for value in secondColumn:
            
            if (not re.match("^-?\d{1,3}\.\d+,-?\d{1,3}\.\d+$", str(value)) and
                not re.match("^[NS]\d{1,2}\.\d+°,[EW]\d{1,2}\.\d+°$", str(value)) and
                not re.match("^[NS]\d{1,2}°\d{1,2}\.\d+,[EW]\d{1,2}°\d{1,2}\.\d+$", str(value)) and
                not re.match("""^[NS]\d{1,2}°\d{1,2}'\d{1,2}\.\d+",[EW]\d{1,2}°\d{1,2}'\d{1,2}\.\d+"$""", str(value))):
                return False

        return True

    #Metoda weryfikująca czy wysokość posiada odpowiedni format
    def checkAltitude(self):

        thirdColumn = self.dataFrame.iloc[:,2]

        for value in thirdColumn:
            if not re.match("^\d\.\d+$", str(value)):
                return False
        
        return True
    
    #Metoda weryfikująca czy znacznik czasowy posiada odpowiedni format
    def checkDataAndTime(self):

        fourthColumn = self.dataFrame.iloc[:,3]

        for value in fourthColumn:
            if not re.match("^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}$", str(value)):
                return False
            
        return True
    
    #Metoda weryfikująca czy metadane posiadają odpowiedni format (NIE NAPISANE)
    def checkMetadata(self):

        pass

    #Metoda zwracająca dane odczytane z pliku CSV w dataframe
    def getData(self):
        return self.dataFrame