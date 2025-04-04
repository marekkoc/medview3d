#!/usr/bin/env python3
"""
==================================================
    3D image viewer. GUI with Tkinter library

    (C) MKocinski & AMaterka
    
    Created: 13.11.2017
    Modified: 17.11.2017
==================================================
"""
print(__doc__)


import sys
import os
import numpy as np
import nibabel as nib
import matplotlib as mpl

import matplotlib.backends.backend_tkagg as bcktagg
import matplotlib.backend_bases as bckbases


if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk
    

from mk_add_path_dropbox import MK_DROPBOX_DANE



def on_key_event(event):
    print('you pressed %s' % event.key)
    bckbases.key_press_handler(event, canvas, toolbar)

def on_scroll_event(event):
    if event.step > 0:
        delta = 1
    else:
        delta = -1
    sliderVar.set(sliderVar.get() + delta)
    axdata.set_data(img[:, :, sliderScale.get()])
    fig.canvas.draw()




def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def onInvert():
    global img
    img = img_max - img
    axdata.set_data(img[:, :, sliderScale.get()])
    fig.canvas.draw()

def onThrashold(val):
    global img
    if var.get():
        maxChB.deselect()
        minChB.deselect()
        img = np.where(img_o>= int(val),img_max,img_min)
        axdata.set_data(img[:, :, sliderScale.get()])
        fig.canvas.draw()

def onReload():
    global img,var
    img = img_o.copy()
    axdata.set_data(img[:, :, sliderScale.get()])
    fig.canvas.draw()
    var.set(False)

def onSlide(val):
    maxChB.deselect()
    minChB.deselect()
    axdata.set_data(img[:, :, sliderScale.get()])
    fig.canvas.draw()

def onMIP():
    global maxVar, minVar
    if maxVar.get():
        minVar.set(False)
        axdata.set_data(img.max(2))
        fig.canvas.draw()
    else:
        axdata.set_data(img[:, :, sliderScale.get()])
        fig.canvas.draw()

def onmIP():
    global maxVar, minVar
    if minVar.get():
        maxVar.set(False)
        axdata.set_data(img.min(2))
        fig.canvas.draw()
    else:
        axdata.set_data(img[:, :, sliderScale.get()])
        fig.canvas.draw()

#def onCut():
#    global img
#
#    xmn = int(xminSB.get())
#    xmx = int(xmaxSB.get())
#    ymn = int(yminSB.get())
#    ymx = int(ymaxSB.get())
#    zmn = int(zminSB.get())
#    zmx = int(zmaxSB.get())
#    img = img_o[xmn:xmx, ymn:ymx, zmn:zmx]
#    print(img.shape)
#    axdata.set_data(img[:, :, sliderScale.get()])
#    fig.canvas.draw()


def info(img):
    print("  Brightness:")
    print("\tmax = %.2f"%img_max)
    print('\tmin = %.2f'%img_min)
    print('  Type = %s' % img.dtype )


if __name__ == '__main__':
    #fname = 'plik_SE00008_i_cut_gauss-490_vef_2o00_3o00.nii'
    #img = nib.load(os.path.join('VEF',fname)).get_data()

    if len(sys.argv)>1:
        fname = sys.argv[1]
        img = nib.load(fname).get_data()
    else:
        print("\nNie podales zadnego obrazu! Wczytamy obraz domyslny.\n")
        fname = 'plik_SE00008_i_cut.nii.gz'
        if os.path.exists(os.path.join(MK_DROPBOX_DANE,fname)):
            img = nib.load(os.path.join(MK_DROPBOX_DANE,fname)).get_data()
        else:
            import scipy.misc as misc
            fname = 'obazek'
            img = misc.face()


    img_o = img.copy()
    img_min = img.min()
    img_max = img.max()
    img_x, img_y, img_z = img.shape
    info(img)




    # Some image parameters & properties
    sl = img.shape[-1]
    immx = img.max()
    if immx <=1.0:
        imgRangeToTh = immx*1000
    elif img.max() <= 10.0:
        imgRangeToTh = immx * 100
    else:
        imgRangeToTh = immx

    # Main window
    root = Tk.Tk()
    root.wm_title("3D viewer - %s" %fname)

    # Matplotlib figure
    fig = mpl.figure.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    axdata = ax.imshow(img[:,:,sl//2],cmap='gray')
    ax.axis('off')

    # a tk.DrawingArea
    canvas = bcktagg.FigureCanvasTkAgg(fig, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    # Matplotlib toolbar
    toolbar = bcktagg.NavigationToolbar2TkAgg(canvas,root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    # connection key_press event (Matplotlib)
    canvas.mpl_connect('key_press_event', on_key_event)
    canvas.mpl_connect('scroll_event', on_scroll_event)

    # tkinter widgets

    thframe = Tk.Frame(master=root)
    var = Tk.BooleanVar()
    check_button = Tk.Checkbutton(master=thframe, text="Thresh.", variable=var)
    check_button.pack(side=Tk.LEFT)
    check_button.deselect()

    threshscale = Tk.Scale(master=thframe, from_=0, to=imgRangeToTh, command= onThrashold, orient=Tk.HORIZONTAL)
    threshscale.pack(side=Tk.LEFT, padx=1, expand=1, fill=Tk.X)
    threshscale.set(imgRangeToTh/2)
    thframe.pack(fill=Tk.X)




    showFrame = Tk.Frame(master=root)
    sliderVar = Tk.IntVar()
    sliderScale = Tk.Scale(master=showFrame, from_=0, to=sl-1, orient=Tk.HORIZONTAL, command=onSlide, variable=sliderVar)
    sliderScale.pack(side=Tk.LEFT, padx=1, expand=1, fill=Tk.X)
    sliderScale.set(sl//2)

    maxVar = Tk.BooleanVar()
    minVar = Tk.BooleanVar()
    maxChB = Tk.Checkbutton(master=showFrame, text='MIP', variable=maxVar,command=onMIP)
    maxChB.pack(side=Tk.TOP)
    maxChB.deselect()
    minChB = Tk.Checkbutton(master=showFrame, text='mIP', variable=minVar,command=onmIP)
    minChB.pack(side=Tk.BOTTOM)
    minChB.deselect()
    showFrame.pack(fill=Tk.X)


#    rangeFrame = Tk.Frame(master=root)
#    xminL = Tk.Label(master=rangeFrame,text='Xmin')
#    xminL.pack(side=Tk.LEFT)
#    xminSB = Tk.Spinbox(master=rangeFrame,from_=0, to=img_x-1,command=onCut,width=3)
#    xminSB.pack(side=Tk.LEFT,expand=0)
#    xmaxL = Tk.Label(master=rangeFrame,text='Xmax')
#    xmaxL.pack(side=Tk.LEFT)
#    xmaxVar = Tk.StringVar()
#    xmaxVar.set(str(img_x-1))
#    xmaxSB = Tk.Spinbox(master=rangeFrame,from_=0, to=img_x-1, textvariable=xmaxVar,command=onCut,width=3)
#    xmaxSB.pack(side=Tk.LEFT, expand=0, fill=Tk.X)
#
#    yminL = Tk.Label(master=rangeFrame,text='Ymin')
#    yminL.pack(side=Tk.LEFT)
#    yminSB = Tk.Spinbox(master=rangeFrame,from_=0, to=img_y-1,command=onCut,width=3)
#    yminSB.pack(side=Tk.LEFT,expand=0)
#    ymaxL = Tk.Label(master=rangeFrame,text='Ymax')
#    ymaxL.pack(side=Tk.LEFT)
#    ymaxVar = Tk.StringVar()
#    ymaxVar.set(str(img_y-1))
#    ymaxSB = Tk.Spinbox(master=rangeFrame,from_=0, to=img_y-1,textvariable=ymaxVar, command=onCut,width=3)
#    ymaxSB.pack(side=Tk.LEFT, expand=0,fill=Tk.X)
#
#
#    zminL = Tk.Label(master=rangeFrame,text='Zmin')
#    zminL.pack(side=Tk.LEFT)
#    zminSB = Tk.Spinbox(master=rangeFrame,from_=0, to=img_z-1,command=onCut,width=3)
#    zminSB.pack(side=Tk.LEFT,expand=0)
#    zmaxL = Tk.Label(master=rangeFrame,text='Zmax')
#    zmaxL.pack(side=Tk.LEFT)
#    zmaxVar = Tk.StringVar()
#    zmaxVar.set(str(img_z-1))
#    zmaxSB = Tk.Spinbox(master=rangeFrame,from_=0, to=img_z-1,textvariable=zmaxVar, command=onCut,width=3)
#    zmaxSB.pack(side=Tk.LEFT, expand=0,fill=Tk.X)
#    rangeFrame.pack()

    # Buttons & frame for them
    buttonFrame = Tk.Frame(master=root)
    invert_button = Tk.Button(master=buttonFrame, text='Invert', command=onInvert)
    invert_button.pack(side=Tk.LEFT, fill=Tk.BOTH)

    reload_button = Tk.Button(master=buttonFrame, text='Reload', command=onReload)
    reload_button.pack(fill=Tk.BOTH, side=Tk.RIGHT)

    quit_frame = Tk.Frame(master=buttonFrame)
    quit_frame.pack(fill=Tk.BOTH, side=Tk.BOTTOM)
    quit_button = Tk.Button(master=quit_frame, text='Quit', command=_quit, bg='gray')
    quit_button.pack(fill=Tk.BOTH)
    buttonFrame.pack(fill=Tk.X, pady=10)






    Tk.mainloop()
    # If you put root.destroy() here, it will cause an error if
    # the window is closed with the window manager.
