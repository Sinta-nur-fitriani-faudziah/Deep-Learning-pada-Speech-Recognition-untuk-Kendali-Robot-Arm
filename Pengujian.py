import numpy as np
import tensorflow as tf
from tensorflow import keras
import librosa
import sounddevice as sd
import soundfile as sf
import serial
import time

# Ambang batas untuk suara beramplitudo kecil
MIN_AMPLITUDE_THRESHOLD = 0.01

def preprocess_audio(audio_path):
    """
    Mengubah audio menjadi Mel-spectrogram untuk digunakan dalam prediksi.
    """
    audio, sample_rate = librosa.load(audio_path, sr=None)
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sample_rate)
    mel_spectrogram = np.expand_dims(mel_spectrogram, axis=-1)
    return mel_spectrogram

def load_model(model_path):
    """
    Memuat model yang sudah dilatih dari path yang diberikan.
    """
    return keras.models.load_model(model_path)

def predict_audio(model, audio_data):
    """
    Memprediksi kelas dari audio yang sudah diproses.
    """
    predictions = model.predict(np.expand_dims(audio_data, axis=0))
    predicted_label = np.argmax(predictions[0])  # Mendapatkan label dengan probabilitas tertinggi
    return predicted_label

def record_audio(file_path, model, duration=2, sample_rate=22050):
    """
    Merekam suara selama durasi yang ditentukan dan mengirimkan prediksi ke Arduino.
    """
    print("Tekan Enter untuk merekam suara atau tekan 'Ctrl+c' untuk berhenti...")

    arduino_port = "COM5"  # Ubah sesuai port Arduino
    arduino = serial.Serial(arduino_port, baudrate=9600, timeout=1)
    time.sleep(2)  # Tunggu Arduino siap

    class_labels = {0: 'ambil', 1: 'simpan'}  # Label untuk kelas suara yang diprediksi

    try:
        while True:
            input("Tekan Enter untuk merekam...")
            # Merekam suara selama durasi yang ditentukan
            audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
            sd.wait()  # Tunggu hingga perekaman selesai

            # Mengecek apakah amplitudo suara cukup besar
            if np.max(np.abs(audio)) < MIN_AMPLITUDE_THRESHOLD:
                print("Suara terlalu kecil. Melewati prediksi.")
                continue

            # Menyimpan audio yang direkam ke file
            sf.write(file_path, audio, sample_rate)

            # Mengolah audio untuk prediksi
            audio_data = preprocess_audio(file_path)

            # Melakukan prediksi dengan model
            predicted_label = predict_audio(model, audio_data)
            predicted_class = class_labels[predicted_label]

            print(f"Prediksi kelas: {predicted_class}")

            # Mengirim hasil prediksi ke Arduino melalui serial
            arduino.write(predicted_class.encode())
            time.sleep(4)  # Memberikan waktu tunda setelah mengirim data ke Arduino

    except KeyboardInterrupt:
        print("\nProgram berhenti.")
        arduino.close()  # Menutup koneksi serial dengan Arduino

if __name__ == "__main__":
    model_path = r"C:\robot arm berbasis speech recognition\model_fix.keras"  # Ubah sesuai dengan path model Anda
    audio_path = "recorded_audio.wav"  # File path untuk menyimpan audio yang direkam
    model = load_model(model_path)  # Memuat model yang sudah dilatih
    record_audio(audio_path, model)  # Memulai perekaman dan prediksi
