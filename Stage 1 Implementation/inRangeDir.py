# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 12:37:14 2018

@author: win8.1
"""

import cv2
import numpy as np
import os
import csv
import sys

lowerBound=np.array([80,0,0])
upperBound=np.array([140,255,255])

'''cam= cv2.VideoCapture(0)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

font=cv2.FONT_HERSHEY_SIMPLEX
ret, img=cam.read()
img=cv2.resize(img,(340,220))
'''


images = sys.argv[1]
with open('percentage.csv', 'a') as csvFile:
    for image in os.listdir(images):
        image_name = image
        #print(image)
        #cv2.imshow(os.path.join(images,image))
        image = os.path.join(images,image)
        img = cv2.imread(image)
        img=cv2.resize(img,(340,220))
        imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(imgHSV,lowerBound,upperBound)
        ratio_blue = cv2.countNonZero(mask)/(img.size/3)
        percentage = np.round(ratio_blue*100, 2)
        print('water percentage:', percentage )
        row = [image_name , percentage]
        writer = csv.writer(csvFile)
        writer.writerow(row)
        cv2.imshow("Water bodies highlighted",mask)
        #cv2.imshow("Orginal image",img)
        cv2.waitKey(50)

csvFile.close()
