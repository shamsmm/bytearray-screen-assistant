from math import ceil

from PIL import Image
import cv2

# Load the video file
# Change the path to the video file as per your system
video_file = "/home/shams/Videos/Webcam/2024-04-27-002825.webm"
cap = cv2.VideoCapture(video_file)

output = bytearray(5 * 128 * 8)

threshold = 60
count = 0

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    count += 1

    if count == 5:
        break

    # Check if frame is retrieved successfully
    if not ret:
        break

    # Convert the frame to PIL Image format
    pil_frame = Image.fromarray(frame)

    # Resize and convert the frame to RGB
    resized_frame = pil_frame.resize((128, 64)).convert("RGB")

    for i in range(resized_frame.size[0]):
        for k in range(ceil(resized_frame.size[1] / 8)):
            index = i + k * resized_frame.size[0] + count * 1024
            output[index] = 0
            for j in range(8):
                pixel = resized_frame.getpixel((i, (k * 8) + j))
                magnitude = sum(pixel) / 3
                output[index] |= (magnitude > threshold) << j

# Release the video capture object
cap.release()

print("const unsigned char data[][1024] = {{{}}};".format(", ".join([format(b, '#04x') for b in output])))
