#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Threshold frame.

    (C) MKocinski & AMaterka

    Created: 17.11.2017
    Modified: 18.11.2017
==================================================
"""
import tkinter as tk


class CheckButtonScaleFrame():
    def __init__(self, parent, checkName='Enable', low=0, up=100, command=None,
                 fexpand=True, fpos=None):

        self.frame = tk.Frame(master=parent, relief=tk.RIDGE, borderwidth=2, width=300)
        label = tk.Label(master=self.frame, text='Thresholding')
        label.pack(side=tk.TOP,anchor=tk.NW)
        # variable for checkbox
        self.var = tk.BooleanVar()
        # checkboks itself
        self.ch = tk.Checkbutton(master=self.frame, text=checkName, variable=self.var)
        self.ch.pack(expand=0,side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        self.ch.deselect()

        self.sc = tk.Scale(master=self.frame,from_=low, to=up,
                                           command=command, orient=tk.HORIZONTAL)
        self.sc.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        if low >=0:
            val = (up-low)//2
        else:
            val = (up+low)//2
        self.sc.set(val)


        self.frame.pack(side=fpos, expand=fexpand, anchor=tk.W, fill=tk.BOTH)


if __name__ == '__main__':
    master = tk.Tk()
    bt = CheckButtonScaleFrame(master)
    tk.mainloop()

