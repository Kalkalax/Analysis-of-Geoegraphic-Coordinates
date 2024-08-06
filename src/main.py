from filepathrequester import FilePathRequester #klasa odpowiedzialna za zapytanie o plik CSV
from filereader import FileReader #klasa odpowiedzialna za wczytanie i sprawdzenie pliku CSV

import sys

if __name__ == "__main__":

    filePathRequester = FilePathRequester()
    filePathRequester.askFilePath()
    filePath = filePathRequester.getPath()

    #print("Pobrana scieżka pliku: " + filePath)

    #Inicjalizacja FileReader oraz przeprowadzenie weryfikacji

    fileReader = FileReader(filePath)
    dataFrame = fileReader.readFile()
    
    if not fileReader.checkPointName():
        print("Wykryto nieakceptowalny znak w nazwie punktu")
        input("Naciśnij Enter, aby zamknąć aplikację...")
        sys.exit(1)
    
    elif not fileReader.checkCoordinates():
        print("Wykryto nieakceptowalny znak w współrzędnych")
        input("Naciśnij Enter, aby zamknąć aplikację...")
        sys.exit(1)

    elif not fileReader.checkAltitude():
        print("Wykryto nieakceptowalny znak w wysokości")
        input("Naciśnij Enter, aby zamknąć aplikację...")
        sys.exit(1)

    elif not fileReader.checkDataAndTime():
        print("Wykryto nieakceptowalny znak w znaczniku czasowym")
        input("Naciśnij Enter, aby zamknąć aplikację...")
        sys.exit(1)

    else:
        print("Wprowadzone dane nie zawierają błędów")
        input("Naciśnij Enter, aby zamknąć aplikację...")
        sys.exit(1)

    

