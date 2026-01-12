import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Simple training data (can be expanded)
texts = [
    "tomato leaf has brown spots",
    "tomato leaf yellow and dry",
    "potato leaf black patches",
    "healthy green leaf",
    "pepper leaf has holes",
    "apple leaf disease",
    "leaf is fresh and healthy"
]

labels = [
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Potato___Early_blight",
    "Healthy",
    "Pepper__bell___Bacterial_spot",
    "Apple___Black_rot",
    "Healthy"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

joblib.dump(model, "models/text_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("✅ Text model trained and saved")
