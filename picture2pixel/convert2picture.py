import argparse
import numpy as np
from PIL import Image
import os
import re
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

def parse_color(line):
    color_match = re.search(r"oled_data\s*=\s*16'b([01]{16});", line)
    if color_match:
        color_value = color_match.group(1)
        red = int(color_value[:5], 2) * (256 // 32)
        green = int(color_value[5:11], 2) * (256 // 64)
        blue = int(color_value[11:], 2) * (256 // 32)
        return (red, green, blue)
    return None

def find_color_for_pixel(pixel_index, lines):
    for line in lines:
        color = parse_color(line)
        if color:
            pixel_ranges = re.findall(r'\(\(pixel_index\s*([<>=!]+)\s*(\d+)\)\s*&&\s*\(pixel_index\s*([<>=!]+)\s*(\d+)\)\)', line)
            for pixel_range in pixel_ranges:
                start = int(pixel_range[1])
                end = int(pixel_range[3])
                if start <= pixel_index <= end:
                    return color
            single_pixel_match = re.findall(r'pixel_index\s*==\s*(\d+)', line)
            if single_pixel_match:
                for pixel_index_str in single_pixel_match:
                    if int(pixel_index_str) == pixel_index:
                        return color
    return None  # Return None if no match is found

def load_p2p_file(filepath, width, height):
    image_array = np.zeros((height, width, 3), dtype=np.uint8)
    unfound_pixels = []

    with open(filepath, 'r') as file:
        lines = file.readlines()

    total_pixels = width * height

    def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
        if iteration == total:
            print()

    for pixel_index in range(total_pixels):
        y = pixel_index // width
        x = pixel_index % width
        color = find_color_for_pixel(pixel_index, lines)
        if color:
            image_array[y, x] = color
        else:
            unfound_pixels.append((x, y))
            image_array[y, x] = (0, 0, 0)  # Default to black if no match is found
        
        print_progress_bar(pixel_index + 1, total_pixels, prefix='[ O_o ] Pixel2Picture:', suffix='Done', length=30)

    return image_array, unfound_pixels

def save_image(image_array, output_path):
    image = Image.fromarray(image_array)
    image.save(output_path)
    print(f"[ ^_^ ] Image saved to {output_path}")

def main(p2p_file, width, height, output_dir):
    # Check if the input file is a URL
    if p2p_file.startswith('http://') or p2p_file.startswith('https://'):
        local_p2p_file = 'downloaded.p2p'
        try:
            response = urlopen(p2p_file)
            with open(local_p2p_file, 'wb') as f:
                f.write(response.read())
            print(f"[ ^_^ ] Pixel data retrieved from {p2p_file} successfully.")
            p2p_file = local_p2p_file
        except HTTPError as e:
            print(f"[ X_X ] HTTP Error: {e.code} - {e.reason} for URL: {p2p_file}")
            return
        except URLError as e:
            print(f"[ X_X ] URL Error: {e.reason} for URL: {p2p_file}")
            return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    base_filename = os.path.splitext(os.path.basename(p2p_file))[0]
    output_path = os.path.join(output_dir, f"{base_filename}.png")
    
    image_array, unfound_pixels = load_p2p_file(p2p_file, width, height)
    save_image(image_array, output_path)
    
    if unfound_pixels:
        print("\n[ >_< ] Uncolored (black) pixels found at:")
        for pixel in unfound_pixels:
            print(f"({pixel[0]}, {pixel[1]})")
    else:
        print("[ ^_^ ] All pixels colored successfully.")
    
    # Clean up the downloaded file if it was used
    if p2p_file == 'downloaded.p2p':
        os.remove(local_p2p_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .p2p file to an image.")
    parser.add_argument("p2p_file", type=str, help="Path to the .p2p file")
    parser.add_argument("width", type=int, help="Width of the image")
    parser.add_argument("height", type=int, help="Height of the image")
    parser.add_argument("output_dir", type=str, help="Directory to save the output image")

    args = parser.parse_args()

    main(args.p2p_file, args.width, args.height, args.output_dir)
