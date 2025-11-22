import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="QR & Barcode Scanner", layout="centered")
st.title("📱 QR & Barcode Scanner")

# Initialize session state for scan history
if "history" not in st.session_state:
    st.session_state.history = []

def decode_qr(image):
    """
    Decode QR codes using OpenCV
    """
    qr_detector = cv2.QRCodeDetector()
    data, points, _ = qr_detector.detectAndDecode(image)
    if data:
        return [f"QR Code: {data}"]
    return []

def decode_barcode(image):
    """
    Decode 1D barcodes using OpenCV contours + thresholding
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    barcodes = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 50 and h > 10:  # Filter out small noise
            barcode_roi = gray[y:y+h, x:x+w]
            barcode_data = cv2.mean(barcode_roi)[0]
            barcodes.append(f"Barcode detected at x:{x}, y:{y}, w:{w}, h:{h}")
    return barcodes

def process_image(pil_image):
    # Convert PIL to OpenCV BGR
    cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    results = decode_qr(cv_image)
    results += decode_barcode(cv_image)
    return results

# Camera input (works on Android)
st.subheader("Scan using Camera")
camera_input = st.camera_input("Point your camera at a QR code or Barcode")

if camera_input:
    img = Image.open(camera_input)
    results = process_image(img)
    if results:
        for res in results:
            st.success(res)
            st.session_state.history.append(res)
    else:
        st.warning("No QR code or Barcode detected.")

# Image upload alternative
st.subheader("Or Upload an Image")
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    results = process_image(img)
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
