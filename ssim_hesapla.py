# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 00:42:59 2020

@author: ebruk
"""

import numpy as np
from skimage import measure
import matplotlib.pyplot as plt
import numpy as np
import cv2
import numpy as np
import math


def calculate_ssim(imageA, imageB):
    s = measure.compare_ssim(imageA, imageB)
    return s    
    
    

