import pytest
from unittest.mock import patch

# Dodaj folder src do ścieżki wyszukiwania modułów
from src.filepathrequester import FilePathRequester

class TestFilePathRequester:

    def test_askFilePath(self, mocker):
        # Zamockowanie funkcji `askopenfilename` z modułu `tkinter.filedialog`
        # `mocker.patch` tworzy mock obiektu, który zastępuje oryginalną funkcję w czasie testu.
        mock_askopenfilename = mocker.patch('tkinter.filedialog.askopenfilename')
        
        # Ustalenie, że zamockowana funkcja `askopenfilename` ma zwracać '/path/to/file.csv'
        mock_askopenfilename.return_value = '/path/to/file.csv'
        
        # Utworzenie instancji klasy `FilePathRequester`, która jest testowana
        requester = FilePathRequester()
        
        # Wywołanie metody `askFilePath` na obiekcie `requester`, 
        # która powinna użyć zamockowanej funkcji `askopenfilename`
        requester.askFilePath()
        
        # Sprawdzenie, że zamockowana funkcja `askopenfilename` została wywołana dokładnie raz
        mock_askopenfilename.assert_called_once()
        
        # Sprawdzenie, że metoda `getPath` zwraca ścieżkę pliku ustawioną przez zamockowaną funkcję
        assert requester.getPath() == '/path/to/file.csv'


    def test_askFilePath_no_file_selected(self, mocker):
        mock_askopenfilename = mocker.patch('tkinter.filedialog.askopenfilename')
        mock_askopenfilename.return_value = ''
        
        requester = FilePathRequester()
        requester.askFilePath()
        
        mock_askopenfilename.assert_called_once()
        assert requester.getPath() == ''
