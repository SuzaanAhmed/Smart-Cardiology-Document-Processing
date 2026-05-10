import os
from OCR import extract_text_from_image
from NLP import extract_fields

data_folder = "data"

for file in os.listdir(data_folder):
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        path = os.path.join(data_folder, file)

        print("\n========================================")
        print(f"📄 Processing: {file}")
        print("========================================")

        text = extract_text_from_image(path)

        print("\n--- OCR TEXT ---\n")
        print(text[:800])

        data = extract_fields(text)

        print("\n--- EXTRACTED DATA ---\n")
        for k, v in data.items():
            print(f"{k}: {v}")