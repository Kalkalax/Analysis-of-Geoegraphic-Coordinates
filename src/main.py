from filepathrequester import FilePathRequester #klasa odpowiedzialna za zapytanie o plik CSV

if __name__ == "__main__":
    p1 = FilePathRequester()
    p1.askFilePath()
    path = p1.getPath()
    print(path)