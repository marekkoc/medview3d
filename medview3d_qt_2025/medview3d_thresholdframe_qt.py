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
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QCheckBox, QSlider, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Any
import numpy as np


class CheckButtonScaleFrame(QFrame):
    def __init__(self, mpl):
        super().__init__()
        
        # Ustawienie stylu ramki
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        
        # additional instance variables
        self.mpl = mpl
        self.low = mpl.mn
        self.up = mpl.mx
        self.rangetoth = self._range2th()
        
        # Główny układ
        layout = QVBoxLayout(self)
        
        # Frame label
        self.label = QLabel('Thresholding')
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.label)
        
        # GLOBAL THRESHOLDING FRAME
        self.gthf = QFrame()
        gthf_layout = QHBoxLayout(self.gthf)
        
        # checkboks itself
        self.ch = QCheckBox("Single Th.")
        self.ch.setStyleSheet("font-size: 14px;")
        self.ch.clicked.connect(self._onCh1)
        gthf_layout.addWidget(self.ch)
        
        self.sc = QSlider(Qt.Horizontal)
        self.sc.setMinimum(int(self.low))
        self.sc.setMaximum(int(self.rangetoth))
        self.sc.setValue(self._setDefaultValue())
        self.sc.valueChanged.connect(self._onGThreshold)
        self.sc.setMinimumHeight(30)
        gthf_layout.addWidget(self.sc)
        
        layout.addWidget(self.gthf)
        
        # DOUBLE THRESHOLDING FRAME
        self.dthf = QFrame()
        dthf_layout = QHBoxLayout(self.dthf)
        
        self.ch2 = QCheckBox('Double Th.')
        self.ch2.setStyleSheet("font-size: 14px;")
        self.ch2.clicked.connect(self._onCh2)
        dthf_layout.addWidget(self.ch2)
        
        self.sclow = QSlider(Qt.Horizontal)
        self.sclow.setMinimum(int(self.low))
        self.sclow.setMaximum(int(self.rangetoth))
        self.sclow.setValue(int(self._setDefaultValue()*0.8))
        self.sclow.valueChanged.connect(self._onDThreshold)
        self.sclow.setMinimumHeight(30)
        dthf_layout.addWidget(self.sclow)
        
        self.scup = QSlider(Qt.Horizontal)
        self.scup.setMinimum(int(self.low))
        self.scup.setMaximum(int(self.rangetoth))
        self.scup.setValue(int(self._setDefaultValue()*1.2))
        self.scup.valueChanged.connect(self._onDThreshold)
        self.scup.setMinimumHeight(30)
        dthf_layout.addWidget(self.scup)
        
        layout.addWidget(self.dthf)

    def _updateAllProps(self):
        self.low = self.mpl.mn
        self.up = self.mpl.mx
        self.rangetoth = self._range2th()

        self.sc.setMinimum(int(self.low))
        self.sc.setMaximum(int(self.up * self.rangetoth))
        self.sclow.setMinimum(int(self.low))
        self.sclow.setMaximum(int(self.up * self.rangetoth))
        self.scup.setMinimum(int(self.low))
        self.scup.setMaximum(int(self.up * self.rangetoth))

        self.mpl.updatethresh = False

    def _onCh1(self):
        if self.ch.isChecked():
            self.ch2.setChecked(False)
        if self.mpl.updatethresh:
            self._updateAllProps()
        self._onGThreshold(self.sc.value())

    def _onCh2(self):
        if self.ch2.isChecked():
            self.ch.setChecked(False)
        if self.mpl.updatethresh:
            self._updateAllProps()
        self._onDThreshold(0)  # Wartość nie ma znaczenia, funkcja pobiera wartości z suwaków

    def _setDefaultValue(self):
        low, up = self.low, self.up
        if low >= 0:
            val = int((up-low)//2)
        else:
            val = int((up+low)//2)
        return val

    def _range2th(self):
        # Some image parameters & properties
        mx = self.mpl.mx
        self.rng2th = 1.0  # Inicjalizacja zmiennej
        if mx <= 1.0:
            self.rng2th = mx*1000
        elif mx <= 10.0:
            self.rng2th = mx*100
        else:
            self.rng2th = mx
        return self.rng2th

    def _onGThreshold(self, val):
        if self.ch.isChecked():
            # Konwertujemy wartość suwaka na właściwą wartość progową
            threshold = val / self.rangetoth
            
            # Tworzymy maskę binarną
            data = np.where(self.mpl.im_o >= threshold, self.mpl.mx, self.mpl.mn)
            
            # Aktualizujemy dane i wymuszamy przerysowanie
            self.mpl.set_data(data)
            self.mpl._redraw()  # Używamy _redraw() zamiast draw()

    def _onDThreshold(self, val):
        if self.ch2.isChecked():
            if self.scup.value() < self.sclow.value():
                self.sclow.setValue(self.scup.value())
            if self.sclow.value() > self.scup.value():
                self.scup.setValue(self.sclow.value())

            up = self.scup.value()
            low = self.sclow.value()
            mx = self.mpl.mx
            mn = self.mpl.mn

            data = np.where(self.mpl.im_o > int(up), mx, self.mpl.im_o)
            data = np.where(data < int(low), mn, data)

            self.mpl.set_data(data)
            self.mpl._redraw() 