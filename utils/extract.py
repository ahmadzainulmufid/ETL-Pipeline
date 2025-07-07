import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"[!] Gagal mengambil halaman {url}: {e}")
        return None

def extract_fashion_data(card):
    """Mengambil data fashion dari elemen collection-card."""
    try:
        title_elem = card.find('h3', class_='product-title')
        price_elem = card.find('span', class_='price')

        title = title_elem.text.strip() if title_elem else None
        price = price_elem.text.strip() if price_elem else None

        rating = None
        colors = None
        size = None
        gender = None

        details = card.find_all('p')
        for p in details:
            text = p.text.strip()
            if "Rating" in text:
                rating = text.replace("Rating: ⭐", "").strip()
            elif "Colors" in text:
                colors = text.strip()
            elif "Size" in text:
                size = text.replace("Size:", "").strip()
            elif "Gender" in text:
                gender = text.replace("Gender:", "").strip()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        }
    except Exception as e:
        print(f"[!] Gagal mengekstrak data dari satu card: {e}")
        return {
            "Title": None,
            "Price": None,
            "Rating": None,
            "Colors": None,
            "Size": None,
            "Gender": None,
            "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def scrape_fashion(base_url, max_page=50, delay=1):
    """Scrape produk fashion dari halaman 1 sampai max_page."""
    data = []

    for page_number in range(1, max_page + 1):
        if page_number == 1:
            url = base_url
        else:
            url = f"{base_url}page{page_number}"

        print(f"[•] Scraping halaman: {url}")
        content = fetching_content(url)

        if content:
            try:
                soup = BeautifulSoup(content, "html.parser")
                product_cards = soup.find_all('div', class_='collection-card')

                if not product_cards:
                    print(f"[!] Tidak ada produk ditemukan di halaman {page_number}. Stop.")
                    break

                for card in product_cards:
                    fashion_item = extract_fashion_data(card)
                    data.append(fashion_item)

                if len(data) >= 1000:
                    break

                time.sleep(delay)
            except Exception as e:
                print(f"[!] Gagal memproses halaman {url}: {e}")
        else:
            print(f"[!] Konten kosong dari {url}, menghentikan scraping.")
            break

    print(f"[✓] Total item diambil: {len(data)}")
    return data[:1000]

def get_raw_fashion_data():
    BASE_URL = 'https://fashion-studio.dicoding.dev/'
    data = scrape_fashion(BASE_URL)
    return pd.DataFrame(data)

def main():
    """Fungsi utama untuk keseluruhan proses scraping hingga menyimpannya."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/'
    extracted_data = scrape_fashion(BASE_URL)

    if not extracted_data:
        print("[!] Tidak ada data yang berhasil diambil.")
        return

    df = pd.DataFrame(extracted_data)
    print("[✓] Data berhasil diambil dan dikonversi menjadi DataFrame")
    print(df.info())
    print(df.head())

if __name__ == '__main__':
    main()
