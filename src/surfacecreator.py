import numpy as np
import pandas as pd



class SurfaceCreator:
    def __init__(self):
        self.usedPointsID = None
        self.usedPointsIDDataFrame = None

    def searchStartingPoints(self, dataFrame):

        unusedPoints = dataFrame.iloc[:].str.split(',', expand=True)
        unusedPoints.columns = ['Latitude', 'Longitude']  # Nadawanie nazw kolumn
        unusedPoints[['Latitude', 'Longitude']] = unusedPoints[['Latitude', 'Longitude']].astype(float)

        unusedPoints['Distance_from_origin'] = np.sqrt(unusedPoints['Latitude']**2 + unusedPoints['Longitude']**2)
        print(unusedPoints)
        
        self.usedPointsID = unusedPoints['Distance_from_origin'].nsmallest(3).index.tolist()
        print(self.usedPointsID)


        self.usedPointsIDDataFrame = unusedPoints.loc[self.usedPointsID] ##
        print(self.usedPointsIDDataFrame)

        self.unusedPoints = unusedPoints.drop(self.usedPointsID)
        print(unusedPoints)

        self.usedPointsDataFrame = dataFrame.loc[self.usedPointsID]

        return self.usedPointsDataFrame
    



    def searchNextPoints(self, dataFrame):


        
        distances = []
        for _, start_point in self.usedPointsIDDataFrame.iterrows():
             
            # Obliczanie odległości euklidesowej między punktami startowymi a wszystkimi innymi punktami
            dist = np.sqrt((self.unusedPoints['Latitude'] - start_point['Latitude'])**2 + 
                            (self.unusedPoints['Longitude'] - start_point['Longitude'])**2)
            distances.append(dist)

        print(distances)

        distance_df = pd.DataFrame(distances).T
        distance_df.columns = [f"Distance_to_start_{i}" for i in range(1, len(start_point) + 1)]
        
        distance_df['Min_Distance'] = distance_df.min(axis=1)
        nearest_point_index = distance_df['Min_Distance'].idxmin()

        self.usedPointsID += distance_df['Min_Distance'].nsmallest(1).index.tolist()
        print(self.usedPointsID)
        
        nearest_point = self.unusedPoints.loc[nearest_point_index]
        print(distance_df)
        print(nearest_point)   

        self.unusedPoints = self.unusedPoints.drop(nearest_point_index)
        print(self.unusedPoints)

        self.usedPointsDataFrame = dataFrame.loc[self.usedPointsID]

        return self.usedPointsDataFrame



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