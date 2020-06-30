import streamlit as st
from skimage.io import imread,imsave
from skimage.transform import resize
import wikipedia

from catchafish.trainer import Trainer

#Display title
st.title('Catch a fish !')

#upload image to predict
uploaded_image = st.file_uploader("Choose image to predict")
if uploaded_image is not None:
    image = imread(uploaded_image)
    st.image(image)
    image = resize(image, (128, 128))

#predict fish
if uploaded_image:
    trainer = Trainer()
    prediction = trainer.predict(image)
    st.markdown(f'{prediction}')
    st.markdown('This fish is a [gold fish](https://fr.wikipedia.org/wiki/Poisson-clown).')
    st.markdown(wikipedia.summary("goldfish",sentences=2))
