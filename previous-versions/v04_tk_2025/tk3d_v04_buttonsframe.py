# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Buttons frame.

    (C) MKocinski & AMaterka

    Created: 18.11.2017
    Modified: 04.04.2025
==================================================
"""
import nibabel as nib
import tkinter as tk
from tkinter import filedialog  # Dodane jawne importowanie filedialog
import numpy as np
import scipy.io as io
import time
import os

#from mk_add_path_dropbox import MK_DROPBOX_DANE
MK_DROPBOX_DANE = '../dane'


class ButtonsFrame(tk.Frame):
    def __init__(self, parent, mpl):
        tk.Frame.__init__(self, master=parent)

        # additional  instance variables
        self.mpl = mpl

        # Frame label z większą czcionką
        self.label = tk.Label(self, text='Actions:', font=('TkDefaultFont', 16))
        self.label.pack(side=tk.TOP, anchor=tk.NW)


        # Buttons & frames for them - wszystkie z większą czcionką
        f0 = tk.Frame(master=self)
        open_button = tk.Button(master=self, bg='gray', text='Open Image', command=self._onOpen, height=2, width=15, font=('TkDefaultFont', 14))
        open_button.pack(expand=1, fill=tk.X)
        f0.pack(expand=1, fill=tk.X)


        f1 = tk.Frame(master=self)
        reload_button = tk.Button(master=f1, text='Reload', command=self._onReload, height=2, width=15, font=('TkDefaultFont', 14))
        reload_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        invert_button = tk.Button(master=f1, text='Invert', command=self._onInvert, font=('TkDefaultFont', 14))
        invert_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        f1.pack(expand=1, fill=tk.BOTH)

        f2 = tk.Frame(master=self)
        info_button = tk.Button(master=f2, text='Info', command=self._onInfo, font=('TkDefaultFont', 14))
        info_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        header_button = tk.Button(master=f2, text='Header', command=self._onHeader, font=('TkDefaultFont', 14))
        header_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        f2.pack(expand=1, fill=tk.BOTH)

        f3 = tk.Frame(master=self)
        save_button = tk.Button(master=f3, text='Save', command=self._onSaveFile, font=('TkDefaultFont', 14))
        save_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        f3.pack(expand=1, fill=tk.BOTH)


        quit_button = tk.Button(master=self, text='Quit', bg='gray', command=self._onQuit, font=('TkDefaultFont', 14))
        quit_button.pack(expand=1, fill=tk.X)

    def _onQuit(self):
        self.master.quit()      # stops mainloop
        self.master.destroy()   # this is necessary on Windows to prevent
                                # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _onInvert(self):
        self.mpl.set_data(self.mpl.mx - self.mpl.im)
        self.mpl._redraw()

    def _onReload(self):
        self.mpl._reload_image()

    def _onHeader(self):
        if self.mpl.hdr:
            print(50*'*')
            print(self.mpl.hdr)
            print(50*'*')
        else:
            print('There is no header!')
            
    def _onInfo(self):
        self.mpl.info()

    def _onOpen(self):
        options = {}
        options['initialdir'] = MK_DROPBOX_DANE
        options['defaultextension']='.nii.gz'
        options['filetypes'] = [('nifti', '.nii'),('nifti', '.nii.gz'), ('numpy','.npy'),('matlab','.mat')]

        fname = filedialog.askopenfilename(**options)
        if fname:
            try:
                self.mpl.load_image(fname)
            except Exception as e:
                print("Open Source File", f"Failed to read file\n'{fname}'")
                print(f"Error: {e}")
            return

    def _onSaveFile(self):
        options = {}
        options['initialdir'] = MK_DROPBOX_DANE
        options['filetypes'] = [('nifti', '.nii'),('nifti', '.nii.gz'), ('numpy','.npy'),('matlab','.mat')]
        options['initialfile'] = self.mpl.fname
        
        f = filedialog.asksaveasfile(**options)
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        
        print("********", f.name)
        try:
            if '.nii' in f.name:
                if self.mpl.hdr:
                    hdr = self.mpl.hdr
                    hdr['descrip'] = 'angio3d-nibabel-' + nib.__version__ + ' by MK ({})'.format(time.strftime("%Y-%m-%d"))
                    img = nib.Nifti1Image(self.mpl.im, affine=self.mpl.nii.affine, header=hdr)
                else:
                    hdr = nib.Nifti1Header()
                    hdr['descrip'] = 'angio3d-nibabel-' + nib.__version__ + ' by MK ({})'.format(time.strftime("%Y-%m-%d"))
                    img = nib.Nifti1Image(self.mpl.im, affine=np.eye(4), header=hdr)
                img.set_data_dtype(self.mpl.im.dtype.name)
                img.to_filename(f.name)
            elif f.name.endswith('.npy'):
                np.save(f.name, self.mpl.im)
            elif f.name.endswith('.mat'):
                io.savemat(f.name, {'im':self.mpl.im})
            else:
                print("Nieobsługiwane rozszerzenie pliku do zapisu!")
        except Exception as e:
            print(f"Błąd podczas zapisywania pliku: {e}")
