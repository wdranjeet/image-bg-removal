import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import os

st.set_page_config(layout="wide", page_title="Image Background Removal App")
st.write("## Remove background from your images")
st.write(":dog: Try uploading an image to see the background magically removed. ")
st.sidebar.write("Upload and download :gear:")


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
col1, col2 = st.columns(2)

# Download the processed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_img = buf.getvalue()
    return byte_img

def process_uploaded_image(uploaded_img):
    image = Image.open(uploaded_img)
    col1.write("Original Image :camera:")
    col1.image(image)  # Display original image

    processed_img = remove(image)  # Remove background
    col2.write("Fixed Image :wrench:")
    col2.image(processed_img)  # Display processed image

    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download Fixed Image", convert_image(processed_img), "fixed.png", "image/png")

# File uploader logic
script_dir = os.path.dirname(__file__)
default_img_path = (script_dir+"/default-image.jpg")

my_upload_image = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if my_upload_image is not None:
    if my_upload_image.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        process_uploaded_image(my_upload_image)
else:
    if os.path.exists(default_img_path):
        process_uploaded_image(default_img_path)
    else:
        st.error("Default image file not found.")
