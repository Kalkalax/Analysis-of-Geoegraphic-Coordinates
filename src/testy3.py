import numpy as np
import pandas as pd



class SurfaceCreator:
    def __init__(self):
        self.usedPointsID = None

    def startingPoints(self, dataFrame):

        points = dataFrame.iloc[:].str.split(',', expand=True)
        points.columns = ['Latitude', 'Longitude']  # Nadawanie nazw kolumn
        points[['Latitude', 'Longitude']] = points[['Latitude', 'Longitude']].astype(float)

        points['Distance_from_origin'] = np.sqrt(points['Latitude']**2 + points['Longitude']**2)
        print(points)
        
        self.usedPointsID = points['Distance_from_origin'].nsmallest(3).index.tolist()
        
        return self.usedPointsID

# if __name__ == "__main__":



#     # Ustalenie ziarna losowego dla reprodukowalności
#     np.random.seed(0)

#     # Generowanie losowych punktów w zakresie (min, max) dla szerokości i długości geograficznej
#     latitudes = np.random.uniform(-90, 90, 20)  # 20 punktów szerokości geograficznej
#     longitudes = np.random.uniform(-180, 180, 20)  # 20 punktów długości geograficznej

#     # Tworzenie DataFrame z punktów w formacie (latitude, longitude)
#     df = pd.DataFrame({'Latitude': latitudes, 'Longitude': longitudes})

#     # Formatowanie jako ciąg znaków bez spacji
#     df['coordinates'] = df.apply(lambda row: f"{row['Latitude']},{row['Longitude']}", axis=1)

#     # Wyświetlanie wyników w pożądanym formacie
#     for idx, point in enumerate(df['coordinates']):
#         print(f"{idx}      {point}")

#     points = df['coordinates']
#     print(points)
#     ######################################################################################################

#     sc = SurfaceCreator()
#     startPointsID = sc.startingPoints(points)
#     print(startPointsID)