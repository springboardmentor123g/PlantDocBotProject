from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from PIL import Image
import io, json, os


app = Flask(__name__)
CORS(app)

IMG_SIZE = 224
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#loading cnn model

print("Loading CNN model...")
try:
    state_dict = torch.load("models/plant_disease_mobilenet.pth", map_location=device)

    with open("models/class_names.json", "r") as f:
        class_names = json.load(f)

    if isinstance(class_names, dict):
        class_names = {int(k): v for k, v in class_names.items()}

    cnn_model = models.mobilenet_v2(pretrained=False)
    cnn_model.classifier[1] = nn.Linear(cnn_model.last_channel, len(class_names))
    cnn_model.load_state_dict(state_dict)
    cnn_model.to(device)
    cnn_model.eval()

    print(" CNN model loaded")
except Exception as e:
    print(" CNN load failed:", e)
    cnn_model = None
    class_names = {}

# image transforming
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

#loading nlp model

print("Loading NLP model...")
try:
    NLP_PATH = "models/plant_nlp_model"

    nlp_tokenizer = AutoTokenizer.from_pretrained(NLP_PATH)
    nlp_model = AutoModelForSequenceClassification.from_pretrained(NLP_PATH)
    nlp_model.to(device)
    nlp_model.eval()

    with open(f"{NLP_PATH}/label_encoder.json", "r") as f:
        label_data = json.load(f)
        id2label = {int(k): v for k, v in label_data["id2label"].items()}

    print(" NLP model loaded")
except Exception as e:
    print("NLP fallback:", e)
    nlp_model = None
    nlp_tokenizer = None
    id2label = {}

#loading disease information

try:
    with open("utils/disease_info.json", "r") as f:
        disease_info = json.load(f)
    print(f" Disease info loaded: {len(disease_info)} diseases")
    print(f" Available keys: {list(disease_info.keys())[:5]}...")  # Debug: show first 5 keys
except Exception as e:
    print(f" Failed to load disease_info.json: {e}")
    disease_info = {}



def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return transform(img).unsqueeze(0).to(device)

def predict_from_image(image_bytes):
    if cnn_model is None:
        return None, 0, []

    img = preprocess_image(image_bytes)

    with torch.no_grad():
        out = cnn_model(img)
        probs = torch.softmax(out, dim=1)[0]

    idx = torch.argmax(probs).item()
    conf = float(probs[idx])

    top_probs, top_idx = torch.topk(probs, min(3, len(probs)))

    top_3 = [{
        "disease": class_names[int(i)],
        "confidence": float(p)
    } for i, p in zip(top_idx, top_probs)]

    return class_names[idx], conf, top_3

def predict_from_text(text):
    if nlp_model is None:
        return "Unknown", 0.5, [{"disease": "Unknown", "confidence": 0.5}]

    inputs = nlp_tokenizer(
        text, return_tensors="pt",
        truncation=True, padding=True, max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = nlp_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]

    idx = torch.argmax(probs).item()
    conf = float(probs[idx])

    top_probs, top_idx = torch.topk(probs, min(3, len(probs)))

    top_3 = [{
        "disease": id2label[int(i)],
        "confidence": float(p)
    } for i, p in zip(top_idx, top_probs)]

    return id2label[idx], conf, top_3

def normalize_disease_name(name):
    
    if not name:
        return name
    
    # Remove extra underscores (some models use ___)
    name = name.replace('___', '_')
    
    # Remove commas and extra spaces
    name = name.replace(',', '').strip()
    
    # Split into parts
    parts = name.split()
    
    # Handle different naming patterns
    if len(parts) == 0:
        return name
    
    # Build normalized name
    normalized_parts = []
    
    for i, part in enumerate(parts):
        part_clean = part.strip('_')
        
        if i == 0:
            # First part: capitalize (Tomato, Potato, Pepper, etc.)
            normalized_parts.append(part_clean.capitalize())
        elif i == 1 and part_clean.lower() in ['bell', 'maize']:
            # Second part if it's 'bell' or 'maize': lowercase
            normalized_parts.append(part_clean.lower())
        elif part_clean.lower() in ['healthy', 'spot', 'blight', 'rust', 'scab', 'rot', 'mold', 'mildew', 'virus', 'scorch']:
            # Common disease keywords: lowercase
            normalized_parts.append(part_clean.lower())
        else:
            # Everything else: capitalize first letter
            normalized_parts.append(part_clean.capitalize())
    
    result = '_'.join(normalized_parts)
    
    print(f" Normalized: '{name}' → '{result}'")
    
    return result

def get_disease_information(name):
    """Get disease information with improved key matching"""
    
    print(f"\n{'='*60}")
    print(f" Looking up disease information")
    print(f"{'='*60}")
    print(f" Model output: '{name}'")
    
    # Try normalized key first
    normalized_key = normalize_disease_name(name)
    print(f" Normalized key: '{normalized_key}'")
    
    # Try exact match with normalized key
    if normalized_key in disease_info:
        print(f" Found exact match!")
        return disease_info[normalized_key]
    
    # Try case-insensitive match
    for key in disease_info:
        if key.lower() == normalized_key.lower():
            print(f" Found case-insensitive match: '{key}'")
            return disease_info[key]
    
    # Try alternative formats
    alternatives = [
        name.replace(',', '').replace(' ', '_'),  # Remove commas, replace spaces
        name.replace(', ', '_').replace(' ', '_'),  # Replace comma-space and spaces
        name.replace('___', '_'),  # Triple underscore to single
        name.replace('__', '_'),  # Double underscore to single
    ]
    
    for alt in alternatives:
        alt_normalized = normalize_disease_name(alt)
        print(f" Trying alternative: '{alt_normalized}'")
        
        if alt_normalized in disease_info:
            print(f" Found match with alternative format!")
            return disease_info[alt_normalized]
        
        # Case-insensitive check for alternative
        for key in disease_info:
            if key.lower() == alt_normalized.lower():
                print(f" Found case-insensitive match with alternative: '{key}'")
                return disease_info[key]
    
    # Last resort: partial match (for debugging)
    print(f" No exact match found. Available keys containing '{normalized_key.split('_')[0]}':")
    matching_keys = [k for k in disease_info.keys() if normalized_key.split('_')[0].lower() in k.lower()]
    for mk in matching_keys[:5]:
        print(f"   - {mk}")
    
    print(f" No match found. Returning default information.")
    print(f"{'='*60}\n")
    
    # Return default information
    return {
        "description": f"Information for {name} is not available in the database.",
        "symptoms": ["Please consult agricultural experts for detailed information"],
        "treatment": ["Consult local agricultural extension service", "Contact plant pathology expert"],
        "prevention": ["Practice good agricultural hygiene", "Monitor plants regularly"]
    }



@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "cnn_loaded": cnn_model is not None,
        "nlp_loaded": nlp_model is not None,
        "disease_db_loaded": len(disease_info) > 0,
        "disease_count": len(disease_info)
    })



@app.route("/predict/image", methods=["POST"])
def predict_image():
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image provided"}), 400
        
        image = request.files["image"].read()
        disease, conf, top3 = predict_from_image(image)
        
        if disease is None:
            return jsonify({"success": False, "error": "CNN model not loaded"}), 500

        return jsonify({
            "success": True,
            "prediction": {
                "disease": disease,
                "confidence": conf,
                "top_3_predictions": top3
            },
            "information": get_disease_information(disease)
        })
    
    except Exception as e:
        print(f" Error in predict_image: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

#prediction of text

@app.route("/predict/text", methods=["POST"])
def predict_text():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"success": False, "error": "No text provided"}), 400
        
        text = data.get("text", "").strip()
        
        if not text:
            return jsonify({"success": False, "error": "Empty text provided"}), 400
        
        disease, conf, top3 = predict_from_text(text)

        return jsonify({
            "success": True,
            "prediction": {
                "disease": disease,
                "confidence": conf,
                "top_3_predictions": top3
            },
            "information": get_disease_information(disease)
        })
    
    except Exception as e:
        print(f" Error in predict_text: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

#combined prediction

@app.route("/predict/combined", methods=["POST"])
def predict_combined():
    try:
        image_result = None
        text_result = None

        # Process image if provided
        if "image" in request.files:
            disease, conf, top3 = predict_from_image(request.files["image"].read())
            if disease:
                image_result = {
                    "disease": disease,
                    "confidence": conf,
                    "top_3_predictions": top3
                }

        # Process text if provided
        text = request.form.get("text", "").strip()
        if text:
            disease, conf, top3 = predict_from_text(text)
            text_result = {
                "disease": disease,
                "confidence": conf,
                "top_3_predictions": top3
            }

        # Determine final prediction (higher confidence wins)
        if image_result and text_result:
            if image_result["confidence"] >= text_result["confidence"]:
                final = image_result
            else:
                final = text_result
        elif image_result:
            final = image_result
        elif text_result:
            final = text_result
        else:
            return jsonify({"success": False, "error": "No valid input provided"}), 400

        return jsonify({
            "success": True,
            "final_disease": final["disease"],
            "image_prediction": image_result,
            "text_prediction": text_result,
            "information": get_disease_information(final["disease"])
        })
    
    except Exception as e:
        print(f"Error in predict_combined: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500



@app.route("/diseases", methods=["GET"])
def list_diseases():
    """Debug endpoint to see all available diseases"""
    return jsonify({
        "total": len(disease_info),
        "diseases": list(disease_info.keys())
    })

#running server

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" PlantDocBot Backend Starting...")
    print("="*60)
    print(f"CNN Model: {' OK' if cnn_model else ' FAIL'}")
    print(f"NLP Model: {' OK' if nlp_model else 'FALLBACK'}")
    print(f"Disease DB: {' OK' if disease_info else ' FAIL'} ({len(disease_info)} diseases)")
    print(f"Device: {device}")
    print("="*60)
    print(" Server: http://127.0.0.1:5000")
    print(" Health check: http://127.0.0.1:5000/health")
    print(" Disease list: http://127.0.0.1:5000/diseases")
    print("="*60 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)