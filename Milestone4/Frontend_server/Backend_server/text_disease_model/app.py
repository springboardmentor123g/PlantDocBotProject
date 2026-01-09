from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io, base64
import torch
from torchvision import transforms
from model import MyCNNModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__)
CORS(app)

# ================= IMAGE MODEL =================
CLASSES = [
    'Apple___Apple_scab','Apple___Black_rot','Apple___Cedar_apple_rust','Apple___healthy',
    'Blueberry___healthy','Cherry___Powdery_mildew','Cherry___healthy',
    'Corn___Cercospora_leaf_spot Gray_leaf_spot','Corn___Common_rust','Corn___Northern_Leaf_Blight','Corn___healthy',
    'Grape___Black_rot','Grape___Esca_(Black_Measles)','Grape___Leaf_blight_(Isariopsis_Leaf_Spot)','Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)','Peach___Bacterial_spot','Peach___healthy',
    'Pepper,_bell___Bacterial_spot','Pepper,_bell___healthy',
    'Potato___Early_blight','Potato___Late_blight','Potato___healthy',
    'Raspberry___healthy','Soybean___healthy','Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch','Strawberry___healthy',
    'Tomato___Bacterial_spot','Tomato___Early_blight','Tomato___Late_blight','Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot','Tomato___Spider_mites Two-spotted_spider_mite','Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus','Tomato___Tomato_mosaic_virus','Tomato___healthy'
]

device = torch.device("cpu")

image_model = MyCNNModel(len(CLASSES))
image_model.load_state_dict(torch.load("plant_disease_cnn.pth", map_location=device))
image_model.eval()

transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor()
])

# ================= TEXT MODEL =================
TEXT_CLASSES = [
    'Apple Scab', 'Apple Black Rot', 'Apple Cedar Apple Rust', 'Apple Healthy',
    'Blueberry Healthy', 'Cherry Powdery Mildew', 'Cherry Healthy',
    'Corn Gray Leaf Spot', 'Corn Common Rust', 'Corn Northern Leaf Blight', 'Corn Healthy',
    'Grape Black Rot', 'Grape Esca', 'Grape Leaf Blight', 'Grape Healthy',
    'Orange Huanglongbing', 'Peach Bacterial Spot', 'Peach Healthy',
    'Pepper Bacterial Spot', 'Pepper Healthy',
    'Potato Early Blight', 'Potato Late Blight', 'Potato Healthy',
    'Raspberry Healthy', 'Soybean Healthy', 'Squash Powdery Mildew',
    'Strawberry Leaf Scorch', 'Strawberry Healthy',
    'Tomato Bacterial Spot', 'Tomato Early Blight', 'Tomato Late Blight',
    'Tomato Leaf Mold', 'Tomato Septoria Leaf Spot', 'Tomato Spider Mites',
    'Tomato Target Spot', 'Tomato Yellow Leaf Curl Virus', 'Tomato Mosaic Virus', 'Tomato Healthy'
]

TEXT_MODEL_PATH = "text_disease_model"
text_tokenizer = AutoTokenizer.from_pretrained(TEXT_MODEL_PATH)
text_model = AutoModelForSequenceClassification.from_pretrained(TEXT_MODEL_PATH)
text_model.eval()

# ================= API =================
@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    image_base64 = data.get("img")
    text_input = data.get("q")

    image_pred = None
    text_pred = None

    try:
        # ---------- IMAGE ----------
        if image_base64:
            img_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            image = transform(image).unsqueeze(0)

            with torch.no_grad():
                outputs = image_model(image)
                pred_idx = torch.argmax(outputs, dim=1)

            image_pred = CLASSES[pred_idx.item()]

        # ---------- TEXT ----------
        if text_input and text_input.strip() != "":
            inputs = text_tokenizer(
                text_input,
                return_tensors="pt",
                truncation=True,
                padding=True
            )

            with torch.no_grad():
                outputs = text_model(**inputs)
                pred_idx = torch.argmax(outputs.logits, dim=1)

            text_pred = TEXT_CLASSES[pred_idx.item()]

        # ---------- FUSION (IMAGE PRIORITY) ----------
        if image_pred and text_pred:
            final_prediction = image_pred   # image gets more weight
        elif image_pred:
            final_prediction = image_pred
        elif text_pred:
            final_prediction = text_pred
        else:
            return jsonify({"error": "No input provided"})

        return jsonify({
            "final_prediction": final_prediction
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
