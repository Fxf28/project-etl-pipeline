# test_main.py
from unittest import TestCase, mock
from main import main

class TestMainFunction(TestCase):
    @mock.patch('main.load_to_postgre')
    @mock.patch('main.load_to_spreadsheets')
    @mock.patch('main.load_to_csv')
    @mock.patch('main.full_clean')
    @mock.patch('main.scrape_product')
    def test_main_success(self, mock_scrape_product, mock_full_clean, mock_load_to_csv, mock_load_to_spreadsheets, mock_load_to_postgre):
        # Arrange
        dummy_products = [{'name': 'T-Shirt', 'price': 100}]
        dummy_df = 'dummy dataframe'

        mock_scrape_product.return_value = dummy_products
        mock_full_clean.return_value = dummy_df

        # Act
        main()

        # Assert
        mock_scrape_product.assert_called_once()
        mock_full_clean.assert_called_once_with(dummy_products)
        mock_load_to_csv.assert_called_once_with(df=dummy_df, filepath='products.csv')
        mock_load_to_spreadsheets.assert_called_once_with(df=dummy_df)
        mock_load_to_postgre.assert_called_once_with(dummy_df, 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashion_products')

    @mock.patch('main.scrape_product', side_effect=Exception('Scraping error'))
    def test_main_scrape_fail(self, mock_scrape_product):
        main()
        mock_scrape_product.assert_called_once()

    @mock.patch('main.scrape_product')
    @mock.patch('main.full_clean', side_effect=Exception('Cleaning error'))
    def test_main_clean_fail(self, mock_full_clean, mock_scrape_product):
        mock_scrape_product.return_value = [{'name': 'T-Shirt', 'price': 100}]
        main()
        mock_scrape_product.assert_called_once()
        mock_full_clean.assert_called_once()

    @mock.patch('main.scrape_product')
    @mock.patch('main.full_clean')
    @mock.patch('main.load_to_csv', side_effect=Exception('CSV error'))
    def test_main_csv_fail(self, mock_load_to_csv, mock_full_clean, mock_scrape_product):
        mock_scrape_product.return_value = [{'name': 'T-Shirt', 'price': 100}]
        mock_full_clean.return_value = 'dummy dataframe'
        main()
        mock_load_to_csv.assert_called_once()

    @mock.patch('main.scrape_product')
    @mock.patch('main.full_clean')
    @mock.patch('main.load_to_csv')
    @mock.patch('main.load_to_spreadsheets', side_effect=Exception('Sheets error'))
    def test_main_spreadsheet_fail(self, mock_load_to_spreadsheets, mock_load_to_csv, mock_full_clean, mock_scrape_product):
        mock_scrape_product.return_value = [{'name': 'T-Shirt', 'price': 100}]
        mock_full_clean.return_value = 'dummy dataframe'
        main()
        mock_load_to_spreadsheets.assert_called_once()

    @mock.patch('main.scrape_product')
    @mock.patch('main.full_clean')
    @mock.patch('main.load_to_csv')
    @mock.patch('main.load_to_spreadsheets')
    @mock.patch('main.load_to_postgre', side_effect=Exception('PostgreSQL error'))
    def test_main_postgre_fail(self, mock_load_to_postgre, mock_load_to_spreadsheets, mock_load_to_csv, mock_full_clean, mock_scrape_product):
        mock_scrape_product.return_value = [{'name': 'T-Shirt', 'price': 100}]
        mock_full_clean.return_value = 'dummy dataframe'
        main()
        mock_load_to_postgre.assert_called_once()

if __name__ == '__main__':
    unittest.main()
