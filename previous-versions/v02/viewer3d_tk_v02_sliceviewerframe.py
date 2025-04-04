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


class SliceViewerFrame():
    def __init__(self, parent, checkName1='MIP', checkName2="mIP",
                 low=0, up=100, commandScale=None, commandSpin=None,
                 fexpand=True, fpos=None, commandMIP=None, commandmIP=None):

        self.frame = tk.Frame(master=parent, relief=tk.RIDGE, borderwidth=2)
        label = tk.Label(master=self.frame, text='Slice manipulation')
        label.pack(side=tk.TOP, anchor=tk.NW)
        # variable for scale
        self.scvar = tk.IntVar()
        self.sc = tk.Scale(master=self.frame, from_=low, to=up,
                           variable=self.scvar, command=commandScale,
                           orient=tk.HORIZONTAL)
        self.sc.pack(expand=True, fill=tk.X)
        if low >= 0:
            val = (up-low)//2
        else:
            val = (up+low)//2
        self.sc.set(val)

        # MIP
        self.mxvar = tk.BooleanVar()
        self.mxch = tk.Checkbutton(master=self.frame, text=checkName1,
                                   variable=self.mxvar, command=commandMIP)
        self.mxch.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.mxch.deselect()

        # spinbox
        self.rngvar = tk.StringVar()
        self.rngvar.set(str(10))
        self.rng = tk.Spinbox(master=self.frame, from_=1, to=100,
                              width=3, command=commandSpin,
                              textvariable=self.rngvar)
        self.rng.pack(side=tk.LEFT, fill=tk.X, expand=1)

        # mIP
        self.mnvar = tk.BooleanVar()
        self.mnch = tk.Checkbutton(master=self.frame, command=commandmIP,
                                   text=checkName2, variable=self.mnvar)
        self.mnch.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.mnch.deselect()

        self.frame.pack(side=tk.LEFT, expand=fexpand, anchor=tk.W, fill=tk.X)


if __name__ == '__main__':

    master = tk.Tk()
    bt = SliceViewerFrame(master)
    tk.mainloop()
