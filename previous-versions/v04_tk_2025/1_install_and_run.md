# Analiza kodu i przygotowanie środowiska uruchomieniowego

Po przeanalizowaniu kodu, zauważyłem kilka elementów, które wymagają uwagi przy tworzeniu środowiska conda. Program został napisany w 2017 roku, więc niektóre biblioteki i funkcje są przestarzałe.

## Główne problemy do rozwiązania:

1. Kod używa `matplotlib.backends.backend_tkagg.NavigationToolbar2TkAgg`, która została zastąpiona przez `NavigationToolbar2Tk` w nowszych wersjach Matplotlib
2. Funkcja `canvas.show()` została zastąpiona przez `canvas.draw()`
3. Niektóre importy i funkcje z bibliotek nibabel, scipy mogą wymagać dostosowania

## Proponowane środowisko conda:

Zalecam użycie Pythona 3.6, który był popularny w 2017 roku, wraz z odpowiednimi wersjami bibliotek:

```yaml:environment.yml
name: tk3d_viewer
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.6
  - numpy=1.13
  - matplotlib=2.1
  - nibabel=2.2
  - scipy=1.0
  - scikit-learn=0.19
  - tk=8.6
  - pip
  - pip:
    - tk3d
```

## Potrzebne modyfikacje w kodzie:

Główny plik `tk3d_v04.py` wymaga aktualizacji:

```python:tk3d_v04.py
# ... existing code ...
# Zmiana importu NavigationToolbar2TkAgg na NavigationToolbar2Tk
import matplotlib.backends.backend_tkagg as bcktagg
import matplotlib.backend_bases as bckbases
# ... existing code ...

# Zmiana canvas.show() na canvas.draw()
canvas = bcktagg.FigureCanvasTkAgg(mpl.fig, master=root)
canvas.draw()  # zamiast canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Zmiana klasy NavigationToolbar2TkAgg na NavigationToolbar2Tk
toolbar = bcktagg.NavigationToolbar2Tk(canvas, root)  # zamiast NavigationToolbar2TkAgg
# ... existing code ...
```

## Instrukcja instalacji i uruchomienia:

1. Utwórz środowisko conda używając pliku environment.yml:
   ```
   conda env create -f environment.yml
   ```

2. Aktywuj środowisko:
   ```
   conda activate tk3d_viewer
   ```

3. Uruchom program:
   ```
   python tk3d_v04.py
   ```

## Uwagi dodatkowe:

1. Program używa modułu `mk_add_path_dropbox`, który prawdopodobnie jest lokalnym modułem autora. Może być konieczne utworzenie tego modułu lub dostosowanie ścieżek.

2. W kodzie występują odwołania do specyficznych ścieżek, które mogą wymagać dostosowania do lokalnego systemu.

3. Funkcja `misc.face()` z scipy jest przestarzała w nowszych wersjach, ale powinna działać w proponowanej wersji 1.0.

4. Kod używa `nib.load(fname).get_data()`, co w nowszych wersjach nibabel zostało zastąpione przez `nib.load(fname).get_fdata()`.

Powyższe środowisko powinno umożliwić uruchomienie programu z minimalnymi modyfikacjami kodu.

