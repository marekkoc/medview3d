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
import tkinter as tk
import numpy as np


class CheckButtonScaleFrame(tk.Frame):

    def __init__(self, parent, mpl):

        super(CheckButtonScaleFrame, self).__init__(master=parent,
                                      relief=tk.RIDGE, borderwidth=2, width=300)
        # additional instance variables
        self.mpl = mpl
        self.low = mpl.mn
        self.up = mpl.mx
        self.rangetoth = self._range2th()

        # Frame label z większą czcionką
        self.label = tk.Label(self, text='Thresholding', font=('TkDefaultFont', 16))
        self.label.pack(side=tk.TOP, anchor=tk.NW)

        # GLOBAL THRESHOLDING FRAME
        self.gthf = tk.Frame(master=self)
        self.var = tk.BooleanVar()
        # checkboks itself
        self.ch = tk.Checkbutton(master=self.gthf, text="Single Th.", variable=self.var, command=self._onCh1, font=('TkDefaultFont', 14))
        self.ch.pack(expand=0,side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        self.ch.deselect()
        self.sc = tk.Scale(master=self.gthf,from_=self.low, to=self.rangetoth,
                                           command=self._onGThreshold, orient=tk.HORIZONTAL,
                                           length=300, width=30,  # Zwiększona szerokość
                                           font=('TkDefaultFont', 14))  # Dodana czcionka
        self.sc.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.sc.set(self._setDefaultValue())

        self.gthf.pack(expand=1, fill = tk.BOTH)

        # DOUBLE THRESHOLDING FRAME
        self.dthf = tk.Frame(master=self)
        self.var2 = tk.BooleanVar()
        self.ch2 = tk.Checkbutton(master=self.dthf,text='Double Th.', variable=self.var2, command=self._onCh2, font=('TkDefaultFont', 14))
        self.ch2.pack(expand=0, side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        self.ch2.deselect()

        self.sclow = tk.Scale(master=self.dthf,from_=self.low, to=self.rangetoth,
                                           command=self._onDThreshold, orient=tk.HORIZONTAL,
                                           length=300, width=30,  # Zwiększona szerokość
                                           font=('TkDefaultFont', 14))  # Dodana czcionka
        self.sclow.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.sclow.set(self._setDefaultValue()*0.8)

        self.scup = tk.Scale(master=self.dthf, from_=self.low,
                         to=self.rangetoth, command=self._onDThreshold, orient=tk.HORIZONTAL,
                         length=300, width=30,  # Zwiększona szerokość
                         font=('TkDefaultFont', 14))  # Dodana czcionka
        self.scup.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.scup.set(self._setDefaultValue()*1.2)

        self.dthf.pack(expand=1, fill=tk.BOTH)

    def _updateAllProps(self):
        self.low = self.mpl.mn
        self.up = self.mpl.mx
        self.rangetoth = self._range2th()

        self.sc.configure(from_=self.low, to=self.up * self.rangetoth)
        self.sclow.configure(from_=self.low, to=self.up * self.rangetoth)
        self.scup.configure(from_=self.low, to=self.up * self.rangetoth)

        self.mpl.updatethresh = False

    def _onCh1(self):
        if self.var.get():
            self.var2.set(False)
        if self.mpl.updatethresh:
            self._updateAllProps()

    def _onCh2(self):
        if self.var2.get():
            self.var.set(False)
        if self.mpl.updatethresh:
            self._updateAllProps()


    def _setDefaultValue(self):
        low, up = self.low, self.up
        if low >= 0:
            val = (up-low)//2
        else:
            val = (up+low)//2
        return val

    def _range2th(self):
        # Some image parameters & properties
        mx = self.mpl.mx
        if  mx <= 1.0:
            self.rng2th = mx*1000
        elif mx <= 10.0:
            self.rng2th = mx*100
        else:
            self.rng2th = mx
        return self.rng2th

    def _onGThreshold(self,val):
        if self.var.get():
            ### ODZNACZYC MIP I mIP !!!
            data = np.where(self.mpl.im_o >= int(val)/self.rng2th, self.mpl.mx, self.mpl.mn)
            self.mpl.set_data(data)
            self.mpl._redraw()

    def _onDThreshold(self,val):
        if self.var2.get():
            if  self.scup.get() < self.sclow.get():
                self.sclow.set(self.scup.get() )
            if self.sclow.get() > self.scup.get():
                self.scup.set(self.sclow.get())

            up = self.scup.get()
            low = self.sclow.get()
            mx = self.mpl.mx
            mn = self.mpl.mn

            data = np.where(self.mpl.im_o > int(up), mx, self.mpl.im_o)
            data = np.where(data < int(low), mn, data)

            self.mpl.set_data(data)
            self.mpl._redraw()


if __name__ == '__main__':
    import matplotlib as mpl
    import scipy.misc as misc
    from tk3d_v04_mpl import MPL
    import matplotlib.pyplot as plt




    im = misc.face()
    mpl = MPL(im)

    master = tk.Tk()
    bt = CheckButtonScaleFrame(master, mpl)
    tk.mainloop()
