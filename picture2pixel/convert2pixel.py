import os
import numpy as np
import argparse
from picture2pixel import process_image, apply_floyd_steinberg_dithering, generate_verilog_code
import urllib.request
from PIL import Image

def picture_to_pixel(filename, width, height, svd_r, output_dir):
    """
    Process the image, apply dithering, and generate Verilog code.
    """
    # Check if the filename is a URL or a local file
    if filename.startswith('http://') or filename.startswith('https://'):
        # If it's a URL, download the image and use the same filename as the URL
        image_filename = os.path.basename(filename)
        local_image_path = os.path.join(output_dir, image_filename)
        try:
            urllib.request.urlretrieve(filename, local_image_path)
            print(f"[ ^_^ ] Image downloaded to {local_image_path}")
        except Exception as e:
            print(f"[ X_X ] Failed to download the image: {e}")
            return
    else:
        # If it's a local file path, use it directly
        local_image_path = filename

    # Process the image
    image = process_image(local_image_path, width, height, svd_r)
    
    # Apply dithering
    processed_image = apply_floyd_steinberg_dithering(image)
    
    # Generate Verilog code
    pixels = processed_image.reshape(-1, 3)
    verilog_code = generate_verilog_code(pixels)

    # Output results
    if output_dir == "0":
        print(f"[ ^_^ ] Printing Verilog code to console:")
        print(verilog_code)
    else:
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"[ ^_^ ] Created output directory: {output_dir}")
        
        base_filename = os.path.splitext(os.path.basename(local_image_path))[0]
        output_file = os.path.join(output_dir, f"{base_filename}.p2p")
        
        # Write the Verilog code to file
        try:
            with open(output_file, 'w') as f:
                f.write(verilog_code)
            print(f"[ ^_^ ] Verilog code saved to: {output_file}")
        except Exception as e:
            print(f"[ X_X ] Failed to write Verilog code to {output_file}: {e}")

    # If the image was downloaded, delete the temporary image file
    if filename.startswith('http://') or filename.startswith('https://'):
        try:
            os.remove(local_image_path)
            print(f"[ ^_^ ] Deleted downloaded image: {local_image_path}")
        except Exception as e:
            print(f"[ X_X ] Failed to delete the temporary image: {e}")
    
    return processed_image

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Convert picture to pixel data.")
    parser.add_argument("filename", type=str, help="Path to the input image file or URL")
    parser.add_argument("width", type=int, help="Width of the output pixel array")
    parser.add_argument("height", type=int, help="Height of the output pixel array")
    parser.add_argument("svd_r", type=int, help="SVD rank to use for image processing")
    parser.add_argument("output_dir", type=str, help="Directory to save the output .p2p file or '0' to print to console")

    # Parse the arguments
    args = parser.parse_args()
    
    # Check if the file exists
    if not os.path.isfile(args.filename) and not args.filename.startswith("http"):
        print(f"[ X_X ] The file {args.filename} does not exist.")
    else:
        picture_to_pixel(args.filename, args.width, args.height, args.svd_r, args.output_dir)
