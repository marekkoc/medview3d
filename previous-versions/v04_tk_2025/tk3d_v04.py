#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. GUI utilize Tkinter library.

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
import tkinter as tk
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

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.backend_bases as bckbases

from tk3d_v04_thresholdframe import CheckButtonScaleFrame
from tk3d_v04_sliceviewerframe import SliceViewerFrame
from tk3d_v04_buttonsframe import ButtonsFrame
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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        img = nib.load(fname).get_fdata()
    else:
        from skimage import data
        fname = 'sample_image'
        img = data.astronaut()

    # Main window
    root = tk.Tk()
    root.wm_title("3D viewer - %s" % fname)

    # Ustawienie skali czcionki dla Tkinter
    default_font = ('TkDefaultFont', 16)
    text_font = ('TkTextFont', 16)
    fixed_font = ('TkFixedFont', 16)
    
    root.option_add("*Font", default_font)
    root.option_add("*Text.Font", text_font)
    root.option_add("*Entry.Font", fixed_font)
    root.option_add("*Button.Font", default_font)
    root.option_add("*Label.Font", default_font)
    root.option_add("*Scale.Font", default_font)
    root.option_add("*Checkbutton.Font", default_font)
    root.option_add("*Radiobutton.Font", default_font)
    root.option_add("*Menu.Font", default_font)
    
    # Zwiększenie rozmiaru okna i zapobieganie zmniejszaniu poniżej minimalnego rozmiaru
    root.geometry("1400x900")
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    
    # Użyj Grid zamiast Pack dla lepszej kontroli układu
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)  # Kontrolki nie powinny się rozszerzać

    # struktura: obraz i wyswietlanie
    mpl = MPL(img)
    mpl.set_filename(fname)
    mpl.set_workdir(MK_DROPBOX_DANE)

    # Ramka na wykres
    plot_frame = tk.Frame(root)
    plot_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    plot_frame.grid_columnconfigure(0, weight=1)
    plot_frame.grid_rowconfigure(0, weight=1)
    plot_frame.grid_rowconfigure(1, weight=0)

    # Canvas Matplotlib
    canvas = FigureCanvasTkAgg(mpl.fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # Pasek narzędzi Matplotlib
    toolbar_frame = tk.Frame(plot_frame)
    toolbar_frame.grid(row=1, column=0, sticky="ew")
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()

    # Połączenie zdarzeń klawiatury i myszy
    canvas.mpl_connect('key_press_event', on_key_event)
    canvas.mpl_connect('scroll_event', on_scroll_event)

    # Ramka na kontrolki
    controls_frame = tk.Frame(root, height=250)
    controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
    controls_frame.grid_columnconfigure(0, weight=1)
    controls_frame.grid_columnconfigure(1, weight=1)
    controls_frame.grid_columnconfigure(2, weight=1)
    
    # Thresholding
    thres = CheckButtonScaleFrame(controls_frame, mpl)
    thres.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    # Slice navigation
    sliceSld = SliceViewerFrame(controls_frame, mpl)
    sliceSld.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

    # Actions: Buttons Frame
    bf = ButtonsFrame(controls_frame, mpl)
    bf.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

    # Dostosowanie układu figury Matplotlib
    mpl.fig.tight_layout()
    
    # Uruchomienie głównej pętli
    tk.mainloop()
