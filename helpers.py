from PIL import Image
import os
import zipfile

def process_images(images, twibbon, watermark, output_size, watermark_opacity):
    """
    Processes images by applying a twibbon and an optional watermark.
    If there is only one image, returns its file path directly.
    If multiple images, returns a ZIP file path.
    """
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    twibbon = twibbon.convert("RGBA")
    if watermark:
        watermark = watermark.convert("RGBA")

    output_files = []  # List to store processed file paths

    for image_file in images:
        img = Image.open(image_file).convert("RGBA")

        # Determine final size based on user selection
        if output_size[1]:  # If height is defined, use fixed dimensions
            img_resized = img.resize(output_size, Image.LANCZOS)
            twibbon_resized = twibbon.resize(output_size, Image.LANCZOS)
        else:  # Keep original aspect ratio with max width
            width_percent = output_size[0] / float(img.size[0])
            height_size = int((float(img.size[1]) * float(width_percent)))
            img_resized = img.resize((output_size[0], height_size), Image.LANCZOS)
            twibbon_resized = twibbon.resize((output_size[0], height_size), Image.LANCZOS)

        # Apply twibbon
        combined = Image.alpha_composite(img_resized, twibbon_resized)

        # Apply watermark if provided
        if watermark:
            # Resize watermark to 50% of image size
            watermark_size = (img_resized.width // 2, img_resized.height // 2)
            watermark_resized = watermark.resize(watermark_size, Image.LANCZOS)

            # Adjust watermark opacity
            watermark_transparent = Image.new("RGBA", watermark_resized.size)
            for x in range(watermark_resized.width):
                for y in range(watermark_resized.height):
                    r, g, b, a = watermark_resized.getpixel((x, y))
                    watermark_transparent.putpixel((x, y), (r, g, b, int(a * watermark_opacity * 255)))

            # Create blank transparent layer for watermark
            watermark_layer = Image.new("RGBA", img_resized.size, (0, 0, 0, 0))

            # Position watermark at the center
            position = ((img_resized.width - watermark_size[0]) // 2, (img_resized.height - watermark_size[1]) // 2)
            watermark_layer.paste(watermark_transparent, position, mask=watermark_transparent)

            # Overlay watermark
            combined = Image.alpha_composite(combined, watermark_layer)

        # Save the processed file
        output_path = os.path.join(output_folder, os.path.splitext(image_file.name)[0] + ".png")
        combined.save(output_path, "PNG", quality=95)
        output_files.append(output_path)

    # If only one image, return the file path directly
    if len(output_files) == 1:
        return output_files[0]

    # Otherwise, create a ZIP file
    zip_filename = os.path.join(output_folder, "processed_images.zip")
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for file in output_files:
            zipf.write(file, os.path.basename(file))

    return zip_filename