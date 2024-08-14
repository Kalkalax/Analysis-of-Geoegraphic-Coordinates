import os

class ConfigurationFlieMenager:
    def __init__(self, configParameters):

        self.configParameters = {
            "host" : configParameters.host,
            "port" : configParameters.port,
            "dbname" : configParameters.dbname, 
            "tbname" : configParameters.tbname, 
            "user" : configParameters.user, 
            "password" : configParameters.password 
        }

        self.fileLocalization = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))
        self.filePath = os.path.join(self.fileLocalization, "config.py")

    def checkExistenceConfigFile(self):

        if os.path.exists(self.filePath):
            return True
        else:
            return False 

    def createConfigFile(self):

        with open(self.filePath, "w") as file:
            for key, value in self.configParameters.items():
                file.write(f"{key} = '{value}'\n")

    def readConfigFile(self):

        try:
            with open (self.filePath, "r") as file:
                for line in file:
                    line = line.strip()
                    if line and '=' in line:  # Sprawdź, czy linia nie jest pusta i zawiera '='
                        key, value = map(str.strip, line.split('=', 1))
                        self.configParameters[key] = value
                return self.configParameters
            
        except FileNotFoundError: 
            print("Plik 'config.py' nie został znaleziony.")
            return None
        
        except IOError:
            print("Nie udało się odczytać pliku 'config.py'.")
            return None