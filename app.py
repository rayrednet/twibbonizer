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

# **Helper Function for File Upload with Preview**
def file_uploader_with_preview(label, file_types, key, multiple=False):
    """Creates a file uploader with an inline preview after upload."""
    uploaded_files = st.sidebar.file_uploader(label, type=file_types, key=key, accept_multiple_files=multiple)

    if uploaded_files:
        if multiple:
            st.sidebar.markdown("#### Image Previews")
            for file in uploaded_files:
                col1, col2 = st.sidebar.columns([3, 1])  # File uploader (left) + Preview (right)
                with col1:
                    st.write(f"📷 {file.name}")
                with col2:
                    st.image(Image.open(file), width=50)  # Small inline preview
        else:
            col1, col2 = st.sidebar.columns([3, 1])  # File uploader (left) + Preview (right)
            with col1:
                st.write(f"✅ Uploaded: {uploaded_files.name}")
            with col2:
                st.image(Image.open(uploaded_files), width=50)  # Small inline preview

    return uploaded_files

# **Twibbon & Watermark Upload**
st.sidebar.header("📌 Upload Templates")
twibbon = file_uploader_with_preview("Upload Twibbon (PNG, Required)", ["png"], "twibbon")
watermark = file_uploader_with_preview("Upload Watermark (PNG, Optional)", ["png"], "watermark")

# **Product Image Upload**
st.sidebar.header("📌 Upload Product Images")
uploaded_images = file_uploader_with_preview("Upload Images (JPG, PNG, WEBP)", ["jpg", "png", "webp"], "product_images", multiple=True)

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

# Watermark settings
if watermark:
    st.sidebar.header("📌 Watermark Settings")
    watermark_opacity = st.sidebar.slider("Watermark Opacity (%)", min_value=10, max_value=100, value=70) / 100
    watermark_size = st.sidebar.slider("Watermark Size (%)", min_value=10, max_value=100, value=50) / 100  # Default 50%

    # **Persistent Watermark Position Selection Using Session State**
    if "watermark_position" not in st.session_state:
        st.session_state.watermark_position = "Center"  # Default position

    st.sidebar.markdown("### 🔧 Select Watermark Position")

    position_mapping = {
        "Top Left": "↖️", "Top Center": "⬆️", "Top Right": "↗️",
        "Left Center": "⬅️", "Center": "🎯", "Right Center": "➡️",
        "Bottom Left": "↙️", "Bottom Center": "⬇️", "Bottom Right": "↘️"
    }

    col1, col2, col3 = st.sidebar.columns(3)
    if col1.button(position_mapping["Top Left"], help="Position: Top Left"):
        st.session_state.watermark_position = "Top Left"
    if col2.button(position_mapping["Top Center"], help="Position: Top Center"):
        st.session_state.watermark_position = "Top Center"
    if col3.button(position_mapping["Top Right"], help="Position: Top Right"):
        st.session_state.watermark_position = "Top Right"

    col1, col2, col3 = st.sidebar.columns(3)
    if col1.button(position_mapping["Left Center"], help="Position: Left Center"):
        st.session_state.watermark_position = "Left Center"
    if col2.button(position_mapping["Center"], help="Position: Center", key="center_btn"):
        st.session_state.watermark_position = "Center"
    if col3.button(position_mapping["Right Center"], help="Position: Right Center"):
        st.session_state.watermark_position = "Right Center"

    col1, col2, col3 = st.sidebar.columns(3)
    if col1.button(position_mapping["Bottom Left"], help="Position: Bottom Left"):
        st.session_state.watermark_position = "Bottom Left"
    if col2.button(position_mapping["Bottom Center"], help="Position: Bottom Center"):
        st.session_state.watermark_position = "Bottom Center"
    if col3.button(position_mapping["Bottom Right"], help="Position: Bottom Right"):
        st.session_state.watermark_position = "Bottom Right"

    # Display selected position
    st.sidebar.success(f"📍 Current Position: {st.session_state.watermark_position}")

# Process Button
if st.sidebar.button("🚀 Process Images"):
    if not uploaded_images or not twibbon:
        st.error("⚠️ Please upload at least one image and a twibbon!")
    else:
        # Convert uploaded files to PIL images
        twibbon_img = Image.open(twibbon)
        watermark_img = Image.open(watermark) if watermark else None  # If no watermark, pass None

        # Process images
        result_path = process_images(
            uploaded_images, 
            twibbon_img, 
            watermark_img, 
            output_size, 
            watermark_opacity, 
            st.session_state.watermark_position, 
            watermark_size
        )

        st.success("✅ Processing Complete!")

        # **Summary Section**
        st.markdown("### 📊 Processing Summary")
        st.write(f"📂 **Total Images Processed:** {len(uploaded_images)}")
        st.write(f"🖼️ **Output Resolution:** {output_size[0]} x {output_size[1]}")
        if watermark:
            st.write(f"🔹 **Watermark Opacity:** {int(watermark_opacity * 100)}%")
            st.write(f"📏 **Watermark Size:** {int(watermark_size * 100)}% of image size")
            st.write(f"📍 **Watermark Position:** {st.session_state.watermark_position}")

        # If only one image, provide direct PNG download
        if result_path.endswith(".png"):
            with open(result_path, "rb") as f:
                st.download_button("📥 Download Image", f, file_name=os.path.basename(result_path), mime="image/png")

        # If multiple images, provide ZIP download
        else:
            zip_filename = os.path.basename(result_path)
            with open(result_path, "rb") as f:
                st.download_button("📥 Download Processed Images", f, file_name=zip_filename, mime="application/zip")

