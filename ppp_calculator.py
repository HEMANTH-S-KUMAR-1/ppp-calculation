import pandas as pd
import numpy as np
import unittest  # Ensure unittest is imported

def calculate_ppp(currency_a: str, currency_b: str, price_data: pd.DataFrame) -> float:
    """
    Calculate the Purchasing Power Parity (PPP) exchange rate between two currencies.

    Parameters:
        currency_a (str): Currency code for Country A.
        currency_b (str): Currency code for Country B.
        price_data (pd.DataFrame): DataFrame containing goods/services and their prices in both currencies.

    Returns:
        float: PPP exchange rate between the two currencies.
    """
    # Validate inputs
    if not isinstance(currency_a, str) or not isinstance(currency_b, str):
        raise ValueError("Currency codes must be strings.")
    
    if 'Price_A' not in price_data.columns or 'Price_B' not in price_data.columns:
        raise ValueError("DataFrame must contain 'Price_A' and 'Price_B' columns.")
    
    # Drop rows with missing or non-numeric data
    price_data = price_data.dropna(subset=['Price_A', 'Price_B'])
    price_data = price_data[(price_data['Price_A'].apply(np.isreal)) & (price_data['Price_B'].apply(np.isreal))]

    if price_data.empty:
        raise ValueError("DataFrame must contain valid numeric price data.")
    
    # Calculate the price ratios
    price_ratios = price_data['Price_A'] / price_data['Price_B']
    
    # Compute the average price ratio
    average_price_ratio = np.mean(price_ratios)
    
    # Return the PPP exchange rate
    return average_price_ratio

# Example usage
data = {
    'Goods_Services': ['Item 1', 'Item 2', 'Item 3'],
    'Price_A': [100, 200, 150],  # Prices in Currency A
    'Price_B': [10, 20, 15],    # Prices in Currency B
}

price_data = pd.DataFrame(data)

try:
    ppp_exchange_rate = calculate_ppp('USD', 'EUR', price_data)
    print(f"PPP Exchange Rate (USD to EUR): {ppp_exchange_rate}")
except ValueError as e:
    print(f"Error: {e}")

# Unit tests
class TestCalculatePPP(unittest.TestCase):
    def test_valid_data(self):
        data = {
            'Goods_Services': ['Item 1', 'Item 2', 'Item 3'],
            'Price_A': [100, 200, 150],
            'Price_B': [10, 20, 15],
        }
        df = pd.DataFrame(data)
        result = calculate_ppp('USD', 'EUR', df)
        expected = 10.0  # Average ratio of Price_A to Price_B
        self.assertAlmostEqual(result, expected, places=2)

    def test_missing_prices(self):
        data = {
            'Goods_Services': ['Item 1', 'Item 2', 'Item 3'],
            'Price_A': [100, np.nan, 150],
            'Price_B': [10, 20, 15],
        }
        df = pd.DataFrame(data)
        result = calculate_ppp('USD', 'EUR', df)
        expected = 10.0  # Average ratio of valid entries
        self.assertAlmostEqual(result, expected, places=2)

    def test_non_numeric_prices(self):
        data = {
            'Goods_Services': ['Item 1', 'Item 2', 'Item 3'],
            'Price_A': [100, 'a', 150],
            'Price_B': [10, 20, 15],
        }
        df = pd.DataFrame(data)
        result = calculate_ppp('USD', 'EUR', df)
        expected = 10.0  # Only valid numeric entries considered
        self.assertAlmostEqual(result, expected, places=2)

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=['Goods_Services', 'Price_A', 'Price_B'])
        with self.assertRaises(ValueError):
            calculate_ppp('USD', 'EUR', df)

if __name__ == '__main__':
    unittest.main()
