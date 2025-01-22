#include <Servo.h> 

// Definisi servo
Servo servoKanan;  // Servo kanan
Servo servoKiri;   // Servo kiri
Servo servoBawah;  // Servo bawah
Servo servoCapit;  // Servo capit

void setup() { 
  Serial.begin(9600); // Inisialisasi komunikasi serial
  servoKanan.attach(12); // Pin servo kanan
  servoKiri.attach(13);  // Pin servo kiri
  servoBawah.attach(10); // Pin servo bawah
  servoCapit.attach(9);  // Pin servo capit

  // Inisialisasi posisi servo ke 90 derajat
  servoKanan.write(90); 
  servoKiri.write(90); 
  servoBawah.write(90); 
  servoCapit.write(90); 
  delay(1000); // Tunggu 1 detik untuk memastikan servo bergerak
}

void loop() { 
  if (Serial.available() > 0) { 
    int kondisi = Serial.parseInt(); // Membaca input angka kondisi dari serial
    Serial.print("Kondisi yang diterima: ");
    Serial.println(kondisi);  // Debug: Tampilkan kondisi yang diterima

    if (kondisi == 0) { 
      Serial.println("Kondisi Ambil dan Simpan: Eksekusi gabungan.");
      kondisiGabungan();
    } else {
      Serial.println("Input tidak valid, masukkan angka 0 untuk Ambil dan Simpan.");
    }
  } 
}

// Fungsi untuk menjalankan kondisi Ambil dan Simpan dalam satu langkah
void kondisiGabungan() {
  Serial.println("Eksekusi Kondisi 1 - Ambil");
  moveServo(90, 45, 100, 45); 
  delay(3000); 

  Serial.println("Eksekusi Kondisi 2 - Ambil");
  moveServo(130, 0, 100, 20); 
  delay(3000); 

  Serial.println("Eksekusi Kondisi 3 - Ambil");
  moveServo(165, 0, 100, 20); 
  delay(3000); 

  Serial.println("Eksekusi Kondisi 4 - Ambil");
  moveServo(165, 0, 100, 150); 
  delay(3000); 

  Serial.println("Eksekusi Kondisi 5 - Simpan");
  moveServo(90, 45, 100, 150); 
  delay(3000); 

  Serial.println("Eksekusi Kondisi 6 - Simpan");
  moveServo(90, 45, 45, 150); 
  delay(3000); 

  Serial.println("Eksekusi Kondisi 7 - Simpan");
  moveServo(135, 20, 45, 150); 
  delay(3000); 

  Serial.println("Eksekusi Kondisi 8 - Simpan");
  moveServo(135, 20, 45, 90); 
  delay(3000); 
}

// Fungsi untuk menggerakkan servo ke posisi tertentu
void moveServo(int angleKanan, int angleKiri, int angleBawah, int angleCapit) { 
  servoKanan.write(angleKanan); // Gerakkan servo kanan
  servoKiri.write(angleKiri); // Gerakkan servo kiri
  servoBawah.write(angleBawah); // Gerakkan servo bawah
  servoCapit.write(angleCapit); // Gerakkan servo capit
  delay(500); // Tunggu hingga servo selesai bergerak
}
