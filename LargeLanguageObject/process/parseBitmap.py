from PIL import Image

from PIL import Image

def image_to_mono_bitmap(image_path, output_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to monochrome
        mono_img = img.convert("1", dither=Image.NONE)

        # Get the image data as a byte array
        img_data = mono_img.tobytes()

        # Calculate the image size
        width, height = mono_img.size
        image_size = width * height // 8

        # Save the image data as a C array
        with open(output_path, "wb") as f:
            f.write(f"static const unsigned char PROGMEM thinkleft[] = {{\n".encode())
            for i in range(image_size):
                f.write(f"0x{img_data[i]:02x}, ".encode())
                if (i + 1) % width == 0:
                    f.write("\n".encode())
            f.write("};\n".encode())

# Example usage
image_to_mono_bitmap("thinkleft.jpg", "thinkleft.h")

