import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imshow
from skimage.color import rgb2gray, rgb2hsv
from skimage.morphology import area_opening
from skimage.exposure import histogram
from skimage.filters import threshold_otsu
from PIL import Image as im
import cv2 as cv
from tensorflow.keras.preprocessing import image


class Img_segmentation_thresholding_method:
    def segmentation(self, dir_path, file_name):
        img = imread(dir_path + file_name)
        
        kernel = np.ones((3,3), np.uint8)
        img = cv2.erode(img, kernel) 
        imshow(img)
        
        img_gray = rgb2gray(img) 
        thresh = threshold_otsu(img_gray) # Otsu’s method to find thresholding value
        img_otsu  = img_gray < thresh

        for x in range(0,len(img)):
            for y in range(0,len(img[x])):
                if img_otsu[x][y]:
                    img[x][y] = [255,255,255]
                else:
                    img[x][y] = [0,0,0]
        
        kernel = np.ones((6, 6), np.uint8)
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel) # Morphological closing to fill the holes
        new_file_name = 'seg_' + file_name
        im.fromarray(closing).save(new_file_name)
        
        imshow(closing)

        # Finding sure foreground area
        dist_transform = cv.distanceTransform(closing,cv.DIST_L2,5)
        ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv.subtract(sure_bg,sure_fg)

if __name__ == "__main__":
    dir_path = '~/Downloads/source/' 
    file_name = 'collage_1.jpeg'
    seg = Img_segmentation_thresholding_method()
    seg.segmentation(dir_path, file_name)
