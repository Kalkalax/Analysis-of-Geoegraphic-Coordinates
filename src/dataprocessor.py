import re
import numpy as np
import pandas as pd

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt


class DataProcessor:
    def __init__(self):
        self.dataValidationErrorStatus = False
        self.usedPointsIDList = []
        self.fig, self.ax = plt.subplots(figsize=(8.00, 8.00), frameon=False)
        self.map = Basemap(projection='merc', llcrnrlat=-85, urcrnrlat=85, llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c', ax=self.ax) 
        # TRZEBA TU ZROBIĆ POBIERANIE SELF.MAP I SELF.FIG Z MAPCREATOR


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
    
    # szukamy najblizszego punktu od środka, a następnie punkt który jest najbliżej niego, 
    # następnie szukamy punktu ktorych suma odleglości do dwoch poprzednich jest najmniejsza
    def findClosestTrianglePoints(self, pointsDistanceMatrix):

        errorStatus = False
        pointsIDList = []

        if len(pointsDistanceMatrix) < 3:

            errorStatus = True

        else:
            #print(pointsDistanceMatrix)
            pointID = pointsDistanceMatrix.nsmallest(1, "Distance_from_origin").index[0]
            pointsIDList = [pointID]

            row = pointsDistanceMatrix.loc[[pointID]]
            #print(row)
        
            cleanedRow = row.iloc[:, 3:]
            cleanedRow = cleanedRow.dropna(axis=1, how='any')
            #print(cleanedRow)

            pointID = cleanedRow.idxmin(axis=1)


            #musimy wyciagnać który punkt zostal znaleziony
            pointID = pointID.iloc[0]
            pointID = int(pointID.split('_')[-1])
            
            pointsIDList = pointsIDList + [pointID]

            row = pointsDistanceMatrix
            cleanedRow = row.iloc[:, 3:]
            cleanedRow = cleanedRow.drop(pointsIDList)
            cleanedRow[f'Sum_of_distances_to_{pointsIDList[0]}_and_{pointsIDList[-1]}'] = cleanedRow[f'Distance_to_point_{pointsIDList[0]}'] + cleanedRow[f'Distance_to_point_{pointsIDList[-1]}']

            pointID = cleanedRow[f'Sum_of_distances_to_{pointsIDList[0]}_and_{pointsIDList[-1]}'].idxmin()

            pointsIDList += [pointID]
            #print(pointsIDList)

            self.usedPointsIDList = pointsIDList
            

        return errorStatus, pointsIDList
        
    def findNextClosestPoints(self, pointsDistanceMatrix):

        cleanedRow = pointsDistanceMatrix.loc[self.usedPointsIDList, pointsDistanceMatrix.columns[3:]]

        for ID in self.usedPointsIDList:

            cleanedRow = cleanedRow.drop(columns = f"Distance_to_point_{ID}")

        if cleanedRow.empty:
            return None
        else:
            pointID = cleanedRow.min().idxmin()
            pointID = int(pointID.split('_')[-1])
            newPointID = [pointID]

            self.usedPointsIDList = self.usedPointsIDList + newPointID

            return newPointID
        
    def sortingPointsList(self, pointsDistanceMatrix, pointIDList, newPointID = None):

        cleanedRow = pointsDistanceMatrix.loc[pointIDList]
        pointID = cleanedRow[f'Distance_to_point_{newPointID[0]}'].idxmin()
        pointListIndex = pointIDList.index(pointID)
        ###
        
        self.newPointIDList = pointIDList.copy()
        self.newPointIDList.insert(pointListIndex, newPointID[0])
        sortedPointsIDList = self.newPointIDList 
        lines = [(sortedPointsIDList[i], sortedPointsIDList[(i + 1) % len(sortedPointsIDList)]) for i in range(len(sortedPointsIDList))]

        #
        for i, lineA in enumerate(lines):
            for j, lineB in enumerate(lines):
                # 
                if abs(i - j) > 1 and abs(i - j) < len(sortedPointsIDList) - 1:


                    # Przypisanie współrzędnych linii A i B do zmiennych (start i koniec)
                    pointAStartLatitude, pointAStartLongitude = pointsDistanceMatrix.loc[lineA[0], ['Latitude', 'Longitude']].values
                    pointAEndLatitude, pointAEndLongitude = pointsDistanceMatrix.loc[lineA[-1], ['Latitude', 'Longitude']].values
                    pointBStartLatitude, pointBStartLongitude = pointsDistanceMatrix.loc[lineB[0], ['Latitude', 'Longitude']].values
                    pointBEndLatitude, pointBEndLongitude = pointsDistanceMatrix.loc[lineB[-1], ['Latitude', 'Longitude']].values

                    # Przekształcenie współrzędnych geograficznych na współrzędne mapy
                    xpointAStart, ypointAStart = self.map(pointAStartLongitude, pointAStartLatitude)
                    xpointAEnd, ypointAEnd = self.map(pointAEndLongitude, pointAEndLatitude)
                    xpointBStart, ypointBStart = self.map(pointBStartLongitude, pointBStartLatitude)
                    xpointBEnd, ypointBEnd = self.map(pointBEndLongitude, pointBEndLatitude)

                    ###### tu musimy wyznaczyć na podstawie xy równanie lini y=ax+b dla obu lini
                    mLineA = (ypointAEnd - ypointAStart) / (xpointAEnd - xpointAStart) if (xpointAEnd - xpointAStart) != 0 else None
                    bLineA = ypointAStart - mLineA * xpointAStart if mLineA is not None else None

                    mLineB = (ypointBEnd - ypointBStart) / (xpointBEnd - xpointBStart) if (xpointBEnd - xpointBStart) != 0 else None
                    bLineB = ypointBStart - mLineB * xpointBStart if mLineB is not None else None

                    ###### nastepnie znaleść punkt przeciecia tych lini
                    xIntersect = (bLineB - bLineA) / (mLineA - mLineB)
                    yIntersect = mLineA * xIntersect + bLineA

                    ###### sprawdzić czy punkt przeciecia leży na naszych liniach 
                    if  (min(xpointAStart, xpointAEnd) < xIntersect < max(xpointAStart, xpointAEnd) and
                         min(ypointAStart, ypointAEnd) < yIntersect < max(ypointAStart, ypointAEnd) and
                         min(xpointBStart, xpointBEnd) < xIntersect < max(xpointBStart, xpointBEnd) and
                         min(ypointBStart, ypointBEnd) < yIntersect < max(ypointBStart, ypointBEnd)):

                        self.newPointIDList = pointIDList.copy()

                        # Wstawienie nowego punktu PO indeksie (dlatego dodajemy 1 do indeksu)
                        self.newPointIDList.insert(pointListIndex + 1, newPointID[0])
                        sortedPointsIDList = self.newPointIDList
                        return sortedPointsIDList
        
        return sortedPointsIDList


        




