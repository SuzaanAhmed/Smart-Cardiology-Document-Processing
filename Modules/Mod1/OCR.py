import cv2
import pytesseract
import os

# Set Tesseract path (Windows)
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def preprocess_image(image_path):
    img = cv2.imread(image_path)

    # Rotate image (important for your ECG)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # Resize (improves OCR)
    img = cv2.resize(img, None, fx=2, fy=2)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Binary threshold
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return thresh


def extract_text_from_image(image_path):
    processed = preprocess_image(image_path)

    # OCR configuration
    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(processed, config=custom_config)

    return text