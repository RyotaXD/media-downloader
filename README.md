# 🚀 Multi-Platform Social Media Downloader

Sebuah script  berbasis CLI (Command Line Interface) Python yang dirancang khusus untuk pengguna Android/Termux agar dapat mengunduh video dari berbagai platform sosial media dengan mudah, cepat, dan otomatis.

### ⚡ Fitur Utama:
- **Multi-Platform:** Mendukung YouTube (Video, Shorts, Playlist), Facebook (Reels, Story, Reguler), dan Instagram (Reels, Story).
- **Multi-Link Support:** Bisa langsung copas banyak URL sekaligus (dipisah spasi, koma, atau baris baru).
- **Auto-Installer Module:** Script otomatis mendeteksi dan menginstall library yang kurang saat pertama kali dijalankan.
- **Penyimpanan Fleksibel:** Bisa diatur lokasi simpannya secara manual atau otomatis ke folder Download bawaan HP.

### 🛠️ Cara Instalasi di Termux:
```
termux-setup-storage
git clone https://github.com/RyotaXD/media-downloader
cd media-downloader
python media.py
