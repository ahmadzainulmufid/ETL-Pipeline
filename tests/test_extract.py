import unittest
from bs4 import BeautifulSoup
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import extract_fashion_data

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.sample_html = """
        <div class="collection-card">
            <h3 class="product-title">T-shirt 01</h3>
            <span class="price">$25.00</span>
            <p>Rating: ⭐4.5</p>
            <p>Colors: 3</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        """
        self.soup = BeautifulSoup(self.sample_html, 'html.parser')
        self.card = self.soup.find('div', class_='collection-card')

    def test_extract_product_data_valid(self):
        """Menguji ekstraksi data produk yang valid."""
        result = extract_fashion_data(self.card)
        self.assertIsInstance(result, dict)

        expected_output = {
            'Title': 'T-shirt 01',
            'Price': '$25.00',
            'Rating': '4.5',
            'Colors': 'Colors: 3',
            'Size': 'M',
            'Gender': 'Unisex'
        }

        for key in expected_output:
            self.assertIn(key, result)
            self.assertEqual(result[key], expected_output[key])

        self.assertIn('Timestamp', result)
        self.assertIsInstance(result['Timestamp'], str)

    def test_extract_invalid_product(self):
        """Menguji ekstraksi pada produk yang tidak valid."""
        invalid_html = "<div class='collection-card'></div>"
        invalid_soup = BeautifulSoup(invalid_html, 'html.parser')
        card = invalid_soup.find('div', class_='collection-card')
        result = extract_fashion_data(card)

        self.assertIsInstance(result, dict)
        self.assertIsNone(result['Title'])
        self.assertIsNone(result['Price'])
        self.assertIsNone(result['Rating'])
        self.assertIsNone(result['Colors'])
        self.assertIsNone(result['Size'])
        self.assertIsNone(result['Gender'])

    def test_partial_data(self):
        """Menguji ekstraksi jika sebagian data hilang."""
        partial_html = """
        <div class="collection-card">
            <h3 class="product-title">T-shirt 02</h3>
            <span class="price">$30.00</span>
        </div>
        """
        partial_soup = BeautifulSoup(partial_html, 'html.parser')
        card = partial_soup.find('div', class_='collection-card')
        result = extract_fashion_data(card)

        self.assertEqual(result['Title'], 'T-shirt 02')
        self.assertEqual(result['Price'], '$30.00')
        self.assertIsNone(result['Rating'])
        self.assertIsNone(result['Colors'])
        self.assertIsNone(result['Size'])
        self.assertIsNone(result['Gender'])

    def test_extract_product_data_no_price(self):
        """Menguji ekstraksi jika harga tidak tersedia."""
        no_price_html = """
        <div class="collection-card">
            <h3 class="product-title">Hoodie 03</h3>
            <p>Rating: ⭐4.3</p>
            <p>Colors: 5</p>
            <p>Size: L</p>
            <p>Gender: Men</p>
        </div>
        """
        no_price_soup = BeautifulSoup(no_price_html, 'html.parser')
        card = no_price_soup.find('div', class_='collection-card')
        result = extract_fashion_data(card)

        self.assertEqual(result['Title'], 'Hoodie 03')
        self.assertIsNone(result['Price'])
        self.assertEqual(result['Rating'], '4.3')
        self.assertEqual(result['Colors'], 'Colors: 5')
        self.assertEqual(result['Size'], 'L')
        self.assertEqual(result['Gender'], 'Men')

if __name__ == '__main__':
    unittest.main()
