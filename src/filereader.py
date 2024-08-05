import pandas as pd
import re

class FileReader:
    def __init__(self, filePath):
        self.filePath = filePath
        self.dataFrame = None
        #print(filePath)

    def readFile(self):
        self.dataFrame = pd.read_csv(self.filePath, sep=';')

        print(self.dataFrame)
        return self.dataFrame
    
    def checkPointName(self):
        #Weryfikacja czy nazwa składa się z samych liter bez znaków numerycznych
        firstColumn = self.dataFrame.iloc[:,0]

        print(firstColumn)

        for value in firstColumn:
            if not re.match("^[A-Za-z ]+$", str(value)):
                return False
            
        return True
        

    def getData(self):
        return self.dataFrame