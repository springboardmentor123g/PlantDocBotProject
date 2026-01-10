from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import os

from app.models.image_model import get_model, predict_image, get_class_names, CLASS_NAMES
from app.models.text_model import predict_symptom

app = FastAPI(title="PlantDocBot API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get absolute path to data files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Disease labels are imported from image_model
print(f"Loaded {len(CLASS_NAMES)} disease classes from model config")

TREATMENTS_PATH = os.path.join(BASE_DIR, "data", "treatments.json")

# Load treatments
try:
    with open(TREATMENTS_PATH, 'r') as f:
        TREATMENTS = json.load(f)
    print(f"Loaded treatments for {len(TREATMENTS)} diseases")
except FileNotFoundError:
    TREATMENTS = {}
    print("No treatments file found, using defaults")

# Load treatments
try:
    with open(TREATMENTS_PATH, 'r') as f:
        TREATMENTS = json.load(f)
    print(f"Loaded treatments for {len(TREATMENTS)} diseases from JSON")
except Exception as e:
    TREATMENTS = {}
    print(f"Error loading treatments.json: {e}")
    # Minimal fallback
    TREATMENTS = {
        "Tomato___Late_blight": {
            "causes": "Phytophthora infestans.",
            "treatment": "Fungicides.",
            "prevention": "Resistant varieties."
        }
    }

# Initialize Image Model
image_model = get_model()

def format_disease_name(disease_raw):
    """Convert disease code to readable format."""
    if not disease_raw:
        return "Unknown"
    # Apple___Apple_scab -> Apple - Apple Scab
    parts = disease_raw.replace("___", " - ").replace("_", " ")
    return parts.title()

def get_treatment_info(disease_name):
    """Retrieve treatment info for a disease."""
    info = TREATMENTS.get(disease_name, {
        "causes": "This condition may be caused by various environmental or pathogenic factors.",
        "treatment": "Consult a local agricultural extension office for specific treatment advice.",
        "prevention": "Maintain good crop hygiene, proper spacing, and regular monitoring."
    })
    return info

@app.get("/")
def read_root():
    return {"message": "PlantDocBot API is running", "classes": len(CLASS_NAMES)}

@app.post("/predict-image")
async def predict_image_endpoint(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    try:
        image_bytes = await file.read()
        disease, confidence = predict_image(image_model, image_bytes, CLASS_NAMES)
        
        readable_disease = format_disease_name(disease)
        treatment_info = get_treatment_info(disease)
        
        return {
            "disease": readable_disease,
            "disease_code": disease,
            "confidence": f"{confidence*100:.2f}%",
            "treatment": treatment_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-text")
async def predict_text_endpoint(text: str = Form(...), context_disease: Optional[str] = Form(None)):
    try:
        disease, confidence = predict_symptom(text)
        
        # Threshold Logic
        if confidence < 0.35:
            # Low confidence - check if it's a follow-up question about context
            if context_disease and context_disease != "Unknown":
                info = get_treatment_info(context_disease)
                text_lower = text.lower()
                disease_name = format_disease_name(context_disease)
                
                # Conversational Q&A
                answer = ""
                if any(x in text_lower for x in ["prevent", "avoid", "stop", "protect"]):
                    answer = f"To prevent **{disease_name}**, you should: {info['prevention']}"
                elif any(x in text_lower for x in ["treat", "cure", "fix", "medicine", "control"]):
                    answer = f"For treatment of **{disease_name}**, typically: {info['treatment']}"
                elif any(x in text_lower for x in ["cause", "why", "happed", "happen", "reason"]): 
                     # 'happed' covers 'happend' typo
                    answer = f"Regarding your question, **{disease_name}** is {info['causes'].lower()}"
                elif any(x in text_lower for x in ["what", "explain", "detail", "about"]):
                     answer = f"Here is a summary for **{disease_name}**:\n\n*   **Causes:** {info['causes']}\n*   **Treatment:** {info['treatment']}"
                
                if answer:
                    return {
                        "type": "chat",
                        "message": answer,
                        "confidence": "Context Q&A"
                    }

            return {
                "type": "chat",
                "message": "I'm not sure I understand the symptom. Could you describe specific visual spots, colors, or patterns? Or upload a photo!",
                "confidence": f"{confidence*100:.2f}%"
            }
            
        readable_disease = format_disease_name(disease)
        treatment_info = get_treatment_info(disease)
        
        return {
            "type": "diagnosis",
            "disease": readable_disease,
            "disease_code": disease,
            "confidence": f"Text Analysis ({confidence*100:.2f}%)",
            "treatment": treatment_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-combined")
async def predict_combined_endpoint(file: UploadFile = File(...), text: str = Form(...)):
    try:
        image_bytes = await file.read()
        img_disease, img_conf = predict_image(image_model, image_bytes, CLASS_NAMES)
        txt_disease, txt_conf = predict_symptom(text)
        
        final_disease = img_disease
        source = "Image Analysis"
        final_conf = img_conf
        
        # Logic: If image is weak but text is strong, use text.
        if img_conf < 0.55 and txt_conf > 0.4:
            final_disease = txt_disease
            source = "Symptom Analysis"
            final_conf = txt_conf
            
        readable_disease = format_disease_name(final_disease)
        treatment_info = get_treatment_info(final_disease)
        
        # Check if text is a question about the diagnosis (Combined Q&A)
        chat_response = None
        if txt_conf < 0.35: # Text is likely not a symptom description
             info = treatment_info
             text_lower = text.lower()
             answer = ""
             if any(x in text_lower for x in ["prevent", "avoid", "stop", "protect"]):
                 answer = f"To prevent this, ensure to: {info['prevention']}"
             elif any(x in text_lower for x in ["treat", "cure", "fix", "medicine", "control"]):
                 answer = f"The recommended treatment is: {info['treatment']}"
             elif any(x in text_lower for x in ["cause", "why", "happed", "happen", "reason"]):
                 answer = f"To answer your question, this is {info['causes'].lower()}"
             elif any(x in text_lower for x in ["what", "explain", "detail", "about"]):
                 answer = f"Here is the summary you asked for:\n\n*   **Causes:** {info['causes']}\n*   **Treatment:** {info['treatment']}"
             
             if answer:
                 chat_response = answer

        return {
            "type": "diagnosis",
            "disease": readable_disease,
            "disease_code": final_disease,
            "confidence": f"{final_conf*100:.2f}% (Source: {source})",
            "treatment": treatment_info,
            "text_analysis_note": "Text analysis was used to refine the result." if source == "Symptom Analysis" else None,
            "chat_response": chat_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
