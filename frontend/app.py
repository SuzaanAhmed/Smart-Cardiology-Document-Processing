# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask, render_template, request, jsonify
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "status": "No file selected"
        })

    

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(file_path) # this is to save the uploaded image file

    try:


        # i want everyone to change the path according to your modules, just mod 1, 2, 3 and 4


        # RUN MODULE 1
        mod1_path = os.path.join(
            "..",
            "Modules",
            "Mod1",
            "main.py"
        )

        subprocess.run(
            ["python", mod1_path],
            check=True
        )


        # RUN MODULE 2

        mod2_path = os.path.join(
            "..",
            "Modules",
            "Mod2",
            "predict.py"
        )

        subprocess.run(
            ["python", mod2_path],
            check=True
        )


        # RUN MODULE 3

        mod3_path = os.path.join(
            "..",
            "Modules",
            "Mod3",
            "app.py"
        )

        subprocess.run(
            ["python", mod3_path],
            check=True
        )


        # RUN MODULE 4

        mod4_path = os.path.join(
            "..",
            "Modules",
            "Mod4",
            "summary.py"
        )

        subprocess.run(
            ["python", mod4_path],
            check=True
        )



        # mod 4 output, read summary here

        summary_folder = os.path.join(
            "..",
            "Modules",
            "Mod4",
            "outputs"
        )

        summary_files = os.listdir(summary_folder)

        latest_summary = ""

        if summary_files:

            latest_file = os.path.join(
                summary_folder,
                summary_files[0]
            )

            with open(latest_file, "r") as f:
                latest_summary = f.read()

        return jsonify({
            "status": "Processing Complete",
            "summary": latest_summary
        })

    except Exception as e:

        return jsonify({
            "status": f"Error: {str(e)}",
            "summary": ""
        })


if __name__ == "__main__":
    app.run(debug=True)