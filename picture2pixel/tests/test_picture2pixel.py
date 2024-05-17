import unittest
import sys
import os
import numpy as np
from urllib.request import urlopen
from urllib.error import URLError

# Add parent directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from picture2pixel.convert2pixel import process_image, apply_floyd_steinberg_dithering, generate_verilog_code

class TestPicture2Pixel(unittest.TestCase):

    def test_process_image(self):
        url = 'https://www.comp.nus.edu.sg/~guoyi/project/picture2pixel/tests/default.png'
        try:
            urlopen(url)
            print(f"[ OK! ] Picture data retrieved from {url} successfully.")
        except URLError:
            self.fail(f"[ ERR ] Failed to retrieve picture data from {url}.")
        
        reconstructed_image = process_image(url, 96, 64, 20)
        self.assertEqual(reconstructed_image.shape, (64, 96, 3))

    def test_apply_floyd_steinberg_dithering(self):
        image = np.zeros((64, 96, 3), dtype=np.uint8)
        dithered_image = apply_floyd_steinberg_dithering(image)
        self.assertEqual(dithered_image.shape, (64, 96, 3))

    def test_generate_verilog_code(self):
        pixels = np.zeros((64 * 96, 3), dtype=np.uint8)
        verilog_code = generate_verilog_code(pixels)
        self.assertIn("else oled_data = 0;", verilog_code)

if __name__ == '__main__':
    unittest.main()
