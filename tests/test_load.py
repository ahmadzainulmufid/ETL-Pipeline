import unittest
import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.load import load_to_postgres

class TestLoad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_url = "postgresql+psycopg2://postgres:admin@localhost:5432/fashiondb"
        cls.table_name = "fashion_data_test"
        cls.engine = create_engine(cls.db_url)

        cls.sample_data = pd.DataFrame([{
            'Title': 'T-shirt 01',
            'Price': 400000.0,
            'Rating': 4.5,
            'Colors': 3,
            'Size': 'M',
            'Gender': 'Unisex',
            'Timestamp': '2025-03-20 12:00:00'
        }])

        # Buat tabel jika belum ada
        with cls.engine.connect() as con:
            con.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {cls.table_name} (
                    "Title" TEXT,
                    "Price" NUMERIC(10, 2),
                    "Rating" NUMERIC(3, 2),
                    "Colors" INTEGER,
                    "Size" TEXT,
                    "Gender" TEXT,
                    "Timestamp" TIMESTAMP
                );
            """))

    def test_load_to_postgres(self):
        try:
            load_to_postgres(self.sample_data, self.db_url, self.table_name)
        except Exception as e:
            self.fail(f"❌ Terjadi kesalahan saat memuat data: {e}")

        with self.engine.connect() as con:
            result = con.execute(text(f'SELECT * FROM {self.table_name} WHERE "Title" = :title'),
                                 {'title': 'T-shirt 01'}).fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result.Title, 'T-shirt 01')
            self.assertEqual(float(result.Price), 400000.0)
            self.assertEqual(float(result.Rating), 4.5)
            self.assertEqual(result.Colors, 3)
            self.assertEqual(result.Size, 'M')
            self.assertEqual(result.Gender, 'Unisex')

    @classmethod
    def tearDownClass(cls):
        with cls.engine.connect() as con:
            con.execute(text(f'DROP TABLE IF EXISTS {cls.table_name}'))
            print(f"✅ Tabel {cls.table_name} dihapus setelah pengujian.")

if __name__ == '__main__':
    unittest.main()
