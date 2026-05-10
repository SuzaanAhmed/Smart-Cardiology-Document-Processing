import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.layers import Reshape, LSTM
from tensorflow.keras.preprocessing.image import ImageDataGenerator

dataset_path = "dataset"

if not os.path.exists(dataset_path):
    raise ValueError(f"Dataset folder not found: {dataset_path}")

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(128,128),
    batch_size=4,
    class_mode='categorical',
    subset='training'
)

val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(128,128),
    batch_size=4,
    class_mode='categorical',
    subset='validation'
)

print("Detected classes:", train_data.class_indices)

num_classes = len(train_data.class_indices)

if num_classes == 0:
    raise ValueError("No class folders detected inside dataset directory!")

model = Sequential()

model.add(Conv2D(32,(3,3),activation='relu',
                 input_shape=(128,128,3)))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))

model.add(Flatten())

model.add(Reshape((1,-1)))

model.add(LSTM(64))

model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(num_classes,activation='softmax'))

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=10
)

os.makedirs("models", exist_ok=True)

model.save("models/ecg_cnn_lstm_model.h5")

print("CNN + LSTM model trained successfully")