import pandas as pd
import re

class DataProcessor:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    # def checkDataPatern(self, coordinates):
    

    #     if re.match(r"^(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)$", str(coordinates)):
    #         return 1
    #     elif re.match(r"^([NS])(\d{1,2}\.\d+)°,[EW](\d{1,2}\.\d+)°$", str(coordinates)):
    #         return 2
    #     elif re.match(r"^([NS])(\d{1,2})°(\d{1,2}\.\d+),([EW])(\d{1,2})°(\d{1,2}\.\d+)$", str(coordinates)):
    #         return 3
    #     elif re.match(r"^([NS])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"\,([EW])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"$", str(coordinates)):
    #         return 4
    #     else:   
    #         return None

    def checkPointName(self):

        firstColumn = self.dataFrame.iloc[:,0]

        for value in firstColumn:
            if not re.match("^[A-Z][a-z]*(\s[a-zA-Z][a-z]*)*$", str(value)):
                return False
    
        return True
    
    def checkAndConvertCoordinates(self):

        secondColumn = self.dataFrame.iloc[:,1]
        

        for value in secondColumn:

            # firstPatern = re.match(r"^(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)$", str(value))
            # secondPatern = re.match(r"^([NS])(\d{1,2}\.\d+)°,[EW](\d{1,2}\.\d+)°$", str(value))
            # thirdPatern = re.match(r"^([NS])(\d{1,2})°(\d{1,2}\.\d+),([EW])(\d{1,2})°(\d{1,2}\.\d+)$", str(value))
            # fourthPatern = re.match(r"^([NS])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"\,([EW])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"$", str(value))
            
            if (pattern := re.match(r"^(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)$", str(value))):
                
                latitude = float(pattern.group(1))
                longitude = float(pattern.group(2))
                print(f"Latitude: {latitude}, Longitude: {longitude}")

            elif (pattern := re.match(r"^([NS])(\d{1,2}\.\d+)°,[EW](\d{1,2}\.\d+)°$", str(value))):
                print(value + " - 2")
            elif (pattern := re.match(r"^([NS])(\d{1,2})°(\d{1,2}\.\d+),([EW])(\d{1,2})°(\d{1,2}\.\d+)$", str(value))):
                print(value + " - 3")
            elif (pattern := re.match(r"^([NS])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"\,([EW])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"$", str(value))):
                print(value + " - 4")
            else:
                return False
                
        return True

        