import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import numpy as np

st.set_page_config(page_title="QR & Barcode Scanner", layout="centered")
st.title("📱 QR & Barcode Scanner")

# Initialize session state for scan history
if "history" not in st.session_state:
    st.session_state.history = []

def decode_barcode(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    decoded_objects = decode(gray)
    results = []
    for obj in decoded_objects:
        results.append(f"{obj.type}: {obj.data.decode('utf-8')}")
    return results

# Camera input (works on Android browser)
st.subheader("Scan using Camera")
camera_input = st.camera_input("Point your camera at a QR code or Barcode")

if camera_input:
    img = Image.open(camera_input)
    results = decode_barcode(img)
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
    results = decode_barcode(img)
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
