import tkinter as tk
from tkinter import filedialog

class FilePathRequester:
    def __init__(self):
        self.filePath = ""

    def askFilePath(self):
        root = tk.Tk() #Ukrycie okna Tk
        root.withdraw()

        self.filePath = filedialog.askopenfilename(filetypes=[("Pliki CSV", "*.csv")])

    def getPath(self):
        return self.filePath