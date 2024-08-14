import re

class DataProcessor:
    def __init__(self):

        pass

    def checkDataPatern(self, value):
    

        if re.match(r"^(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)$", str(value)):
            return 1
        elif re.match(r"^([NS])(\d{1,2}\.\d+)°,[EW](\d{1,2}\.\d+)°$", str(value)):
            return 2
        elif re.match(r"^([NS])(\d{1,2})°(\d{1,2}\.\d+),([EW])(\d{1,2})°(\d{1,2}\.\d+)$", str(value)):
            return 3
        elif re.match(r"^([NS])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"\,([EW])(\d{1,2})°(\d{1,2})'(\d{1,2}\.\d+)\"$", str(value)):
            return 4
        else:   
            return None

