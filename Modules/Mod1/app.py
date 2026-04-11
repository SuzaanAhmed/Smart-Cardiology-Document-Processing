from flask import Flask, render_template, request
import os
from OCR import extract_text_from_image
from NLP import extract_fields
from storage import save_all

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    extracted_data = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            text = extract_text_from_image(path)
            data = extract_fields(text)

            extracted_data = save_all(data)

    return render_template("index.html", data=extracted_data)


if __name__ == "__main__":
    app.run(debug=True)