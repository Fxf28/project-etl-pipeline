import pandas as pd
import numpy as np
from unittest import TestCase
from utils.transform import (
    transform_to_dataframe,
    handle_title,
    handle_price,
    convert_price_to_rupiah,
    handle_rating,
    handle_colors,
    handle_size,
    handle_gender,
    handle_timestamp,
    drop_missing_values,
    full_clean,
)

class TestTransform(TestCase):
    def setUp(self):
        self.sample_data = [
            {
                "Title": " Product 1 ",
                "Price": "$10.99",
                "Rating": "Rating: ⭐ 4.5 / 5",
                "Colors": "Colors: 3 options",
                "Size": "Size: M",
                "Gender": "Gender: Men",
                "Timestamp": "2024-01-01 12:00:00"
            },
            {
                "Title": "Unknown Product",
                "Price": "Price Unavailable",
                "Rating": "Rating: ⭐ Invalid Rating / 5",
                "Colors": "Colors: Unknown",
                "Size": "Size: Unknown",
                "Gender": "Gender: Unknown",
                "Timestamp": "Invalid Timestamp"
            },
        ]

    def test_transform_to_dataframe_success(self):
        df = transform_to_dataframe(self.sample_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 2)

    def test_transform_to_dataframe_error(self):
        with self.assertRaises(ValueError):  # ValueError seharusnya dilempar jika input None
            transform_to_dataframe(None)

    def test_handle_title_success(self):
        df = pd.DataFrame({'Title': [' Product ', 'Unknown Product', '', None]})
        df = handle_title(df)
        self.assertEqual(df['Title'].isna().sum(), 3)

    def test_handle_title_error(self):
        with self.assertRaises(Exception):
            handle_title(None)

    def test_handle_price_success(self):
        df = pd.DataFrame({'Price': ['$10.99', 'Price Unavailable', '$1,000.50']})
        df = handle_price(df)
        self.assertTrue(pd.isna(df.loc[1, 'Price']))
        self.assertEqual(df.loc[0, 'Price'], 10.99)
        self.assertEqual(df.loc[2, 'Price'], 1000.5)

    def test_handle_price_error(self):
        with self.assertRaises(Exception):
            handle_price(None)

    def test_convert_price_to_rupiah_success(self):
        df = pd.DataFrame({'Price': [10]})
        df = convert_price_to_rupiah(df)
        self.assertEqual(df['Price'].iloc[0], 160000)

    def test_convert_price_to_rupiah_error(self):
        with self.assertRaises(Exception):
            convert_price_to_rupiah(None)

    def test_handle_rating_success(self):
        df = pd.DataFrame({'Rating': ['Rating: ⭐ 4.5 / 5', 'Rating: ⭐ Invalid Rating / 5', None]})
        df = handle_rating(df)
        self.assertEqual(df.loc[0, 'Rating'], 4.5)
        self.assertTrue(pd.isna(df.loc[1, 'Rating']))

    def test_handle_rating_error(self):
        with self.assertRaises(Exception):
            handle_rating(None)

    def test_handle_colors_success(self):
        df = pd.DataFrame({'Colors': ['Colors: 5 options', 'Colors: Unknown']})
        df = handle_colors(df)
        self.assertEqual(df['Colors'].iloc[0], 5)
        self.assertTrue(pd.isna(df['Colors'].iloc[1]))

    def test_handle_colors_error(self):
        with self.assertRaises(Exception):
            handle_colors(None)

    def test_handle_size_success(self):
        df = pd.DataFrame({'Size': ['Size: M', 'Size: L', 'Unknown', '']})
        df = handle_size(df)
        self.assertEqual(df['Size'].iloc[0], 'M')
        self.assertEqual(df['Size'].iloc[1], 'L')
        self.assertTrue(pd.isna(df['Size'].iloc[2]))
        self.assertTrue(pd.isna(df['Size'].iloc[3]))

    def test_handle_size_error(self):
        with self.assertRaises(Exception):
            handle_size(None)

    def test_handle_gender_success(self):
        df = pd.DataFrame({'Gender': ['Gender: Men', 'Gender: Women', 'Gender: Unisex', 'Unknown', '']})
        df = handle_gender(df)
        self.assertEqual(df['Gender'].iloc[0], 'Men')
        self.assertEqual(df['Gender'].iloc[1], 'Women')
        self.assertEqual(df['Gender'].iloc[2], 'Unisex')
        self.assertTrue(pd.isna(df['Gender'].iloc[3]))
        self.assertTrue(pd.isna(df['Gender'].iloc[4]))

    def test_handle_gender_error(self):
        with self.assertRaises(Exception):
            handle_gender(None)

    def test_handle_timestamp_success(self):
        df = pd.DataFrame({'Timestamp': ['2024-01-01 12:00:00', 'Invalid Timestamp']})
        df = handle_timestamp(df)

        # Memastikan bahwa tipe data adalah string setelah pemformatan
        self.assertIsInstance(df['Timestamp'].iloc[0], str)

        # Memastikan nilai pertama mengikuti format yang benar (YYYY-MM-DDTHH:MM:SS.MMMMMM)
        self.assertEqual(df['Timestamp'].iloc[0], '2024-01-01T12:00:00.000000')

        # Memastikan nilai kedua adalah NaT (Not a Time)
        self.assertTrue(pd.isna(df['Timestamp'].iloc[1]))

    def test_handle_timestamp_error(self):
        with self.assertRaises(Exception):
            handle_timestamp(None)

    def test_drop_missing_values_success(self):
        df = pd.DataFrame({
            'Title': ['Product', None],
            'Price': [10, None],
            'Rating': [4, None]
        })
        df = drop_missing_values(df)
        self.assertEqual(df.shape[0], 1)

    def test_drop_missing_values_error(self):
        with self.assertRaises(Exception):
            drop_missing_values(None)

    def test_full_clean_success(self):
        cleaned_df = full_clean(self.sample_data)
        self.assertEqual(cleaned_df.shape[0], 1)
        self.assertEqual(cleaned_df['Title'].iloc[0], 'Product 1')
        self.assertAlmostEqual(cleaned_df['Price'].iloc[0], 10.99 * 16000, places=2)
        self.assertEqual(cleaned_df['Rating'].iloc[0], 4.5)

    def test_full_clean_error(self):
        with self.assertRaises(Exception):
            full_clean(None)

if __name__ == '__main__':
    unittest.main()
