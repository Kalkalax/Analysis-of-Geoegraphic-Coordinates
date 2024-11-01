import re # Library for operations on regular expressions
import pandas as pd # Library for data analysis and operations on data frames
import numpy as np # Library for efficient calculations on multidimensional arrays

# Class responsible for processing geographic point data.
class DataProcessor:
    def __init__(self):
        self.dataValidationErrorStatus = False
        self.usedPointsIDList = []
        self.fig, self.ax, self.map = None, None, None

    # Method responsible for verifying that the names of geographical points match the specified pattern
    def checkPointName(self, dataFrame):

        errorStatus = False
        errorList = []

        # Iterate through all the rows in the DataFrame and retrieve the value from the first column in that row
        for index in range(len(dataFrame)):

            value = dataFrame.iloc[index, 0]

            # Check that the name of the geographical point satisfies the required formula
            if not re.match("^[A-Z][a-z]*(\s[a-zA-Z][a-z]*)*$", str(value)):
                
                errorStatus = True
                self.dataValidationErrorStatus = errorStatus

                # Adding an error message to the error list
                errorList.append(f"# Point name '{value}' with index ID = {index} contains invalid characters")
    
        return errorStatus, errorList, dataFrame

    # The method responsible for verifying and converting geographical coordinates into a standard format.
    def checkAndConvertCoordinates(self, dataFrame, decimalplaces = 6):

        errorStatus = False
        errorList = []

        # Iterate through all the rows in the DataFrame and retrieve the value from the second column in that row
        for index in range(len(dataFrame)):

            value = dataFrame.iloc[index, 1]
            
            # Checking and converting coordinates in decimal format
            if (pattern := re.match(r"^(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)$", str(value))):
                
                latitude = round(float(pattern.group(1)), decimalplaces)
                longitude = round(float(pattern.group(2)), decimalplaces)

            # Checking and converting coordinates in degree format
            elif (pattern := re.match(r"^([NS])(\d{1,3}\.\d+)°,([EW])(\d{1,3}\.\d+)°$", str(value))):
                
                latitude = round(float(pattern.group(2)) * (-1 if pattern.group(1) == 'S' else 1), decimalplaces)
                longitude = round(float(pattern.group(4)) * (-1 if pattern.group(3) == 'W' else 1), decimalplaces)

            # Checking and converting coordinates in degrees and minutes format
            elif (pattern := re.match(r"^([NS])(\d{1,3})°(\d{1,3}\.\d+),([EW])(\d{1,3})°(\d{1,3}\.\d+)$", str(value))):
                
                latitude = round(int(pattern.group(2)) + float(pattern.group(3)) / 60 * (-1 if pattern.group(1) == 'S' else 1), decimalplaces)
                longitude = round(int(pattern.group(5)) + float(pattern.group(6)) / 60 * (-1 if pattern.group(4) == 'W' else 1), decimalplaces)

            # Checking and converting coordinates in degrees, minutes and seconds format
            elif (pattern := re.match(r"^([NS])(\d{1,3})°(\d{1,3})'(\d{1,3}\.\d+)\"\,([EW])(\d{1,3})°(\d{1,3})'(\d{1,3}\.\d+)\"$", str(value))):

                latitude = round(int(pattern.group(2)) + int(pattern.group(3)) / 60 + float(pattern.group(4)) / 3600 * (-1 if pattern.group(1) == 'S' else 1), decimalplaces)
                longitude = round(int(pattern.group(6)) + int(pattern.group(7)) / 60 + float(pattern.group(8)) / 3600 * (-1 if pattern.group(5) == 'W' else 1), decimalplaces)

            # In case of incorrect coordinate format
            else:
                errorStatus = True
                self.dataValidationErrorStatus = errorStatus

                # Adding an error message to the error list
                errorList.append(f"# The ordinates of point '{value}' with index ID = {index} have an inappropriate format")
            
            # Insert the converted coordinates into the DataFrame
            dataFrame.iloc[index, 1] = f"{latitude},{longitude}"

        return errorStatus, errorList, dataFrame
    
    # Method responsible for checking height values for correct format
    def checkAltitude(self, dataFrame):

        errorStatus = False
        errorList = []

        # Iterate through all the rows of the DataFrame and retrieve the value from the third column of the row in question
        for index in range(len(dataFrame)):
            value = dataFrame.iloc[index, 2]

            # Check that the height value meets the required formula
            if not re.match("^\d\.\d+$", str(value)):
                errorStatus = True
                self.dataValidationErrorStatus = errorStatus

                # Adding an error message to the error list
                errorList.append(f"# Height of point '{value}' with index ID = {index} contains invalid format")
        
        return errorStatus, errorList, dataFrame
    
    # Method responsible for checking timestamp values for correct format
    def checkDataAndTime(self, dataFrame):
    
        errorStatus = False  
        errorList = []  

        # Iterate through all the rows of the DataFrame and retrieve the value from the fourth column of the row in question
        for index in range(len(dataFrame)):
            value = dataFrame.iloc[index, 3]

            # Check that the timestamp value meets the required formula
            if not re.match(r"^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}$", str(value)):
                errorStatus = True  
                self.dataValidationErrorStatus = errorStatus  

                # Adding an error message to the error list
                errorList.append(f"# The timestamp of point '{value}' with index ID = {index} contains an invalid format")

        return errorStatus, errorList, dataFrame

    # Method responsible for checking the metadata of points in the DataFrame for correctness
    def checkMetadata(self, dataFrame):
        
        errorStatus = False  
        errorList = []  #

        # Here you can add logic to verify the metadata in the DataFrame 
        # For example: checking that the metadata is not empty, has the right format, etc.

        return errorStatus, errorList, dataFrame 

    # Method responsible for returning data validation error status
    def getDataValidationErrorStatus(self):

        return self.dataValidationErrorStatus
    
    # Method responsible for creating a distance matrix between points based on coordinates
    def createPointsDistanceMatrix(self, dataFrame):
        
        inputDataFrameSize = 0 
        outputDataFrameSize = 0  
        mergedRows = 0  

        # Separating the 'coordinates' column into latitude and longitude coordinates
        pointsDistanceMatrix = dataFrame['coordinates'].str.split(',', expand=True)

        inputDataFrameSize = len(pointsDistanceMatrix)  

        # Naming columns and converting values to float
        pointsDistanceMatrix.columns = ['Latitude', 'Longitude']  
        pointsDistanceMatrix[['Latitude', 'Longitude']] = pointsDistanceMatrix[['Latitude', 'Longitude']].astype(float) 

        # Calculating the distance from a point (0,0)
        pointsDistanceMatrix['Distance_from_origin'] = np.sqrt(pointsDistanceMatrix['Latitude']**2 + pointsDistanceMatrix['Longitude']**2)

        # Creating a distance matrix
        distance_matrix = pd.DataFrame(index=pointsDistanceMatrix.index, columns=pointsDistanceMatrix.index)

        # Calculating the distance between points
        for i, start_point in pointsDistanceMatrix.iterrows():
            for j, end_point in pointsDistanceMatrix.iterrows():
                if i != j:
                    distance = np.sqrt((end_point['Latitude'] - start_point['Latitude']) ** 2 + 
                                    (end_point['Longitude'] - start_point['Longitude']) ** 2)
                    distance_matrix.iloc[i, j] = distance  
                else:
                    # Setting NaN value for distance to self
                    distance_matrix.iloc[i, j] = np.nan  

        # Naming the columns of the distance matrix
        distance_matrix.columns = [f'Distance_to_point_{i}' for i in range(len(pointsDistanceMatrix))]
        distance_matrix.index = pointsDistanceMatrix.index

        # Combining the distance matrix with the coordinate DataFrame
        pointsDistanceMatrix = pd.concat([pointsDistanceMatrix, distance_matrix], axis=1)

        # Deleting duplicate coordinates
        duplicateLocations = pointsDistanceMatrix[pointsDistanceMatrix.duplicated(subset=['Latitude', 'Longitude'], keep='first')]
        duplicateLocationsID = duplicateLocations.index.tolist()

        # Removal of duplicate points and their distances
        for ID in duplicateLocationsID:
            pointsDistanceMatrix = pointsDistanceMatrix.drop(ID)  
            pointsDistanceMatrix = pointsDistanceMatrix.drop(columns=f"Distance_to_point_{ID}") 

        # Calculation of the number of merged rows
        outputDataFrameSize = len(pointsDistanceMatrix) 
        mergedRows = inputDataFrameSize - outputDataFrameSize  

        return pointsDistanceMatrix, mergedRows  

    # Method responsible for finding the nearest points forming a triangle based on the distance matrix
    def findClosestTrianglePoints(self, pointsDistanceMatrix):

        errorStatus = False 
        pointsIDList = []  

        # Checking whether there are enough points in the matrix
        if len(pointsDistanceMatrix) < 3:
            errorStatus = True 
        else:
            # Finding the closest point to the starting point
            pointID = pointsDistanceMatrix.nsmallest(1, "Distance_from_origin").index[0]
            pointsIDList = [pointID] 

            # Extracting a row from the distance matrix for the nearest point
            row = pointsDistanceMatrix.loc[[pointID]]
        
            # Row clean-up to remove NaN columns and leave only distance columns
            cleanedRow = row.iloc[:, 3:] 
            cleanedRow = cleanedRow.dropna(axis=1, how='any') 
        
            # Finding the point with the smallest distance in the cleaned row and adding it to the list
            pointID = cleanedRow.idxmin(axis=1)  
            pointID = pointID.iloc[0] 
            pointID = int(pointID.split('_')[-1]) 
            pointsIDList = pointsIDList + [pointID] 

            # Extracting the entire distance matrix
            row = pointsDistanceMatrix
            cleanedRow = row.iloc[:, 3:] 
            cleanedRow = cleanedRow.drop(pointsIDList)  

            # Calculating the sum of distances to two points in a list
            cleanedRow[f'Sum_of_distances_to_{pointsIDList[0]}_and_{pointsIDList[-1]}'] = cleanedRow[f'Distance_to_point_{pointsIDList[0]}'] + cleanedRow[f'Distance_to_point_{pointsIDList[-1]}']
            
            # Finding the point with the smallest sum of distances and adding it to the list
            pointID = cleanedRow[f'Sum_of_distances_to_{pointsIDList[0]}_and_{pointsIDList[-1]}'].idxmin()
            pointsIDList += [pointID]

            self.usedPointsIDList = pointsIDList  
            
        return errorStatus, pointsIDList

    # Method responsible for finding the nearest point from among the remaining points not yet included in the list of used points
    def findNextClosestPoints(self, pointsDistanceMatrix):
        
        # Create a cleaned row of distance matrix based on the points used
        cleanedRow = pointsDistanceMatrix.loc[self.usedPointsIDList, pointsDistanceMatrix.columns[3:]]

        # Delete distance columns to points that have already been used
        for ID in self.usedPointsIDList:
            cleanedRow = cleanedRow.drop(columns=f"Distance_to_point_{ID}")

        # Checking if the cleared matrix is empty
        if cleanedRow.empty:
            return None 
        else:
            # Finding the point with the shortest distance among the other points and creating a list with the new point
            pointID = cleanedRow.min().idxmin()
            pointID = int(pointID.split('_')[-1]) 
            newPointID = [pointID]

            # Updating the list of points in use
            self.usedPointsIDList = self.usedPointsIDList + newPointID

            return newPointID 

    # Method responsible for sorting the list of points based on the distance to the new point and detecting line intersections between points.   
    def sortingPointsList(self, pointsDistanceMatrix, pointIDList, newPointID=None):
        

        # Create cleaned row of distance matrix based on given point IDs
        cleanedRow = pointsDistanceMatrix.loc[pointIDList]

        # Finding the ID of the point with the shortest distance to the new point
        pointID = cleanedRow[f'Distance_to_point_{newPointID[0]}'].idxmin()
        pointListIndex = pointIDList.index(pointID)  
        
        # Create a new list of points with a new point added
        self.newPointIDList = pointIDList.copy()
        self.newPointIDList.insert(pointListIndex, newPointID[0])  
        sortedPointsIDList = self.newPointIDList  
        lines = [(sortedPointsIDList[i], sortedPointsIDList[(i + 1) % len(sortedPointsIDList)]) for i in range(len(sortedPointsIDList))]

        # Iterate through all pairs of lines to see if they intersect
        for i, lineA in enumerate(lines):
            for j, lineB in enumerate(lines):
                # Check that lines A and B are different and not adjacent to each other
                if abs(i - j) > 1 and abs(i - j) < len(sortedPointsIDList) - 1:
                    # Assignment of coordinates of lines A and B to variables (start and end)
                    pointAStartLatitude, pointAStartLongitude = pointsDistanceMatrix.loc[lineA[0], ['Latitude', 'Longitude']].values
                    pointAEndLatitude, pointAEndLongitude = pointsDistanceMatrix.loc[lineA[-1], ['Latitude', 'Longitude']].values
                    pointBStartLatitude, pointBStartLongitude = pointsDistanceMatrix.loc[lineB[0], ['Latitude', 'Longitude']].values
                    pointBEndLatitude, pointBEndLongitude = pointsDistanceMatrix.loc[lineB[-1], ['Latitude', 'Longitude']].values

                    # Transforming geographical coordinates into map coordinates
                    xpointAStart, ypointAStart = self.map(pointAStartLongitude, pointAStartLatitude)
                    xpointAEnd, ypointAEnd = self.map(pointAEndLongitude, pointAEndLatitude)
                    xpointBStart, ypointBStart = self.map(pointBStartLongitude, pointBStartLatitude)
                    xpointBEnd, ypointBEnd = self.map(pointBEndLongitude, pointBEndLatitude)

                    # Determining the equation of the line y=ax+b for both lines
                    mLineA = (ypointAEnd - ypointAStart) / (xpointAEnd - xpointAStart) if (xpointAEnd - xpointAStart) != 0 else None
                    bLineA = ypointAStart - mLineA * xpointAStart if mLineA is not None else None
                    mLineB = (ypointBEnd - ypointBStart) / (xpointBEnd - xpointBStart) if (xpointBEnd - xpointBStart) != 0 else None
                    bLineB = ypointBStart - mLineB * xpointBStart if mLineB is not None else None

                    # Finding the intersection of these lines
                    if mLineA is not None and mLineB is not None:  
                        xIntersect = (bLineB - bLineA) / (mLineA - mLineB)
                        yIntersect = mLineA * xIntersect + bLineA

                        # Checking that the intersection point lies on our lines
                        if (min(xpointAStart, xpointAEnd) < xIntersect < max(xpointAStart, xpointAEnd) and
                            min(ypointAStart, ypointAEnd) < yIntersect < max(ypointAStart, ypointAEnd) and
                            min(xpointBStart, xpointBEnd) < xIntersect < max(xpointBStart, xpointBEnd) and
                            min(ypointBStart, ypointBEnd) < yIntersect < max(ypointBStart, ypointBEnd)):
                            
                            # Inserting a new point AFTER the index (therefore adding 1 to the index)
                            self.newPointIDList = pointIDList.copy()
                            self.newPointIDList.insert(pointListIndex + 1, newPointID[0])
                            sortedPointsIDList = self.newPointIDList

                            return sortedPointsIDList 
            
        return sortedPointsIDList 
