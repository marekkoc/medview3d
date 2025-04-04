#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================================
    3D image viewer. Class responsible for image manipulation

    (C) MKocinski & AMaterka
    
    Created: 17.11.2017
    Modified: 17.11.2017
=================================================================
"""

class ImageInfo(object):
    def __init__(self,im):
        
        self.im = im.copy()
        self.mx = im.max()
        self.mn = im.min()
        self.sl = im.shape[-1]
        
        self.x, self.y, self.z = im.shape
        
    def info(self):
        print("  Brightness:")
        print("\tmax = %.2f" % self.mx)
        print('\tmin = %.2f' % self.mn)
        print('\tptp = %d' % self.im.ptp())
        print('  Type = %s' % self.im.dtype )
        
    def range2th(self):
        # Some image parameters & properties
        if self.mx <=1.0:
            self.rng2th = self.mx*1000
        elif self.mx <= 10.0:
            self.rng2th = self.mx * 100
        else:
            self.rng2th = self.mx
        return self.rng2th
        
    


