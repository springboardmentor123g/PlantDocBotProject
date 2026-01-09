

"""
Plant Disease Detection Server - Fixed with Correct Endpoints

This server connects to your Colab-trained model via ngrok for real-time predictions.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
import uuid
from datetime import datetime
from PIL import Image
import io
import traceback
import requests

# Constants
UPLOAD_DIR = "uploads"
DATA_FILE = "data.json"
MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}






# 🔥 NGROK CONFIGURATION
# Copy your ngrok URL from Colab (e.g., "https://1234-xx-xx-xx.ngrok-free.app")
NGROK_URL = "https://hydrographic-rhetorically-spring.ngrok-free.dev"  # ⚠️ UPDATE THIS AFTER RUNNING COLAB
PREDICTION_ENDPOINT = f"{NGROK_URL}/predict"
HEALTH_ENDPOINT = f"{NGROK_URL}/health"

# Disease classes mapping (for reference)
DISEASE_CLASSES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_data_file():
    """Initialize data.json file"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"chats": {}}, f, indent=4)
        return
    
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        if "chats" not in data:
            data["chats"] = {}
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
    except Exception as e:
        print(f"⚠️ Error reading data file: {e}")
        with open(DATA_FILE, "w") as f:
            json.dump({"chats": {}}, f, indent=4)

init_data_file()


def parse_class_name(class_name):
    """Parse disease class name into plant and disease"""
    parts = class_name.replace('_', ' ').split('   ')
    if len(parts) >= 2:
        plant = parts[0].strip()
        disease = parts[1].strip()
        is_healthy = 'healthy' in disease.lower()
        return plant, disease, is_healthy
    return "Unknown", class_name, False


def get_treatment_advice(disease_name):
    """Get treatment advice based on disease"""
    disease_lower = disease_name.lower()
    
    treatments = {
        "healthy": "✅ Your plant looks healthy! Continue with regular care:\n• Water consistently\n• Ensure adequate sunlight\n• Monitor for any changes\n• Maintain proper soil nutrition",
        
        "apple scab": "🍎 Apple Scab Treatment:\n• Remove and destroy infected leaves\n• Apply fungicide (Captan or Myclobutanil)\n• Improve air circulation by pruning\n• Avoid overhead watering\n• Clean up fallen leaves in autumn",
        
        "black rot": "⚫ Black Rot Treatment:\n• Prune infected branches 8-12 inches below lesions\n• Apply copper-based fungicide\n• Remove mummified fruits immediately\n• Improve drainage\n• Practice crop rotation",
        
        "cedar apple rust": "🍂 Cedar Apple Rust Treatment:\n• Remove galls from nearby cedar trees\n• Apply fungicide in early spring\n• Plant resistant varieties\n• Maintain proper spacing for air flow",
        
        "powdery mildew": "🌫️ Powdery Mildew Treatment:\n• Improve air circulation\n• Reduce humidity\n• Apply sulfur-based fungicide or neem oil\n• Remove infected leaves\n• Water at base, not leaves",
        
        "bacterial spot": "🦠 Bacterial Spot Treatment:\n• Remove infected leaves immediately\n• Apply copper-based bactericide\n• Use drip irrigation (avoid overhead watering)\n• Ensure proper plant spacing\n• Disinfect tools between cuts",
        
        "early blight": "🍂 Early Blight Treatment:\n• Remove infected lower leaves\n• Apply fungicide (Chlorothalonil or Mancozeb)\n• Mulch around plants to prevent soil splash\n• Practice 3-year crop rotation\n• Ensure adequate spacing",
        
        "late blight": "⚠️ Late Blight Treatment (URGENT):\n• Act quickly - spreads rapidly!\n• Remove and destroy infected plants\n• Apply fungicide preventively to healthy plants\n• Avoid overhead watering\n• Improve drainage",
        
        "leaf spot": "🍃 Leaf Spot Treatment:\n• Remove infected leaves\n• Improve drainage and air circulation\n• Apply appropriate fungicide\n• Avoid wetting foliage\n• Clean up plant debris",
        
        "rust": "🦀 Rust Treatment:\n• Remove infected leaves promptly\n• Apply fungicide (sulfur or copper-based)\n• Ensure good air circulation\n• Avoid overhead watering\n• Plant resistant varieties",
        
        "cercospora": "Cercospora Leaf Spot Treatment:\n• Remove infected leaves\n• Ensure proper plant spacing\n• Apply fungicide if severe\n• Improve drainage\n• Rotate crops",
        
        "esca": "🍇 Esca (Black Measles) Treatment:\n• Prune infected vines carefully\n• Improve drainage\n• No cure - manage symptoms\n• Protect pruning wounds\n• Remove severely infected plants",
        
        "haunglongbing": "🍊 Citrus Greening Treatment:\n• ⚠️ No cure available\n• Remove and destroy infected trees\n• Control Asian citrus psyllid (vector)\n• Use disease-free planting material\n• Report to agricultural authorities",
        
        "septoria": "Septoria Leaf Spot Treatment:\n• Remove infected lower leaves\n• Apply fungicide preventively\n• Avoid overhead watering\n• Mulch to prevent soil splash\n• Practice crop rotation",
        
        "spider mites": "🕷️ Spider Mites Treatment:\n• Spray plants with water to dislodge\n• Use insecticidal soap or neem oil\n• Introduce predatory mites\n• Increase humidity\n• Remove heavily infested leaves",
        
        "target spot": "🎯 Target Spot Treatment:\n• Remove infected leaves\n• Apply fungicide (Chlorothalonil)\n• Improve air circulation\n• Reduce humidity\n• Practice crop rotation",
        
        "mosaic virus": "🦠 Mosaic Virus Treatment:\n• Remove and destroy infected plants\n• Control aphids (disease vectors)\n• Use virus-free seeds/transplants\n• Disinfect tools\n• Plant resistant varieties",
        
        "yellow leaf curl": "💛 Yellow Leaf Curl Virus Treatment:\n• Control whiteflies (primary vector)\n• Remove infected plants\n• Use insect-proof screening\n• Plant resistant varieties\n• Use reflective mulches",
    }
    
    # Find matching treatment
    for key, treatment in treatments.items():
        if key in disease_lower:
            return treatment
    
    # Default treatment
    return "🔬 General Treatment Recommendations:\n• Consult with a local agricultural expert\n• Take clear photos for diagnosis\n• Monitor plant regularly\n• Remove infected parts if safe\n• Maintain good cultural practices"


class RemoteModelPredictor:
    """Connects to the Colab model via ngrok"""
    
    def __init__(self, ngrok_url):
        self.ngrok_url = ngrok_url
        self.prediction_endpoint = f"{ngrok_url}/predict"
        self.health_endpoint = f"{ngrok_url}/health"
        self.is_connected = self.check_connection()
    
    def check_connection(self):
        """Verify connection to Colab model"""
        try:
            response = requests.get(self.health_endpoint, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Connected to Colab model")
                print(f"   Status: {data.get('status', 'Unknown')}")
                print(f"   Model: {data.get('model', 'Unknown')}")
                print(f"   Classes: {data.get('num_classes', 'Unknown')}")
                return True
            else:
                print(f"⚠️ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to Colab model: {e}")
            print(f"   Make sure ngrok tunnel is running in Colab")
            print(f"   Current URL: {self.ngrok_url}")
            return False
    
    def predict(self, image_path):
        """Send image to Colab for prediction"""
        try:
            print(f"📤 Sending image to Colab: {image_path}")
            
            with open(image_path, 'rb') as f:
                files = {'file': ('plant_image.jpg', f, 'image/jpeg')}
                response = requests.post(
                    self.prediction_endpoint,
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                
                # Parse the class name
                predicted_class = result.get('class', result.get('predicted_class', 'Unknown'))
                plant, disease, is_healthy = parse_class_name(predicted_class)
                
                # Format confidence - handle string and numeric types
                confidence = result.get('confidence', result.get('probability', 0))
                try:
                    # Convert to float if it's a string
                    if isinstance(confidence, str):
                        confidence = float(confidence)
                    
                    # Format based on value
                    if isinstance(confidence, (int, float)):
                        confidence_str = f"{confidence*100:.2f}%" if confidence <= 1 else f"{confidence:.2f}%"
                    else:
                        confidence_str = "N/A"
                except (ValueError, TypeError):
                    confidence_str = str(confidence) if confidence else "N/A"
                
                # Get treatment advice
                treatment = get_treatment_advice(disease)
                
                # Structure the response
                prediction_result = {
                    "plant": plant,
                    "disease": disease,
                    "confidence": confidence_str,
                    "is_healthy": is_healthy,
                    "raw_class": predicted_class,
                    "treatment": treatment,
                    "success": True
                }
                
                # Add top predictions if available
                if 'top_predictions' in result:
                    top_preds = []
                    for pred in result['top_predictions']:
                        pred_plant, pred_disease, pred_healthy = parse_class_name(pred.get('class', ''))
                        pred_conf = pred.get('probability', pred.get('confidence', 0))
                        # Handle string confidence values
                        try:
                            if isinstance(pred_conf, str):
                                pred_conf = float(pred_conf)
                            pred_conf_str = f"{pred_conf*100:.2f}%" if pred_conf <= 1 else f"{pred_conf:.2f}%"
                        except (ValueError, TypeError):
                            pred_conf_str = str(pred_conf) if pred_conf else "N/A"
                        top_preds.append({
                            "plant": pred_plant,
                            "disease": pred_disease,
                            "confidence": pred_conf_str,
                            "is_healthy": pred_healthy
                        })
                    prediction_result['top_predictions'] = top_preds
                
                print(f"✅ Prediction successful")
                print(f"   Plant: {plant}")
                print(f"   Disease: {disease}")
                print(f"   Confidence: {confidence_str}")
                
                return prediction_result
            
            else:
                print(f"❌ Prediction failed: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return {
                    "error": f"Prediction failed: {response.status_code}",
                    "plant": "Unknown",
                    "disease": "Prediction Error",
                    "success": False
                }
        
        except requests.exceptions.Timeout:
            print("❌ Prediction timeout")
            return {
                "error": "Prediction timeout - model took too long to respond",
                "plant": "Unknown",
                "disease": "Request Timeout",
                "success": False
            }
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            traceback.print_exc()
            return {
                "error": str(e),
                "plant": "Unknown",
                "disease": "Error Occurred",
                "success": False
            }


# Initialize remote predictor
print("\n🌍 Initializing Remote Model Connection...")
if NGROK_URL == "YOUR_NGROK_URL_HERE":
    print("❌ ERROR: Please update NGROK_URL in the code!")
    print("   1. Run the Colab notebook Cell 12")
    print("   2. Copy the ngrok URL from the output")
    print("   3. Update NGROK_URL variable in this file")
    print("   4. Restart this server")
    disease_model = None
else:
    disease_model = RemoteModelPredictor(NGROK_URL)

print()


def parse_multipart(body, boundary):
    """Enhanced multipart parser"""
    parts = {}
    files = {}
    
    try:
        sections = body.split(b'--' + boundary.encode())
        
        for section in sections:
            if not section or section == b'--\r\n' or section == b'--':
                continue
            
            if b'\r\n\r\n' not in section:
                continue
            
            header_part, content = section.split(b'\r\n\r\n', 1)
            content = content.rstrip(b'\r\n')
            
            header_lines = header_part.decode('utf-8', errors='ignore').split('\r\n')
            disposition = None
            
            for line in header_lines:
                if line.startswith('Content-Disposition:'):
                    disposition = line
                    break
            
            if not disposition:
                continue
            
            name = None
            filename = None
            
            if 'name="' in disposition:
                name_start = disposition.index('name="') + 6
                name_end = disposition.index('"', name_start)
                name = disposition[name_start:name_end]
            
            if 'filename="' in disposition:
                fn_start = disposition.index('filename="') + 10
                fn_end = disposition.index('"', fn_start)
                filename = disposition[fn_start:fn_end]
            
            if filename:
                files[name] = {'filename': filename, 'content': content}
            else:
                parts[name] = content.decode('utf-8', errors='ignore')
    
    except Exception as e:
        print(f"Error parsing multipart: {e}")
    
    return parts, files


class PlantDocHandler(BaseHTTPRequestHandler):
    """HTTP request handler"""
    
    def log_message(self, format, *args):
        if self.path.startswith('/uploads/'):
            return
        print(f"{self.address_string()} - [{self.log_date_time_string()}] {format%args}")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests"""
        try:
            if disease_model is None:
                self.send_error(503, "Model not connected. Please configure NGROK_URL.")
                return
            
            if not disease_model.is_connected:
                self.send_error(503, "Model connection lost. Check Colab ngrok tunnel.")
                return
            
            parsed_url = urllib.parse.urlparse(self.path)

            if parsed_url.path != "/submit":
                self.send_error(404, "Endpoint not found")
                return

            params = urllib.parse.parse_qs(parsed_url.query)
            q_text = params.get("q", [""])[0]
            img_token = params.get("img", [""])[0]
            chat_id = params.get("chat_id", [None])[0]
            
            if chat_id in ['', 'null', 'undefined', None]:
                chat_id = None
            
            print(f"\n{'='*60}")
            print(f"📨 RECEIVED REQUEST")
            print(f"{'='*60}")
            print(f"chat_id: {chat_id}")
            print(f"text: {q_text[:50] if q_text else 'None'}")
            print(f"image: {img_token if img_token else 'None'}")

            content_length = int(self.headers.get("Content-Length", 0))
            
            if content_length > MAX_IMAGE_SIZE:
                self.send_error(413, "Request too large")
                return
            
            body = self.rfile.read(content_length)

            saved_image_url = None
            disease_prediction = None
            has_image = False
            has_text = bool(q_text and q_text.strip())
            
            content_type = self.headers.get("Content-Type", "")
            
            # Parse multipart form data
            if "multipart/form-data" in content_type:
                boundary = content_type.split("boundary=")[1]
                parts, files = parse_multipart(body, boundary)

                if 'image' in files:
                    has_image = True
                    file_info = files['image']
                    file_data = file_info['content']
                    filename = file_info['filename']
                    
                    file_ext = os.path.splitext(filename)[1].lower()
                    if file_ext not in ALLOWED_EXTENSIONS:
                        self.send_error(400, "Invalid file type")
                        return

                    img_id = str(uuid.uuid4())
                    img_path = f"{UPLOAD_DIR}/{img_id}.jpg"

                    try:
                        # Save and process image
                        img = Image.open(io.BytesIO(file_data)).convert('RGB')
                        img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                        img.save(img_path, "JPEG", quality=85, optimize=True)
                        saved_image_url = f"/uploads/{img_id}.jpg"
                        
                        print(f"🔬 Sending image to Colab for prediction...")
                        disease_prediction = disease_model.predict(img_path)
                        
                    except Exception as e:
                        print(f"Error processing image: {e}")
                        traceback.print_exc()
                        self.send_error(500, "Image processing failed")
                        return

            # Build response text based on what we have
            response_text = ""
            
            # SCENARIO 1: Both image and text (80% image, 20% text consideration)
            if has_image and has_text and disease_prediction and disease_prediction.get('success'):
                plant = disease_prediction['plant']
                disease = disease_prediction['disease']
                confidence = disease_prediction['confidence']
                is_healthy = disease_prediction.get('is_healthy', False)
                treatment = disease_prediction.get('treatment', '')
                
                # Add text context to response
                if is_healthy:
                    response_text = f"🌿 **{plant}** - Healthy Plant!\n\n"
                    response_text += f"✅ Your plant appears to be in excellent health.\n"
                    response_text += f"📊 Image Analysis Confidence: {confidence}\n\n"
                    response_text += f"💬 **Your Question:** {q_text}\n\n"
                    response_text += f"Regarding your question, your {plant} looks healthy. "
                    response_text += "If you have specific concerns, please describe the symptoms you're observing.\n\n"
                    response_text += treatment
                else:
                    response_text = f"🔬 **Plant Disease Analysis**\n\n"
                    response_text += f"🌱 **Plant Type:** {plant}\n"
                    response_text += f"⚠️ **Disease Detected:** {disease}\n"
                    response_text += f"📊 **Image Analysis Confidence:** {confidence}\n\n"
                    response_text += f"💬 **Your Question:** {q_text}\n"
                    response_text += f"Based on both the image analysis (80% weight) and your question about '{q_text}', "
                    response_text += f"the primary diagnosis is {disease}.\n\n"
                    response_text += f"**💊 Treatment Recommendations:**\n{treatment}\n"
                    
                    # Add alternative predictions
                    if disease_prediction.get('top_predictions') and len(disease_prediction['top_predictions']) > 1:
                        response_text += "\n\n**🔍 Alternative Diagnoses:**\n"
                        for i, pred in enumerate(disease_prediction['top_predictions'][1:4], 2):
                            response_text += f"{i}. {pred['plant']} - {pred['disease']} ({pred['confidence']})\n"
                        response_text += "\n💡 If these symptoms match your observations better, focus on the corresponding treatment."
            
            # SCENARIO 2: Image only
            elif has_image and not has_text and disease_prediction and disease_prediction.get('success'):
                plant = disease_prediction['plant']
                disease = disease_prediction['disease']
                confidence = disease_prediction['confidence']
                is_healthy = disease_prediction.get('is_healthy', False)
                treatment = disease_prediction.get('treatment', '')
                
                if is_healthy:
                    response_text = f"🌿 **{plant}** - Healthy Plant!\n\n"
                    response_text += f"✅ Your plant appears to be in excellent health.\n"
                    response_text += f"📊 Confidence: {confidence}\n\n"
                    response_text += treatment
                else:
                    response_text = f"🔬 **Plant Disease Analysis**\n\n"
                    response_text += f"🌱 **Plant Type:** {plant}\n"
                    response_text += f"⚠️ **Disease Detected:** {disease}\n"
                    response_text += f"📊 **Confidence:** {confidence}\n\n"
                    response_text += f"**💊 Treatment Recommendations:**\n{treatment}\n"
                    
                    if disease_prediction.get('top_predictions') and len(disease_prediction['top_predictions']) > 1:
                        response_text += "\n\n**🔍 Alternative Diagnoses:**\n"
                        for i, pred in enumerate(disease_prediction['top_predictions'][1:4], 2):
                            response_text += f"{i}. {pred['plant']} - {pred['disease']} ({pred['confidence']})\n"
            
            # SCENARIO 3: Failed image prediction
            elif has_image and disease_prediction and not disease_prediction.get('success'):
                error_msg = disease_prediction.get('error', 'Unknown error')
                response_text = f"❌ **Prediction Failed**\n\n"
                response_text += f"Error: {error_msg}\n\n"
                if has_text:
                    response_text += f"💬 Your question: {q_text}\n\n"
                response_text += "Please try again or check:\n"
                response_text += "• Image quality and clarity\n"
                response_text += "• Ensure the image shows plant leaves clearly\n"
                response_text += "• Check Colab ngrok connection\n"
                response_text += "• Verify network connectivity"
            
            # SCENARIO 4: Text only (no image)
            elif has_text and not has_image:
                response_text = f"💬 **Question Received:** {q_text}\n\n"
                response_text += "📸 **Please upload an image** for accurate disease detection.\n\n"
                response_text += "Our AI model analyzes plant leaf images to detect:\n"
                response_text += "• Disease type and severity\n"
                response_text += "• Specific plant species\n"
                response_text += "• Treatment recommendations\n\n"
                response_text += "💡 **Tip:** Take a clear photo of the affected leaves in good lighting for best results."
                
                # Create a text-only prediction object
                disease_prediction = {
                    "plant": "Unknown",
                    "disease": "Image Required",
                    "confidence": "N/A",
                    "is_healthy": False,
                    "treatment": "Please upload a clear image of your plant for analysis.",
                    "success": False,
                    "text_only": True
                }
            
            # SCENARIO 5: Nothing provided
            else:
                response_text = "Please provide either:\n"
                response_text += "• 📸 An image of your plant for disease detection\n"
                response_text += "• 💬 A question about plant care\n"
                response_text += "• 🖼️ Both for comprehensive analysis"

            # Create message object
            message = {
                "timestamp": datetime.now().isoformat(),
                "query_text": q_text,
                "image_token": img_token,
                "bw_image_url": saved_image_url,
                "disease_prediction": disease_prediction,
                "response_text": response_text,
                "has_image": has_image,
                "has_text": has_text
            }

            # Save to database
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            
            if "chats" not in data:
                data["chats"] = {}

            if chat_id and chat_id in data["chats"]:
                print(f"✅ APPENDING to existing chat: {chat_id}")
                data["chats"][chat_id]["messages"].append(message)
                data["chats"][chat_id]["updated_at"] = datetime.now().isoformat()
                
                # Update title if needed
                if data["chats"][chat_id]["title"] in ["New Chat", "Image upload", "New Plant Analysis"]:
                    if disease_prediction and disease_prediction.get('success'):
                        plant = disease_prediction.get('plant', 'Unknown')
                        disease = disease_prediction.get('disease', 'Unknown')
                        data["chats"][chat_id]["title"] = f"{plant} - {disease}"
                    elif has_text:
                        data["chats"][chat_id]["title"] = q_text[:50] + ("..." if len(q_text) > 50 else "")
            else:
                chat_id = str(uuid.uuid4())
                print(f"🆕 Creating NEW chat: {chat_id}")
                
                # Create meaningful title
                if disease_prediction and disease_prediction.get('success'):
                    title = f"{disease_prediction['plant']} - {disease_prediction['disease']}"
                elif has_text:
                    title = q_text[:50] + ("..." if len(q_text) > 50 else "")
                else:
                    title = "New Plant Analysis"
                
                data["chats"][chat_id] = {
                    "id": chat_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "title": title,
                    "messages": [message]
                }

            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)

            response = {
                "chat_id": chat_id,
                "message": message,
                "success": True
            }

            print(f"📤 Response sent successfully\n{'='*60}\n")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            print(f"Error in POST handler: {e}")
            traceback.print_exc()
            self.send_error(500, f"Server error: {str(e)}")





    def do_DELETE(self):
        """Handle chat deletion"""
        try:
            if self.path.startswith("/chat/"):
                chat_id = self.path.split("/chat/")[1]
                
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                
                if chat_id in data["chats"]:
                    # Delete associated images
                    for msg in data["chats"][chat_id]["messages"]:
                        if msg.get("bw_image_url"):
                            img_path = "." + msg["bw_image_url"]
                            if os.path.exists(img_path):
                                os.remove(img_path)
                    
                    del data["chats"][chat_id]
                    
                    with open(DATA_FILE, "w") as f:
                        json.dump(data, f, indent=4)
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode())
                else:
                    self.send_error(404, "Chat not found")
            else:
                self.send_error(404, "Invalid endpoint")
        
        except Exception as e:
            print(f"Error in DELETE handler: {e}")
            self.send_error(500, f"Server error: {str(e)}")

    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path.startswith("/uploads/"):
                filepath = "." + self.path
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        self.send_response(200)
                        self.send_header("Content-Type", "image/jpeg")
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Cache-Control', 'public, max-age=31536000')
                        self.end_headers()
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "Image not found")
            
            elif self.path == "/data":
                with open(DATA_FILE) as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(f.read().encode())
            
            elif self.path.startswith("/chat/"):
                chat_id = self.path.split("/chat/")[1]
                with open(DATA_FILE) as f:
                    data = json.load(f)
                    if chat_id in data["chats"]:
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(data["chats"][chat_id]).encode())
                    else:
                        self.send_error(404, "Chat not found")
            
            else:
                self.send_error(404, "Endpoint not found")
        
        except Exception as e:
            print(f"Error in GET handler: {e}")
            traceback.print_exc()
            self.send_error(500, f"Server error: {str(e)}")


if __name__ == "__main__":
    server_address = ("localhost", 8000)
    httpd = HTTPServer(server_address, PlantDocHandler)
    
    print("\n" + "="*70)
    print("🌱 Plant Disease Detection Server")
    print("="*70)
    print(f"🌍 Server running at http://localhost:8000")
    
    if disease_model and disease_model.is_connected:
        print(f"✅ Connected to Colab model via ngrok")
        print(f"🔗 ngrok URL: {NGROK_URL}")
        print(f"✨ Ready to process plant disease predictions!")
    else:
        print(f"❌ Not connected to Colab model")
        print(f"⚠️  Please update NGROK_URL in the code")
        print(f"   1. Run Colab Cell 12")
        print(f"   2. Copy ngrok URL")
        print(f"   3. Update NGROK_URL variable")
        print(f"   4. Restart server")
    
    print("="*70)
    print("Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()