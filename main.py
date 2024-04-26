from math import ceil

from PIL import Image

file_image = Image.open(
    "image.png")
input_image = file_image.resize((128, 64)).convert("RGB")
width, height = input_image.size

size = width * ceil((height / 8))
output = bytearray(size)
threshold = 100

for i in range(width):
    for k in range(ceil(height / 8)):
        index = i + k * width
        output[index] = 0
        for j in range(8):
            pixel = input_image.getpixel((i, (k * 8) + j))
            magnitude = sum(pixel) / 3
            output[index] |= (magnitude > threshold) << j


print("const unsigned char data[] = {{{}}};".format(", ".join([format(b, '#04x') for b in output])))
