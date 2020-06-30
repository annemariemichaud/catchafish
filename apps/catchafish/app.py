import streamlit as st
from skimage.io import imread,imsave
from skimage.transform import resize
import wikipedia


#Display title
st.title('Catch a fish !')

#upload image to predict
uploaded_image = st.file_uploader("Choose image to predict")
if uploaded_image is not None:
	image = imread(uploaded_image)
	st.image(image)

#predict fish
if uploaded_image:
	st.markdown('This fish is a [gold fish](https://fr.wikipedia.org/wiki/Poisson-clown).')
	st.markdown(wikipedia.summary("goldfish",sentences=2))
			