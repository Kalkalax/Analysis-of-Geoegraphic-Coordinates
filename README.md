<h1 align="center">Analysis of Geoegraphic Coordinates</h1>

<p align="center">
  <a href="https://github.com/kamilkalarus">Kamil Kalarus</a>
</p>

## Description

The application is used to visualise a closed geometric figure on an interactive map, which is created by connecting all geographical points. This makes it possible to determine the actual perimeter of the created figure. 

Geographical data is imported from CSV files, allowing you to easily add locations and create complex shapes.Once imported, the data undergoes a meticulous verification for format compatibility. Once successfully verified, they are stored in a PostgreSQL database, ensuring their security and performance. The application then determines a closed geometric figure from the downloaded locations, plots it on a world map and calculates its actual perimeter.

## Table of contents
- [Functionality](#functionality)
- [Demo](#demo)
- [Requirements](#requirements)
  - [Operating System](#operating-system)
  - [Software versions](#software-versions)
  - [Python libraries](#python-libraries)
- [Setup](#setup)
  - [Using a ready-made .exe file (_relese_)](#using-a-ready-made-exe-file-relese)
  - [Manual (_develop_)](#manual-develop)
- [Input data set](#input-data-set)
  - [Data format requirements](#data-format-requirements)
  - [Example content of CSV data file](#example-content-of-csv-data-file)
- [Documentation](#documentation)


## Functionality

- ***Import of CSV files*** - The application allows the user to upload a CSV file with geographical data and checks that the file is available and correctly indicated.

- ***Data verification*** - It performs a check of the data in the CSV file to ensure that it does not contain errors. If problems are detected, the application informs the user of the necessary corrections.

- ***Configuration file support*** - The application checks for the presence of a configuration file with database login data. If it is not present, it automatically creates it.

- ***Creation of a database*** - If the indicated database does not exist, the application creates a new database and the corresponding tables. Otherwise, it checks whether the tables are already created.

- ***Entry of data into the database*** - Only verified data is entered into the database. The application ensures that no duplicates occur.

- ***Extracting data from the database*** - The application takes data from the database and displays it on a world map, avoiding repeated points if their times or other values are identical.

- ***Drawing a geometric figure*** - The algorithm identifies the first three points and checks the possibility of forming a closed figure. For a larger number of points, the nearest point is added to the figure.

- ***Interactive display of algorithm activities*** - Each step of the algorithm is continuously displayed to the user, allowing them to observe the progress of the figure and the selection of the nearest point.

## Demo
The performance of the algorithm on 22 location points, two of which were merged due to identical geographical coordinates, is shown below.

  ![Demo aplikacji](docs/demo.gif)

## Requirements

The following requirements must be met in order to guarantee the correct functioning of the application. The application has not been tested on other configurations, which may pose a potential risk to its correct functioning.

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

To run the applications without installation, download the contents from the `relese` branch. Then run `AoGC.exe`. 

>Remember the installation of PostgreSQL 16 is necessary for the database to function properly. It is also possible that additional configuration will be required.


### Manual (_develop_)

To run applications in the Python language interpreter, the required libraries must be installed. To do this, open the console in the repository location and use one of the following commands:
- In the Python language console:

  ```python
  pip install -r docs/requirements.txt 
  ```
- or on the command line (cmd):

  ```python
  python3 -m pip install -r docs/requirements.txt 
  ```


## Input data set
### Data format requirements
The application only accepts data in the `.csv` extension. The input data must be pre-formatted accordingly.
Each data file should contain data as in the example below, the order of columns in the file must not be changed (modify the `DataProcessor` class if necessary)

The table below provides a detailed description of each column:

|Column|Description|Notes|
|:--------:|:--------:|:--------:|
|point name|Name of coordinate point or own name | May contain only Latin characters
|coordinates|Geographical coordinates of the point |Data in decimal format, in degrees, in degrees with minutes, and in degrees with minutes and seconds are acceptable<sup>1</sup>|
|altitude|Altitude of point| The value must be expressed in kilometres|
|metadata|Additional metadata| Not required for proper operation<sup>2</sup>|

<sup>1</sup> If you have problems with the data, you can modify the regexes found in `dataprocessor.checkAndConvertCoordinates()` or adapt the data to the required format. All acceptable formats are listed below and can be checked at [regex101](https://regex101.com/):

```regex
^(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)$
^([NS])(\d{1,3}\.\d+)°,([EW])(\d{1,3}\.\d+)°$
^([NS])(\d{1,3})°(\d{1,3}\.\d+),([EW])(\d{1,3})°(\d{1,3}\.\d+)$
^([NS])(\d{1,3})°(\d{1,3})'(\d{1,3}\.\d+)\"\,([EW])(\d{1,3})°(\d{1,3})'(\d{1,3}\.\d+)\"$
```
<sup>2</sup> if the metadata needs to be verified, modify the `dataprocessor.checkMetadata()` method with your own verification method (not used by default)

### Example content of CSV data file
```csv
point name;coordinates;altitude;data and time;metadata
Tokyo;N35°40'58.220",E139°45'34.038";0.044;15.06.2024 08:20;
```

## Documentation

[Documentation](docs/Documentation.md)
