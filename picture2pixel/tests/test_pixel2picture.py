import unittest
import sys
import os
import numpy as np
from urllib.request import urlopen
from urllib.error import URLError

# Add parent directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from picture2pixel.convert2picture import parse_color, find_color_for_pixel, load_p2p_file, save_image

class TestPixel2Picture(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.p2p_url = 'https://www.comp.nus.edu.sg/~guoyi/project/picture2pixel/tests/default.p2p'
        cls.width = 96
        cls.height = 64
        cls.p2p_filename = 'default.p2p'

        try:
            response = urlopen(cls.p2p_url)
            with open(cls.p2p_filename, 'wb') as f:
                f.write(response.read())
            print(f"[ OK! ] Pixel data retrieved from {cls.p2p_url} successfully.")
        except URLError:
            cls.fail(f"[ ERR ] Failed to retrieve pixel data from {cls.p2p_url}.")

    @classmethod
    def tearDownClass(cls):
        # Clean up generated file after all tests
        if os.path.exists(cls.p2p_filename):
            os.remove(cls.p2p_filename)

    def test_parse_color(self):
        line = "oled_data = 16'b1111100000111110;"
        color = parse_color(line)
        self.assertEqual(color, (248, 4, 240))

    def test_find_color_for_pixel(self):
        lines = [
            "oled_data = 16'b1111100000111110;", 
            "if (pixel_index == 0) begin oled_data = 16'b1111100000111110; end"
        ]
        color = find_color_for_pixel(0, lines)
        self.assertEqual(color, (248, 4, 240))

    def test_load_p2p_file(self):
        image_array, unfound_pixels = load_p2p_file(self.p2p_filename, self.width, self.height)
        self.assertEqual(image_array.shape, (64, 96, 3))
        self.assertIsInstance(unfound_pixels, list)

    def test_save_image(self):
        image_array = np.zeros((64, 96, 3), dtype=np.uint8)
        output_path = "output_image.png"
        save_image(image_array, output_path)
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path)  # Clean up after the test

if __name__ == '__main__':
    unittest.main()
