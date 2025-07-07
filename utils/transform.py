import pandas as pd
from utils.extract import get_raw_fashion_data

import pandas as pd
import re

def clean_fashion_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # Kolom yang wajib ada
        required_cols = ["Title", "Rating", "Price", "Colors", "Size", "Gender"]
        for col in required_cols:
            if col not in df.columns:
                raise KeyError(f"Kolom '{col}' tidak ditemukan di DataFrame")

        # Buang baris yang berisi nilai invalid eksplisit
        dirty_patterns = {
            "Title": ["Unknown Product"],
            "Rating": ["Invalid Rating / 5", "Not Rated", None],
            "Price": ["Price Unavailable", None]
        }

        for col, patterns in dirty_patterns.items():
            df = df[~df[col].isin(patterns)]

        df = df.dropna()

        # Bersihkan dan ubah kolom Price ke float lalu konversi ke IDR
        def clean_price(val):
            match = re.search(r'(\d+[\.,]?\d*)', str(val).replace(',', ''))
            return float(match.group(1)) * 16000 if match else None

        df['Price'] = df['Price'].apply(clean_price)

        # Bersihkan dan ubah kolom Rating ke float
        def clean_rating(val):
            match = re.search(r'(\d+(\.\d+)?)', str(val))
            return float(match.group(1)) if match else None

        df['Rating'] = df['Rating'].apply(clean_rating)

        # Ambil angka dari Colors
        def clean_colors(val):
            match = re.search(r'(\d+)', str(val))
            return int(match.group(1)) if match else None

        df['Colors'] = df['Colors'].apply(clean_colors)

        # Bersihkan teks Size dan Gender
        df['Size'] = df['Size'].str.replace('Size:', '', regex=False).str.strip()
        df['Gender'] = df['Gender'].str.replace('Gender:', '', regex=False).str.strip()

        # Drop baris yang masih ada null setelah cleaning
        df = df.dropna()

        df = df.drop_duplicates().reset_index(drop=True)
        return df

    except Exception as e:
        print(f"[!] Terjadi error saat membersihkan data: {e}")
        return pd.DataFrame()

def main():
    raw_df = get_raw_fashion_data()
    clean_df = clean_fashion_data(raw_df)

    if clean_df.empty:
        print("[!] Data tidak berhasil dibersihkan atau kosong.")
    else:
        print("[✓] Data berhasil dibersihkan")
        print(clean_df.info())
        print(clean_df.head())

if __name__ == '__main__':
    main()
