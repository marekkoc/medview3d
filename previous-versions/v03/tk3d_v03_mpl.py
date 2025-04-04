#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================================
    3D image viewer. Class responsible Matplotlib figure
    and image manipulation.

    (C) MKocinski & AMaterka

    Created: 27.11.2017
    Modified: 27.11.2017
=================================================================
"""

import matplotlib as mpl
import numpy as np

class MPL(object):
    def __init__(self,im):

        self.im = im
        self.im_o = im.copy()
        self.mx = im.max()
        self.mn = im.min()
        self.av = im.mean()
        self.sl = im.shape[-1]

        self.x, self.y, self.z = im.shape

        self.fig = mpl.figure.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.axdata = self.ax.imshow(self.im[:, :, self.sl//2], cmap='gray', aspect='equal')
        self.ax.axis('off')

        # Wartosci progow w progowaniu
        self.globth = 0
        self.lowth = 0
        self.uppth = 0

        # aktualna pozycja suwaka
        self.slice = 0
        
        # aktualna liczba przekrojow MIP/mIP 
        self.rn = 1

    def info(self):
        print("  Brightness:")
        print("\tmax = %.2f" % self.mx)
        print('\tmin = %.2f' % self.mn)
        print('\tptp = %d' % self.im.ptp())
        print('  Type = %s' % self.im.dtype )

    def shape(self):
        return self.im.shape

    def set_data(self,img):
        self.im = img

    def set_slice(self,sl):
        self.slice = sl

    def _redraw(self):        
        self.axdata.set_data(self.im[:, :, self.slice])
        self.fig.canvas.draw()
        
    def _redraw_mip(self, typ):
        
        rn = self.rn
        cur = self.slice
        r = np.array([cur-rn, cur+rn]).clip(0, self.sl)
        
        if typ == 'MIP':
            self.axdata.set_data(self.im[:, :, r[0]:r[1]].max(2))
        elif typ =='mIP':
            self.axdata.set_data(self.im[:, :, r[0]:r[1]].min(2))
        else:
            print('Zla flaga. Funkcja MPL::_redraw_mip()')
    
        self.fig.canvas.draw()
        
        

