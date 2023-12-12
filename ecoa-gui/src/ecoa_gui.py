#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from ecoa_app import create_window, ECOA_Application


if __name__=='__main__':
    root = Tk()
    #root.withdraw()
    # Creation of the main window
    img_path = r'../images/ECOA_Win.png'
    ecoa_icon_img = ImageTk.PhotoImage(Image.open(img_path))
    create_window(root, "ECOA Tools Launcher", ecoa_icon_img, 900, 550)
    
    # Creation of the content of the app
    ECOA_Application(root)
    
    root.mainloop()
