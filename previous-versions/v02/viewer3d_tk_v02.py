#!/usr/bin/env python3
"""
==================================================
    3D image viewer. GUI utilize Tkinter library.

    (C) MKocinski & AMaterka

    Wersja programu z dnia 18.11.2017

    Created: 13.11.2017
    Modified: 18.11.2017
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

from viewer3d_tk_v02_thresholdframe import CheckButtonScaleFrame
from viewer3d_tk_v02_sliceviewerframe import SliceViewerFrame
from viewer3d_tk_v02_image import ImageInfo
from viewer3d_tk_v02_buttonsframe import ButtonsFrame


from mk_add_path_dropbox import MK_DROPBOX_DANE



def on_key_event(event):
    print('you pressed %s' % event.key)
    bckbases.key_press_handler(event, canvas, toolbar)

def on_scroll_event(event):
    if event.step > 0:
        delta = 1
    else:
        delta = -1
    sv.scvar.set(sv.scvar.get() + delta)
    axdata.set_data(img[:, :, sv.sc.get()])
    fig.canvas.draw()


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def onInvert():
    global img
    img = img_max - img
    axdata.set_data(img[:, :, sv.sc.get()])
    fig.canvas.draw()


def onThrashold(val):
    global img
    if thres.var.get():
        sv.mxch.deselect()
        sv.mnch.deselect()
        img = np.where(img_o >= int(val), img_max, img_min)
        axdata.set_data(img[:, :, sv.sc.get()])
        fig.canvas.draw()


def onReload():
    global img, thres
    img = img_o.copy()
    axdata.set_data(img[:, :, sv.sc.get()])
    fig.canvas.draw()
    thres.var.set(False)


def onSlide(val):
    if sv.mxvar.get():
        onMIP()
    elif sv.mnvar.get():
        onmIP()
    else:
        axdata.set_data(img[:, :, sv.sc.get()])

    fig.canvas.draw()

def onMIPRangeChange():
    val = sv.sc.get()
    onSlide(val)


def onMIP():
    if sv.mxvar.get():
        sv.mnvar.set(False)
        rn = int(sv.rngvar.get())
        cur = sv.sc.get()
        r = np.array([cur-rn,cur+rn]).clip(0,img_z)
        axdata.set_data(img[:, :, r[0]:r[1]].max(2))
    else:
        axdata.set_data(img[:, :, sv.sc.get()])
    fig.canvas.draw()


def onmIP():
    if sv.mnvar.get():
        sv.mxvar.set(False)
        rn = int(sv.rngvar.get())
        cur = sv.sc.get()
        r = np.array([cur-rn,cur+rn]).clip(0,img_z)
        axdata.set_data(img[:, :, r[0]:r[1]].min(2))
    else:
        axdata.set_data(img[:, :, sv.sc.get()])
    fig.canvas.draw()


if __name__ == '__main__':
    # fname = 'plik_SE00008_i_cut_gauss-490_vef_2o00_3o00.nii'
    # img = nib.load(os.path.join('VEF',fname)).get_data()

    if len(sys.argv) > 1:
        fname = sys.argv[1]
        img = nib.load(fname).get_data()
    else:
        print("\nNie podales zadnego obrazu! Wczytamy obraz domyslny.\n")
        fname = 'plik_i_cut.nii.gz'
        print(os.path.join(MK_DROPBOX_DANE, fname))
        if os.path.exists(os.path.join(MK_DROPBOX_DANE, fname)):
            img = nib.load(os.path.join(MK_DROPBOX_DANE, fname)).get_data()
        else:
            import scipy.misc as misc
            fname = 'obazek'
            img = misc.face()

    iminfo = ImageInfo(img)
    img_o = iminfo.im
    img_min = iminfo.mn
    img_max = iminfo.mx
    img_x, img_y, img_z = img.shape
    sl = iminfo.sl
    imgRangeToTh = iminfo.range2th()

    # Main window
    root = tk.Tk()
    root.wm_title("3D viewer - %s" % fname)

    # Matplotlib figure
    fig = mpl.figure.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    axdata = ax.imshow(img[:, :, sl//2], cmap='gray', aspect='equal')
    ax.axis('off')

#    ax2 = fig.add_subplot(122)
#    axdata2 = ax2.imshow(np.random.rand(100,100))


    # a tk.DrawingArea
    canvas = bcktagg.FigureCanvasTkAgg(fig, master=root)
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
    thres = CheckButtonScaleFrame(parent=root, low=img_min, up=imgRangeToTh,
                                  fpos=tk.LEFT, fexpand=True,
                                  command=onThrashold, checkName='')

    # Slice navigation
    sv = SliceViewerFrame(parent=root, up=sl-1, fpos=tk.LEFT, fexpand=True,
                          commandScale=onSlide,
                          commandMIP=onMIP,
                          commandmIP=onmIP,
                          commandSpin=onMIPRangeChange)
    # Actions: Buttons Frame
    #bf = ButtonsFrame(parent=root)


#    # Buttons & frame for them
#    buttonFrame = tk.Frame(master=root)
#    invert_button = tk.Button(master=buttonFrame, text='Invert', command=onInvert)
#    invert_button.pack(fill=tk.BOTH)
#
#    reload_button = tk.Button(master=buttonFrame, text='Reload', command=onReload)
#    reload_button.pack(fill=tk.BOTH)
#
#    cluster_button = tk.Button(master=buttonFrame, text='Cluster',state=tk.DISABLED)
#    cluster_button.pack(fill=tk.X)
#
#    snake_button = tk.Button(master=buttonFrame, text='Snake', state=tk.DISABLED)
#    snake_button.pack(fill=tk.X)
#
#    seed_button = tk.Button(master=buttonFrame, text='Grow', state=tk.DISABLED)
#    seed_button.pack(fill=tk.X)
#
#    save_button = tk.Button(master=buttonFrame, text='Save to Nifti', state=tk.DISABLED)
#    save_button.pack(fill=tk.X)
#
#    quit_frame = tk.Frame(master=buttonFrame)
#    quit_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
#    quit_button = tk.Button(master=quit_frame, text='Quit', command=_quit, bg='gray')
#    quit_button.pack(fill=tk.BOTH)
#
#
#    buttonFrame.pack(expand=False,side=tk.RIGHT)

    fig.tight_layout()
    tk.mainloop()
    # If you put root.destroy() here, it will cause an error if
    # the window is closed with the window manager.
