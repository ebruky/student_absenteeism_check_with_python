# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 00:41:30 2020

@author: ebruk
"""
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt
import numpy as np
import cv2
import numpy as np
import math

def calculate_psnr(imageA, imageB):
    
    imageA = imageA.astype(np.float64)
    imageB = imageB.astype(np.float64)
    mse = np.mean((imageA - imageB)**2)
    if mse == 0:
        return inf
    return 20 * math.log10(255.0 / math.sqrt(mse))