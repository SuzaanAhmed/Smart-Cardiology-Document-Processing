from OCR import extract_text_from_image
from NLP import extract_fields

# Path to your ECG image
image_path = "data/ecg1.jpg"

# Step 1: OCR
text = extract_text_from_image(image_path)

print("\n================ OCR TEXT ================\n")
print(text[:1500])

# Step 2: NLP Extraction
data = extract_fields(text)

print("\n============= EXTRACTED DATA =============\n")
for key, value in data.items():
    print(f"{key}: {value}")