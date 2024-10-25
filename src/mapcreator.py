from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

class MapCreator:
    def __init__(self, pointsDistanceMatrix):
        self.pointsDistanceMatrix = pointsDistanceMatrix
        self.map = Basemap
        #self.i = 1


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
        #self.map.drawmapboundary(fill_color='None', color='None')
        self.map.drawmapboundary(fill_color='white', color='white')  # Ustaw kolor morza na biało

        # Ustawienie koloru tła osi (tło całej mapy)
        self.ax.set_facecolor('white')  # Tło osi na biało
        
        
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
        #plt.savefig("mapa_wykres1.png", format='png', bbox_inches='tight')


    def markAllPoints(self):

        
        for idx, (latitude, longitude) in zip(self.pointsDistanceMatrix.index, zip(self.pointsDistanceMatrix['Latitude'], self.pointsDistanceMatrix['Longitude'])):
            xpoint, ypoint = self.map(longitude, latitude)
            self.map.plot(xpoint, ypoint, "r.")
            #plt.annotate(str(idx), (xpoint, ypoint), textcoords="offset points", xytext=(5,5), ha='center', color="blue", fontsize=9)

    def changePointColor(self, pointsIDList):

        for point in pointsIDList:

            row = self.pointsDistanceMatrix.loc[[point]]

            latitude = row['Latitude'].values[0]
            longitude = row['Longitude'].values[0]

            xpoint, ypoint = self.map(longitude, latitude)
            self.map.plot(xpoint, ypoint, "b.")

    def drawLineConnectingPoints(self, sortedPointsIDList):
    # Sprawdzenie, czy istnieją narysowane linie i ich usunięcie
        if hasattr(self, 'plotted_lines'):
            for line in self.plotted_lines:
                line.remove()
            self.plotted_lines.clear()  # Opróżnij listę po usunięciu linii
        else:
            self.plotted_lines = []  # Utworzenie listy, jeśli nie istnieje

        # Dodaj punkt końcowy, aby zamknąć pętlę
        self.sortedPointsIDList = sortedPointsIDList + [sortedPointsIDList[0]]

        for i in range((len(self.sortedPointsIDList)-1)):

            pointAID = self.sortedPointsIDList[i]
            pointBID = self.sortedPointsIDList[i+1]

            pointALatitude = self.pointsDistanceMatrix.loc[pointAID]['Latitude']
            pointALongitude = self.pointsDistanceMatrix.loc[pointAID]['Longitude']

            pointBLatitude = self.pointsDistanceMatrix.loc[pointBID]['Latitude']
            pointBLongitude = self.pointsDistanceMatrix.loc[pointBID]['Longitude']

            xPointA, yPointA = self.map(pointALongitude, pointALatitude)
            xPointB, yPointB = self.map(pointBLongitude, pointBLatitude)
            
            # Rysowanie linii i zapisywanie obiektów linii do listy
            line, = self.map.plot([xPointA, xPointB], [yPointA, yPointB], linewidth=1, color='b')
            self.plotted_lines.append(line)  # Dodaj obiekt linii do listy


    def updatChart(self):

        plt.pause(0.2)
        plt.draw()
        #plt.savefig(f"mapa_wykres{self.i}.png", format='png', bbox_inches='tight')
        #self.i += 1 
        