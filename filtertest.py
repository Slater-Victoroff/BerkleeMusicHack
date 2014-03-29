# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 20:17:08 2014

@author: jwei
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('''insert image here''')

blur = cv2.blur(img,(21,21)) #uses normalized box filter  -> adjust #s to change blurriness
bilat = cv2.bilateralFilter(img,9,75,75)

#Plotting the three plots to compare
plt.subplot(2,2,1),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([]) #gets rid of all the tickmarks
plt.subplot(2,2,2),plt.imshow(bilat),plt.title('Bilateral')
plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(blur),plt.title('Blurred')
plt.xticks([]), plt.yticks([])
plt.show()