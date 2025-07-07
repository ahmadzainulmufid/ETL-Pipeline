# main.py

from utils.extract import get_raw_fashion_data
from utils.transform import clean_fashion_data
from utils.load import load_to_csv, load_to_postgres, load_to_google_sheets

import os

def main():
    # 1. Extract
    print("[•] Mulai proses Extract...")
    raw_df = get_raw_fashion_data()

    if raw_df.empty:
        print("[!] Gagal mengambil data.")
        return

    # 2. Transform
    print("[•] Mulai proses Transform...")
    clean_df = clean_fashion_data(raw_df)

    if clean_df.empty:
        print("[!] Gagal membersihkan data.")
        return

    # 3. Load
    print("[•] Mulai proses Load...")

    # Simpan ke CSV
    load_to_csv(clean_df, "fashion_data.csv")

    # Simpan ke Google Sheets
    spreadsheet_id = "1Ix__N02xzVcVvMO-oBxYv7tByjAVC1A2IrkJPj00CMI"
    sheet_name = "Fashion Data"
    json_keyfile = "etl-sheets-project-457914-2a2f116c4a46.json"
    load_to_google_sheets(clean_df, spreadsheet_id, sheet_name, json_keyfile)

    # Simpan ke PostgreSQL
    db_url = os.getenv("POSTGRES_URL", "postgresql://postgres:admin@localhost:5432/fashiondb")
    load_to_postgres(clean_df, db_url)

    print("[✓] Proses ETL selesai!")

if __name__ == "__main__":
    main()
