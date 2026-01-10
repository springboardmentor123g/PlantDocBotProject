# PlantDocBot: AI Plant Disease Diagnosis

PlantDocBot is an end-to-end AI application for diagnosing plant diseases. It uses a **Convolutional Neural Network (CNN)** for image-based diagnosis and **Natural Language Processing (NLP)** for symptom-based diagnosis, all integrated into a **React-based ChatGPT-style interface**.

## Features
- **Image Diagnosis**: Upload a photo of a plant leaf to detect diseases using MobileNetV2 (PyTorch).
- **Symptom Diagnosis**: Describe symptoms in text to get a prediction using NLP (TF-IDF).
- **Combined Analysis**: Use both image and text for robust predictions.
- **Treatment Recommendations**: Get causes, treatments, and prevention tips.
- **Interactive Chat UI**: A modern, responsive interface built with React.

## Project Structure
- `frontend/`: React + Vite application
- `backend/`: FastAPI application
  - `app/models/`: AI models (Image & Text)
  - `app/data/`: Disease labels and treatment database

## Setup & Run Instructions

### Prerequisites
- Node.js & npm
- Python 3.9+

### 1. Start the Backend
The backend handles AI inference and API requests.

```bash
cd plantdocbot/backend
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the server
python run.py
```
*Server will start at http://localhost:8001*

### 2. Start the Frontend
The frontend provides the user interface.

```bash
cd plantdocbot/frontend
# Install dependencies (if not already installed)
npm install

# Run the development server
npm run dev
```
*App will verify at http://localhost:5173*

## Usage
1. Open the web app at `http://localhost:5173`.
2. **To use Image:** Click "Upload Image", select a leaf photo, and press Send.
3. **To use Text:** Type symptoms (e.g., "yellow spots on leaves") and press Send.
4. **Combined:** Upload an image AND type a description for better accuracy.

## Models
- **Image Model**: MobileNetV2 fine-tuned on PlantVillage dataset.
- **Text Model**: TF-IDF Vectorizer + SGDClassifier trained on symptom descriptions.

## Credits
- Dataset: [PlantVillage](https://www.kaggle.com/datasets/emmarex/plantdisease)
- Text Data: [HunggingFace](https://huggingface.co/datasets/ButterChicken98/plantvillage-image-text-pairs)
