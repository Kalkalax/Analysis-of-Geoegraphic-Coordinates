from mpl_toolkits.basemap import Basemap # Map-making library
import numpy as np # Library for efficient calculations on multidimensional arrays
import matplotlib.pyplot as plt # Library for creating graphs

class MapCreator:
    def __init__(self, pointsDistanceMatrix):
        self.pointsDistanceMatrix = pointsDistanceMatrix  
        self.map = Basemap

    #Method responsible for creating and displaying the map
    def createMap(self):

        # Activate interactive mode for drawing graphs
        plt.ion()

        # Create a figure and axes for the map
        self.fig, self.ax = plt.subplots(figsize=(8.00, 8.00), frameon=False)

        # Create a map and save it as a class attribute
        self.map = Basemap(projection='merc', llcrnrlat=-85, urcrnrlat=85,
                           llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c', ax=self.ax)

        # Drawing the coastline
        self.map.drawcoastlines(color='#74C558') 
        self.map.fillcontinents(color='#74C558', lake_color='white') 

        # Setting the sea colour to white
        self.map.drawmapboundary(fill_color='white', color='white')  

        # Setting the background colour of the axis (background of the whole map)
        self.ax.set_facecolor('white') 

        # Drawing the parallels and meridians
        self.map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0]) 
        self.map.drawmeridians(np.arange(self.map.lonmin, self.map.lonmax + 30, 60), labels=[0, 0, 0, 1])  

        # Setting the colour and line width for all frames (spines)
        for spine in self.ax.spines.values():
            spine.update({'edgecolor': 'black', 'linewidth': 0.3})  

        # Adjustment of chart margins
        plt.subplots_adjust(left=0.07, right=0.93, top=0.93, bottom=0.07)

        # Displaying the map
        plt.show()

    # Method responsible for marking points on a map based on their geographical coordinates.
    def markAllPoints(self):
    
        # Iterating through all the points in the point distance matrix
        for idx, (latitude, longitude) in zip(self.pointsDistanceMatrix.index, 
                                          zip(self.pointsDistanceMatrix['Latitude'], 
                                              self.pointsDistanceMatrix['Longitude'])):
            
            # Converting geographical coordinates (longitude and latitude) into map coordinates
            xpoint, ypoint = self.map(longitude, latitude)

            # Drawing a point on the map as a red dot
            self.map.plot(xpoint, ypoint, "r.")

            # Optional: add an annotation with the index of the point next to the dot on the map
            # plt.annotate(str(idx), (xpoint, ypoint), textcoords="offset points", xytext=(5,5),ha='center', color="blue", fontsize=9)

    # Method responsible for changing the colour of points on the map based on a list of point identifiers.
    def changePointColor(self, pointsIDList):
    
    # Iteration through all point identifiers in the passed list
        for point in pointsIDList:
            # Retrieve a row from the point distance matrix based on the point identifier
            row = self.pointsDistanceMatrix.loc[[point]]

            # Extract geographical coordinates (latitude and longitude) from the line
            latitude = row['Latitude'].values[0]
            longitude = row['Longitude'].values[0]

            # Converting geographical coordinates (longitude and latitude) into map coordinates
            xpoint, ypoint = self.map(longitude, latitude)

            # Drawing a point on the map as a blue dot
            self.map.plot(xpoint, ypoint, "b.")

    # Method responsible for drawing lines connecting points on the map based on a sorted list of point identifiers.
    def drawLineConnectingPoints(self, sortedPointsIDList):
    
        # Check if there are already drawn lines and delete them
        if hasattr(self, 'plotted_lines'):
            for line in self.plotted_lines:
                line.remove()  
            self.plotted_lines.clear()  
        else:
            self.plotted_lines = []  

        # Add an end point to close the loop
        self.sortedPointsIDList = sortedPointsIDList + [sortedPointsIDList[0]]

        # Iterate through a sorted list of points to draw lines between consecutive points
        for i in range((len(self.sortedPointsIDList) - 1)):
            pointAID = self.sortedPointsIDList[i]  
            pointBID = self.sortedPointsIDList[i + 1]  

            # Get the geographical coordinates of point A
            pointALatitude = self.pointsDistanceMatrix.loc[pointAID]['Latitude']
            pointALongitude = self.pointsDistanceMatrix.loc[pointAID]['Longitude']

            # Get the geographical coordinates of point B
            pointBLatitude = self.pointsDistanceMatrix.loc[pointBID]['Latitude']
            pointBLongitude = self.pointsDistanceMatrix.loc[pointBID]['Longitude']

            # Conversion of geographical coordinates of points A and B to map coordinates
            xPointA, yPointA = self.map(pointALongitude, pointALatitude)
            xPointB, yPointB = self.map(pointBLongitude, pointBLatitude)
            
            # Drawing a line between points A and B and saving the line objects in a list
            line, = self.map.plot([xPointA, xPointB], [yPointA, yPointB], linewidth=1, color='b')
            self.plotted_lines.append(line) 


    # The method responsible for updating the graph (map) as the programme runs.
    def updatChart(self):

        plt.pause(0.2)  
        plt.draw()  

        