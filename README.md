# Bike Sharing Data Analysis Dashboard 🚲 - Coding Camp 2026

Proyek ini merupakan hasil analisis data pada dataset Bike Sharing yang divisualisasikan ke dalam sebuah dashboard interaktif menggunakan library Streamlit. Proyek ini bertujuan untuk memberikan wawasan (insights) mengenai faktor-faktor yang memengaruhi jumlah penyewaan sepeda.

## 📂 Struktur Direktori
- `dashboard/`: Berisi berkas utama aplikasi `dashboard.py` dan clean dataset `main_data.csv`.
- `data/`: Berisi dataset mentah asli (`day.csv`).
- `img/`: Berisi aset visual seperti logo dashboard.
- `notebook.ipynb`: Berkas Notebook untuk proses pembersihan, eksplorasi, dan analisis data (EDA).
- `requirements.txt`: Daftar library Python yang digunakan.
- `README.md`: Panduan penggunaan dashboard ini.

## 🚀 Cara Menjalankan Dashboard

### 1. Setup Environment (Visual Studio Code)
Buka terminal di VS Code (Ctrl+Shift+`) dan ikuti langkah-langkah berikut:

**Membuat Virtual Environment:**
```bash
python -m venv venv
```

**Mengaktifkan Virtual Environtment:**
1. Windows
```bash
.\venv\Scripts\activate
```
2. Mac/Linux
```bash
source venv/bin/activate
```

### 2. Pengecekan & Instalasi Library
Sebelum menjalankan dashboard, pastikan library yang dibutuhkan sudah terpasang.

**Cek Streamlit**
```bash
streamlit --version
```
Jika muncul error, silakan instal library melalui requirements.txt

**Instalasi Library:**
```bash
pip install -r requirements.txt
```


### 3. Menjalankan Dashboard Streamlit
Pastikan posisi terminal berada di root direktori proyek, lalu jalankan perintah:

```bash
python -m streamlit run dashboard/dashboard.py
```




