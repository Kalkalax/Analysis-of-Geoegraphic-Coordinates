from filepathrequester import FilePathRequester # Class responsible for asking the user for the path to the CSV file
from filereader import FileReader # Class responsible for loading and validating a CSV file
from dataprocessor import DataProcessor # Class responsible for verification and data operations
from configurationparameters import ConfigurationParameters # Class containing database configuration parameters
from configurationfliemenager import ConfigurationFlieMenager # Class responsible for validating, loading and creating database configurations
from databasemanager import DatabaseManager # The class responsible for managing and creating the database
from mapcreator import MapCreator # Class responsible for displaying and updating the map based on the data
import sys # Module providing access to system-specific functions and parameters
from tabulate import tabulate  # Library function for formatting data into tables

def exitWithMessage(message):
    print(message)
    input("# Press Enter to close the application....")
    sys.exit(1)

def exitWithoutMessage():
    input("# Press Enter to close the application....")
    sys.exit(1)

if __name__ == "__main__":

    ###################################################################

    print("# Specify the locations of the CSV file with the coordinate points.")

    # FilePathRequester initialisation
    filePathRequester = FilePathRequester()

    # Download the path to the file specified by the user and display a message about the progress of the operation
    if filePathRequester.askFilePath():
        filePath = filePathRequester.getPath()
        print("# The indication of the location of the CSV file has proceeded correctly.")
    else:
        exitWithMessage("# No read file location indicated.")

    ################################################################### 

    # FileReader initialisation
    fileReader = FileReader(filePath)

    # Load the CSV file from the specified location and display a message about the progress of the operation
    if fileReader.readFile():
        dataFrame = fileReader.getData()
        print("# The CSV file has been loaded correctly.")
    else:
        exitWithoutMessage()

    # Display in table form the data loaded from the indicated file
    print()
    print(tabulate(dataFrame, headers = 'keys', tablefmt = 'fancy_grid'))
    print()
   
    ###################################################################

    # DataProcessor initialisation
    dataProcessor = DataProcessor()
    
    # Verification of the format of the names of the indicated geographical points and return of the verification status
    errorStatus, errorList, dataFrame = dataProcessor.checkPointName(dataFrame)

    # Display a corresponding message about the progress of the verification of the format of the geographical point names
    if not errorStatus:
        print("# All coordinate points in the file have correct names.")
    else:
        for error in errorList:
            print(error)
    
    # Verify coordinate format, convert forgivable forms to a single standard and return verification status
    errorStatus, errorList, dataFrame = dataProcessor.checkAndConvertCoordinates(dataFrame)

    # Display a corresponding message about the progress of coordinate format verification
    if not errorStatus:
        print("# All coordinate points in the file have the correct geographical coordinate format.")
    else:
        for error in errorList:
            print(error)

    # Verify altitude format and return verification status
    errorStatus, errorList, dataFrame = dataProcessor.checkAltitude(dataFrame)
    
    # Display a corresponding message about the progress of the altitude format verification
    if not errorStatus:
        print("# All coordinate points in the file have the correct altitude format.")
    else:
        for error in errorList:
            print(error)

    # Verify timestamp format and return verification status
    errorStatus, errorList, dataFrame = dataProcessor.checkDataAndTime(dataFrame)

    # Display the corresponding timestamp format verification progress message
    if not errorStatus:
        print("# All coordinate points in the file have a corresponding timestamp format.")
    else:
        for error in errorList:
            print(error)

    # Verify metadata format and return verification status
    errorStatus, errorList, dataFrame = dataProcessor.checkMetadata(dataFrame)

    # Display an appropriate message about the progress of the metadata format verification
    if not errorStatus:
        print("# All coordinate points in the file have the appropriate matadata format.")
    else:
        for error in errorList:
            print(error)

    # Retrieve the verification status of all data and display a corresponding message
    if not (dataValidationErrorStatus := dataProcessor.getDataValidationErrorStatus()):
        print()
        print("# Verification of all data from the file has been successful.")
        print()
    else:
        print()
        exitWithMessage("# Verification of all data in the file did not take place correctly.")

    ###################################################################

    # Initialisation of ConfigurationParameters and ConfigurationFlieMenager
    configurationParameters = ConfigurationParameters()
    configurationFlieMenager = ConfigurationFlieMenager(configurationParameters)
    
    # Loop iterating until a suitable database configuration is found or created and displaying a message about the operations performed
    while True:
        if configurationFlieMenager.checkExistenceConfigFile():
            break
        else:
            print("# The database configuration file 'config.py' does not exist.")
            print("# Create database configuration file 'config.py'.")
            configurationFlieMenager.createConfigFile()

    # Loading configuration from designated file
    config = configurationFlieMenager.readConfigFile()
    
    # Check the status of the loaded configuration and display a corresponding status message
    if config: 
        print("# The database configuration file 'config.py' was loaded correctly.")
        print()
    else:
        exitWithMessage("# The database configuration file 'config.py' was not loaded correctly.")

    #########################################################

    # Initialisation of the DatabaseManager
    databaseManager = DatabaseManager(config)

    # A loop iterating until a suitable database is found or created and displaying an appropriate message about the operations performed
    while True:
        if databaseManager.checkDatabaseExistence():
            print(f"# The database {configurationParameters.dbname} exists.")
            break
        elif not databaseManager.checkDatabaseExistence():
            print(f"# The database {configurationParameters.dbname} does not exist.")
            print(f"# Create database {configurationParameters.dbname}.")
            databaseManager.createDatabase()
            print(f"# Create data table {configurationParameters.tbname}.")
            databaseManager.createDatabaseTable()
        else: 
            exitWithoutMessage()

    # Loop iterating until a suitable data table is found or created and displaying an appropriate message about the operations performed
    while True:
        if databaseManager.checkDatabaseTableExistence():
            print(f"# The data table {configurationParameters.tbname} exists.")
            break
        elif not databaseManager.checkDatabaseTableExistence():
            print(f"# The data table {configurationParameters.tbname} does not exist.")
            print(f"# Create data table {configurationParameters.tbname}.")
            databaseManager.createDatabaseTable()

        else:
            exitWithoutMessage()

    print()

    # Add new data to the database and display a message about the amount of data added
    if (addedRow := databaseManager.insertData(dataFrame)) is not None:
        print(f"# Added {addedRow} new records to the database.")
    else:
        exitWithoutMessage()

    # Download all data from the database and display a message about the amount of data downloaded
    if (dataFrame := databaseManager.getData()) is not None:
        print(f"# Downloaded {len(dataFrame)} records from the database.")
    else:
        exitWithoutMessage()
    
    print()

    #########################################################

    # Create a matrix of distances of unique points from each other
    pointsDistanceMatrix, mergedRows = dataProcessor.createPointsDistanceMatrix(dataFrame)

    # Display a message about the number of merged locations
    if mergedRows == 0:
        print("# All retrieved locations from the database are unique.")
    else:
        print(f"# Merged {mergedRows} locations from the database.")
    print()

    #########################################################

    # MapCreator initialisation and world map display
    mapCreator = MapCreator(pointsDistanceMatrix)
    mapCreator.createMap()

    # Draw all points on the map and update the chart
    mapCreator.markAllPoints()
    mapCreator.updatChart()

    #########################################################

    # Finding the three points that determine the starting triangle needed to connect all the points
    errorStatus, pointsIDList = dataProcessor.findClosestTrianglePoints(pointsDistanceMatrix)

    # Display a message whether the operation to determine a geometric figure from the found points is possible
    if errorStatus:
        exitWithMessage("# The number of points is not sufficient to determine the plane")
    else:
        print(f"# The figure connecting the marked points has been drawn")

    # Display a message about the status of the points used
    pointsDistanceMatrixSize = len(pointsDistanceMatrix)
    print(f"# Points used: {len(pointsIDList)} / {pointsDistanceMatrixSize}")

    #########################################################

    # Change the colour of the vertices of the start triangle on the graph and update the graph
    mapCreator.changePointColor(pointsIDList)
    mapCreator.updatChart()

    # Connect the designated points forming a triangle with lines and update the graph
    mapCreator.drawLineConnectingPoints(pointsIDList)
    mapCreator.updatChart()

    # Transfer of map configuration from MapCreator to dataProcessor
    dataProcessor.map = mapCreator.map
    dataProcessor.fig = mapCreator.fig
    dataProcessor.ax = mapCreator.ax
    
    # Loop iterating until all coordinate points are used
    while True:

        # Finding the nearest point from those already used
        newPointID = dataProcessor.findNextClosestPoints(pointsDistanceMatrix)

        if newPointID is None:
            break
        else:
            
            # Change the colour of the newly found nearest point and update the chart
            mapCreator.changePointColor(newPointID)
            mapCreator.updatChart()

            # Finding the right sequence of connecting points to eliminate line intersections
            pointsIDList = dataProcessor.sortingPointsList(pointsDistanceMatrix, pointsIDList, newPointID)

            # Delete old lines, apply new lines in order and update chart
            mapCreator.drawLineConnectingPoints(pointsIDList)
            mapCreator.updatChart()

            # Display a message about the status of the points used
            print(f"# Points used: {len(pointsIDList)} / {pointsDistanceMatrixSize}")

    print()

    # Display a message that the process of connecting all lines and the order of connecting points is complete
    print(f"# The figure connecting all the marked points has been determined")
    print("# Final order of connecting points:", pointsIDList)

    #########################################################
          
# Stop the program until the user closes it
exitWithoutMessage()
