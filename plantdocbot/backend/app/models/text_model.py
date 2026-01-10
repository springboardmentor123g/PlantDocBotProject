import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_PATH = "app/models/text_model.pkl"

class SymptomClassifier:
    def __init__(self):
        self.model = None
        self._auto_init()

    def _auto_init(self):
        """Auto-initialize with built-in symptom data for fast startup."""
        if os.path.exists(MODEL_PATH):
            self.load_model()
        else:
            print("Training text model with built-in symptom data...")
            self._train_fast()

    def _train_fast(self):
        """Train instantly using built-in symptom-disease mappings."""
        texts, labels = self._get_symptom_data()
        
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=3000, stop_words='english', ngram_range=(1, 2))),
            ('clf', LogisticRegression(max_iter=500, random_state=42))
        ])
        
        print(f"Training on {len(texts)} symptom samples...")
        self.model.fit(texts, labels)
        
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(self.model, f)
        print("Text model ready!")

    def _get_symptom_data(self):
        """Comprehensive symptom training data for all 38 disease classes."""
        data = {
            "Apple___Apple_scab": [
                "dark olive green spots on apple leaves", "velvety texture on leaf surface",
                "leaves curling and distorted", "scab lesions on apple fruit", "brown scabby patches"
            ],
            "Apple___Black_rot": [
                "brown rotting spots on apple", "concentric rings on fruit lesions",
                "frog eye leaf spot on apple", "black pycnidia on rotted areas", "fruit mummies"
            ],
            "Apple___Cedar_apple_rust": [
                "bright orange spots on apple leaves", "yellow spots with red border",
                "tube-like projections under leaves", "rust colored pustules", "orange gelatinous spore horns"
            ],
            "Apple___healthy": ["green healthy apple leaves", "no spots or discoloration", "normal leaf texture", "healthy apple tree"],
            "Blueberry___healthy": ["healthy blueberry plant", "green blueberry leaves", "no disease symptoms"],
            "Cherry_(including_sour)___Powdery_mildew": [
                "white powdery coating on cherry leaves", "curled distorted leaves",
                "stunted shoot growth", "powdery fungal growth"
            ],
            "Cherry_(including_sour)___healthy": ["healthy cherry leaves", "green cherry plant", "no visible disease"],
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": [
                "rectangular gray lesions on corn", "lesions parallel to veins",
                "gray leaf spot on maize", "tan colored spots"
            ],
            "Corn_(maize)___Common_rust_": [
                "reddish brown pustules on corn", "rust colored spots both sides",
                "powdery spores on leaves", "cinnamon brown pustules"
            ],
            "Corn_(maize)___Northern_Leaf_Blight": [
                "long elliptical gray green lesions", "cigar shaped spots on corn",
                "lesions parallel to leaf veins", "tan brown elongated spots"
            ],
            "Corn_(maize)___healthy": ["healthy corn plant", "green maize leaves", "no spots or lesions"],
            "Grape___Black_rot": [
                "brown circular spots with dark border", "tiny black dots in lesions",
                "shriveled mummified grapes", "reddish brown leaf spots"
            ],
            "Grape___Esca_(Black_Measles)": [
                "tiger stripe pattern on grape leaves", "interveinal discoloration",
                "dark spots on berries", "wood decay symptoms"
            ],
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": [
                "angular reddish brown spots", "leaf blight on grape",
                "dark brown lesions with yellow halo"
            ],
            "Grape___healthy": ["healthy grape vine", "green grape leaves", "no disease symptoms"],
            "Orange___Haunglongbing_(Citrus_greening)": [
                "yellow shoots on citrus", "blotchy mottled leaves",
                "asymmetric chlorosis", "lopsided bitter fruit", "citrus greening disease"
            ],
            "Peach___Bacterial_spot": [
                "angular water soaked lesions on peach", "dark spots on fruit",
                "shot hole symptoms", "gumming on branches"
            ],
            "Peach___healthy": ["healthy peach tree", "green peach leaves", "no visible problems"],
            "Pepper,_bell___Bacterial_spot": [
                "small raised spots on pepper leaves", "water soaked lesions",
                "spots with yellow halo", "scab like spots on fruit"
            ],
            "Pepper,_bell___healthy": ["healthy bell pepper plant", "green pepper leaves", "no visible problems"],
            "Potato___Early_blight": [
                "dark brown spots on potato leaves", "target board pattern",
                "concentric rings on lesions", "lower leaves affected first"
            ],
            "Potato___Late_blight": [
                "water soaked spots on potato", "white mold on leaf undersides",
                "rapidly spreading infection", "brown tuber rot", "potato dying rapidly"
            ],
            "Potato___healthy": ["healthy potato plant", "green potato leaves", "no visible disease"],
            "Raspberry___healthy": ["healthy raspberry plant", "green raspberry leaves", "no disease symptoms"],
            "Soybean___healthy": ["healthy soybean plant", "green soybean leaves", "normal growth"],
            "Squash___Powdery_mildew": [
                "white powdery spots on squash", "circular white patches",
                "leaves turning yellow", "powdery coating spreading"
            ],
            "Strawberry___Leaf_scorch": [
                "purple spots on strawberry leaves", "leaf margins turning brown",
                "irregular purple blotches", "scorched leaf appearance"
            ],
            "Strawberry___healthy": ["healthy strawberry plant", "green strawberry leaves", "no visible problems"],
            "Tomato___Bacterial_spot": [
                "small dark spots on tomato leaves", "water soaked lesions",
                "yellow halo around spots", "spots on tomato fruit", "bacterial infection on tomato"
            ],
            "Tomato___Early_blight": [
                "concentric rings on tomato leaves", "target like spots",
                "brown lesions on lower leaves", "yellowing around spots"
            ],
            "Tomato___Late_blight": [
                "water soaked gray green spots", "white fuzzy growth under leaves",
                "rapidly spreading lesions", "brown rotting on tomato fruit"
            ],
            "Tomato___Leaf_Mold": [
                "yellow spots on upper leaf surface", "olive green mold underneath",
                "velvety fungal growth", "leaves turning brown and dying"
            ],
            "Tomato___Septoria_leaf_spot": [
                "small circular spots with dark border", "gray centers with dark edges",
                "many tiny spots on leaves", "lower leaves affected first"
            ],
            "Tomato___Spider_mites Two-spotted_spider_mite": [
                "tiny yellow spots stippling", "webbing on leaf undersides",
                "bronze discolored leaves", "spider mite damage"
            ],
            "Tomato___Target_Spot": [
                "concentric ring spots", "brown target shaped lesions",
                "spots with light center dark edge"
            ],
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus": [
                "leaves curling upward", "yellow leaf margins",
                "stunted plant growth", "small cupped leaves"
            ],
            "Tomato___Tomato_mosaic_virus": [
                "mottled light dark green pattern", "mosaic pattern on leaves",
                "distorted leaf growth", "fernlike leaves"
            ],
            "Tomato___healthy": ["healthy green tomato plant", "no disease symptoms", "normal tomato leaves"]
        }
        
        texts, labels = [], []
        for disease, symptoms in data.items():
            for symptom in symptoms:
                texts.append(symptom)
                labels.append(disease)
        return texts, labels

    def load_model(self):
        try:
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            print("Text model loaded successfully.")
        except Exception as e:
            print(f"Error loading: {e}")
            self._train_fast()

    def predict(self, text):
        if not self.model:
            return "Model not loaded", 0.0
            
        # Get probability for the prediction
        probs = self.model.predict_proba([text])[0]
        max_prob = max(probs)
        prediction = self.model.predict([text])[0]
        
        return prediction, max_prob

# Initialize on module load
text_classifier = SymptomClassifier()

def predict_symptom(text):
    return text_classifier.predict(text)
