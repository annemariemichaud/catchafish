import streamlit as st
from skimage.io import imread,imsave
from skimage.transform import resize

#Display title
st.title('Catch a fish !')

#upload image to predict
uploaded_image = st.file_uploader("Choose image to predict")
if uploaded_image is not None:
	image = imread(uploaded_image)
	image = resize(image,(256,256))
	st.image(image)

#predict fish
if uploaded_image:
	st.markdown("This fish is a [golden fish](https://fr.wikipedia.org/wiki/Poisson-clown)")
	option = st.selectbox("choose the species",("","species1", "species2", "add"))
	if option == "species1" or option == "species2":
		imsave("images/test.jpg",image)
		st.write('thank you for your feebdack')
	elif option == "add":
		new = st.text_input("add new species")
		if new:
			st.write(f"thank you {new} been added")
			imsave("images/test.jpg",image)
			