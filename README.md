# 🏎️ Hand Gesture Racing Game 🏎️

![Game Screenshot](https://github.com/ahnafyura/Car_Game_with_handGesture/images/car.png)

## 📄 Deskripsi Proyek

Proyek ini adalah implementasi game balap mobil 2D bergaya *top-down* yang unik, di mana kontrol mobil tidak menggunakan keyboard atau gamepad, melainkan **gerakan tangan yang dideteksi secara *real-time* melalui webcam**. Game ini menggabungkan kekuatan Pygame untuk grafis dan simulasi fisika sederhana, dengan MediaPipe Hands untuk pelacakan *landmark* tangan yang presisi.

Tujuan utama proyek ini adalah untuk menciptakan pengalaman bermain game yang inovatif dan imersif, memanfaatkan teknologi *computer vision* untuk interaksi yang lebih intuitif.

## ✨ Fitur Utama

* **Kontrol Gerakan Tangan:** Menggunakan webcam untuk mendeteksi posisi kedua tangan dan menerjemahkannya menjadi input kemudi (belok kiri/kanan).
* **Game Balap 2D Top-Down:** Visualisasi sirkuit balap dan mobil dari perspektif atas.
* **Sistem Fisika Mobil Dasar:** Implementasi akselerasi, friksi, kecepatan maksimum, dan kecepatan belok yang dipengaruhi kecepatan mobil.
* **Deteksi Tabrakan Cerdas:** Menggunakan Pygame masks untuk mendeteksi tabrakan mobil dengan area *off-track* (rumput hijau) di sirkuit.
* **Deteksi Batas Layar:** Game Over jika mobil keluar dari area permainan.
* **Countdown Pra-Balapan:** Hitungan mundur (3, 2, 1, GO!) sebelum balapan dimulai.
* **Sistem Lap dan Waktu:** Pelacakan jumlah lap dan waktu lap terbaik.
* **HUD (Head-Up Display):** Menampilkan informasi lap dan waktu balapan.
* **Visualisasi Webcam:** Menampilkan *feed* webcam dengan *landmark* tangan yang dideteksi (titik hijau, garis putih) di pojok kanan bawah layar.
* **Debug Mode:** Mode visualisasi mask tabrakan (tekan 'M') untuk membantu pengembangan.

## 🛠️ Alur Pembuatan & Perancangan

Proyek ini dirancang dengan pendekatan modular, memisahkan logika utama game, logika mobil, dan logika pelacakan tangan ke dalam file Python yang berbeda untuk kemudahan pengelolaan dan pemahaman:

* **`main.py`**: Core game loop, pengelolaan game state (countdown, playing, game over), rendering grafis, deteksi tabrakan sirkuit & batas layar, dan integrasi modul lain.
* **`car.py`**: Kelas `Car` yang mengelola atribut (posisi, sudut, kecepatan, akselerasi) dan perilaku (rotasi, gerakan, update) mobil balap.
* **`hand_tracker.py`**: Kelas `HandTracker` yang bertanggung jawab untuk inisialisasi webcam, pemrosesan video dengan MediaPipe Hands, deteksi landmark tangan, dan penerjemahan gerakan tangan menjadi input kemudi.

**Tahapan Utama:**

1.  **Setup Lingkungan:** Inisialisasi Pygame dan MediaPipe.
2.  **Aset Grafis:** Desain sirkuit (sirkuit.png) dan sprite mobil (car.png).
3.  **Implementasi `Car` Class:** Mengembangkan dasar pergerakan dan fisika mobil.
4.  **Implementasi `HandTracker` Class:** Membangun jembatan antara webcam, MediaPipe, dan input game.
5.  **Main Game Loop:** Mengintegrasikan semua komponen, membuat game state, dan flow permainan.
6.  **Deteksi Tabrakan:** Implementasi Pygame masks untuk interaksi lingkungan yang presisi.
7.  **Refinement & Debugging:** Iterasi untuk meningkatkan responsivitas kontrol, akurasi deteksi, dan memperbaiki bug.

## 🚀 Cara Menggunakan Repositori

Ikuti langkah-langkah di bawah ini untuk mengunduh, menginstal dependensi, dan menjalankan game ini di sistem Anda.

### Prasyarat

Pastikan Anda memiliki Python 3.x terinstal di sistem Anda.

### Instalasi

1.  **Clone Repositori:**
    Buka terminal atau command prompt Anda dan jalankan perintah berikut untuk mengunduh proyek:
    ```bash
    git clone [https://github.com/NamaPenggunaAnda/NamaRepositoriAnda.git](https://github.com/NamaPenggunaAnda/NamaRepositoriAnda.git)
    cd NamaRepositoriAnda
    ```
    *(Ganti `NamaPenggunaAnda` dan `NamaRepositoriAnda` dengan nama pengguna dan nama repositori GitHub Anda)*

2.  **Buat Virtual Environment (Opsional tapi Direkomendasikan):**
    Ini membantu mengelola dependensi proyek Anda.
    ```bash
    python -m venv venv
    ```

3.  **Aktifkan Virtual Environment:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instal Dependensi:**
    Setelah virtual environment aktif, instal semua pustaka yang diperlukan:
    ```bash
    pip install pygame opencv-python mediapipe
    ```

### Menjalankan Game

1.  **Pastikan Webcam Tersedia:** Pastikan tidak ada aplikasi lain yang menggunakan webcam Anda.
2.  **Jalankan Script Utama:**
    Dari direktori root proyek (setelah mengaktifkan virtual environment), jalankan:
    ```bash
    python main.py
    ```

### Kontrol Game

* **Kemudi:**
    * **Tangan Kiri di Atas Tangan Kanan:** Belok Kiri
    * **Tangan Kanan di Atas Tangan Kiri:** Belok Kanan
    * **Kedua Tangan Sejajar / Lurus ke Depan:** Mobil Lurus (dan akselerasi maju)
* **`R` (Keyboard):** Restart game saat Game Over.
* **`M` (Keyboard):** Toggle (hidup/mati) visualisasi debug mask tabrakan.

### Aset Gambar

Pastikan Anda memiliki file gambar berikut di dalam folder `assets/` di root proyek:
* `car.png` (sprite mobil)
* `sirkuit.png` (gambar trek balap)

### Penyesuaian (Opsional)

* **Kecepatan Mobil:** Ubah nilai `self.max_speed`, `self.acceleration`, `self.friction`, dan `self.rotation_speed` di `car.py` untuk menyesuaikan performa mobil.
* **Warna Hijau Sirkuit:** Pastikan `GREEN_BORDER_COLOR` di `main.py` sesuai dengan nilai RGB yang tepat dari warna hijau di `sirkuit.png` Anda. Gunakan alat *color picker* pada editor gambar Anda.
* **Posisi Start Mobil:** Sesuaikan koordinat `Car(360, 515)` di `reset_game()` dalam `main.py` agar mobil memulai di garis start dengan benar.
* **Garis Finish:** Sesuaikan `FINISH_LINE_RECT` di `main.py` agar tepat mengenai garis finish di sirkuit Anda.

## 🤝 Kontribusi

Kontribusi Anda sangat dihargai! Jika Anda memiliki ide untuk fitur baru, perbaikan bug, atau peningkatan, jangan ragu untuk:

1.  *Fork* repositori ini.
2.  Buat branch baru (`git checkout -b feature/NamaFiturBaru`).
3.  Lakukan perubahan Anda.
4.  *Commit* perubahan Anda (`git commit -m 'Tambahkan NamaFiturBaru'`).
5.  *Push* ke branch Anda (`git push origin feature/NamaFiturBaru`).
6.  Buka *Pull Request*.

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE). *(Anda bisa membuat file LICENSE.md jika belum ada)*

---
