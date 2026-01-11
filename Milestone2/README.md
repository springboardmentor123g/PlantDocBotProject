🌱 AgroBot 

AgroBot is a simple and smart system that detects plant diseases using Deep Learning (CNN) and answers user questions using an NLP chatbot.
It now supports multilanguage chat, so users can ask doubts in any language (Telugu, Hindi, Tamil, English, etc.).

🚀 Overview

AgroBot is a complete AI system built using:

🧠 CNN Model (TensorFlow/Keras) for detecting diseases from plant leaf images.

💬 NLP Engine for symptom-based text queries

🌐 Flask Web App for user interaction

🖼️ Image Upload to analyze plant leaves

🌏 Multilanguage Support → auto-detects language and replies back

📄 MIT Licensed for open-source usage

This system helps farmers and students quickly identify plant diseases and get treatment suggestions.

🖼️ Demo Workflow

1️⃣ Upload an image of a plant leaf
2️⃣ CNN model predicts the disease
3️⃣ NLP system handles text-based queries like:
“My potato has brown spots”
4️⃣ Web UI displays:
✔ Detected disease
✔ Causes
✔ Symptoms
✔ Treatment
✔ Prevention
✔ Possible alternative diseases

🛠️ Tech Stack
Component	-->Technology
Frontend	-->HTML, CSS, Bootstrap
Backend	-->Flask (Python)
AI Model-->	TensorFlow, Keras
NLP	Custom symptom-disease database
Storage	Local file storage
Deployment	GitHub / PythonAnywhere / Render


🧩 Key Features
✔ 1. Plant Disease Classification (CNN)

Real-time prediction from leaf images.

✔ 2. NLP Chatbot

Understands symptoms and replies with:

Disease

Cause

Treatment

Prevention

Possible diseases

✔ 3. Multilanguage Chat

Supports any language:

Hindi

Telugu

Tamil

Malayalam

English

Kannada

Bengali
…and more.

✔ 4. Login System

Simple username + password authentication.






⚙️ How to Run
Step 1 — Install Dependencies
pip install -r requirements.txt


(If you want, I can create this file for you.)

Step 2 — Run the Flask App
python app.py

Step 3 — Open in Browser
http://127.0.0.1:5000/

