# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 21:28:19 2020

@author: ebruk
"""

import numpy as np

def calculate_mse(img1, img2):
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    mse = np.mean((img1 - img2)**2)
    return mse