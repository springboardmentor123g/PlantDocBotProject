from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os, sqlite3
import tensorflow as tf
import numpy as np
import cv2
from googletrans import Translator
from nlp_db import SYMPTOM_DB, check_symptom

# ================== APP CONFIG ==================
app = Flask(__name__)
app.secret_key = "secret123"

translator = Translator()

DATABASE = "database.db"
UPLOAD_FOLDER = "static/uploads"
DATASET_FOLDER = "dataset"
MODEL_PATH = "plant_model.h5"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

INITIAL_GREETING_EN = "Hello! I'm your agricultural assistant. How can I help you today?"

# ================== DATABASE ==================
def get_db_connection():
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

# ================== LOAD MODEL ==================
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✔ Model loaded successfully")
except Exception as e:
    print("❌ Model load failed:", e)
    model = None

# ================== CLASS NAMES ==================
class_names = sorted([
    d for d in os.listdir(DATASET_FOLDER)
    if os.path.isdir(os.path.join(DATASET_FOLDER, d))
]) if os.path.isdir(DATASET_FOLDER) else []

# ================== IMAGE PREDICTION ==================
def predict_image(img_path):
    try:
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (128, 128))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)
        return class_names[np.argmax(pred)]
    except:
        return "Prediction Failed"

# ================== GREETING TRANSLATION API ==================
@app.route("/translate_greeting", methods=["POST"])
def translate_greeting():
    data = request.get_json(force=True)
    lang = data.get("language", "en")
    try:
        text = translator.translate(INITIAL_GREETING_EN, dest=lang).text
    except:
        text = INITIAL_GREETING_EN
    return jsonify({"greeting": text})

# ================== CHATBOT API ==================
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json(force=True)

    user_msg = (data.get("message") or "").strip()
    image_prediction = data.get("image_prediction")
    image_url = data.get("image_url")
    user_lang = data.get("language", "en")

    reply_parts = []

    # Translate user message → English
    if user_msg:
        try:
            user_msg_en = translator.translate(user_msg, dest="en", src=user_lang).text.lower()
        except:
            user_msg_en = user_msg.lower()
    else:
        user_msg_en = ""

    # ===== IMAGE + TEXT =====
    if image_prediction and user_msg_en:
        reply_parts.append(f"🖼 Image Result: {image_prediction}")

        results = check_symptom(user_msg_en)
        for r in results:
            for symptom, info in r.items():
                reply_parts.append(
                    f"🌿 Symptom: {symptom}\n"
                    f"🦠 Diseases: {', '.join(info.get('diseases', []))}\n"
                    f"🧬 Cause: {info.get('cause')}\n"
                    f"💊 Treatment: {info.get('treatment')}\n"
                    f"🛡 Prevention: {info.get('prevention')}"
                )

    # ===== ONLY TEXT =====
    elif user_msg_en:
        results = check_symptom(user_msg_en)
        for r in results:
            for symptom, info in r.items():
                reply_parts.append(
                    f"🌿 Symptom: {symptom}\n\n"
                    f"🦠 Diseases: {', '.join(info.get('diseases', []))}\n\n"
                    f"🧬 Cause: {info.get('cause')}\n\n"
                    f"💊 Treatment: {info.get('treatment')}\n\n"
                    f"🛡 Prevention: {info.get('prevention')}"
                )

    # ===== ONLY TEXT =====
    elif user_msg_en:
        results = check_symptom(user_msg_en)
        for r in results:
            for symptom, info in r.items():
                reply_parts.append(
                    f"🌿 Symptom: {symptom}\n\n"
                    f"🦠 Diseases: {', '.join(info.get('diseases', []))}\n\n"
                    f"🧬 Cause: {info.get('cause')}\n\n"
                    f"💊 Treatment: {info.get('treatment')}\n\n"
                    f"🛡 Prevention: {info.get('prevention')}"
                )

    # ===== ONLY IMAGE =====
    elif image_prediction:
        d = SYMPTOM_DB.get(image_prediction)
        if d:
            reply_parts.append(
                f"🖼 Disease Detected: {d.get('name', image_prediction)}\n\n"
                f"🌿 Symptoms: {d.get('symptoms')}\n\n"
                f"🧬 Cause: {d.get('cause')}\n\n"
                f"💊 Treatment: {d.get('treatment')}\n\n"
                f"🛡 Prevention: {d.get('prevention')}"
            )
        else:
            reply_parts.append(f"🖼 Disease Detected: {image_prediction}")

    else:
        reply_parts.append("Please type symptoms or upload a plant leaf image.")

    final_en = "\n\n".join(reply_parts)

    try:
        final_translated = translator.translate(final_en, dest=user_lang).text
    except:
        final_translated = final_en

    return jsonify({"reply": final_translated,})

# ================== LOGIN ==================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        session["role"] = request.form.get("role", "farmer")
        return redirect("/admin" if session["role"] == "admin" else "/dashboard")
    return render_template("login.html")

# ================== DASHBOARD ==================
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    uploaded_image = None
    result = None
    error = None

    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]
        if file.filename:
            # Save uploaded file to existing static/uploads
            filename = file.filename.replace(" ", "_")
            filepath = os.path.join("static/uploads", filename)
            file.save(filepath)
            uploaded_image = filename  # pass this to template

            # Optional: predict if model exists
            if model:
                result = predict_image(filepath)
            else:
                error = "Model not loaded"

            # If coming from chat image button, return JSON
            if request.headers.get("X-Chat-Image") == "true":
                return jsonify({"prediction": result})

    return render_template(
        "dashboard.html",
        uploaded_image=uploaded_image,
        result=result,
        error=error
    )


# ================== ADMIN PANEL ==================
@app.route("/admin")
def admin_panel():
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    diseases = conn.execute("SELECT * FROM diseases").fetchall()
    conn.close()
    return render_template("admin_panel.html", diseases=diseases)

@app.route("/add_disease", methods=["POST"])
def add_disease():
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO diseases (disease, symptoms, prevention) VALUES (?, ?, ?)",
        (request.form["disease"], request.form["symptoms"], request.form["prevention"])
    )
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route("/update_disease/<int:id>", methods=["POST"])
def update_disease(id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE diseases SET disease=?, symptoms=?, prevention=? WHERE id=?",
        (request.form["disease"], request.form["symptoms"], request.form["prevention"], id)
    )
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route("/delete_disease/<int:id>")
def delete_disease(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM diseases WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

# ================== HOME & LOGOUT ==================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================== RUN ==================
if __name__ == "__main__":
    app.run(debug=True)
