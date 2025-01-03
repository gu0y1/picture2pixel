import argparse
import os
import numpy as np
import urllib.request
from PIL import Image
from picture2pixel import process_image, apply_floyd_steinberg_dithering

def image_to_mem(image_path, width, height, svd_r, output_dir):
    """
    Convert image to .mem file (row-major order).
    """
    # Check if the image_path is a URL or a local file path
    if image_path.startswith('http://') or image_path.startswith('https://'):
        # If it's a URL, download the image and use the same filename as the URL
        image_filename = os.path.basename(image_path)
        local_image_path = os.path.join(output_dir, image_filename)
        try:
            urllib.request.urlretrieve(image_path, local_image_path)
            print(f"[ ^_^ ] Image downloaded to {local_image_path}")
        except Exception as e:
            print(f"[ X_X ] Failed to download the image: {e}")
            return
    else:
        # If it's a local file path, use it directly
        local_image_path = image_path
    
    # Process the image using process_image (SVD, resizing, etc.)
    processed_image = process_image(local_image_path, width, height, svd_r)
    
    # Apply Floyd-Steinberg dithering
    processed_image = apply_floyd_steinberg_dithering(processed_image)
    
    # Convert the processed image (numpy array) to .mem format
    image_filename_without_ext = os.path.splitext(os.path.basename(local_image_path))[0]
    mem_file_path = os.path.join(output_dir, f"{image_filename_without_ext}.mem")

    # Flatten the image and convert it to RGB565 format
    pixels = processed_image.reshape(-1, 3)
    
    with open(mem_file_path, 'w') as f:
        for pixel in pixels:
            r, g, b = pixel
            r = (r >> 3) & 0x1F  # 5 bits for red
            g = (g >> 2) & 0x3F  # 6 bits for green
            b = (b >> 3) & 0x1F  # 5 bits for blue
            
            # Combine into RGB565
            rgb_565 = (r << 11) | (g << 5) | b
            f.write(f"{rgb_565:04X}\n")
    
    print(f"[ ^_^ ] .mem file saved to {mem_file_path}")
    
    # If the image was downloaded, delete the temporary image file
    if image_path.startswith('http://') or image_path.startswith('https://'):
        try:
            os.remove(local_image_path)
            print(f"[ ^_^ ] Deleted downloaded image: {local_image_path}")
        except Exception as e:
            print(f"[ X_X ] Failed to delete the temporary image: {e}")


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Tool for converting images to .mem files")

    # Define the command-line arguments
    parser.add_argument("image_url", type=str, help="Path to the image file or URL")
    parser.add_argument("width", type=int, help="Width of the image")
    parser.add_argument("height", type=int, help="Height of the image")
    parser.add_argument("svd_r", type=int, help="SVD rank for image processing")
    parser.add_argument("output_dir", type=str, help="Directory to save the output .mem file")

    # Parse the arguments
    args = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Call the image_to_mem function with parsed arguments
    image_to_mem(args.image_url, args.width, args.height, args.svd_r, args.output_dir)


if __name__ == "__main__":
    main()
