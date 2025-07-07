# 🧪 ETL Pipeline: Fashion Studio Scraper

Proyek ini adalah implementasi dari **ETL Pipeline** dengan prinsip modular code, digunakan untuk melakukan scraping data fashion dari [https://fashion-studio.dicoding.dev/](https://fashion-studio.dicoding.dev/), membersihkan data, dan menyimpannya ke **CSV**, **Google Sheets**, dan **PostgreSQL**.

ETL ini dirancang untuk memenuhi standar **pengolahan data bersih**, **pengujian unit**, dan **pengelolaan dependensi** yang baik dalam proses rekayasa data.

---

## 🧱 Kriteria 1: ETL Modular dan Lengkap

### ✅ Tahapan Extract
- Mengambil data dari **50 halaman** pada [fashion-studio.dicoding.dev](https://fashion-studio.dicoding.dev/).
- Data yang diambil:
  - `Title`
  - `Price`
  - `Rating`
  - `Colors`
  - `Size`
  - `Gender`
- Ditambahkan kolom baru `timestamp` (waktu ekstraksi).

### ✅ Tahapan Transform
- Harga dikonversi dari Dolar ke Rupiah dengan kurs tetap: **Rp16.000**.
- Membersihkan data:
  - Menghapus duplikat.
  - Menghapus nilai null dan invalid (seperti "Unknown Product", "Invalid Rating").
  - Membersihkan format teks seperti: `“3 Colors”` → `3`, `“Size: M”` → `M`, dll.
- Mengonversi semua tipe data sesuai spesifikasi:
  - `Price`: integer
  - `Rating`: float
  - `Colors`: integer
  - `Size`, `Gender`: string
  - `Title`: string

### ✅ Tahapan Load
- Data hasil transformasi disimpan ke:
  - `products.csv` (Flat File)
  - **Google Sheets** (dengan akses publik)
  - **PostgreSQL** (melalui script `load.py`)

---

## 💾 Kriteria 2: Penyimpanan Data di Repositori

✔️ Disimpan dalam **3 jenis repositori**:

| Jenis Repositori   | Status | Keterangan                       |
|--------------------|--------|----------------------------------|
| CSV                | ✅     | File `products.csv`              |
| Google Sheets      | ✅     | Diunggah dengan service account  |
| PostgreSQL         | ✅     | Tabel dimuat dari `load.py`      |

🔑 Berkas **`google-sheets-api.json`** sudah disertakan dan digunakan untuk akses via API.

---

## 🧪 Kriteria 3: Unit Testing

✔️ **Seluruh fungsi ETL (extract, transform, load)** sudah diuji melalui unit test dengan modul `pytest`.

- Lokasi semua test: `tests/`
- Cakupan test (test coverage): **60–70%**
- Semua test sudah lulus dan berjalan tanpa error

📌 **Fungsi yang diuji:**
- `scrape_main()` – test jumlah data dan struktur
- `clean_data()` – test pembersihan duplikat, null, invalid
- `save_to_csv()`, `save_to_gsheets()`, `save_to_postgres()` – test penyimpanan

---

## 🚀 Menjalankan Proyek

### 1. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 2. Jalankan Pipeline
```bash
python main.py
```

### 3. Jalankan Unit Test
```bash
pytest --cov=utils tests/
```

---

## 🧰 Tools & Teknologi
  - Python 3.8+
  - Requests, BeautifulSoup (Scraping)
  - Pandas (Transformasi data)
  - Google Sheets API
  - psycopg2 (PostgreSQL)
  -pytest + pytest-cov (Unit Testing)
