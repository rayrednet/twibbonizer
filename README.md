# 🖼️ Twibbonizer

Easily add a **twibbon** and **watermark** to multiple images at once! 🎨✨

## ❓ What is a Twibbon?
A **twibbon** is a **transparent overlay** that people add to their profile pictures or images to show support for a cause, campaign, or branding. Twibbonizer helps you easily apply twibbons to multiple images with optional watermarking.

## 🌟 Features
- **Batch Processing:** Upload multiple images and apply the twibbon/watermark in one go.
- **Customizable Output:** Adjust output resolution, watermark opacity, size, and position.
- **Live Preview:** See uploaded images, twibbon, and watermark before processing.
- **Smart Output:** 
  - If one image is uploaded, a **direct PNG download** is provided.
  - If multiple images are uploaded, a **ZIP file with timestamp** is generated.
- **Streamlit UI:** Simple, fast, and easy-to-use interface.
- **Cloud Hosted:** Runs on Streamlit Community Cloud for instant online access.

## 🚀 Live Demo
Try it here: [Twibbonizer on Streamlit](https://twibbonizer.streamlit.app/)

🎥 **Watch the Demo Video:** [YouTube Link](https://youtu.be/QgeiMd0JXS0)

## 📌 How to Use
### 1️⃣ Upload Files
- **Twibbon (Required)** - Must be a **transparent PNG**.
- **Watermark (Optional)** - Also a **transparent PNG**.
- **Product Images** - Supports JPG, PNG, and WEBP formats.

### 2️⃣ Adjust Settings
- **Output Image Size**
  - Choose **Square (1080x1080, etc.)** or **Keep Original Aspect Ratio**.
- **Watermark Options** (Optional)
  - Set **opacity** (10% - 100%)
  - Adjust **size** (10% - 100%)
  - Choose **position** (center, top-left, top-right, etc.)

### 3️⃣ Process & Download
- Click **"🚀 Process Images"**
- View the **summary report** (processed images, settings used, etc.)
- Download the processed **PNG** (single image) or **ZIP file** (multiple images)

## 🛠️ Installation (For Local Development)
Clone the repository and install dependencies:

```sh
# Clone the repo
git clone https://github.com/rayrednet/twibbonizer.git
cd twibbonizer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

# Install dependencies
pip install -r requirements.txt
```

### Run the App Locally
```sh
streamlit run app.py
```

### Run the Jupyter Notebook Example
If you want to try **a local trial with hardcoded paths**, run the Jupyter notebook:
```sh
jupyter notebook twibbonizer.ipynb
```

## 📦 Deployment
This app is deployed on **Streamlit Community Cloud**.
To deploy it yourself:
1. Push all changes to a **GitHub repository**.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Click **"New App"** → Select your GitHub repo.
4. Set **main script path** to `app.py`.
5. Deploy & share your app!

## 📄 File Structure
```
📂 twibbonizer/
├── 📂 data/                   # Example images (twibbons, watermarks, etc.)
├── 📂 output/                 # Temporary output directory
├── 📂 processed_images/        # Processed output images with timestamps
├── 📂 venv/                   # Virtual environment (ignored in deployment)
├── 📜 app.py                   # Streamlit application
├── 📜 helpers.py               # Image processing logic
├── 📜 twibbonizer.ipynb        # Jupyter Notebook for local trial (hardcoded paths)
├── 📜 requirements.txt         # Python dependencies
├── 📜 README.md                # Documentation (this file)
```

## 📄 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.