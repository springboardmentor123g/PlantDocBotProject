import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import os

# Configuration
# Configuration
LOCAL_DATASET_PATH = r"C:\PD\New Plant Diseases Dataset(Augmented)"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# app/models/image_model.py -> app/models/plant_disease_model.pth (same dir)
MODEL_PATH = os.path.join(BASE_DIR, "plant_disease_model.pth")

# All 38 PlantVillage disease classes
CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot", 
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

NUM_CLASSES = len(CLASS_NAMES)  # 38

def get_model():
    """Initializes and returns the model."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Initialize MobileNetV2 exactly as in training script
    model = models.mobilenet_v2(pretrained=False) # No need for internet weights if loading local
    # Replace classifier to match training
    model.classifier[1] = nn.Linear(model.last_channel, NUM_CLASSES)
    
    model = model.to(device)
    
    if os.path.exists(MODEL_PATH):
        print(f"Loading model weights from {MODEL_PATH}")
        try:
            model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
            print("Model weights loaded successfully!")
        except Exception as e:
            print(f"Error loading weights: {e}")
            # Fallback (optional, but good for stability)
            model = models.mobilenet_v2(pretrained=True)
            model.classifier[1] = nn.Linear(model.last_channel, NUM_CLASSES)
            model = model.to(device)
    else:
        print("No trained weights found. Using pretrained MobileNetV2.")
        # Fallback to random/pretrained
        model = models.mobilenet_v2(pretrained=True)
        model.classifier[1] = nn.Linear(model.last_channel, NUM_CLASSES)
        model = model.to(device)
    
    model.eval()
    return model

def transform_image(image_bytes):
    """Preprocesses the image for the model."""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return transform(image).unsqueeze(0)

def predict_image(model, image_bytes, class_names=None):
    """
    Predicts the disease class from an image byte stream.
    Returns: class_name, confidence
    """
    # Use embedded CLASS_NAMES if none provided
    if not class_names:
        class_names = CLASS_NAMES
    
    device = next(model.parameters()).device
    tensor = transform_image(image_bytes).to(device)
    
    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        top_prob, top_catid = torch.topk(probabilities, 1)
        
        confidence = top_prob.item()
        class_idx = top_catid.item()
        
        if class_names and class_idx < len(class_names):
            predicted_class = class_names[class_idx]
        else:
            predicted_class = f"Unknown Disease (Class {class_idx})"
            
    return predicted_class, confidence

def get_class_names():
    """Return the list of class names."""
    return CLASS_NAMES
