# Picture2Pixel


**Picture2Pixel** is an open-source Python library designed to transform images into pixel art that can be displayed on FPGA-driven OLED screens. By employing advanced computer graphics techniques, this library preprocesses images to minimize distortion during the pixelation process. The resulting artwork is expressed as combinations of predicate logic in Verilog language, ensuring compatibility with FPGA technology. This optimization not only enhances display efficiency on OLED screens but also reduces energy consumption, making it ideal for developers looking to integrate low-power, high-efficiency visual displays into their hardware projects.

**Picture2Pixel** can also convert both single images and batches of images (including GIFs) into formats suitable for FPGA OLED displays. Please view more magnificent GIF demos on our website: [Picture2Pixel.org](http://https://www.comp.nus.edu.sg/~guoyi/project/picture2pixel/)

## Project Wiki (MUST READ!)
We have created a comprehensive Wiki for the Picture2Pixel project, which includes development documentation, tutorials, and examples to help developers deploy, use, and further develop our project.
- **Tutorials**: Detailed Python and Verilog tutorials, including examples, to help you achieve stunning FPGA display effects similar to those on our official website.
- **Development Documentation**: Detailed development documentation, including function descriptions and technical standards for Python and Verilog, to facilitate further development of our Python Library.

## Installation

Install the `picture2pixel` package using pip:

```bash
pip install picture2pixel
```

## Usage

### Convert Image to Pixel Data

Convert an image to pixel data and generate Verilog code:

```bash
python -m picture2pixel.convert2pixel <image_url> <width> <height> <svd_r> <output_dir>
```

Example:

```bash
python -m picture2pixel.convert2pixel https://www.comp.nus.edu.sg/~guoyi/project/picture2pixel/tests/default.png 96 64 20 output_directory
```

### Convert Pixel Data to Image

This function is for Convert pixel data from a `.p2p` file back into an image:

```bash
python -m picture2pixel.convert2picture <p2p_file> <width> <height> <output_dir>
```

Example:

```bash
python -m picture2pixel.convert2picture https://www.comp.nus.edu.sg/~guoyi/project/picture2pixel/tests/default.p2p 96 64 output_directory
```

## Project Structure

```plaintext
picture2pixel/
├── __init__.py
├── convert2pixel.py
├── convert2picture.py
├── image_processing.py
├── verilog_generator.py
├── tests/
│   ├── __init__.py
│   ├── test_picture2pixel.py
│   ├── test_pixel2picture.py
│   ├── test_integrated.py
README.md
requirements.txt
setup.py
```

## License

Copyright (c) <2024> <copyright Chen Guoyi, Fang Sihan>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

------------

Picture2Pixel is developed and maintained by:
- Chen [Guoyi@comp.nus.edu.sg](mailto:guoyi@comp.nus.edu.sg)
- Fang [Sihan@comp.nus.edu.sg](mailto:sihan@comp.nus.edu.sg)

THIS PROJECT IS SPONSORED BY DEPARTMENT OF ELECTRICAL AND COMPUTER ENGINEERING, NATIONAL UNIVERSITY OF SINGAPORE.
