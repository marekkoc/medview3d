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
from medview3d_thresholdframe_qt import CheckButtonScaleFrame
from medview3d_sliceviewerframe_qt import SliceViewerFrame
from medview3d_buttonsframe_qt import ButtonsFrame
from medview3d_mpl import MPL

#from mk_add_path_dropbox import MK_DROPBOX_DANE
MK_DROPBOX_DANE = 'dane'

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
        
        main_layout.addWidget(plot_frame, 8)  # Proporcja dla obszaru wykresu
        
        # Ramka na kontrolki
        controls_frame = QFrame()
        controls_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setContentsMargins(5, 5, 5, 5)
        
        # Thresholding
        self.thres = CheckButtonScaleFrame(self.mpl)
        controls_layout.addWidget(self.thres)
        
        # Slice navigation
        self.sliceSld = SliceViewerFrame(self.mpl)
        controls_layout.addWidget(self.sliceSld)
        
        # Actions: Buttons Frame
        self.bf = ButtonsFrame(self.mpl)
        controls_layout.addWidget(self.bf)
        
        main_layout.addWidget(controls_frame, 2)  # Proporcja dla panelu kontrolnego
        
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
        # Sprawdź dostępne obrazy w Twojej wersji skimage
        fname = 'cie-gra-se8-cut2-cl4.npy'
        img = np.random.rand(100, 100, 10) * 255  # Wygeneruj losowy obraz 3D jako alternatywę
        img2: np.ndarray = np.load(os.path.join(MK_DROPBOX_DANE, 'cie-gra-se8-cut2-cl4.npy'))
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Nowoczesny styl interfejsu
    
    # Ustawienie globalnej czcionki
    font = app.font()
    font.setPointSize(12)
    app.setFont(font)
    
    window = MainWindow(img2, fname)
    window.show()
    
    sys.exit(app.exec_())
