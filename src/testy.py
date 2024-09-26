import numpy as np
import matplotlib.pyplot as plt
from alphashape import alphashape
from shapely.geometry import Point, Polygon

# Generowanie losowych punktów
np.random.seed(0)
points = np.random.rand(30, 2)  # 30 punktów 2D

# Funkcja do rysowania dynamicznej otoczki
def dynamic_concave_hull(points, start_alpha=160, min_alpha=5, alpha_step=1):
    hull_points = []  # Lista punktów, które tworzą otoczkę

    # Iteracja po punktach
    for point in points:
        hull_points.append(point)  # Dodanie nowego punktu do listy
        
        # Ustalanie wartości alpha na podstawie liczby punktów
        current_alpha = start_alpha
        
        # Zmniejszanie alpha do momentu znalezienia sensownej otoczki
        while current_alpha >= min_alpha:
            concave_hull = alphashape(hull_points, current_alpha)
            # Sprawdzanie czy jest to wielokąt
            if isinstance(concave_hull, Polygon):
                # Wykrycie nowego punktu
                if all(Point(p).within(concave_hull) for p in hull_points):
                    break
            current_alpha -= alpha_step  # Zmniejszenie alpha, aby spróbować dopasować punkt

        # Rysowanie obecnej otoczki
        plt.clf()  # Czyść poprzednie rysunki
        plt.plot(points[:, 0], points[:, 1], 'o', color='blue', label='Punkty')  # Rysowanie wszystkich punktów
        hull_x, hull_y = np.array(hull_points).T  # Ekstrakcja współrzędnych punktów otoczki
        plt.plot(hull_x, hull_y, 'r.', label='Dodane punkty')  # Dodane punkty
        
        if isinstance(concave_hull, Polygon):
            x, y = concave_hull.exterior.xy
            plt.plot(x, y, 'g-', label=f'Concave Hull (α={current_alpha:.2f})')  # Rysowanie otoczki
        plt.title('Dynamiczna Wypukła Otoczka (Dynamic Alpha)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid()
        plt.legend()
        plt.pause(0.5)  # Pauza, aby obserwować proces dodawania punktów

    plt.show()

# Uruchomienie dynamicznej otoczki
dynamic_concave_hull(points)
