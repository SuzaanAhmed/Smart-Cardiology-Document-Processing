# ================================
# ECG HEARTBEAT CLASSIFICATION
# CNN + LSTM HYBRID MODEL
# ================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers, backend
import joblib


# ================================
# FOCAL LOSS FOR IMBALANCED DATA
# ================================

def focal_loss(gamma=2.0, alpha=0.25):
    """Focal loss reduces contribution of easy examples, focuses on hard negatives"""
    def focal_loss_fixed(y_true, y_pred):
        epsilon = backend.epsilon()
        y_pred = backend.clip(y_pred, epsilon, 1. - epsilon)
        y_true = tf.cast(y_true, tf.float32)
        alpha_t = alpha * y_true + (1 - alpha) * (1 - y_true)
        p_t = y_true * y_pred + (1 - y_true) * (1 - y_pred)
        focal_weight = backend.pow(1. - p_t, gamma)
        focal_loss = -alpha_t * focal_weight * backend.log(p_t)
        return backend.mean(backend.sum(focal_loss, axis=-1))
    return focal_loss_fixed


# ================================
# LOAD DATASET
# ================================

train_path = "C:/Users/akash/OneDrive/Desktop/New folder (2)/Smart-Cardiology-Document-Processing/Modules/Mod2/archive (1)/mitbih_train.csv"
test_path = "C:/Users/akash/OneDrive/Desktop/New folder (2)/Smart-Cardiology-Document-Processing/Modules/Mod2/archive (1)/mitbih_test.csv"


train_data = pd.read_csv(train_path)
test_data = pd.read_csv(test_path)

print("Train Shape:", train_data.shape)
print("Test Shape:", test_data.shape)


# ================================
# SPLIT FEATURES AND LABELS
# ================================

X_train = train_data.iloc[:, :-1].values
y_train = train_data.iloc[:, -1].values

X_test = test_data.iloc[:, :-1].values
y_test = test_data.iloc[:, -1].values

from sklearn.utils.class_weight import compute_class_weight
import numpy as np

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)

class_weights = dict(enumerate(class_weights))

print("Class Weights:", class_weights)


# ================================
# NORMALIZE DATA
# ================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save scaler (important for testing later)
joblib.dump(scaler, "scaler.pkl")


# ================================
# RESHAPE FOR CNN + LSTM
# ================================

X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)


# ================================
# ONE-HOT ENCODING LABELS
# ================================

y_train_cat = to_categorical(y_train)
y_test_cat = to_categorical(y_test)


# ================================
# BUILD CNN + LSTM MODEL
# ================================

model = Sequential()

# CNN Layer 1
model.add(Conv1D(64, kernel_size=5,
                 activation='relu',
                 input_shape=(X_train.shape[1], 1)))
model.add(BatchNormalization())
model.add(MaxPooling1D(pool_size=2))


# CNN Layer 2
model.add(Conv1D(128, kernel_size=5, activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling1D(pool_size=2))


# LSTM Layer
model.add(LSTM(32, return_sequences=False))


# Dense Layers with L2 Regularization
model.add(Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(Dropout(0.4))
model.add(Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(Dropout(0.3))

# Output Layer (5 classes)
model.add(Dense(5, activation='softmax'))


# ================================
# COMPILE MODEL
# ================================

optimizer = Adam(learning_rate=0.001)  # Increased from 0.0005 for better minority class learning
model.compile(
    optimizer=optimizer,
    loss=focal_loss(gamma=2.0, alpha=0.25),  # Focal loss handles imbalanced data better
    metrics=['accuracy']
)

model.summary()


# ================================
# CALLBACKS
# ================================

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    min_delta=0.001  # Require meaningful improvement
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=0.00001,
    verbose=1
)


# ================================
# TRAIN MODEL
# ================================

history = model.fit(
    X_train,
    y_train_cat,
    epochs=10,
    batch_size=16,  # Smaller batch size for better gradient updates on minority classes
    validation_split=0.2,
    callbacks=[early_stop, reduce_lr],
    class_weight=class_weights,
    verbose=1
)

# ================================
# EVALUATE MODEL
# ================================

loss, accuracy = model.evaluate(X_test, y_test_cat)

print("\nTest Accuracy:", accuracy)


# ================================
# PREDICTIONS
# ================================

predictions = model.predict(X_test)
predictions = np.argmax(predictions, axis=1)


# ================================
# CLASSIFICATION REPORT
# ================================

print("\nClassification Report:\n")
print(classification_report(y_test, predictions))


# ================================
# CONFUSION MATRIX
# ================================

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, predictions))


# ================================
# SAVE MODEL
# ================================

model.save("cnn_lstm_ecg_model.h5")

print("\nModel saved as cnn_lstm_ecg_model.h5")


# ================================
# PLOT TRAINING ACCURACY
# ================================

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Model Accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Train", "Validation"])
plt.show()


# ================================
# PLOT TRAINING LOSS
# ================================

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Model Loss")
plt.ylabel("Loss")
plt.xlabel("Epogich")
plt.legend(["Train", "Validation"])
plt.show()