from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

class MapCreator:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame
        self.map = Basemap
        
        self.points = None
        

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
        
        

    def addPoint(self, dataFrame, color):
        # Pobieranie kolumny 'coordinates' z DataFrame
        self.points = dataFrame
        
        # Iteracja przez wiersze w Series
        for coord in self.points:
            # Parsowanie współrzędnych z kolumny
            lat_long = coord.split(',')  # Rozdzielenie współrzędnych po przecinku
            latitude = float(lat_long[0].strip())  # Szerokość geograficzna
            longitude = float(lat_long[1].strip())  # Długość geograficzna

            # Konwersja współrzędnych geograficznych na współrzędne mapy
            xpoint, ypoint = self.map(longitude, latitude)

            # Dodanie punktu na mapę (czerwony punkt 'r.')
            self.map.plot(xpoint, ypoint, color)

    # Odświeżenie wykresu
        plt.pause(0.5)
        plt.draw()


    def addLine(self):

        pass


    def getData(self):

        return self.points


