from PIL import Image, ImageEnhance
import os
import zipfile
import datetime

def process_images(images, twibbon, watermark, output_size, watermark_opacity, watermark_position, watermark_size):
    """
    Processes images by applying a twibbon and an optional watermark.
    Adds a timestamp to the output filenames and the ZIP file.
    Fixes opacity scaling issue for watermarks.
    """
    output_folder = "processed_images"
    os.makedirs(output_folder, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    twibbon = twibbon.convert("RGBA")
    if watermark:
        watermark = watermark.convert("RGBA")

    output_files = []

    for image_file in images:
        img = Image.open(image_file).convert("RGBA")

        # Resize image & twibbon
        if output_size[1]:
            img_resized = img.resize(output_size, Image.LANCZOS)
            twibbon_resized = twibbon.resize(output_size, Image.LANCZOS)
        else:
            width_percent = output_size[0] / float(img.size[0])
            height_size = int((float(img.size[1]) * float(width_percent)))
            img_resized = img.resize((output_size[0], height_size), Image.LANCZOS)
            twibbon_resized = twibbon.resize((output_size[0], height_size), Image.LANCZOS)

        # Apply twibbon
        combined = Image.alpha_composite(img_resized, twibbon_resized)

        if watermark:
            # Resize watermark
            watermark_size_px = (int(img_resized.width * watermark_size), int(img_resized.height * watermark_size))
            watermark_resized = watermark.resize(watermark_size_px, Image.LANCZOS)

            # **Fix opacity scaling issue using ImageEnhance**
            alpha = watermark_resized.split()[3]  # Extract alpha channel
            alpha = ImageEnhance.Brightness(alpha).enhance(watermark_opacity)  # Adjust opacity
            watermark_resized.putalpha(alpha)

            # Transparent overlay
            overlay = Image.new("RGBA", img_resized.size, (0, 0, 0, 0))

            # Positioning
            positions = {
                "Top Left": (10, 10),
                "Top Center": ((img_resized.width - watermark_size_px[0]) // 2, 10),
                "Top Right": (img_resized.width - watermark_size_px[0] - 10, 10),
                "Left Center": (10, (img_resized.height - watermark_size_px[1]) // 2),
                "Center": ((img_resized.width - watermark_size_px[0]) // 2, (img_resized.height - watermark_size_px[1]) // 2),
                "Right Center": (img_resized.width - watermark_size_px[0] - 10, (img_resized.height - watermark_size_px[1]) // 2),
                "Bottom Left": (10, img_resized.height - watermark_size_px[1] - 10),
                "Bottom Center": ((img_resized.width - watermark_size_px[0]) // 2, img_resized.height - watermark_size_px[1] - 10),
                "Bottom Right": (img_resized.width - watermark_size_px[0] - 10, img_resized.height - watermark_size_px[1] - 10),
            }
            position = positions.get(watermark_position, positions["Center"])

            # Place watermark
            overlay.paste(watermark_resized, position, watermark_resized)

            # Merge overlay with image
            combined = Image.alpha_composite(combined, overlay)

        # **Save image with timestamp**
        output_filename = f"{os.path.splitext(image_file.name)[0]}_{timestamp}.png"
        output_path = os.path.join(output_folder, output_filename)
        combined.save(output_path, "PNG", quality=95)
        output_files.append(output_path)

    # **Ensure the ZIP file is timestamped**
    if len(output_files) > 1:
        zip_filename = f"processed_images_{timestamp}.zip"
        zip_path = os.path.join(output_folder, zip_filename)

        print(f"Creating ZIP file: {zip_path}")  # Debugging

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in output_files:
                zipf.write(file, os.path.basename(file))

        return zip_path  # Return ZIP file path

    return output_files[0]  # Return single processed image path
