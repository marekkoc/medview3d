#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================================
    3D image viewer. Class responsible for image manipulation

    (C) MKocinski & AMaterka
    
    Created: 17.11.2017
    Modified: 04.04.2025
=================================================================
"""

class ImageInfo(object):
    def __init__(self,im):
        
        self.im = im
        self.mx = im.max()
        self.mn = im.min()
        self.av = im.mean()
        self.sl = im.shape[-1]
        
        self.x, self.y, self.z = im.shape
        
    def info(self):
        print("  Brightness:")
        print("\tmax = %.2f" % self.mx)
        print('\tmin = %.2f' % self.mn)
        print('\tptp = %d' % self.im.ptp())
        print('  Type = %s' % self.im.dtype )
        
    def shape(self):
        return self.im.shape
        

        
    


