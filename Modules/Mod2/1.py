import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
print("Num GPUs Available:", len(tf.config.list_physical_devices('GPU')))

train_path = "C:/Users/akash/OneDrive/Desktop/New folder (2)/Smart-Cardiology-Document-Processing/Modules/Mod2/archive (1)/mitbih_train.csv"
test_path  = "C:/Users/akash/OneDrive/Desktop/New folder (2)/Smart-Cardiology-Document-Processing/Modules/Mod2/archive (1)/mitbih_test.csv"

train_df = pd.read_csv(train_path, header=None)
test_df  = pd.read_csv(test_path, header=None)

# Split features and labels
X_train = train_df.iloc[:, :-1].values
y_train = train_df.iloc[:, -1].values

X_test = test_df.iloc[:, :-1].values
y_test = test_df.iloc[:, -1].values

# ==============================
# 4. PREPROCESSING
# ==============================

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# Reshape for CNN (samples, timesteps, channels)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test  = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Convert labels to categorical
num_classes = len(np.unique(y_train))
y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test  = tf.keras.utils.to_categorical(y_test, num_classes)

# ==============================
# 5. BUILD CNN MODEL
# ==============================

model = Sequential([
    Conv1D(64, kernel_size=5, activation='relu', input_shape=(X_train.shape[1],1)),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),

    Conv1D(128, kernel_size=5, activation='relu'),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),

    Conv1D(256, kernel_size=3, activation='relu'),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),

    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),

    Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ==============================
# 6. CALLBACKS
# ==============================

callbacks = [
    EarlyStopping(patience=5, restore_best_weights=True),
    ModelCheckpoint("best_model.h5", save_best_only=True)
]

# ==============================
# 7. TRAIN MODEL (BIG BATCH + GPU)
# ==============================

history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=30,
    batch_size=64,   # Large batch size
    callbacks=callbacks,
    verbose=1
)

# ==============================
# 8. EVALUATION
# ==============================

test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print("\nTest Accuracy:", test_acc)
print("Test Loss:", test_loss)

# Predictions
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

# Classification Report
print("\nClassification Report:\n")
print(classification_report(y_true, y_pred_classes))

# ==============================
# 9. CONFUSION MATRIX
# ==============================

cm = confusion_matrix(y_true, y_pred_classes)

plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

# ==============================
# 10. ACCURACY & LOSS CURVES
# ==============================

plt.figure(figsize=(12,5))

# Accuracy
plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.legend()
plt.title("Accuracy Curve")

# Loss
plt.subplot(1,2,2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.legend()
plt.title("Loss Curve")

plt.show()

# ==============================
# 11. SAVE FINAL MODEL
# ==============================

model.save("cnn_heartbeat_model.h5")
print("Model Saved Successfully!")