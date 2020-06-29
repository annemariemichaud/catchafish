import streamlit as st
import os
import cv2 as cv
import matplotlib.pyplot as plt

st.title('Features detection with Fish !')


feature = st.selectbox('choose a feature',['SIFT','edge detection'])
from skimage.filters import prewitt_h
from skimage.io import imread
from skimage import filters
from skimage.transform import resize

path = '../../catchafish/data/train_data/fish_05/wpdim9cb.jpg'
img1 = cv.imread(path)


if feature == "SIFT" :

	#detection of keypoints
	img1 = cv.resize(img1, (256,256), interpolation = cv.INTER_AREA) 
	gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
	sift = cv.xfeatures2d.SIFT_create()
	keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
	img_1 = cv.drawKeypoints(gray1,keypoints_1,img1)
else:
	img1 = imread(path,as_gray=True)
	img1 = resize(img1,(256,256))
	img1 = filters.prewitt(img1)


st.image(img1)
 