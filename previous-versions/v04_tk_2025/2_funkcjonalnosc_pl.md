# Analiza programu tk3d_v04.py

Program tk3d_v04.py to przeglądarka obrazów 3D z interfejsem graficznym opartym na bibliotece Tkinter. Oto jego główne funkcjonalności:

1. **Wczytywanie obrazów 3D**:
   - Obsługa formatów NIFTI (.nii, .nii.gz), NumPy (.npy) i MATLAB (.mat)
   - Możliwość wczytania obrazu z linii poleceń lub przez interfejs graficzny

2. **Wyświetlanie przekrojów obrazu**:
   - Wizualizacja pojedynczych przekrojów 2D z obrazu 3D
   - Nawigacja między przekrojami za pomocą suwaka
   - Możliwość przewijania przekrojów za pomocą kółka myszy

3. **Projekcje intensywności**:
   - MIP (Maximum Intensity Projection) - projekcja maksymalnej intensywności
   - mIP (Minimum Intensity Projection) - projekcja minimalnej intensywności
   - Regulacja zakresu projekcji (liczby przekrojów)

4. **Operacje progowania**:
   - Progowanie pojedyncze (Single Threshold) - wartości powyżej progu są ustawiane na maksimum, poniżej na minimum
   - Progowanie podwójne (Double Threshold) - wartości poza zakresem są ustawiane na wartości graniczne

5. **Manipulacja obrazem**:
   - Inwersja obrazu (odwrócenie wartości pikseli)
   - Przywracanie oryginalnego obrazu (Reload)

6. **Informacje o obrazie**:
   - Wyświetlanie podstawowych informacji o obrazie (min, max, średnia, typ danych)
   - Wyświetlanie nagłówka pliku NIFTI (jeśli dostępny)

7. **Zapisywanie obrazów**:
   - Możliwość zapisania przetworzonego obrazu w formatach NIFTI, NumPy lub MATLAB
   - Zachowanie metadanych z oryginalnego pliku NIFTI

8. **Interfejs użytkownika**:
   - Pasek narzędzi Matplotlib do manipulacji widokiem (przybliżanie, oddalanie, przesuwanie)
   - Podział interfejsu na obszar wyświetlania obrazu i panel kontrolny
   - Panel kontrolny podzielony na sekcje: progowanie, nawigacja przekrojów i akcje

9. **Dostosowanie do wysokiej rozdzielczości**:
   - Obsługa ekranów o wysokiej rozdzielczości (HiDPI)
   - Zwiększone rozmiary czcionek i elementów interfejsu

10. **Struktura modułowa**:
    - Podział kodu na moduły odpowiedzialne za różne funkcjonalności
    - Klasa MPL do obsługi obrazu i wizualizacji
    - Oddzielne klasy dla poszczególnych elementów interfejsu

Program jest przeznaczony do analizy obrazów przegrody nosowo-szczękowej, ale może być używany do przeglądania dowolnych obrazów 3D w obsługiwanych formatach.
