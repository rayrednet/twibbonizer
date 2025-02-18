import streamlit as st
from PIL import Image
import os
from helpers import process_images

# Set app name and favicon
st.set_page_config(
    page_title="Twibbonizer",
    page_icon="favicon.png",
)

# Streamlit UI
st.title("🖼️ Twibbonizer")
st.write(
    "Easily add a **twibbon** and **watermark** to multiple images at once! "
    "Upload your product images, select your templates, and adjust settings before downloading the processed images."
)
st.warning("⚠️ **Note:** Twibbon and Watermark must have a transparent background (PNG format).")
st.info("ℹ️ Watermark is optional! You can leave it empty if you don't want to apply one.")

# Upload Twibbon & Watermark
st.sidebar.header("📌 Upload Templates")
twibbon = st.sidebar.file_uploader("Upload Twibbon (PNG, Required)", type=["png"])
watermark = st.sidebar.file_uploader("Upload Watermark (PNG, Optional)", type=["png"])

# Upload Images
st.sidebar.header("📌 Upload Product Images")
uploaded_images = st.sidebar.file_uploader("Upload Images (JPG, PNG, WEBP)", type=["jpg", "png", "webp"], accept_multiple_files=True)

# Image Size Settings
st.sidebar.header("📌 Output Image Settings")
image_mode = st.sidebar.radio("Choose Image Mode", ["Square", "Keep Original Aspect Ratio"])

custom_width = None
custom_height = None

# Square Mode - Allow custom resolution
if image_mode == "Square":
    square_size = st.sidebar.number_input("Square Resolution (px)", min_value=512, max_value=4096, value=1080, step=128)
    output_size = (square_size, square_size)
else:
    # Keep Original Aspect Ratio - Let user input max width & height
    custom_width = st.sidebar.number_input("Max Width (px)", min_value=512, max_value=4096, value=1080, step=128)
    custom_height = st.sidebar.number_input("Max Height (px)", min_value=512, max_value=4096, value=1080, step=128)
    output_size = (custom_width, custom_height)

# Watermark Opacity (Only if watermark is uploaded)
watermark_opacity = st.sidebar.slider("Watermark Opacity (%)", min_value=10, max_value=100, value=70) / 100 if watermark else None

# Process Button
if st.sidebar.button("🚀 Process Images"):
    if not uploaded_images or not twibbon:
        st.error("⚠️ Please upload at least one image and a twibbon!")
    else:
        # Convert uploaded files to PIL images
        twibbon_img = Image.open(twibbon)
        watermark_img = Image.open(watermark) if watermark else None  # If no watermark, pass None

        # Process images
        result_path = process_images(uploaded_images, twibbon_img, watermark_img, output_size, watermark_opacity)

        # If only one image, provide direct PNG download
        if result_path.endswith(".png"):
            with open(result_path, "rb") as f:
                st.success("✅ Processing Complete! Download your image below.")
                st.download_button("📥 Download Image", f, file_name=os.path.basename(result_path), mime="image/png")

        # If multiple images, provide ZIP download
        else:
            with open(result_path, "rb") as f:
                st.success("✅ Processing Complete! Download your ZIP file below.")
                st.download_button("📥 Download Processed Images", f, file_name="processed_images.zip", mime="application/zip")
