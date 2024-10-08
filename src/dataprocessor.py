import re
import numpy as np
import pandas as pd

class DataProcessor:
    def __init__(self):
        self.dataValidationErrorStatus = False
        self.usedPointsIDList = []


    def checkPointName(self, dataFrame):

        errorStatus = False
        errorList = []

        for index in range(len(dataFrame)):

            value = dataFrame.iloc[index, 0]

            if not re.match("^[A-Z][a-z]*(\s[a-zA-Z][a-z]*)*$", str(value)):
                
                errorStatus = True
                self.dataValidationErrorStatus = errorStatus
                errorList.append(f"! Nazwa punktu '{value}' o indeksie ID = {index} zawiera niedozwolone znaki")
    
        return errorStatus, errorList, dataFrame

    def checkAndConvertCoordinates(self, dataFrame, decimalplaces = 6):

        errorStatus = False
        errorList = []

        for index in range(len(dataFrame)):

            value = dataFrame.iloc[index, 1]
            
            if (pattern := re.match(r"^(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)$", str(value))):
                
                latitude = round(float(pattern.group(1)), decimalplaces)
                longitude = round(float(pattern.group(2)), decimalplaces)

            elif (pattern := re.match(r"^([NS])(\d{1,3}\.\d+)°,([EW])(\d{1,3}\.\d+)°$", str(value))):
                
                latitude = round(float(pattern.group(2)) * (-1 if pattern.group(1) == 'S' else 1), decimalplaces)
                longitude = round(float(pattern.group(4)) * (-1 if pattern.group(3) == 'W' else 1), decimalplaces)

            elif (pattern := re.match(r"^([NS])(\d{1,3})°(\d{1,3}\.\d+),([EW])(\d{1,3})°(\d{1,3}\.\d+)$", str(value))):
                
                latitude = round(int(pattern.group(2)) + float(pattern.group(3)) / 60 * (-1 if pattern.group(1) == 'S' else 1), decimalplaces)
                longitude = round(int(pattern.group(5)) + float(pattern.group(6)) / 60 * (-1 if pattern.group(4) == 'W' else 1), decimalplaces)

            elif (pattern := re.match(r"^([NS])(\d{1,3})°(\d{1,3})'(\d{1,3}\.\d+)\"\,([EW])(\d{1,3})°(\d{1,3})'(\d{1,3}\.\d+)\"$", str(value))):

                latitude = round(int(pattern.group(2)) + int(pattern.group(3)) / 60 + float(pattern.group(4)) / 3600 * (-1 if pattern.group(1) == 'S' else 1), decimalplaces)
                longitude = round(int(pattern.group(6)) + int(pattern.group(7)) / 60 + float(pattern.group(8)) / 3600 * (-1 if pattern.group(5) == 'W' else 1), decimalplaces)

            else:

                errorStatus = True
                self.dataValidationErrorStatus = errorStatus
                errorList.append(f"! Kordynaty punktu '{value}' o indeksie ID = {index} posiadają nie odpowiedni format")
                
            dataFrame.iloc[index, 1] = f"{latitude},{longitude}"

        return errorStatus, errorList, dataFrame
    
    def checkAltitude(self, dataFrame):

        errorStatus = False
        errorList = []

        for index in range(len(dataFrame)):

            value = dataFrame.iloc[index, 2]

            if not re.match("^\d\.\d+$", str(value)):
                
                errorStatus = True
                self.dataValidationErrorStatus = errorStatus
                errorList.append(f"! Wysokość punktu '{value}' o indeksie ID = {index} zawiera niepoprawny format")
        
        return errorStatus, errorList, dataFrame

    def checkDataAndTime(self, dataFrame):

        errorStatus = False
        errorList = []

        for index in range(len(dataFrame)):

            value = dataFrame.iloc[index, 3]

            if not re.match("^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}$", str(value)):
                
                errorStatus = True
                self.dataValidationErrorStatus = errorStatus
                errorList.append(f"! Znacznik czasowy punktu '{value}' o indeksie ID = {index} zawiera niepoprawny format")
        
        return errorStatus, errorList, dataFrame
    
    def checkMetadata(self, dataFrame):

        errorStatus = False
        errorList = []

        return errorStatus, errorList, dataFrame

    def getDataValidationErrorStatus(self):

        return self.dataValidationErrorStatus
    
    def createPointsDistanceMatrix(self, dataFrame):

        inputDataFrameSize = 0
        outputDataFrameSize = 0
        mergedRows = 0

        pointsDistanceMatrix = dataFrame['coordinates'].str.split(',', expand=True)

        inputDataFrameSize = len(pointsDistanceMatrix)

        pointsDistanceMatrix.columns = ['Latitude', 'Longitude']  # Nadawanie nazw kolumn
        pointsDistanceMatrix[['Latitude', 'Longitude']] = pointsDistanceMatrix[['Latitude', 'Longitude']].astype(float)
        
        pointsDistanceMatrix['Distance_from_origin'] = np.sqrt(pointsDistanceMatrix['Latitude']**2 + pointsDistanceMatrix['Longitude']**2)

        distance_matrix = pd.DataFrame(index = pointsDistanceMatrix.index, columns = pointsDistanceMatrix.index)

        for i, start_point in pointsDistanceMatrix.iterrows():
            for j, end_point in pointsDistanceMatrix.iterrows():
                if i != j:
                    distance = np.sqrt((end_point['Latitude'] - start_point['Latitude']) ** 2 + 
                                    (end_point['Longitude'] - start_point['Longitude']) ** 2)
                    distance_matrix.iloc[i, j] = distance
                else:
                    distance_matrix.iloc[i, j] = np.nan

        distance_matrix.columns = [f'Distance_to_point_{i}' for i in range(len(pointsDistanceMatrix))]
        distance_matrix.index = pointsDistanceMatrix.index

        pointsDistanceMatrix = pd.concat([pointsDistanceMatrix, distance_matrix], axis=1)

        #pointsDistanceMatrix = pointsDistanceMatrix.drop_duplicates(subset=['Latitude', 'Longitude'])

        #Nowe usuwanie duplikatów
        duplicateLocations = pointsDistanceMatrix[pointsDistanceMatrix.duplicated(subset=['Latitude', 'Longitude'], keep='first')]
        duplicateLocationsID = duplicateLocations.index.tolist()

        for ID in duplicateLocationsID:

            pointsDistanceMatrix = pointsDistanceMatrix.drop(ID)
            pointsDistanceMatrix = pointsDistanceMatrix.drop(columns = f"Distance_to_point_{ID}")


        
        outputDataFrameSize = len(pointsDistanceMatrix)
        mergedRows = inputDataFrameSize - outputDataFrameSize
        
        return pointsDistanceMatrix, mergedRows
    
    def findClosestTrianglePoints(self, pointsDistanceMatrix):

        errorStatus = False
        pointsIDList = []

        if len(pointsDistanceMatrix) < 3:

            errorStatus = True

        else:
            
            pointID = pointsDistanceMatrix.nsmallest(1, "Distance_from_origin").index[0]
            pointsIDList = [pointID]

            row = pointsDistanceMatrix.iloc[[pointID]]
        
            cleanedRow = row.iloc[:, 3:]
            cleanedRow = cleanedRow.dropna(axis=1, how='any')

            pointID = cleanedRow.idxmin(axis=1)

            #musimy wyciagnać który punkt zostal znaleziony
            pointID = pointID.iloc[0]
            pointID = int(pointID.split('_')[-1])
            
            pointsIDList += [pointID]

            row = pointsDistanceMatrix
            cleanedRow = row.iloc[:, 3:]
            cleanedRow = cleanedRow.drop(pointsIDList)
            cleanedRow[f'Sum_of_distances_to_{pointsIDList[0]}_and_{pointsIDList[-1]}'] = cleanedRow[f'Distance_to_point_{pointsIDList[0]}'] + cleanedRow[f'Distance_to_point_{pointsIDList[-1]}']
            
            pointID = cleanedRow[f'Sum_of_distances_to_{pointsIDList[0]}_and_{pointsIDList[-1]}'].idxmin()
            pointsIDList += [pointID]

            self.usedPointsIDList = pointsIDList

        return errorStatus, pointsIDList
        
    def findNextClosestPoints(self):

        pass
        