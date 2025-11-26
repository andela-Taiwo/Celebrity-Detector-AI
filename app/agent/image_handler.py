import cv2
import numpy as np
from io import BytesIO
from typing import Optional


def process_image(image_file: BytesIO) -> tuple[bytes, Optional[tuple[int, int]]]:
    """
    Process an uploaded image and highlight the largest detected face.

    Step-by-step:
    1. Save the incoming file to an in-memory buffer and extract the raw bytes.
    2. Convert the bytes to a NumPy array and decode it into an OpenCV image.
    3. Transform the image to grayscale to optimize face detection.
    4. Load OpenCV's Haar cascade classifier and detect faces in the grayscale image.
    5. If no faces are found, return the original bytes and `None`.
    6. Choose the largest detected face, draw a bounding box on the color image, and
       re-encode it as JPEG bytes.
    7. Return the updated image bytes along with the bounding box coordinates.
    """
    in_memory_file = BytesIO()
    image_file.save(in_memory_file)
    image_bytes = in_memory_file.getvalue()

    np_array = np.frombuffer(image_bytes, np.uint8)

    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(gray_image, 1.1, 5)

    if len(faces) == 0:
        return image_bytes, None
    largest_face = max(faces, key=lambda x: x[2] * x[3])

    (x, y, w, h) = largest_face
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)

    is_success, buffer = cv2.imencode(".jpg", image)

    return buffer.tobytes(), largest_face
