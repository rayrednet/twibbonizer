from PIL import Image
import os
import zipfile

def process_images(images, twibbon, watermark, output_size, watermark_opacity, watermark_position, watermark_size):
    """
    Processes images by applying a twibbon and an optional watermark.
    Allows users to adjust watermark position and size.
    If there is only one image, returns its file path directly.
    If multiple images, returns a ZIP file path.
    """
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    twibbon = twibbon.convert("RGBA")
    if watermark:
        watermark = watermark.convert("RGBA")

    output_files = []  

    for image_file in images:
        img = Image.open(image_file).convert("RGBA")

        # Determine size
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
            # Resize watermark based on user-defined percentage
            watermark_size_px = (int(img_resized.width * watermark_size), int(img_resized.height * watermark_size))
            watermark_resized = watermark.resize(watermark_size_px, Image.LANCZOS)

            # Adjust watermark opacity
            watermark_layer = Image.new("RGBA", watermark_resized.size)
            for x in range(watermark_resized.width):
                for y in range(watermark_resized.height):
                    r, g, b, a = watermark_resized.getpixel((x, y))
                    watermark_layer.putpixel((x, y), (r, g, b, int(a * watermark_opacity * 255)))  # Adjust transparency

            # Create transparent layer for watermark placement
            overlay = Image.new("RGBA", img_resized.size, (0, 0, 0, 0))

            # Positioning based on user input
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

            # Place watermark on overlay layer
            overlay.paste(watermark_layer, position, watermark_layer)

            # Merge overlay with main image
            combined = Image.alpha_composite(combined, overlay)

        output_path = os.path.join(output_folder, os.path.splitext(image_file.name)[0] + ".png")
        combined.save(output_path, "PNG", quality=95)
        output_files.append(output_path)

    return output_files[0] if len(output_files) == 1 else output_folder
