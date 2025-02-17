# Twibbonizer 🖼️✨

**Twibbonizer** is a Python script that overlays a **twibbon** and **watermark** onto product images automatically.  
It resizes images, applies transparency, and organizes the processed files efficiently.



## 📌 Features
✅ Automatically processes all images in `katalog_1` and `katalog_2`  
✅ Overlays **twibbon** on top of product images  
✅ Adds a **centered watermark** with adjustable opacity  
✅ Resizes images to **1080x1080 pixels**  
✅ Supports **JPG, PNG, WEBP** formats  
✅ Saves images in an organized `/output` folder  

## 🔧 Installation & Usage
### **1️⃣ Install Dependencies**
Make sure you have **Python** and install `Pillow` (Python Imaging Library):

```sh
pip install pillow
```

### **2️⃣ Place Your Images**
- Add product images to **`katalog_1/`** and **`katalog_2/`**  
- Place **`twibbon_1.png`** (twibbon overlay) in the main folder  
- Place **`watermark_1.png`** (logo or branding watermark) in the main folder  

### **3️⃣ Run the Script**
Run the script to process the images:

```sh
python twibbonizer.py
```

### **4️⃣ View Output**
Processed images will be saved inside the **`/output/katalog_1/`** and **`/output/katalog_2/`** folders.


## ⚙️ Customization
### **Change Watermark Opacity**
Modify this line in `twibbonizer.py`:

```python
watermark_opacity = 0.7
```

| Opacity Value | Effect |
|--------------|--------|
| `0.3` (30%) | Very transparent |
| `0.5` (50%) | Semi-transparent |
| `0.7` (70%) | More visible |
| `1.0` (100%) | Fully visible |


## ✅ Requirements
- **Python 3.7+**
- **Pillow library** (`pip install pillow`)
- **PNG twibbon & watermark with transparency**


## 🛠️ Troubleshooting
- **Images not showing correctly?** Ensure the twibbon and watermark have a transparent background.
- **Watermark too big?** Adjust the `50%` scaling inside the script.
- **Need a different position?** Modify the `(x, y)` coordinates in the script.
