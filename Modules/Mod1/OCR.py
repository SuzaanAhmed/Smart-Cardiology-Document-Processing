import cv2
import pytesseract
import os

# Set Tesseract path (Windows)
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def preprocess_image(image_path):
    img = cv2.imread(image_path)

    # Resize (improves OCR)
    img = cv2.resize(img, None, fx=1.5, fy=1.5)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return thresh


def extract_text_from_image(image_path):
    processed_img = preprocess_image(image_path)

    text = pytesseract.image_to_string(processed_img)

    return text