import tkinter as tk # Library for creating graphical interfaces
from tkinter import filedialog # Module to open dialogues for file selection


# Class that handles the selection of the file path and passing it on to the next class
class FilePathRequester:
    def __init__(self):
        self.filePath = ""  

    # Method to launch file selection dialog box
    def askFilePath(self):

        # Initialise the Tkinter window and hide the main window to make it invisible
        root = tk.Tk()  
        root.withdraw()

        # Call up dialog box to select CSV file
        self.filePath = filedialog.askopenfilename(filetypes=[("Pliki CSV", "*.csv")])
        
        # Checking whether the user has selected a file
        if not self.filePath == "":
            return True 
        else:
            return False  

    # Method that returns the path to the selected files
    def getPath(self):
        return self.filePath  