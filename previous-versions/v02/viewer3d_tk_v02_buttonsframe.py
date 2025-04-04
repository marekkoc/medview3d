# -*- coding: utf-8 -*-
"""
==================================================
    3D image viewer. Buttons frame.

    (C) MKocinski & AMaterka

    Created: 18.11.2017
    Modified: 18.11.2017
==================================================
"""
import tkinter as tk

class ButtonsFrame(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, master=parent)
        self.grid()


        self.label = tk.Label(self, text='Actions:')
        self.label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        # Buttons & frame for them

        invert_button = tk.Button(master=self, text='Invert')
        invert_button.grid(row=1, column=0, padx=1, pady=1, sticky=tk.W+tk.E)

        reload_button = tk.Button(master=self, text='Reload')
        reload_button.grid(row=1, column=1, padx=1, pady=1, sticky=tk.W+tk.E)

        cluster_button = tk.Button(master=self, text='Cluster', state=tk.DISABLED)
        cluster_button.grid(row=2, column=0, padx=1, pady=1, sticky=tk.W+tk.E)

        snake_button = tk.Button(master=self, text='Snake', state=tk.DISABLED)
        snake_button.grid(row=2, column=1, padx=1, pady=1, sticky=tk.W+tk.E)

        seed_button = tk.Button(master=self, text='Grow', state=tk.DISABLED)
        seed_button.grid(row=3, column=0, padx=1, pady=1, sticky=tk.W+tk.E)

        save_button = tk.Button(master=self, text='Save to Nifti', state=tk.DISABLED)
        save_button.grid(row=3, column=1, padx=1, pady=1, sticky=tk.W+tk.E)

        quit_button = tk.Button(master=self, text='Quit', bg='gray')
        quit_button.grid(row=4, column=0, columnspan=2, padx=1, pady=1, sticky=tk.W+tk.E)



if __name__ == '__main__':
    root = tk.Tk()
    app = ButtonsFrame()
    root.mainloop()
