import argparse
import os
import numpy as np
from PIL import Image

def mem_to_image(mem_file_path, width, height, output_dir):
    """
    Convert a .mem file to an image.
    """
    # Read the .mem file
    with open(mem_file_path, 'r') as f:
        lines = f.readlines()

    if len(lines) != width * height:
        print(f"[ERROR] The number of lines in {mem_file_path} does not match the expected size of {width}x{height}.")
        return

    pixels = []
    
    # Process each line in the .mem file
    for line in lines:
        rgb_565 = int(line.strip(), 16)  # Convert the hex string to an integer
        r = (rgb_565 >> 11) & 0x1F     # Extract the red component (5 bits)
        g = (rgb_565 >> 5) & 0x3F      # Extract the green component (6 bits)
        b = rgb_565 & 0x1F             # Extract the blue component (5 bits)

        # Convert RGB565 to 8-bit RGB
        r = (r << 3) | (r >> 2)         # Expand 5 bits to 8 bits
        g = (g << 2) | (g >> 4)         # Expand 6 bits to 8 bits
        b = (b << 3) | (b >> 2)         # Expand 5 bits to 8 bits

        pixels.append((r, g, b))        # Add the pixel to the list
    
    # Create an image from the pixel data
    img = Image.new("RGB", (width, height))
    img.putdata(pixels)

    # Save the image to the specified output directory
    output_image_path = os.path.join(output_dir, 'output_image.png')
    img.save(output_image_path)
    print(f"[ ^_^ ] Image saved to {output_image_path}")


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Tool for converting .mem files to images")
    
    # Define the command-line arguments
    parser.add_argument("mem_file_path", type=str, help="Path to the .mem file")
    parser.add_argument("width", type=int, help="Width of the output image")
    parser.add_argument("height", type=int, help="Height of the output image")
    parser.add_argument("output_dir", type=str, help="Directory to save the output image")

    # Parse the arguments
    args = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Call the mem_to_image function with parsed arguments
    mem_to_image(args.mem_file_path, args.width, args.height, args.output_dir)


if __name__ == "__main__":
    main()
