from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
import joblib
import json
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Load trained models
image_model = tf.keras.models.load_model("models/image_model.h5")
text_model = joblib.load("models/text_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

# Load class names for image model
with open("models/class_names.json", "r") as f:
    class_names = json.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    image_prediction = ""
    text_prediction = ""

    if request.method == "POST":

        # -------- IMAGE PREDICTION --------
        if "image" in request.files:
            file = request.files["image"]
            if file.filename != "":
                img = Image.open(file).convert("RGB")
                img = img.resize((224, 224))
                img = np.array(img) / 255.0
                img = np.expand_dims(img, axis=0)

                pred = image_model.predict(img)
                predicted_index = np.argmax(pred)
                image_prediction = class_names[predicted_index]

        # -------- TEXT PREDICTION --------
        if request.form.get("query"):
            query = request.form["query"]
            vec = vectorizer.transform([query])
            text_prediction = text_model.predict(vec)[0]

    return render_template(
        "index.html",
        image_prediction=image_prediction,
        text_prediction=text_prediction
    )


if __name__ == "__main__":
    app.run(debug=True)
