from filepathrequester import FilePathRequester #klasa odpowiedzialna za zapytanie o plik CSV
from filereader import FileReader #klasa odpowiedzialna za wczytanie i sprawdzenie pliku CSV

if __name__ == "__main__":

    filePathRequester = FilePathRequester()
    filePathRequester.askFilePath()
    filePath = filePathRequester.getPath()

    #print("Pobrana scieżka pliku: " + filePath)

    fileReader = FileReader(filePath)
    dataFrame = fileReader.readFile()
    
    #fileReader.checkPointName()
    if not fileReader.checkPointName():
        print("Wykryto nieakceptowalny znak w nazwie punktu")
    else:
        print("GIT")

    #fileReader.checkCoordinates()
    if not fileReader.checkCoordinates():
        print("Wykryto nieakceptowalny znak w współrzędnych")
    else:
        print("GIT")


