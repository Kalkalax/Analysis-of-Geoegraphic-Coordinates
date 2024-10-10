from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

class MapCreator:
    def __init__(self, pointsDistanceMatrix):
        self.pointsDistanceMatrix = pointsDistanceMatrix
        self.map = Basemap


    def createMap(self):

        plt.ion()

        # Tworzenie figury i osi
        self.fig, self.ax = plt.subplots(figsize=(8.00, 8.00), frameon=False)

        # Tworzenie mapy i zapisanie jej jako atrybut klasy
        self.map = Basemap(projection='merc', llcrnrlat=-85, urcrnrlat=85,
                           llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c', ax=self.ax)

        # Rysowanie linii brzegowej i wypełnianie kontynentów
        self.map.drawcoastlines(color='#74C558')
        self.map.fillcontinents(color='#74C558', lake_color='white')
        self.map.drawmapboundary(fill_color='None', color='None')
        
        # Równoleżniki i południki
        self.map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
        self.map.drawmeridians(np.arange(self.map.lonmin, self.map.lonmax + 30, 60), labels=[0, 0, 0, 1])

        # Ustawienie koloru i szerokości linii dla wszystkich ramek (spines)
        for spine in self.ax.spines.values():
            spine.update({'edgecolor': 'black', 'linewidth': 0.3})

        
        # Dostosowanie marginesów
        plt.subplots_adjust(left=0.07, right=0.93, top=0.93, bottom=0.07)
        
        # Wyświetlenie mapy
        plt.show()


    def markAllPoints(self):

        for latitude, longitude  in zip(self.pointsDistanceMatrix['Latitude'], self.pointsDistanceMatrix['Longitude']):    
            
            xpoint, ypoint = self.map(longitude, latitude)
            self.map.plot(xpoint, ypoint, "r.")
        
        #plt.pause(0.5)
        #plt.draw()

    def changePointColor(self, pointsIDList):

        #plt.pause(0.5)

        for point in pointsIDList:

            #print(point)
            row = self.pointsDistanceMatrix.loc[[point]]
           # print(row)
            latitude = row['Latitude'].values[0]
            longitude = row['Longitude'].values[0]
            #print(latitude.values, longitude.values)
            xpoint, ypoint = self.map(longitude, latitude)
            self.map.plot(xpoint, ypoint, "b.")

        #plt.draw()

    def updatChart(self):

        plt.pause(0.5)
        plt.draw()
        