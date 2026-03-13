# ☕ Coffee Order System (Redis-Powered)

Tugas Mata Kuliah: **Topik Khusus**

Proyek ini adalah sistem manajemen pesanan kopi sederhana namun canggih yang menggunakan **FastAPI** sebagai framework backend dan **Redis** untuk manajemen database serta antrean (queue).

## ✨ Fitur Utama
- **FastAPI**: Backend modern, cepat, dan berperforma tinggi.
- Menggunakan **Redis Hash** untuk menyimpan detail pesanan pelanggan.
- Menggunakan **Redis List** untuk mengelola antrean dapur secara real-time (FIFO).
- **Interactive API Docs**: Dokumentasi API otomatis yang bisa langsung dicoba melalui Swagger UI.

## 🛠️ Cara Menjalankan
1. **Persiapan Redis**:
   Pastikan **Redis Server** sudah terinstal dan berjalan di laptop Anda (default port: 6379).

2. **Instalasi Library**:
   Buka terminal di folder proyek dan jalankan perintah:
   ```bash
   pip install fastapi uvicorn redis
