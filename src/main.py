from filepathrequester import FilePathRequester #klasa odpowiedzialna za zapytanie o plik CSV
from filereader import FileReader #klasa odpowiedzialna za wczytanie i sprawdzenie pliku CSV
from dataprocessor import DataProcessor

from configurationparameters import ConfigurationParameters #klasa zawierające configuracje bazy danych
from configurationfliemenager import ConfigurationFlieMenager #klasa odpowiedzialna za weryfikacje wczytywanie i tworzenie konfiguracji bazy danych

from databasemanager import DatabaseManager 


import sys

def exitWithMessage(message):
    print(message)
    input("# Naciśnij Enter, aby zamknąć aplikację...")
    sys.exit(1)

def exitWithoutMessage():
    input("# Naciśnij Enter, aby zamknąć aplikację...")
    sys.exit(1)

if __name__ == "__main__":

    #Inicjalizacja FilePathRequester i pobranie lokalizacji pliku CSV

    print("# Podaj lokalizacje pliku CSV z punktami współrzędnych")

    filePathRequester = FilePathRequester()
    if filePathRequester.askFilePath():
        filePath = filePathRequester.getPath()
        print("# Wskazanie lokalizacji pliku CSV przebiegło prawidłowo")
    else:
        exitWithMessage("# Nie wskazano lokalizacji pliku do odczytu")

    #Inicjalizacja FileReader 

    fileReader = FileReader(filePath)

    if fileReader.readFile():
        dataFrame = fileReader.getData()
        print("# Wczytywanie pliku CSV przebiegło prawidłowo")
    else:
        exitWithoutMessage()
    
    print(dataFrame) # <- do tąd jest git
    
   

    #Tu piszemy DataProcesor
    dataProcessor = DataProcessor(dataFrame)
    #########################################################
    if dataProcessor.checkPointName():
        print("Nazwa poprawna")
    else:
        exitWithMessage("bład w nazwie")

    if dataProcessor.checkAndConvertCoordinates():
        print("kordynaty ok")
    else:
        exitWithMessage("bład w kordynatach")

    if dataProcessor.checkAltitude():
        print("wysokosc ok")
    else:
        exitWithMessage("bład w wysokosci")

    if dataProcessor.checkDataAndTime():
        print("data ok")
    else:
        exitWithMessage("bład w dacie")  

    if dataProcessor.checkMetadata():
        print("metadata ok")
    else:
        exitWithMessage("bład w metadacie")  

    dataFrame = dataProcessor.getData()
    print(dataFrame)
    #########################################################



    

    #Inicjalizacja ConfigurationParameters i ConfigurationFlieMenager oraz wczytanie konfiguracji bądz jej utworzenie

    configurationParameters = ConfigurationParameters()
    configurationFlieMenager = ConfigurationFlieMenager(configurationParameters)
    
    while True:
        if configurationFlieMenager.checkExistenceConfigFile():
            break
        else:
            configurationFlieMenager.createConfigFile()

    config = configurationFlieMenager.readConfigFile()
    
    if config: 
        print("# Plik konfiguracyjny bazy danych załadowano poprawnie")
    else:
        input("# Naciśnij Enter, aby zamknąć aplikację...")
        sys.exit(1)

    print(config)

    #########################################################
    databaseManager = DatabaseManager(config)

    while True:
        if databaseManager.checkDatabaseExistence():
            print("baza danych istnieje")
            break
        elif not databaseManager.checkDatabaseExistence():
            print("baza danych nie istnieje")
            print("Tworzenie bazy danych")
            databaseManager.createDatabase()
            print("Tworzenie tabeli danych")
            databaseManager.createDatabaseTable()
        else: 
            exitWithMessage("błąd bazy danych")

    while True:
        if databaseManager.checkDatabaseTableExistence():
            print("tabela danych istnieje")
            break
        elif not databaseManager.checkDatabaseTableExistence():
            print("tabela danych nie istnieje")
            print("Tworzenie tabeli danych")
            databaseManager.createDatabaseTable()

        else:
            exitWithMessage("błąd bazy danych")


    #########################################################




    exitWithMessage("")

