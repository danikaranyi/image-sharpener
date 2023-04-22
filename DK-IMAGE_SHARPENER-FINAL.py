import streamlit as st
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os
import io

# ask for image in a slider
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg", "tiff", "bmp"])

# display the image with its original size
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

# add image sharpener option with an adjustable slider to the image in the st.sidebar
if st.sidebar.checkbox('Image Sharpener'):
    radius = st.sidebar.slider('Radius', 1, 20, step=2)
    amount = st.sidebar.slider('Amount', 0.0, 2.0, step=0.1)
    threshold = st.sidebar.slider('Threshold', 0, 60)

    # convert image to numpy array
    img_array = np.array(image.convert('RGB'))
    
    # apply unsharp masking
    blurred = cv2.GaussianBlur(img_array, (radius, radius), 0)
    unsharp_mask = cv2.addWeighted(img_array, 1 + amount, blurred, -amount, 0)
    sharpened = cv2.threshold(unsharp_mask, threshold, 255, cv2.THRESH_TOZERO)[1]
    
    # display the sharpened image
    st.image(sharpened, caption='Sharpened Image', use_column_width=True)

# add a download button to the sidebar
if st.sidebar.button('Download Processed Image'):
    # get the processed image as a PIL Image object
    if sharpened is not None:
        processed_image = Image.fromarray(sharpened)
    else:
        st.warning('Please select an image processing option.')
        processed_image = None
    
    # download the processed image
    if processed_image is not None:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext == '':
            file_ext = '.jpg'
        file_name = os.path.splitext(uploaded_file.name)[0] + '_processed' + file_ext
        bytes_buffer = io.BytesIO()
        processed_image.save(bytes_buffer, format=file_ext[1:].upper())
        st.download_button(label='Download Processed Image', data=bytes_buffer.getvalue(), file_name=file_name, mime='image/'+file_ext[1:])
