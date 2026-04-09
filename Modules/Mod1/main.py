from ocr import extract_text_from_image
from nlp import extract_fields

# Image path
image_path = "data/ecg_sample.png"

# Step 1: OCR
text = extract_text_from_image(image_path)

print("\n================ OCR TEXT ================\n")
print(text[:1000])

# Step 2: NLP Extraction
data = extract_fields(text)

print("\n============= EXTRACTED DATA =============\n")
for key, value in data.items():
    print(f"{key}: {value}")