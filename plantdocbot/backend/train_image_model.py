import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
import kagglehub
import os
import time

# Configuration
# Configuration
BATCH_SIZE = 32
NUM_EPOCHS = 1 # 1 Epoch for quick demo training
LEARNING_RATE = 0.001

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "app", "models", "plant_disease_model.pth")
LABELS_SAVE_PATH = os.path.join(BASE_DIR, "app", "data", "disease_labels.json")

def train_model():
    print("--- Starting Image Model Training Setup ---")
    
    # 1. Setup Dataset Path
    # Corrected path based on directory inspection
    train_dir = r"C:\PD\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\train"
    
    if not os.path.exists(train_dir):
        print(f"Error: Training directory not found at {train_dir}")
        # Last ditch effort check parent just in case
        train_dir = r"C:\PD\New Plant Diseases Dataset(Augmented)\train"
        if not os.path.exists(train_dir):
             print("Error: Dataset absolutely not found. Please check paths.")
             return

    print(f"Looking for training data in: {train_dir}")

    # 2. Data Preprocessing
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    try:
        train_dataset = datasets.ImageFolder(train_dir, transform=transform)
        
        # USE SUBSET FOR SPEED (20% of data)
        # This reduces training time from ~30 mins to ~6 mins
        subset_ratio = 0.2
        train_size = int(subset_ratio * len(train_dataset))
        ignored_size = len(train_dataset) - train_size
        train_subset, _ = torch.utils.data.random_split(train_dataset, [train_size, ignored_size])
        
        train_loader = torch.utils.data.DataLoader(train_subset, batch_size=BATCH_SIZE, shuffle=True)
        print(f"Dataset Size: {len(train_dataset)}")
        print(f"Training on random 20% subset: {len(train_subset)} images")
        print(f"Classes: {len(train_dataset.classes)}")
        
        # Save class names for inference
        import json
        with open(LABELS_SAVE_PATH, "w") as f:
            json.dump(train_dataset.classes, f)
        print(f"Updated {LABELS_SAVE_PATH} with dataset classes.")
            
    except Exception as e:
        print(f"Could not load images: {e}")
        print("Please ensure the dataset path is correct structure.")
        return

    # 3. Model Setup (MobileNetV2)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")
    
    model = models.mobilenet_v2(pretrained=True)
    # Freeze partial layers if needed, but for fine-tuning we often train classifier
    for param in model.parameters():
        param.requires_grad = False # Freeze base
        
    # Replace classifier
    num_classes = len(train_dataset.classes)
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=LEARNING_RATE)

    # 4. Training Loop
    print("Starting training loop...")
    model.train()
    for epoch in range(NUM_EPOCHS):
        running_loss = 0.0
        start = time.time()
        
        for i, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 10 == 0:
                print(f"Epoch {epoch+1}, Batch {i}, Loss: {loss.item():.4f}")
                
        print(f"Epoch {epoch+1} finished. Time: {time.time()-start:.2f}s")

    # 5. Save Model
    print("Saving model...")
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train_model()
