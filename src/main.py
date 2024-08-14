from filepathrequester import FilePathRequester #klasa odpowiedzialna za zapytanie o plik CSV
from filereader import FileReader #klasa odpowiedzialna za wczytanie i sprawdzenie pliku CSV

from configurationparameters import ConfigurationParameters #klasa zawierające configuracje bazy danych
from configurationfliemenager import ConfigurationFlieMenager #klasa odpowiedzialna za weryfikacje wczytywanie i tworzenie konfiguracji bazy danych


import sys

def exitWithMessage(message):
    print(message)
    input("Naciśnij Enter, aby zamknąć aplikację...")
    sys.exit(1)

if __name__ == "__main__":

    #Inicjalizacja FilePathRequester i pobranie lokalizacji pliku CSV

    print("Podaj lokalizacje pliku CSV z punktami współrzędnych")

    filePathRequester = FilePathRequester()
    filePathRequester.askFilePath()
    filePath = filePathRequester.getPath()

    #Inicjalizacja FileReader oraz przeprowadzenie weryfikacji

    fileReader = FileReader(filePath)
    dataFrame = fileReader.readFile()

    print(dataFrame)
    
    if not fileReader.checkPointName():
        exitWithMessage("Wykryto nieodpowiedni format nazw punktów")
    
    elif not fileReader.checkCoordinates():
        exitWithMessage("Wykryto nieodpowiedni format współrzędnych")
        
    elif not fileReader.checkAltitude():
        exitWithMessage("Wykryto nieodpowiedni format wysokości")
        
    elif not fileReader.checkDataAndTime():
        exitWithMessage("Wykryto nieodpowiedni format znaczników czasowych")
        
    else:
        print("Wprowadzone dane nie zawierają błędów")


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
        print("Plik konfiguracyjny bazy danych załadowano poprawnie")
    else:
        input("Naciśnij Enter, aby zamknąć aplikację...")
        sys.exit(1)

    #print(config)

