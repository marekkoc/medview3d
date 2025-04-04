#!/usr/bin/env python3
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
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFileDialog, QFrame)
from PyQt5.QtCore import Qt, QCoreApplication
import numpy as np
import scipy.io as io
import time
import os

#from mk_add_path_dropbox import MK_DROPBOX_DANE
MK_DROPBOX_DANE = '../dane'


class ButtonsFrame(QFrame):
    def __init__(self, mpl):
        super().__init__()
        
        # Ustawienie stylu ramki
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        
        # additional instance variables
        self.mpl = mpl
        
        # Główny układ
        layout = QVBoxLayout(self)
        
        # Frame label
        self.label = QLabel('Actions:')
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.label)
        
        # Open Image button
        open_button = QPushButton('Open Image')
        open_button.setStyleSheet("background-color: lightgray; font-size: 14px;")
        open_button.setMinimumHeight(50)
        open_button.clicked.connect(self._onOpen)
        layout.addWidget(open_button)
        
        # Reload & Invert buttons
        f1_layout = QHBoxLayout()
        reload_button = QPushButton('Reload')
        reload_button.setStyleSheet("font-size: 14px;")
        reload_button.setMinimumHeight(50)
        reload_button.clicked.connect(self._onReload)
        f1_layout.addWidget(reload_button)
        
        invert_button = QPushButton('Invert')
        invert_button.setStyleSheet("font-size: 14px;")
        invert_button.clicked.connect(self._onInvert)
        f1_layout.addWidget(invert_button)
        layout.addLayout(f1_layout)
        
        # Info & Header buttons
        f2_layout = QHBoxLayout()
        info_button = QPushButton('Info')
        info_button.setStyleSheet("font-size: 14px;")
        info_button.clicked.connect(self._onInfo)
        f2_layout.addWidget(info_button)
        
        header_button = QPushButton('Header')
        header_button.setStyleSheet("font-size: 14px;")
        header_button.clicked.connect(self._onHeader)
        f2_layout.addWidget(header_button)
        layout.addLayout(f2_layout)
        
        # Save button
        save_button = QPushButton('Save')
        save_button.setStyleSheet("font-size: 14px;")
        save_button.clicked.connect(self._onSaveFile)
        layout.addWidget(save_button)
        
        # Quit button
        quit_button = QPushButton('Quit')
        quit_button.setStyleSheet("background-color: lightgray; font-size: 14px;")
        quit_button.clicked.connect(self._onQuit)
        layout.addWidget(quit_button)

    def _onQuit(self):
        QCoreApplication.instance().quit()

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
        options = QFileDialog.Options()
        file_filter = "Nifti Files (*.nii *.nii.gz);;Numpy Files (*.npy);;Matlab Files (*.mat);;All Files (*)"
        fname, _ = QFileDialog.getOpenFileName(
            None, "Open Image File", MK_DROPBOX_DANE, file_filter, options=options
        )
        
        if fname:
            try:
                self.mpl.load_image(fname)
            except Exception as e:
                print("Open Source File", f"Failed to read file\n'{fname}'")
                print(f"Error: {e}")
            return

    def _onSaveFile(self):
        options = QFileDialog.Options()
        file_filter = "Nifti Files (*.nii *.nii.gz);;Numpy Files (*.npy);;Matlab Files (*.mat);;All Files (*)"
        fname, _ = QFileDialog.getSaveFileName(
            None, "Save Image File", os.path.join(MK_DROPBOX_DANE, self.mpl.fname),
            file_filter, options=options
        )
        
        if not fname:
            return
        
        print("********", fname)
        try:
            if '.nii' in fname:
                if self.mpl.hdr:
                    hdr = self.mpl.hdr
                    hdr['descrip'] = 'angio3d-nibabel-' + nib.__version__ + ' by MK ({})'.format(time.strftime("%Y-%m-%d"))
                    img = nib.Nifti1Image(self.mpl.im, affine=self.mpl.nii.affine, header=hdr)
                else:
                    hdr = nib.Nifti1Header()
                    hdr['descrip'] = 'angio3d-nibabel-' + nib.__version__ + ' by MK ({})'.format(time.strftime("%Y-%m-%d"))
                    img = nib.Nifti1Image(self.mpl.im, affine=np.eye(4), header=hdr)
                img.set_data_dtype(self.mpl.im.dtype.name)
                img.to_filename(fname)
            elif fname.endswith('.npy'):
                np.save(fname, self.mpl.im)
            elif fname.endswith('.mat'):
                io.savemat(fname, {'im':self.mpl.im})
            else:
                print("Nieobsługiwane rozszerzenie pliku do zapisu!")
        except Exception as e:
            print(f"Błąd podczas zapisywania pliku: {e}") 