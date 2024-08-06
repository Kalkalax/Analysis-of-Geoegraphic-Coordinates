from filepathrequester import FilePathRequester #klasa odpowiedzialna za zapytanie o plik CSV
from filereader import FileReader #klasa odpowiedzialna za wczytanie i sprawdzenie pliku CSV

import sys

def exitWithMessage(message):
    print(message)
    input("Naciśnij Enter, aby zamknąć aplikację...")
    sys.exit(1)




if __name__ == "__main__":

    filePathRequester = FilePathRequester()
    filePathRequester.askFilePath()
    filePath = filePathRequester.getPath()

    #print("Pobrana scieżka pliku: " + filePath)

    #Inicjalizacja FileReader oraz przeprowadzenie weryfikacji

    fileReader = FileReader(filePath)
    dataFrame = fileReader.readFile()
    
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


    

