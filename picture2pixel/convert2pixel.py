import os
import numpy as np
import argparse
from picture2pixel import process_image, apply_floyd_steinberg_dithering, generate_verilog_code

def picture_to_pixel(filename, width, height, svd_r, output_dir):
    # Process the image
    image = process_image(filename, width, height, svd_r)
    
    # Apply dithering
    processed_image = apply_floyd_steinberg_dithering(image)
    
    # Generate Verilog code
    pixels = processed_image.reshape(-1, 3)
    verilog_code = generate_verilog_code(pixels)

    # Output results
    if output_dir == "0":
        print(verilog_code)
    else:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        output_file = os.path.join(output_dir, f"{base_filename}.p2p")
        with open(output_file, 'w') as f:
            f.write(verilog_code)
    
    return processed_image

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert picture to pixel data.")
    parser.add_argument("filename", type=str, help="Path to the input image file")
    parser.add_argument("width", type=int, help="Width of the output pixel array")
    parser.add_argument("height", type=int, help="Height of the output pixel array")
    parser.add_argument("svd_r", type=int, help="SVD rank to use for image processing")
    parser.add_argument("output_dir", type=str, help="Directory to save the output .p2p file or '0' to print to console")

    args = parser.parse_args()
    
    if not os.path.isfile(args.filename) and not args.filename.startswith("http"):
        print(f"Error: The file {args.filename} does not exist.")
    else:
        picture_to_pixel(args.filename, args.width, args.height, args.svd_r, args.output_dir)
