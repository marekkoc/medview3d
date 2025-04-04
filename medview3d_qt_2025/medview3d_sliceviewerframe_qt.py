#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Slice Viewer Frame

    (C) MKocinski & AMaterka

    Created: 17.11.2017
    Modified: 04.04.2025
==================================================
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QCheckBox, QSlider, QFrame, QSpinBox)
from PyQt5.QtCore import Qt
import numpy as np


class SliceViewerFrame(QFrame):
    def __init__(self, mpl):
        super().__init__()
        
        # Ustawienie stylu ramki
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        
        # additional instance variable
        self.mpl = mpl
        self.low = 0
        self.up = mpl.sl-1
        
        # Główny układ
        layout = QVBoxLayout(self)
        
        # label
        label = QLabel('Slice manipulation')
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)
        
        # Slider dla przekrojów
        self.sc = QSlider(Qt.Horizontal)
        self.sc.setMinimum(self.low)
        self.sc.setMaximum(self.up)
        self.sc.setValue((self.up+self.low)//2)
        self.sc.valueChanged.connect(self._onSliceChange)
        self.sc.setMinimumHeight(30)
        layout.addWidget(self.sc)
        
        # Układ dla MIP, spinbox i mIP
        controls_layout = QHBoxLayout()
        
        # MIP
        self.mxch = QCheckBox('MIP')
        self.mxch.setStyleSheet("font-size: 14px;")
        self.mxch.clicked.connect(self._onMIP)
        controls_layout.addWidget(self.mxch)
        
        # spinbox
        self.rng = QSpinBox()
        self.rng.setMinimum(1)
        self.rng.setMaximum(100)
        self.rng.setValue(10)
        self.rng.valueChanged.connect(self._onMipRange)
        self.rng.setStyleSheet("font-size: 14px;")
        controls_layout.addWidget(self.rng)
        
        # mIP
        self.mnch = QCheckBox('mIP')
        self.mnch.setStyleSheet("font-size: 14px;")
        self.mnch.clicked.connect(self._onmIP)
        controls_layout.addWidget(self.mnch)
        
        layout.addLayout(controls_layout)

    def _onSliceChange(self, val):
        """Callback dla zmiany przekroju"""
        self.mpl.set_slice(int(val))
        self.mpl._redraw()
        
    def _onMIP(self):
        """Callback dla włączenia/wyłączenia MIP"""
        if self.mxch.isChecked():
            self.mnch.setChecked(False)
            self.mpl.rn = self.rng.value()
            self.mpl._redraw_mip('MIP')
        else:
            self.mpl._redraw()
            
    def _onmIP(self):
        """Callback dla włączenia/wyłączenia mIP"""
        if self.mnch.isChecked():
            self.mxch.setChecked(False)
            self.mpl.rn = self.rng.value()
            self.mpl._redraw_mip('mIP')
        else:
            self.mpl._redraw()
            
    def _onMipRange(self):
        """Callback dla zmiany zakresu MIP/mIP"""
        try:
            self.mpl.rn = self.rng.value()
            if self.mxch.isChecked():
                self.mpl._redraw_mip('MIP')
            elif self.mnch.isChecked():
                self.mpl._redraw_mip('mIP')
        except ValueError:
            pass
            
    def get_slice(self):
        """Zwraca aktualny numer przekroju"""
        return self.sc.value()
        
    def set_slice(self, val):
        """Ustawia numer przekroju"""
        val = max(self.low, min(self.up, val))
        self.sc.setValue(val) 