import numpy as np
import matplotlib.pyplot as plt

# Generowanie losowych punktów
np.random.seed(0)
points = np.random.rand(30, 2)  # 30 punktów 2D
available_points = points

# Ustalony środek wykresu (np. (0.5, 0.5))
center = np.array([0.5, 0.5])

# Rysowanie środka wykresu
plt.plot(center[0], center[1], 'kx', markersize=10, label='Środek')  # Środek wykresu

# Obliczanie odległości od ustalonego środka
distances = np.linalg.norm(points - center, axis=1)

# Znajdowanie indeksów trzech najbliższych punktów do ustalonego środka
closest_indices = np.argsort(distances)[:3]

# Dodać trzy punkty do listy użytych punktów

used_points = []  # Inicjalizacja pustej listy na użyte punkty
for idx in closest_indices:
    used_points.append(points[idx])  # Dodanie najbliższego punktu do listy


available_points = np.delete(points, closest_indices, axis=0)

# Wydrukuj informacje o punktach
print("Trzy podstawowe punkty:", points)
print("Wszystkie punkty:", len(available_points))  # + len(used_points) aby uzyskać oryginalną liczbę punktów
print("Użyte punkty:", len(used_points))


# Rysowanie wszystkich punktów jako niebieskich
plt.plot(points[:, 0], points[:, 1], 'o', color='blue', label='Punkty')

# Rysowanie najbliższych punktów jako czerwonych
for idx in closest_indices:
    plt.plot(points[idx, 0], points[idx, 1], '.', color='red', markersize=7, label='Dodane punkty' if idx == closest_indices[0] else "")  # Tylko pierwszy punkt otrzymuje etykietę



while len(available_points) > 0: 

    plt.clf()
    plt.plot(points[:, 0], points[:, 1], 'o', color='blue', label='Punkty')

    min_distance = float('inf')
    closest_point = None

    for point in available_points:  # Iteracja przez pozostałe punkty
        for used_point in used_points:  # Iteracja przez użyte punkty
            distance = np.linalg.norm(point - used_point)  # Obliczanie odległości
            if distance < min_distance:  # Sprawdzenie, czy nowa odległość jest mniejsza
                min_distance = distance
                closest_point = point
                print(closest_point)

    #Rysowanie najbliższego punktu w zielonym kolorze
    if closest_point is not None:
        plt.plot(closest_point[0], closest_point[1], 'go', markersize=8, label='Najbliższy punkt')  # Kolorowanie najbliższego punktu

        
        # Usuwanie najbliższego punktu z listy dostępnych punktów
        closest_point_index = np.where((available_points == closest_point).all(axis=1))[0][0]  # Znajdowanie indeksu
        used_points.append(points[closest_point_index])
        available_points = np.delete(available_points, closest_point_index, axis=0)

        # Wydrukuj ilości punktów
        print("Wszystkie punkty:", len(available_points))  # Ilość pozostałych punktów
        print("Użyte punkty:", len(used_points))  # Ilość użytych punktów

    # Wydrukuj najbliższy punkt
    print("Najbliższy punkt do użytych punktów:", closest_point)


    # Rysowanie pozostałych dostępnych punktów w niebieskim kolorze
    for available_point in used_points:
        plt.plot(available_point[0], available_point[1], 'r.', markersize=7, label='Dostępne punkty' if available_point is used_points[0] else "")



    
    # Ustawienia wykresu
    plt.title('Punkty z Kolorowaniem')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid()
    #plt.legend()
    plt.pause(1) 




