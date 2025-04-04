#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. GUI utilize Tkinter library.

    (C) MKocinski & AMaterka

    Wersja programu nr 04 (z dnia 28.11.2017 r.)

    Created: 13.11.2017
    Modified: 01.12.2017
==================================================
"""
print(__doc__)

import os
import sys
import numpy as np
import tkinter as tk
import nibabel as nib
import matplotlib as mpl

import matplotlib.backends.backend_tkagg as bcktagg
import matplotlib.backend_bases as bckbases

from tk3d_v04_thresholdframe import CheckButtonScaleFrame
from tk3d_v04_sliceviewerframe import SliceViewerFrame
from tk3d_v04_buttonsframe import ButtonsFrame
from tk3d_v04_mpl import MPL


from mk_add_path_dropbox import MK_DROPBOX_DANE



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
    #fname = 'plik_SE00008_i_cut_gauss-490_vef_2o00_3o00.nii'
    #img = nib.load(os.path.join('VEF',fname)).get_data()

    if len(sys.argv) > 1:
        fname = sys.argv[1]
        img = nib.load(fname).get_data()
    else:
        import scipy.misc as misc
        fname = 'obazek'
        img = misc.face()


    # Main window
    root = tk.Tk()
    root.wm_title("3D viewer - %s" % fname)

    # struktura: obraz i wyswietlanie
    mpl = MPL(img)
    mpl.set_filename(fname)
    mpl.set_workdir(MK_DROPBOX_DANE)

#    ax2 = fig.add_subplot(122)
#    axdata2 = ax2.imshow(np.random.rand(100,100))


    # a tk.DrawingArea
    canvas = bcktagg.FigureCanvasTkAgg(mpl.fig, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Matplotlib toolbar
    toolbar = bcktagg.NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # connection key_press event (Matplotlib)
    canvas.mpl_connect('key_press_event', on_key_event)
    canvas.mpl_connect('scroll_event', on_scroll_event)

    # Thresholding
    thres = CheckButtonScaleFrame(root, mpl)

    # Slice navigation
    sliceSld = SliceViewerFrame(root, mpl)

    # Actions: Buttons Frame
    bf = ButtonsFrame(root, mpl)


    mpl.fig.tight_layout()
    tk.mainloop()
    # If you put root.destroy() here, it will cause an error if
    # the window is closed with the window manager.
