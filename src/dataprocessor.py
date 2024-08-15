import pandas as pd
import re

class DataProcessor:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    def checkPointName(self):

        for index in range(len(self.dataFrame)):

            value = self.dataFrame.iloc[index, 0]

            if not re.match("^[A-Z][a-z]*(\s[a-zA-Z][a-z]*)*$", str(value)):
                return False
    
        return True
    
    def checkAndConvertCoordinates(self, decimalplaces = 6):

        for index in range(len(self.dataFrame)):

            value = self.dataFrame.iloc[index, 1]
            
            if (pattern := re.match(r"^(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)$", str(value))):
                
                latitude = round(float(pattern.group(1)), decimalplaces)
                longitude = round(float(pattern.group(2)), decimalplaces)

            elif (pattern := re.match(r"^([NS])(\d{1,2}\.\d+)°,([EW])(\d{1,2}\.\d+)°$", str(value))):
                
                latitude = round(float(pattern.group(2)) * (-1 if pattern.group(1) == 'S' else 1), decimalplaces)
                longitude = round(float(pattern.group(4)) * (-1 if pattern.group(3) == 'W' else 1), decimalplaces)

            elif (pattern := re.match(r"^([NS])(\d{1,2})°(\d{1,2}\.\d+),([EW])(\d{1,2})°(\d{1,2}\.\d+)$", str(value))):
                
                latitude = round(int(pattern.group(2)) + float(pattern.group(3)) / 60 * (-1 if pattern.group(1) == 'S' else 1), decimalplaces)
                longitude = round(int(pattern.group(5)) + float(pattern.group(6)) / 60 * (-1 if pattern.group(4) == 'W' else 1), decimalplaces)

            elif (pattern := re.match(r"^([NS])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"\,([EW])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"$", str(value))):

                latitude = round(int(pattern.group(2)) + int(pattern.group(3)) / 60 + float(pattern.group(4)) / 3600 * (-1 if pattern.group(1) == 'S' else 1), decimalplaces)
                longitude = round(int(pattern.group(6)) + int(pattern.group(7)) / 60 + float(pattern.group(8)) / 3600 * (-1 if pattern.group(5) == 'W' else 1), decimalplaces)

            else:
                return False
            
            self.dataFrame.iloc[index, 1] = f"{latitude},{longitude}"

        return True
    

    def checkAltitude(self):

        for index in range(len(self.dataFrame)):

            value = self.dataFrame.iloc[index, 2]

            if not re.match("^\d\.\d+$", str(value)):
                return False
        
        return True

    def checkDataAndTime(self):

        for index in range(len(self.dataFrame)):

            value = self.dataFrame.iloc[index, 3]

            if not re.match("^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}$", str(value)):
                return False
            
        return True
    
    def checkMetadata(self):

        pass

    def getData(self):

        return self.dataFrame

        