# Analiza programu i zamiana biblioteki tk na PyQt5

Program, który analizuję, to przeglądarka obrazów 3D wykorzystująca bibliotekę Tkinter do interfejsu graficznego. Poniżej przedstawiam plan konwersji na PyQt5.

## Główne zmiany potrzebne do konwersji:

1. Zmiana importów z Tkinter na PyQt5
2. Zmiana struktury klas i dziedziczenia
3. Dostosowanie układu (layout) z pack/grid na QVBoxLayout, QHBoxLayout, QGridLayout
4. Zmiana widgetów Tkinter na odpowiedniki PyQt5
5. Dostosowanie obsługi zdarzeń

Zacznijmy od głównego pliku:

```python:tk3d_v04.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. GUI utilize PyQt5 library.

    (C) MKocinski & AMaterka

    Wersja programu nr 04 ( 04.04.2025 r.)
    Wersja uruchomiona i zakutalizowana.  

   Projekt: anazlia obrazów przegrody nosowo-szczękowej.
   

    Created: 13.11.2017
    Modified: 04.04.2025
==================================================
"""
print(__doc__)

import os
import sys
import numpy as np
import nibabel as nib
import matplotlib as mpl
import ctypes

# Zwiększenie skali DPI dla systemów Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# Zwiększenie rozmiaru czcionki i elementów Matplotlib
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.labelsize'] = 16
mpl.rcParams['xtick.labelsize'] = 16
mpl.rcParams['ytick.labelsize'] = 16
mpl.rcParams['legend.fontsize'] = 16
mpl.rcParams['figure.titlesize'] = 18

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QFrame)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.backend_bases as bckbases

# Importy własnych modułów (będą musiały zostać zaktualizowane)
from tk3d_v04_thresholdframe_qt import CheckButtonScaleFrame
from tk3d_v04_sliceviewerframe_qt import SliceViewerFrame
from tk3d_v04_buttonsframe_qt import ButtonsFrame
from tk3d_v04_mpl import MPL

#from mk_add_path_dropbox import MK_DROPBOX_DANE
MK_DROPBOX_DANE = '../dane'

def on_key_event(event):
    print('you pressed %s' % event.key)
    bckbases.key_press_handler(event, canvas, toolbar)

def on_scroll_event(event):
    if event.step > 0:
        delta = 1
    else:
        delta = -1
    curslice = sliceSld.get_slice()
    sliceSld.set_slice(curslice + delta)
    mpl.set_slice(curslice + delta)
    mpl._redraw()

class MainWindow(QMainWindow):
    def __init__(self, img, fname):
        super().__init__()
        
        # struktura: obraz i wyswietlanie
        self.mpl = MPL(img)
        self.mpl.set_filename(fname)
        self.mpl.set_workdir(MK_DROPBOX_DANE)
        
        self.setWindowTitle("3D viewer - %s" % fname)
        self.setGeometry(100, 100, 1400, 900)
        
        # Główny widget i układ
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Ramka na wykres
        plot_frame = QFrame()
        plot_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        plot_layout = QVBoxLayout(plot_frame)
        
        # Canvas Matplotlib
        self.canvas = FigureCanvas(self.mpl.fig)
        plot_layout.addWidget(self.canvas, 1)
        
        # Pasek narzędzi Matplotlib
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout.addWidget(self.toolbar)
        
        # Połączenie zdarzeń klawiatury i myszy
        self.canvas.mpl_connect('key_press_event', on_key_event)
        self.canvas.mpl_connect('scroll_event', on_scroll_event)
        
        main_layout.addWidget(plot_frame, 1)
        
        # Ramka na kontrolki
        controls_frame = QFrame()
        controls_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        controls_layout = QHBoxLayout(controls_frame)
        
        # Thresholding
        self.thres = CheckButtonScaleFrame(self.mpl)
        controls_layout.addWidget(self.thres)
        
        # Slice navigation
        self.sliceSld = SliceViewerFrame(self.mpl)
        controls_layout.addWidget(self.sliceSld)
        
        # Actions: Buttons Frame
        self.bf = ButtonsFrame(self.mpl)
        controls_layout.addWidget(self.bf)
        
        main_layout.addWidget(controls_frame)
        
        # Dostosowanie układu figury Matplotlib
        self.mpl.fig.tight_layout()
        
        # Ustawienie globalnych zmiennych dla funkcji obsługi zdarzeń
        global canvas, toolbar, sliceSld, mpl
        canvas = self.canvas
        toolbar = self.toolbar
        sliceSld = self.sliceSld
        mpl = self.mpl

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        img = nib.load(fname).get_fdata()
    else:
        from skimage import data
        fname = 'sample_image'
        img = data.astronaut()
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Nowoczesny styl interfejsu
    
    # Ustawienie globalnej czcionki
    font = app.font()
    font.setPointSize(12)
    app.setFont(font)
    
    window = MainWindow(img, fname)
    window.show()
    
    sys.exit(app.exec_())
```

Teraz przygotujmy moduł dla ramki progowania (threshold):

```python:tk3d_v04_thresholdframe_qt.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Threshold frame.

    (C) MKocinski & AMaterka

    Created: 17.11.2017
    Modified: 04.04.2025
==================================================
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QCheckBox, QSlider, QFrame)
from PyQt5.QtCore import Qt
import numpy as np


class CheckButtonScaleFrame(QFrame):

    def __init__(self, mpl):
        super().__init__()
        
        # Ustawienie stylu ramki
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        
        # additional instance variables
        self.mpl = mpl
        self.low = mpl.mn
        self.up = mpl.mx
        self.rangetoth = self._range2th()
        
        # Główny układ
        layout = QVBoxLayout(self)
        
        # Frame label
        self.label = QLabel('Thresholding')
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.label)
        
        # GLOBAL THRESHOLDING FRAME
        self.gthf = QFrame()
        gthf_layout = QHBoxLayout(self.gthf)
        
        # checkboks itself
        self.ch = QCheckBox("Single Th.")
        self.ch.setStyleSheet("font-size: 14px;")
        self.ch.clicked.connect(self._onCh1)
        gthf_layout.addWidget(self.ch)
        
        self.sc = QSlider(Qt.Horizontal)
        self.sc.setMinimum(int(self.low))
        self.sc.setMaximum(int(self.rangetoth))
        self.sc.setValue(self._setDefaultValue())
        self.sc.valueChanged.connect(self._onGThreshold)
        self.sc.setMinimumHeight(30)
        gthf_layout.addWidget(self.sc)
        
        layout.addWidget(self.gthf)
        
        # DOUBLE THRESHOLDING FRAME
        self.dthf = QFrame()
        dthf_layout = QHBoxLayout(self.dthf)
        
        self.ch2 = QCheckBox('Double Th.')
        self.ch2.setStyleSheet("font-size: 14px;")
        self.ch2.clicked.connect(self._onCh2)
        dthf_layout.addWidget(self.ch2)
        
        self.sclow = QSlider(Qt.Horizontal)
        self.sclow.setMinimum(int(self.low))
        self.sclow.setMaximum(int(self.rangetoth))
        self.sclow.setValue(int(self._setDefaultValue()*0.8))
        self.sclow.valueChanged.connect(self._onDThreshold)
        self.sclow.setMinimumHeight(30)
        dthf_layout.addWidget(self.sclow)
        
        self.scup = QSlider(Qt.Horizontal)
        self.scup.setMinimum(int(self.low))
        self.scup.setMaximum(int(self.rangetoth))
        self.scup.setValue(int(self._setDefaultValue()*1.2))
        self.scup.valueChanged.connect(self._onDThreshold)
        self.scup.setMinimumHeight(30)
        dthf_layout.addWidget(self.scup)
        
        layout.addWidget(self.dthf)

    def _updateAllProps(self):
        self.low = self.mpl.mn
        self.up = self.mpl.mx
        self.rangetoth = self._range2th()

        self.sc.setMinimum(int(self.low))
        self.sc.setMaximum(int(self.up * self.rangetoth))
        self.sclow.setMinimum(int(self.low))
        self.sclow.setMaximum(int(self.up * self.rangetoth))
        self.scup.setMinimum(int(self.low))
        self.scup.setMaximum(int(self.up * self.rangetoth))

        self.mpl.updatethresh = False

    def _onCh1(self):
        if self.ch.isChecked():
            self.ch2.setChecked(False)
        if self.mpl.updatethresh:
            self._updateAllProps()
        self._onGThreshold(self.sc.value())

    def _onCh2(self):
        if self.ch2.isChecked():
            self.ch.setChecked(False)
        if self.mpl.updatethresh:
            self._updateAllProps()
        self._onDThreshold(0)  # Wartość nie ma znaczenia, funkcja pobiera wartości z suwaków

    def _setDefaultValue(self):
        low, up = self.low, self.up
        if low >= 0:
            val = int((up-low)//2)
        else:
            val = int((up+low)//2)
        return val

    def _range2th(self):
        # Some image parameters & properties
        mx = self.mpl.mx
        if mx <= 1.0:
            self.rng2th = mx*1000
        elif mx <= 10.0:
            self.rng2th = mx*100
        else:
            self.rng2th = mx
        return self.rng2th

    def _onGThreshold(self, val):
        if self.ch.isChecked():
            ### ODZNACZYC MIP I mIP !!!
            data = np.where(self.mpl.im_o >= int(val)/self.rng2th, self.mpl.mx, self.mpl.mn)
            self.mpl.set_data(data)
            self.mpl._redraw()

    def _onDThreshold(self, val):
        if self.ch2.isChecked():
            if self.scup.value() < self.sclow.value():
                self.sclow.setValue(self.scup.value())
            if self.sclow.value() > self.scup.value():
                self.scup.setValue(self.sclow.value())

            up = self.scup.value()
            low = self.sclow.value()
            mx = self.mpl.mx
            mn = self.mpl.mn

            data = np.where(self.mpl.im_o > int(up), mx, self.mpl.im_o)
            data = np.where(data < int(low), mn, data)

            self.mpl.set_data(data)
            self.mpl._redraw()
```

Teraz moduł dla ramki przeglądarki przekrojów (slice viewer):

```python:tk3d_v04_sliceviewerframe_qt.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Slice Viewer Frame

    (C) MKocinski & AMaterka

    Created: 17.11.2017
    Modified: 04.04.2025
==================================================
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QCheckBox, QSlider, QFrame, QSpinBox)
from PyQt5.QtCore import Qt
import numpy as np


class SliceViewerFrame(QFrame):
    def __init__(self, mpl):
        super().__init__()
        
        # Ustawienie stylu ramki
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        
        # additional instance variable
        self.mpl = mpl
        self.low = 0
        self.up = mpl.sl-1
        
        # Główny układ
        layout = QVBoxLayout(self)
        
        # label
        label = QLabel('Slice manipulation')
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)
        
        # Slider dla przekrojów
        self.sc = QSlider(Qt.Horizontal)
        self.sc.setMinimum(self.low)
        self.sc.setMaximum(self.up)
        self.sc.setValue((self.up+self.low)//2)
        self.sc.valueChanged.connect(self._onSliceChange)
        self.sc.setMinimumHeight(30)
        layout.addWidget(self.sc)
        
        # Układ dla MIP, spinbox i mIP
        controls_layout = QHBoxLayout()
        
        # MIP
        self.mxch = QCheckBox('MIP')
        self.mxch.setStyleSheet("font-size: 14px;")
        self.mxch.clicked.connect(self._onMIP)
        controls_layout.addWidget(self.mxch)
        
        # spinbox
        self.rng = QSpinBox()
        self.rng.setMinimum(1)
        self.rng.setMaximum(100)
        self.rng.setValue(10)
        self.rng.valueChanged.connect(self._onMipRange)
        self.rng.setStyleSheet("font-size: 14px;")
        controls_layout.addWidget(self.rng)
        
        # mIP
        self.mnch = QCheckBox('mIP')
        self.mnch.setStyleSheet("font-size: 14px;")
        self.mnch.clicked.connect(self._onmIP)
        controls_layout.addWidget(self.mnch)
        
        layout.addLayout(controls_layout)

    def _onSliceChange(self, val):
        """Callback dla zmiany przekroju"""
        self.mpl.set_slice(int(val))
        self.mpl._redraw()
        
    def _onMIP(self):
        """Callback dla włączenia/wyłączenia MIP"""
        if self.mxch.isChecked():
            self.mnch.setChecked(False)
            self.mpl.rn = self.rng.value()
            self.mpl._redraw_mip('MIP')
        else:
            self.mpl._redraw()
            
    def _onmIP(self):
        """Callback dla włączenia/wyłączenia mIP"""
        if self.mnch.isChecked():
            self.mxch.setChecked(False)
            self.mpl.rn = self.rng.value()
            self.mpl._redraw_mip('mIP')
        else:
            self.mpl._redraw()
            
    def _onMipRange(self):
        """Callback dla zmiany zakresu MIP/mIP"""
        try:
            self.mpl.rn = self.rng.value()
            if self.mxch.isChecked():
                self.mpl._redraw_mip('MIP')
            elif self.mnch.isChecked():
                self.mpl._redraw_mip('mIP')
        except ValueError:
            pass
            
    def get_slice(self):
        """Zwraca aktualny numer przekroju"""
        return self.sc.value()
        
    def set_slice(self, val):
        """Ustawia numer przekroju"""
        val = max(self.low, min(self.up, val))
        self.sc.setValue(val)
```

Teraz moduł dla ramki przycisków:

```python:tk3d_v04_buttonsframe_qt.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Buttons frame.

    (C) MKocinski & AMaterka

    Created: 18.11.2017
    Modified: 04.04.2025
==================================================
"""
import nibabel as nib
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFileDialog, QFrame)
from PyQt5.QtCore import Qt, QCoreApplication
import numpy as np
import scipy.io as io
import time
import os

#from mk_add_path_dropbox import MK_DROPBOX_DANE
MK_DROPBOX_DANE = '../dane'


class ButtonsFrame(QFrame):
    def __init__(self, mpl):
        super().__init__()
        
        # Ustawienie stylu ramki
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        
        # additional instance variables
        self.mpl = mpl
        
        # Główny układ
        layout = QVBoxLayout(self)
        
        # Frame label
        self.label = QLabel('Actions:')
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.label)
        
        # Open Image button
        open_button = QPushButton('Open Image')
        open_button.setStyleSheet("background-color: lightgray; font-size: 14px;")
        open_button.setMinimumHeight(50)
        open_button.clicked.connect(self._onOpen)
        layout.addWidget(open_button)
        
        # Reload & Invert buttons
        f1_layout = QHBoxLayout()
        reload_button = QPushButton('Reload')
        reload_button.setStyleSheet("font-size: 14px;")
        reload_button.setMinimumHeight(50)
        reload_button.clicked.connect(self._onReload)
        f1_layout.addWidget(reload_button)
        
        invert_button = QPushButton('Invert')
        invert_button.setStyleSheet("font-size: 14px;")
        invert_button.clicked.connect(self._onInvert)
        f1_layout.addWidget(invert_button)
        layout.addLayout(f1_layout)
        
        # Info & Header buttons
        f2_layout = QHBoxLayout()
        info_button = QPushButton('Info')
        info_button.setStyleSheet("font-size: 14px;")
        info_button.clicked.connect(self._onInfo)
        f2_layout.addWidget(info_button)
        
        header_button = QPushButton('Header')
        header_button.setStyleSheet("font-size: 14px;")
        header_button.clicked.connect(self._onHeader)
        f2_layout.addWidget(header_button)
        layout.addLayout(f2_layout)
        
        # Save button
        save_button = QPushButton('Save')
        save_button.setStyleSheet("font-size: 14px;")
        save_button.clicked.connect(self._onSaveFile)
        layout.addWidget(save_button)
        
        # Quit button
        quit_button = QPushButton('Quit')
        quit_button.setStyleSheet("background-color: lightgray; font-size: 14px;")
        quit_button.clicked.connect(self._onQuit)
        layout.addWidget(quit_button)

    def _onQuit(self):
        QCoreApplication.instance().quit()

    def _onInvert(self):
        self.mpl.set_data(self.mpl.mx - self.mpl.im)
        self.mpl._redraw()

    def _onReload(self):
        self.mpl._reload_image()

    def _onHeader(self):
        if self.mpl.hdr:
            print(50*'*')
            print(self.mpl.hdr)
            print(50*'*')
        else:
            print('There is no header!')
            
    def _onInfo(self):
        self.mpl.info()

    def _onOpen(self):
        options = QFileDialog.Options()
        file_filter = "Nifti Files (*.nii *.nii.gz);;Numpy Files (*.npy);;Matlab Files (*.mat);;All Files (*)"
        fname, _ = QFileDialog.getOpenFileName(
            None, "Open Image File", MK_DROPBOX_DANE, file_filter, options=options
        )
        
        if fname:
            try:
                self.mpl.load_image(fname)
            except Exception as e:
                print("Open Source File", f"Failed to read file\n'{fname}'")
                print(f"Error: {e}")
            return

    def _onSaveFile(self):
        options = QFileDialog.Options()
        file_filter = "Nifti Files (*.nii *.nii.gz);;Numpy Files (*.npy);;Matlab Files (*.mat);;All Files (*)"
        fname, _ = QFileDialog.getSaveFileName(
            None, "Save Image File", os.path.join(MK_DROPBOX_DANE, self.mpl.fname),
            file_filter, options=options
        )
        
        if not fname:
            return
        
        print("********", fname)
        try:
            if '.nii' in fname:
                if self.mpl.hdr:
                    hdr = self.mpl.hdr
                    hdr['descrip'] = 'angio3d-nibabel-' + nib.__version__ + ' by MK ({})'.format(time.strftime("%Y-%m-%d"))
                    img = nib.Nifti1Image(self.mpl.im, affine=self.mpl.nii.affine, header=hdr)
                else:
                    hdr = nib.Nifti1Header()
                    hdr['descrip'] = 'angio3d-nibabel-' + nib.__version__ + ' by MK ({})'.format(time.strftime("%Y-%m-%d"))
                    img = nib.Nifti1Image(self.mpl.im, affine=np.eye(4), header=hdr)
                img.set_data_dtype(self.mpl.im.dtype.name)
                img.to_filename(fname)
            elif fname.endswith('.npy'):
                np.save(fname, self.mpl.im)
            elif fname.endswith('.mat'):
                io.savemat(fname, {'im':self.mpl.im})
            else:
                print("Nieobsługiwane rozszerzenie pliku do zapisu!")
        except Exception as e:
            print(f"Błąd podczas zapisywania pliku: {e}")
```

Klasa MPL może pozostać praktycznie bez zmian, ponieważ jest odpowiedzialna za manipulację obrazem i nie jest bezpośrednio związana z interfejsem użytkownika. Jedyna zmiana to dostosowanie do używania FigureCanvasQTAgg zamiast FigureCanvasTkAgg.

## Podsumowanie zmian:

1. Zamieniono wszystkie widgety Tkinter na odpowiedniki PyQt5:
   - `tk.Frame` → `QFrame`
   - `tk.Button` → `QPushButton`
   - `tk.Scale` → `QSlider`
   - `tk.Checkbutton` → `QCheckBox`
   - `tk.Spinbox` → `QSpinBox`
   - `tk.Label` → `QLabel`

2. Zmieniono system układu:
   - `pack()` i `grid()` → `QVBoxLayout`, `QHBoxLayout`, `QGridLayout`

3. Zmieniono sposób obsługi zdarzeń:
   - `command=funkcja` → `clicked.connect(funkcja)`
   - `variable=var` → bezpośrednie połączenie z metodami `isChecked()` i `setChecked()`

4. Zmieniono sposób obsługi dialogów:
   - `filedialog.askopenfilename()` → `QFileDialog.getOpenFileName()`
   - `filedialog.asksaveasfile()` → `QFileDialog.getSaveFileName()`

5. Zmieniono sposób obsługi głównego okna:
   - `tk.Tk()` → `QMainWindow`
   - `mainloop()` → `app.exec_()`

6. Dostosowano stylizację:
   - Użyto `setStyleSheet()` zamiast opcji Tkinter

Ta konwersja zachowuje wszystkie funkcjonalności oryginalnego programu, jednocześnie wykorzystując zalety PyQt5, takie jak nowoczesny wygląd, lepsze wsparcie dla wysokich rozdzielczości i bardziej elastyczny system układu.
