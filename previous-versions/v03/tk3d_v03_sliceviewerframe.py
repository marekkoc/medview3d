#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Button Frame 1

    (C) MKocinski & AMaterka

    Created: 17.11.2017
    Modified: 18.11.2017
==================================================
"""
import tkinter as tk
import numpy as np


class SliceViewerFrame(tk.Frame):
    def __init__(self, parent, mpl):

        super(SliceViewerFrame, self).__init__(master=parent,
                                      relief=tk.RIDGE, borderwidth=2)

        # additional instance variable
        self.mpl = mpl
        self.low = 0
        self.up = mpl.sl-1

        # label
        label = tk.Label(master=self, text='Slice manipulation')
        label.pack(side=tk.TOP, anchor=tk.NW)

        # variable for scale
        self.scvar = tk.IntVar()
        self.sc = tk.Scale(master=self, from_=self.low, to=self.up,
                           variable=self.scvar, command=self._onSliceChange,
                           orient=tk.HORIZONTAL)
        self.sc.pack(expand=True, fill=tk.X)
        self.sc.set((self.up+self.low)//2)

        # MIP
        self.mxvar = tk.BooleanVar()
        self.mxch = tk.Checkbutton(master=self, text='MIP',
                                   variable=self.mxvar, command=self._onMIP)
        self.mxch.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.mxch.deselect()

        # spinbox
        self.rngvar = tk.StringVar()
        self.rngvar.set(str(10))
        self.rng = tk.Spinbox(master=self, from_=1, to=100,
                              width=3, command=self._onMipRange,
                              textvariable=self.rngvar)
        self.rng.pack(side=tk.LEFT, fill=tk.X, expand=1)

        # mIP
        self.mnvar = tk.BooleanVar()
        self.mnch = tk.Checkbutton(master=self, command=self._onmIP,
                                   text='mIP', variable=self.mnvar)
        self.mnch.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.mnch.deselect()

        self.pack(side=tk.LEFT, expand=True, anchor=tk.W, fill=tk.BOTH)


    def _onSliceChange(self,val):
        
        self.mpl.set_slice(self.sc.get())        
        
        if self.mxvar.get():
            self._onMIP()
        elif self.mnvar.get():
            self._onmIP()
        else:
            self.mpl._redraw()


    def _onMIP(self):
        if self.mxvar.get():
            self.mnvar.set(False)
            self.mpl.rn = int(self.rngvar.get())    
            self.mpl._redraw_mip('MIP')        
        else:
            self.mpl._redraw()

    def _onmIP(self):
        if self.mnvar.get():
            self.mxvar.set(False)
            self.mpl.rn = int(self.rngvar.get())    
            self.mpl._redraw_mip('mIP')
        else:
            self.mpl._redraw()

    def _onMipRange(self):
        self.mpl.rn = self.rngvar.get()
        self._onSliceChange(self.sc.get())


if __name__ == '__main__':
    import matplotlib as mpl
    import scipy.misc as misc
    from tk3d_v03_mpl import MPL

    im = misc.face()
    mpl = MPL(im)

    master = tk.Tk()
    bt = SliceViewerFrame(master, mpl)
    tk.mainloop()
