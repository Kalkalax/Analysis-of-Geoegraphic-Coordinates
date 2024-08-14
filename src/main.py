from filepathrequester import FilePathRequester #klasa odpowiedzialna za zapytanie o plik CSV
from filereader import FileReader #klasa odpowiedzialna za wczytanie i sprawdzenie pliku CSV
from dataprocessor import DataProcessor

from configurationparameters import ConfigurationParameters #klasa zawierające configuracje bazy danych
from configurationfliemenager import ConfigurationFlieMenager #klasa odpowiedzialna za weryfikacje wczytywanie i tworzenie konfiguracji bazy danych


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
    ###
    if dataProcessor.checkPointName():
        print("Nazwa poprawna")
    else:
        exitWithMessage("bład w nazwie")

    if dataProcessor.checkAndConvertCoordinates():
        print("kordynaty ok")
    else:
        exitWithMessage("bład w kordynatach")




    # for index in range(len(dataFrame)):

    #     coordinates = dataFrame.iloc[index,1]
    #     print(coordinates)
    #     regexPatern = dataProcessor.checkDataPatern(coordinates)
        
    #     if regexPatern == 1:
    #         print("1")
    #     elif regexPatern == 2:
    #         print("2")
    #     elif regexPatern == 3:
    #         print("3")
    #     elif regexPatern == 4:
    #         print("4")
    #     elif regexPatern == None:
    #         exitWithMessage(f"# Wykryto nieoczekiwany błąd w kordynatach pod indeksem {index}")


    

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

    #print(config)

