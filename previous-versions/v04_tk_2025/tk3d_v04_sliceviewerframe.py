#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Button Frame 1

    (C) MKocinski & AMaterka

    Created: 17.11.2017
    Modified: 04.04.2025
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

        # label z większą czcionką
        label = tk.Label(master=self, text='Slice manipulation', font=('TkDefaultFont', 16))
        label.pack(side=tk.TOP, anchor=tk.NW)

        # variable for scale
        self.scvar = tk.IntVar()
        self.sc = tk.Scale(master=self, from_=self.low, to=self.up,
                           variable=self.scvar, command=self._onSliceChange,
                           orient=tk.HORIZONTAL, length=300, width=30,  # Zwiększona szerokość
                           font=('TkDefaultFont', 14))  # Dodana czcionka
        self.sc.pack(expand=True, fill=tk.X)
        self.sc.set((self.up+self.low)//2)

        # MIP z większą czcionką
        self.mxvar = tk.BooleanVar()
        self.mxch = tk.Checkbutton(master=self, text='MIP',
                                   variable=self.mxvar, command=self._onMIP,
                                   font=('TkDefaultFont', 14))  # Dodana czcionka
        self.mxch.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.mxch.deselect()

        # spinbox z większą czcionką
        self.rngvar = tk.StringVar()
        self.rngvar.set(str(10))
        self.rng = tk.Spinbox(master=self, from_=1, to=100,
                              width=5, command=self._onMipRange,
                              textvariable=self.rngvar, font=('TkDefaultFont', 14))  # Zwiększona czcionka
        self.rng.pack(side=tk.LEFT, fill=tk.X, expand=1)

        # mIP z większą czcionką
        self.mnvar = tk.BooleanVar()
        self.mnch = tk.Checkbutton(master=self, command=self._onmIP,
                                   text='mIP', variable=self.mnvar,
                                   font=('TkDefaultFont', 14))  # Dodana czcionka
        self.mnch.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.mnch.deselect()

    def _onSliceChange(self, val):
        """Callback dla zmiany przekroju"""
        self.mpl.set_slice(int(val))
        self.mpl._redraw()
        
    def _onMIP(self):
        """Callback dla włączenia/wyłączenia MIP"""
        if self.mxvar.get():
            self.mnch.deselect()
            self.mpl.rn = int(self.rngvar.get())
            self.mpl._redraw_mip('MIP')
        else:
            self.mpl._redraw()
            
    def _onmIP(self):
        """Callback dla włączenia/wyłączenia mIP"""
        if self.mnvar.get():
            self.mxch.deselect()
            self.mpl.rn = int(self.rngvar.get())
            self.mpl._redraw_mip('mIP')
        else:
            self.mpl._redraw()
            
    def _onMipRange(self):
        """Callback dla zmiany zakresu MIP/mIP"""
        try:
            self.mpl.rn = int(self.rngvar.get())
            if self.mxvar.get():
                self.mpl._redraw_mip('MIP')
            elif self.mnvar.get():
                self.mpl._redraw_mip('mIP')
        except ValueError:
            pass
            
    def get_slice(self):
        """Zwraca aktualny numer przekroju"""
        return self.scvar.get()
        
    def set_slice(self, val):
        """Ustawia numer przekroju"""
        val = max(self.low, min(self.up, val))
        self.sc.set(val)
