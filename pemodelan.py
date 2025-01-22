import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Path dataset
dataset_path = r"C:\robot arm berbasis speech recognition\dataset"

# Mengecek keberadaan folder dataset
if not os.path.exists(dataset_path):
    print(f"Error: The path {dataset_path} does not exist.")
else:
    # Inisialisasi list untuk fitur dan label
    features = []
    labels = []

    # Membaca folder dataset
    for label in os.listdir(dataset_path):
        label_path = os.path.join(dataset_path, label)
        if os.path.isdir(label_path):  # Memastikan folder
            print(f"Loading files from: {label_path}")
            for file in os.listdir(label_path):
                if file.endswith(".wav"):  # Memastikan format file adalah .wav
                    file_path = os.path.join(label_path, file)
                    try:
                        # Memuat file audio
                        audio, sr = librosa.load(file_path, sr=None)
                        # Ekstraksi fitur MFCC
                        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
                        mfcc = np.mean(mfcc.T, axis=0)  # Rata-rata MFCC

                        # Menambahkan fitur dan label ke list
                        features.append(mfcc)
                        labels.append(label)

                    except Exception as e:
                        print(f"Error processing {file}: {e}")

    # Memeriksa apakah fitur dan label telah diisi
    if len(features) == 0 or len(labels) == 0:
        print("Error: No valid data found. Check dataset paths and files.")
    else:
        print(f"Loaded {len(features)} samples.")

        # Mengonversi fitur dan label ke array numpy
        features = np.array(features)
        labels = np.array(labels)

        # Encoding label ke integer
        label_encoder = LabelEncoder()
        labels = label_encoder.fit_transform(labels)

        # Membagi data untuk training dan validation (80% training, 20% validasi)
        x_train, x_val, y_train, y_val = train_test_split(features, labels, test_size=0.2, random_state=42)

        # Membuat model neural network menggunakan Keras
        model = Sequential()
        model.add(Dense(128, input_dim=x_train.shape[1], activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(len(np.unique(labels)), activation='softmax'))  # Output sesuai jumlah kelas

        # Menyusun model
        model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # Melatih model
        model.fit(x_train, y_train, epochs=300, batch_size=32, validation_data=(x_val, y_val))

        # Menghitung akurasi pada data validasi
        _, accuracy = model.evaluate(x_val, y_val)
        print(f"Validation accuracy: {accuracy:.2f}")

        # Membuat prediksi pada data validasi
        y_pred = np.argmax(model.predict(x_val), axis=-1)

        # Membuat confusion matrix
        cm = confusion_matrix(y_val, y_pred)

        # Menampilkan confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("True Label")
        plt.show()
