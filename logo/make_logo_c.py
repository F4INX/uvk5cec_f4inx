# -*- coding: utf-8 -*-
"""
Logo RLE packer.

Hadrien F4INX Theveneau, 2024
"""

# from itertools import islice
import textwrap
from PIL import Image


def rle_tuples_gen(image_png_path):
    """ Function to analyze the image pixels and detect consecutive sequences"""
    def is_black(pixel):
        """Helper function to convert RGB to boolean (True if black, False if white)."""
        return pixel == (0, 0, 0)
    # Load the image
    with Image.open(image_png_path) as img:
        # Convert image to RGB (if it's not already in that format)
        img = img.convert('RGB')
        # Get the size of the image
        width, height = img.size
        # Initialize variables to track the current color and count
        current_color = None
        current_count = 0
        # Iterate through the pixels from left to right, and top to bottom
        for y in range(height):
            for x in range(width):
                # Get the current pixel
                pixel = img.getpixel((x, y))
                # Determine if the pixel is black or white
                pixel_is_black = is_black(pixel)
                # If this is the first pixel or if the color changes, we need to start a new sequence
                if current_color is None or pixel_is_black != current_color:
                    # If it's not the first pixel, we need to record the previous sequence
                    if current_color is not None:
                        yield (current_color, current_count)
                    # Reset the count and set the current color to the new color
                    current_count = 1
                    current_color = pixel_is_black
                else:
                    # If the color hasn't changed, simply increment the count
                    current_count += 1
        # After finishing the loop, we need to add the last sequence to the list
        if current_color is not None:
            yield (current_color, current_count)


def rle_compressor(image_png_path):
    """
    Compress the image using Run-Length Encoding (RLE).
    For each tuple (current_color, current_count) produced by rle_tuples_gen(image_path):
    Produces a byte whose MSB is current_color and LSBs current_count
    Assuming current_count is between 0 and 127.
    """
    for color, count in rle_tuples_gen(image_png_path):
        # Ensure that count is within the allowable range for a 7-bit number
        if count > 127:
            # If the count is greater than 127, we need to split it into multiple bytes
            while count > 127:
                yield (color << 7) | 127
                count -= 127
        # Pack the color and count into one byte: MSB for color, rest for count
        yield (color << 7) | count


def rle_c_string(input_bytes):
    """
    Transforms input_bytes iterator into a C-style string with hexadecimal bytes.
    """
    # Start with a double quote to open the string
    output_string = "\""
    # Iterate over the input bytes and format each byte as hexadecimal
    for byte in input_bytes:
        output_string += "\\x{:02x}".format(byte)
    # Close the string with a double quote
    output_string += "\""
    return output_string


def make_c_image(image_png_path, image_c_path):
    with open(image_c_path, 'w', newline='\n') as f:
        logo_rlc = rle_c_string(rle_compressor(image_png_path))
        f.write(textwrap.dedent(f"""\
            char * LOGO_RLE = {logo_rlc};
        """))


# Now let's call the function with the provided image
image_png_path = 'f6kgl-f5kff.png'
image_c_path = 'logo.c'
# for byte in islice(rle_compressor(image_path), 10):  # Show the first 10 bytes of compressed data for brevity
#     print(f"0b{byte:08b}")
# print(rle_c_string(rle_compressor(image_path)))
make_c_image(image_png_path, image_c_path)
