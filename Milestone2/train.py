import tensorflow as tf
import matplotlib.pyplot as plt

dataset_path = "dataset"   # folder where all class folders exist

# Load dataset and automatically split 80% train, 20% test
train_data = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    image_size=(128,128),
    batch_size=32,
    validation_split=0.2,
    subset="training",
    seed=42
)

valid_data = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    image_size=(128,128),
    batch_size=32,
    validation_split=0.2,
    subset="validation",
    seed=42
)

class_names = train_data.class_names
print("Number of classes:", len(class_names))
print("Classes:", class_names)

# Normalization
AUTOTUNE = tf.data.AUTOTUNE

train_data = train_data.map(lambda x, y: (tf.cast(x, tf.float32)/255.0, y)).prefetch(AUTOTUNE)
valid_data = valid_data.map(lambda x, y: (tf.cast(x, tf.float32)/255.0, y)).prefetch(AUTOTUNE)

# CNN Model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation="relu", input_shape=(128,128,3)),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(64, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(128, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(class_names), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(train_data, validation_data=valid_data, epochs=10)

model.save("plant_model.h5")
print("Model saved!")
