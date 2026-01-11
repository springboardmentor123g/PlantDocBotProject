import tensorflow as tf
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

# Load model
model = tf.keras.models.load_model("plant_model.h5")

# Get class names from dataset folder
dataset_folder = "dataset"
class_names = [name for name in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, name))]
class_names.sort()
print("Classes:", class_names)

def predict_image(img_path):
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (128,128))
    img_norm = img_resized / 255.0
    img_exp = np.expand_dims(img_norm, axis=0)

    prediction = model.predict(img_exp)
    class_id = np.argmax(prediction)
    predicted_class = class_names[class_id]

    # Display image with prediction
    plt.imshow(img_rgb)
    plt.title(f"Predicted: {predicted_class}")
    plt.axis("off")
    plt.show()

# Predict all images in test_images folder
folder_path = "test_images"
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(folder_path, filename)
        print("\nPredicting:", filename)
        predict_image(img_path)
