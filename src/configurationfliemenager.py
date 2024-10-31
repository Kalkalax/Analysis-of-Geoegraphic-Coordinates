import os # Module for operations on system paths and files

# Class that manages the database configuration file
class ConfigurationFlieMenager:
    def __init__(self, configParameters):

        # Create a dictionary with the database configuration parameters
        self.configParameters = {
            "host" : configParameters.host,
            "port" : configParameters.port,
            "dbname" : configParameters.dbname, 
            "tbname" : configParameters.tbname, 
            "user" : configParameters.user, 
            "password" : configParameters.password 
        }

        # Determine the location where the configuration file will be stored
        self.fileLocalization = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))
        # Create the full path to the configuration file
        self.filePath = os.path.join(self.fileLocalization, "config.py")

    # Method to check if the configuration file exists
    def checkExistenceConfigFile(self):

        # Check if the configuration file exists
        if os.path.exists(self.filePath):
            return True
        else:
            return False 

    # Method that creates a configuration file
    def createConfigFile(self):

        # Open file in write mode
        with open(self.filePath, "w") as file:
            #Iterates through the dictionary and writes each key and value on a new line in the format 'key = value'
            for key, value in self.configParameters.items():
                file.write(f"{key} = '{value}'\n")

    # Method that reads the configuration file 
    def readConfigFile(self):

        try:
            # Open the file in read mode
            with open (self.filePath, "r") as file:
                #Iterate through each line in the file, remove whitespace characters, and check that the line is not empty
                for line in file:
                    line = line.strip()
                    if line and '=' in line: 
                        # Separate the key and the value and update the member
                        key, value = map(str.strip, line.split('=', 1))
                        self.configParameters[key] = value
                return self.configParameters
            
        except FileNotFoundError: 
            print("# The database configuration file 'config.py' was not found.")
            return None
        
        except IOError:
            print("# Failed to read database configuration file 'config.py'.")
            return None