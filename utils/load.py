import pandas as pd
import os

# Untuk PostgreSQL
from sqlalchemy import create_engine

# Untuk Google Sheets
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

def load_to_csv(df: pd.DataFrame, file_path: str = "fashion_data.csv"):
    df.to_csv(file_path, index=False)
    print(f"[✓] Data disimpan ke CSV di: {file_path}")

def load_to_postgres(df: pd.DataFrame, db_url: str, table_name: str = "fashion_data"):
    try:
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"[✓] Data berhasil disimpan ke PostgreSQL: Tabel {table_name}")
    except Exception as e:
        print(f"[!] Gagal menyimpan ke PostgreSQL: {e}")

def load_to_google_sheets(df: pd.DataFrame, spreadsheet_id: str, sheet_name: str, json_keyfile: str):
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        sheet.clear()
        set_with_dataframe(sheet, df)
        print(f"[✓] Data berhasil diunggah ke Google Sheets: Sheet '{sheet_name}'")
    except Exception as e:
        print(f"[!] Gagal menyimpan ke Google Sheets: {e}")

def main():
    # Load hasil transform
    from utils.transform import clean_fashion_data
    from utils.extract import get_raw_fashion_data

    raw_df = get_raw_fashion_data()
    df = clean_fashion_data(raw_df)

    # 1. Simpan ke CSV
    load_to_csv(df, "fashion_data.csv")

    # 2. Simpan ke Google Sheets
    spreadsheet_id = "1Ix__N02xzVcVvMO-oBxYv7tByjAVC1A2IrkJPj00CMI"
    sheet_name = "Fashion Data"
    json_keyfile = "etl-sheets-project-457914-2a2f116c4a46.json"
    load_to_google_sheets(df, spreadsheet_id, sheet_name, json_keyfile)

    # 3. Simpan ke PostgreSQL
    # Format DB_URL: "postgresql://username:password@localhost:5432/database"
    db_url = os.getenv("POSTGRES_URL", "postgresql://postgres:admin@localhost:5432/fashiondb")
    load_to_postgres(df, db_url)

if __name__ == "__main__":
    main()
