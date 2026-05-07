import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    # Resize
    img = cv2.resize(img, None, fx=1.5, fy=1.5)

    h, w, _ = img.shape

    # Rotate if vertical
    if h > w:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    h, w, _ = img.shape

    # Focus on top area
    crop = img[0:int(h * 0.40), :]

    # grayscale
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # Slight blur
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # OCR
    results = reader.readtext(gray)

    text = ""
    for (bbox, txt, prob) in results:
        if prob > 0.4:
            text += txt + " "

    return text