import os
import sounddevice as sd
import soundfile as sf
from datetime import datetime

def record_audio(file_path, duration=2, sample_rate=22050):
    """
    Fungsi untuk merekam audio dan menyimpannya ke file WAV.
    """
    print("Mulai merekam...")
    try:
        # Rekam audio
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()  # Tunggu hingga proses rekaman selesai
        print("Selesai merekam.")
        # Simpan audio ke file WAV
        sf.write(file_path, audio, sample_rate)
    except Exception as e:
        print(f"Terjadi kesalahan saat merekam: {e}")

if __name__ == "__main__":
    data_path = "dataset"
    sample_rate = 22050  # Hertz
    duration = 2  # Durasi rekaman dalam detik
    num_samples_per_digit = 5

    # Membuat folder dataset jika belum ada
    os.makedirs(data_path, exist_ok=True)

    print("Proses perekaman dimulai. Tekan Ctrl+C untuk berhenti kapan saja.")
    try:
        for i in range(num_samples_per_digit):
            print(f"\nRekaman ke-{i+1}.")
            print("Masukkan kode angka (0-5):")
            while True:
                try:
                    # Meminta input angka dari user
                    code = int(input("Kode angka: "))
                    if 0 <= code <= 5:
                        break
                    else:
                        print("Masukkan kode angka yang valid (0-5).")
                except ValueError:
                    print("Masukkan angka yang valid (0-5).")

            # Membuat folder untuk setiap angka jika belum ada
            digit_path = os.path.join(data_path, str(code))
            os.makedirs(digit_path, exist_ok=True)

            # Membuat nama file dengan timestamp untuk mencegah konflik
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(digit_path, f"{code}_{timestamp}_{i}.wav")

            # Merekam audio dan menyimpannya
            record_audio(file_path, duration=duration, sample_rate=sample_rate)

        print("\nSelesai merekam semua data.")
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh pengguna.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
