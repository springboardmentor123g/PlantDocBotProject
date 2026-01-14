import os
import shutil
import random

RAW_DIR = "dataset/raw"
TRAIN_DIR = "dataset/train"
VALID_DIR = "dataset/valid"

SPLIT_RATIO = 0.8  # 80% train, 20% validation

os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VALID_DIR, exist_ok=True)

for class_name in os.listdir(RAW_DIR):
    class_path = os.path.join(RAW_DIR, class_name)

    if not os.path.isdir(class_path):
        continue

    images = os.listdir(class_path)
    random.shuffle(images)

    split_point = int(len(images) * SPLIT_RATIO)
    train_images = images[:split_point]
    valid_images = images[split_point:]

    os.makedirs(os.path.join(TRAIN_DIR, class_name), exist_ok=True)
    os.makedirs(os.path.join(VALID_DIR, class_name), exist_ok=True)

    for img in train_images:
        shutil.copy(
            os.path.join(class_path, img),
            os.path.join(TRAIN_DIR, class_name, img)
        )

    for img in valid_images:
        shutil.copy(
            os.path.join(class_path, img),
            os.path.join(VALID_DIR, class_name, img)
        )

print("✅ Dataset split completed successfully")
