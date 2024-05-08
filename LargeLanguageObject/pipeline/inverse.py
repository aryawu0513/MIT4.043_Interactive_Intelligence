from PIL import Image

def invert_image(image_path, output_path):
    with Image.open(image_path) as img:
        # Invert the image
        inverted_img = Image.eval(img, lambda px: 255 - px)

        # Save the inverted image
        inverted_img.save(output_path)

# Example usage
invert_image("IMG_2513.jpg", "outputspeech.jpg")