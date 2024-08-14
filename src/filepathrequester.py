import tkinter as tk
from tkinter import filedialog

#Klasa obsługująca wybór scieżki do pliku i zwrócenie jej kolejnej klasie
class FilePathRequester:
    def __init__(self):
        self.filePath = ""

    #Metoda uruchamiająca wywołanie okna dialogowego do wyboru pliku
    def askFilePath(self):

        root = tk.Tk() #Ukrycie okna Tk
        root.withdraw()

        self.filePath = filedialog.askopenfilename(filetypes=[("Pliki CSV", "*.csv")])
        if not self.filePath == "":
            return True
        else:
            return False

    #Metoda zwracająca scieżke do wybranego pliku
    def getPath(self):
        
        return self.filePath