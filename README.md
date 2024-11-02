<h1 align="center">Analysis of Geoegraphic Coordinates</h1>

<p align="center">
  <a href="https://github.com/kamilkalarus">Kamil Kalarus</a>
</p>

## Description

Aplikacja służy do wizualizacji zamkniętej figury geometrycznej na interaktywnej mapie, która powstaje w wyniku połączenia wszystkich punktów geograficznych. Umożliwia to wyznaczenie rzeczywistego obwodu stworzonej figury. 

Dane geograficzne importowane są z plików CSV, co pozwala na łatwe dodawanie lokalizacji i tworzenie złożonych kształtów.Po zaimportowaniu dane przechodzą skrupulatną weryfikację pod kątem zgodności formatów. Po pozytywnej weryfikacji, są one przechowywane w bazie danych PostgreSQL, co zapewnia ich bezpieczeństwo oraz wydajność. Następnie aplikacja wyznacza zamkniętą figurę geometryczną z pobranych lokalizacji, nanosi ją na mapę świata oraz oblicza jej rzeczywisty obwód.

## Table of contents
- [Functionality](#functionality)
- [Demo](#demo)
- [Requirements](#requirements)
  - [Operating System](#operating-system)
  - [Software versions](#software-versions)
  - [Python libraries](#python-libraries)
- [Setup](#setup)
  - [Using a ready-made `.exe` file (_relese_)](#using-a-ready-made-exe-file-relese)
  - [Manual (_develop_)](#manual-develop)
- [Input data set](#input-data-set)
  - [Data format requirements](#data-format-requirements)
  - [Example content of CSV data file](#example-content-of-csv-data-file)
- [Documentation](#documentation)


## Functionality

- ***Import plików CSV*** - Aplikacja umożliwia użytkownikowi załadowanie pliku CSV z danymi geograficznymi oraz sprawdza, czy plik jest dostępny i poprawnie wskazany.

- ***Weryfikacja danych*** - Przeprowadza kontrolę danych w pliku CSV, aby upewnić się, że nie zawierają błędów. W przypadku wykrycia problemów, aplikacja informuje użytkownika o koniecznych poprawkach.

- ***Obsługa pliku konfiguracyjnego*** - Aplikacja sprawdza obecność pliku konfiguracyjnego z danymi logowania do bazy danych. Jeśli go nie ma, automatycznie go tworzy.

- ***Tworzenie bazy danych*** - Jeśli wskazana baza danych nie istnieje, aplikacja tworzy nową bazę oraz odpowiednie tabele. W przeciwnym razie sprawdza, czy tabele są już utworzone.

- ***Wprowadzanie danych do bazy*** - Tylko zweryfikowane dane są wprowadzane do bazy danych. Aplikacja zapewnia, że nie wystąpią duplikaty.

- ***Wyciąganie danych z bazy*** - Aplikacja pobiera dane z bazy danych i wyświetla je na mapie świata, unikając powtarzających się punktów, jeśli ich godziny lub inne wartości są identyczne.

- ***Rysowanie figury geometrycznej*** - Algorytm identyfikuje pierwsze trzy punkty i sprawdza możliwość utworzenia zamkniętej figury. Dla większej liczby punktów do figury dodawany jest najbliższy punkt.

- ***Interaktywne wyświetlanie działań algorytmu*** - Każdy krok algorytmu jest na bieżąco wyświetlany użytkownikowi, co pozwala mu obserwować postęp w tworzeniu figury i doborze najbliższego punktu.

## Demo
Poniżej przedstawiono działanie algorytmu na 22 punktach lokalizacyjnych, z których dwa zostały scalone ze względu na identyczne współrzędne geograficzne.

  ![Demo aplikacji](docs/demo.gif)

## Requirements

Aby zagwarantować poprawne działanie aplikacji, należy spełnić poniższe wymagania. Aplikacja nie była testowana na innych konfiguracjach, co może stanowić potencjalne ryzyko dla jej prawidłowego funkcjonowania.

#### Operating System:
- Windows 11 Home 23H2+
#### Software versions:
- Python 3.12+
- PostgreSQL 16
- pgAdmin 4 (optionally)
#### Python libraries:
- `pandas`, `numpy`, `matplotlib`, `basemap`, `basemap_data`, `psycopg2`, `tabulate`, `haversin`


## Setup

### Using a ready-made `.exe` file (_relese_)

Aby uruchomić aplikacje bez instalacji należy pobrać zawartość z gałęzi `relese`. Następnie należy uruchomić `AoGC.exe. 

>Pamiętaj instalacja PostgreSQL 16 jest niezbędna do prawidłowego funkcjonowania bazy danych. Możliwe, że będzie również wymagana dodatkowa konfiguracja.


### Manual (_develop_)

Aby uruchomić aplikacje w interpreterze jezyka Python należy zainstalowac wymagane biblioteki. Aby to zrobić otwórz konsole w lokalizacji repozytorium i użyj jednego z poniższych poleceń:
- W konsoli języka Python:

  ```python
  pip install -r docs/requirements.txt 
  ```
- bądz w wierszu poleceń (cmd):

  ```python
  python3 -m pip install -r docs/requirements.txt 
  ```


## Input data set
### Data format requirements
Aplikacja przyjmuje dane tylko w rozszerzeniu `.csv`. Dane wejściowe muszą być odpowiednio wstępnie sformatowane.
Każdy plik danych powinien zawierać dane jak w przykładzie poniżej, kolejność kolumn w pliku nie może ulec zmianie (w razie takiej potrzeby należy zmodyfikować klase `DataProcessor`)

Poniżej w tabeli zamieszczono szczegółowy opis każdej z kolumn:

|Kolumna|Opis|Uwagi|
|:--------:|:--------:|:--------:|
|point name|Nazwa punktu współrzędnych bądz nazwa własnna | Może zawierać tylko znaki alfabetu łacińskiego
|coordinates|Współrzędne geograficzne punktu |Akceptowalne są dane w formacie dziesiętnym, w stopnaich, w stopniach z minutami, oraz w stopniach z minutami i sekundami<sup>1</sup>|
|altitude|Wysokość punktu n.p.m| Wartość musi być wyrażona w kilometrach|
|metadata|Dodatkowe metadane| Nie są wymagane do prawidłowego działania<sup>2</sup>|

<sup>1</sup> w razie problemów z danymi można zmodyfikować regexy znajdujące się w `dataprocessor.checkAndConvertCoordinates()` bądz dostosować dane do wymaganego formatu. Wszystkie akceptowalne formaty znajdują się poniżej a ich działanie można sprawdzić na stronie [regex101: build, test, and debug regex](https://regex101.com/)

```regex
^(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)$
^([NS])(\d{1,3}\.\d+)°,([EW])(\d{1,3}\.\d+)°$
^([NS])(\d{1,3})°(\d{1,3}\.\d+),([EW])(\d{1,3})°(\d{1,3}\.\d+)$
^([NS])(\d{1,3})°(\d{1,3})'(\d{1,3}\.\d+)\"\,([EW])(\d{1,3})°(\d{1,3})'(\d{1,3}\.\d+)\"$
```
<sup>2</sup> jeśli metadane będą wymagały weryfikacji należy zmodyfikować metode `dataprocessor.checkMetadata()` uzupełniając ją o własną metode weryfikacji (domyślnie nieużywana)

### Example content of CSV data file
```csv
point name;coordinates;altitude;data and time;metadata
Tokyo;N35°40'58.220",E139°45'34.038";0.044;15.06.2024 08:20;
```

## Documentation

[Documentation](docs/Documentation.md)
