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
import scipy.io as io
import nibabel as nib
import matplotlib as mpl
import numpy as np

class MPL(object):
    def __init__(self,img):


        if isinstance(img, np.ndarray):
            self.im = img
            self.hdr = None
            self.nii = None
        elif isinstance(img, nib.nifti1.Nifti1Image):
            self.nii = img
            self.im = img.get_data()
            self.hdr = img.get_header()
        else:
            print('Wrong data faormat-(constructor of the MPL class)')
            return

        self._update_img_params()

        self.fig = mpl.figure.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.axdata = self.ax.imshow(self.im[:, :, self.sl//2],
                                     cmap='gray', aspect='equal',
                                     vmin=self.mn, vmax=self.mx)
        self.ax.axis('off')

        # Wartosci progow w progowaniu
        self.globth = 0
        self.lowth = 0
        self.uppth = 0

        # aktualna pozycja suwaka
        self.slice = 0

        # aktualna liczba przekrojow MIP/mIP
        self.rn = 1

        # zmienne zwiazane ze sciezkami
        self.fname = ''
        self.wdir = ''

        # dodatkowa flaga do aktualizacji parametrow w inncyh oknach
        self.updatethresh = False
        self.updateslicer = False


    def _update_img_params(self):

        self.im_o = self.im.copy()
        self.mx = self.im.max()
        self.mn = self.im.min()
        self.av = self.im.mean()
        self.sl = self.im.shape[-1]
        self.x, self.y, self.z = self.im.shape

    def info(self):
        print("  Brightness:")
        print("\tmax = %.2f" % self.mx)
        print('\tmin = %.2f' % self.mn)
        print('\tptp = %d' % self.im.ptp())
        print('  Type = %s' % self.im.dtype )

    def load_image(self, fname):

        if '.nii' in fname:
            self.nii = nib.load(fname)
            self.im = self.nii.get_data()
            self.hdr = self.nii.get_header()
        elif fname.endswith('.npy'):
            self.im = np.load(fname)
            self.hdr = None
            self.nii = None
        elif fname.endswith('.mat'):
            self.im = io.load(fname)['im']
            self.hdr = None
            self.nii = None
        else:
            print("Nieobslugiwane rozszerzenie pliku do odczytu!")

        self._update_img_params()

        self.updatethresh = True
        self.updateslicer = True
        self.axdata = self.ax.imshow(self.im[:, :, self.sl//2],
                                     cmap='gray', aspect='equal',
                                     vmin=self.mn, vmax=self.mx)

        self.slice = self.sl // 2
        self._redraw()

    def set_filename(self,filename):
        if 'nii' in filename:
            filename = filename.split('.nii')[0]
        self.fname = filename

    def set_workdir(self,savedir):
        self.wdir = savedir

    def shape(self):
        return self.im.shape

    def set_data(self,img):
        self.im = img

    def set_slice(self,sl):
        self.slice = sl

    def _reload_image(self):
        self.im = self.im_o.copy()
        self._redraw()

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



