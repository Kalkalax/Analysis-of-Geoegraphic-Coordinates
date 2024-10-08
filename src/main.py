from filepathrequester import FilePathRequester #klasa odpowiedzialna za zapytanie o plik CSV
from filereader import FileReader #klasa odpowiedzialna za wczytanie i sprawdzenie pliku CSV
from dataprocessor import DataProcessor

from configurationparameters import ConfigurationParameters #klasa zawierające configuracje bazy danych
from configurationfliemenager import ConfigurationFlieMenager #klasa odpowiedzialna za weryfikacje wczytywanie i tworzenie konfiguracji bazy danych

from databasemanager import DatabaseManager 

#from mapcreator import MapCreator 
from new_mapcreator import MapCreator

from surfacecreator import SurfaceCreator





import sys
from tabulate import tabulate

def exitWithMessage(message):
    print(message)
    input("# Naciśnij Enter, aby zamknąć aplikację...")
    sys.exit(1)

def exitWithoutMessage():
    input("# Naciśnij Enter, aby zamknąć aplikację...")
    sys.exit(1)

if __name__ == "__main__":

    # Inicjalizacja FilePathRequester i pobranie lokalizacji pliku CSV
    ###################################################################

    print("# Podaj lokalizacje pliku CSV z punktami współrzędnych")

    filePathRequester = FilePathRequester()
    if filePathRequester.askFilePath():
        filePath = filePathRequester.getPath()
        print("# Wskazanie lokalizacji pliku CSV przebiegło prawidłowo")
    else:
        exitWithMessage("# Nie wskazano lokalizacji pliku do odczytu")

    # Inicjalizacja FileReader i wczytanie zawartośći pliku
    ################################################################### 

    fileReader = FileReader(filePath)

    if fileReader.readFile():
        dataFrame = fileReader.getData()
        print("# Wczytywanie pliku CSV przebiegło prawidłowo")
    else:
        exitWithoutMessage()

    print()
    print(tabulate(dataFrame, headers = 'keys', tablefmt = 'fancy_grid'))
    print()
   
    # Inicjalizacja DataProcesor, weryfikacja i przetworzenie danych 
    # przed wstawieniem do bazy danych
    ###################################################################
    # -DODAĆ GENEROWANIE RAPORTU Z WYKRYTYMI BŁĘDAMI JEŚLI SIĘ POJAWIŁY
    ###################################################################

    dataProcessor = DataProcessor()
    
    errorStatus, errorList, dataFrame = dataProcessor.checkPointName(dataFrame)

    if not errorStatus:
        print("# Wszystkie punkty współrzędnych w pliku posiadają poprawne nazwy")
    else:
        for error in errorList:
            print(error)
    
    errorStatus, errorList, dataFrame = dataProcessor.checkAndConvertCoordinates(dataFrame)

    if not errorStatus:
        print("# Wszystkie punkty współrzędnych w pliku posiadają odpowiedni format współrzędnych geograficznych")
    else:
        for error in errorList:
            print(error)

    errorStatus, errorList, dataFrame = dataProcessor.checkAltitude(dataFrame)
    
    if not errorStatus:
        print("# Wszystkie punkty współrzędnych w pliku posiadają odpowiedni format wysokości n.p.m")
    else:
        for error in errorList:
            print(error)

    errorStatus, errorList, dataFrame = dataProcessor.checkDataAndTime(dataFrame)

    if not errorStatus:
        print("# Wszystkie punkty współrzędnych w pliku posiadają odpowiedni format znaczników czasowych")
    else:
        for error in errorList:
            print(error)

    errorStatus, errorList, dataFrame = dataProcessor.checkMetadata(dataFrame)

    if not errorStatus:
        print("# Wszystkie punkty współrzędnych w pliku posiadają odpowiedni format matadanych")
    else:
        for error in errorList:
            print(error)

    if not (dataValidationErrorStatus := dataProcessor.getDataValidationErrorStatus()):
        print()
        print("# Weryfikacja wszystkich danych z pliku przebiegła prawidłowo")
        print()
    else:
        print()
        exitWithMessage("! Weryfikacja wszystkich danych z pliku nie przebiegła prawidłowo")

    #########################################################

 # <- do tąd jest git
    

    # Inicjalizacja ConfigurationParameters i ConfigurationFlieMenager 
    # oraz wczytanie konfiguracji bądz jej utworzenie

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
        input("# Naciśnij Enter, aby zamknąć aplikację...") # to chyba do zmiany
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
            exitWithMessage("błąd bazy danych") # to chyba do zmiany

    while True:
        if databaseManager.checkDatabaseTableExistence():
            print("tabela danych istnieje")
            break
        elif not databaseManager.checkDatabaseTableExistence():
            print("tabela danych nie istnieje")
            print("Tworzenie tabeli danych")
            databaseManager.createDatabaseTable()

        else:
            exitWithMessage("błąd bazy danych") # to chyba do zmiany


    if (addedRow := databaseManager.insertData(dataFrame)) is not None:
        print(f"# Dodano {addedRow} nowych rekordów do bazy danych ")
    else:
        exitWithoutMessage()


    if (dataFrame := databaseManager.getData()) is not None:
        print(dataFrame)
        print(f"# Pobrano {len(dataFrame)} rekordów z bazy danych ")
    else:
        exitWithoutMessage()
#########################################################
#########################################################
#########################################################
    pointsDistanceMatrix, mergedRows = dataProcessor.createPointsDistanceMatrix(dataFrame)

    if mergedRows == 0:
        print("# Wszystkie pobrane lokalizacje z bazy danych są unikalne")
    else:
        print(f"# Scalono {mergedRows} lokalizacje z bazy danych")


    print(pointsDistanceMatrix)

    errorStatus, pointsIDList = dataProcessor.findClosestTrianglePoints(pointsDistanceMatrix)

    if errorStatus:
        exitWithMessage("# Liczba punktów nie jest wystarczająca do wyznaczenia płaszczyzny")

    print(f"Lista punktów: {pointsIDList}")



    #########################################################

    mapCreator = MapCreator(pointsDistanceMatrix)
    mapCreator.createMap()

    mapCreator.markAllPoints()




    
    exitWithoutMessage() #----------------------------------------------

#########################################################
#########################################################
#########################################################

    mapCreator = MapCreator(dataFrame)
    mapCreator.createMap()
    mapCreator.addPoint(dataFrame['coordinates'], "r.")

##################################################

    surfaceCreator = SurfaceCreator()

    startPointsID = surfaceCreator.searchStartingPoints(dataFrame['coordinates'])
    print(startPointsID)
    mapCreator.addPoint(startPointsID, "b.")

    startPointsID = surfaceCreator.searchNextPoints(dataFrame['coordinates'])
    mapCreator.addPoint(startPointsID, "b.")
    startPointsID = surfaceCreator.searchNextPoints(dataFrame['coordinates'])
    mapCreator.addPoint(startPointsID, "b.")
    startPointsID = surfaceCreator.searchNextPoints(dataFrame['coordinates'])
    mapCreator.addPoint(startPointsID, "b.")
    startPointsID = surfaceCreator.searchNextPoints(dataFrame['coordinates'])
    mapCreator.addPoint(startPointsID, "b.")









    exitWithMessage("")

