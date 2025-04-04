# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Buttons frame.

    (C) MKocinski & AMaterka

    Created: 18.11.2017
    Modified: 01.12.2017
==================================================
"""
import nibabel as nib
import tkinter as tk
import numpy as np
import scipy.io as io
import time

from mk_add_path_dropbox import MK_DROPBOX_DANE


class ButtonsFrame(tk.Frame):
    def __init__(self, parent, mpl):
        tk.Frame.__init__(self, master=parent)

        # additional  instance variables
        self.mpl = mpl

        # Frame label
        self.label = tk.Label(self, text='Actions:')
        self.label.pack(side=tk.TOP, anchor=tk.NW)


        # Buttons & frames for them
        f0 = tk.Frame(master=self)
        open_button = tk.Button(master=self, bg='gray', text='Open Image', command=self._onOpen)
        open_button.pack(expand=1, fill=tk.X)
        f0.pack(expand=1, fill=tk.X)


        f1 = tk.Frame(master=self)
        reload_button = tk.Button(master=f1, text='Reload', command=self._onReload)
        reload_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        invert_button = tk.Button(master=f1, text='Invert', command=self._onInvert)
        invert_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        f1.pack(expand=1, fill=tk.BOTH)

        f2 = tk.Frame(master=self)
        info_button = tk.Button(master=f2, text='Info', command=self._onInfo)
        info_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        header_button = tk.Button(master=f2, text='Header', command=self._onHeader)
        header_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        f2.pack(expand=1, fill=tk.BOTH)

        f3 = tk.Frame(master=self)
        save_button = tk.Button(master=f3, text='Save', command=self._onSaveFile)
        save_button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        f3.pack(expand=1, fill=tk.BOTH)


        quit_button = tk.Button(master=self, text='Quit', bg='gray', command=self._onQuit)
        quit_button.pack(expand=1, fill=tk.X)

        self.pack(expand=1, fill=tk.X)

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

        fname = tk.filedialog.askopenfilename(**options)
        if fname:
            try:
                self.mpl.load_image(fname)
            except:                     # <- naked except is a bad idea
                print("Open Source File", "Failed to read file\n'%s'" % fname)
            return

    def _onSaveFile(self):
        options = {}
        #options['mode'] = 'wb'
        options['initialdir'] = MK_DROPBOX_DANE
        #options['defaultextension']=''
        options['filetypes'] = [('nifti', '.nii'),('nifti', '.nii.gz'), ('numpy','.npy'),('matlab','.mat')]
        options['initialfile'] = self.mpl.fname
        #options['parent'] = self.mpl.sdir
        f = tk.filedialog.asksaveasfile(**options)
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        print("********",f.name)
        if '.nii' in f.name:
            if self.mpl.hdr:
                hdr = self.mpl.hdr
                hdr['descrip'] = 'angio3d-nibabel-' + nib.__version__ + ' by MK ({})'.format(time.strftime("%Y-%m-%d"))
                img = nib.Nifti1Image(self.mpl.im, affine=self.mpl.nii.get_affine(), header=hdr)
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
            print("Nieobslugiwane rozszerzenie pliku do zapisu!")



if __name__ == '__main__':
    import matplotlib as mpl
    import scipy.misc as misc
    from tk3d_v04_mpl import MPL

    im = misc.face()
    mpl = MPL(im)

    root = tk.Tk()
    bt = ButtonsFrame(root,mpl)
    root.mainloop()
