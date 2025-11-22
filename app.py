import streamlit as st
from PIL import Image
import numpy as np
import cv2
from pyzxing import BarCodeReader

st.set_page_config(page_title="QR & Barcode Scanner", layout="centered")
st.title("📱 QR & Barcode Scanner")

# Initialize session state for scan history
if "history" not in st.session_state:
    st.session_state.history = []

# Initialize ZXing reader
reader = BarCodeReader()

def decode_image_with_zxing(image):
    # Save uploaded PIL image temporarily
    temp_file = "temp_image.png"
    image.save(temp_file)
    results = reader.decode(temp_file)
    decoded_list = []
    if results:
        for r in results:
            if r.get("raw") and r.get("format"):
                decoded_list.append(f"{r['format']}: {r['raw']}")
    return decoded_list

# Camera input (works on Android browser)
st.subheader("Scan using Camera")
camera_input = st.camera_input("Point your camera at a QR code or Barcode")

if camera_input:
    img = Image.open(camera_input)
    results = decode_image_with_zxing(img)
    if results:
        for res in results:
            st.success(res)
            st.session_state.history.append(res)
    else:
        st.warning("No QR code or Barcode detected.")

# Image upload as alternative
st.subheader("Or Upload an Image")
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    results = decode_image_with_zxing(img)
    if results:
        for res in results:
            st.success(res)
            st.session_state.history.append(res)
    else:
        st.warning("No QR code or Barcode detected.")

# Display scan history
st.subheader("📜 Scan History")
if st.session_state.history:
    for i, item in enumerate(st.session_state.history[::-1], 1):
        st.write(f"{i}. {item}")
else:
    st.info("No scans yet.")
