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
    if prediction.startswith(('A', 'E', 'I', 'O', 'U')):
        st.markdown(f'This fish is an {prediction}.')
    else:
        st.markdown(f'This fish is a {prediction}.')
    st.markdown(wikipedia.summary(prediction,sentences=1))
