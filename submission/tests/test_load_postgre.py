from unittest import TestCase, mock
import io
from contextlib import redirect_stdout

import pandas as pd

from utils.load_postgre import *

class TestLoadToPostgre(TestCase):
    @mock.patch('utils.load_postgre.create_engine')
    def test_load_to_postgre_success(self, mock_create_engine):
        # Prepare DataFrame
        df = pd.DataFrame({'a': [1, 2]})
        # Setup fake engine and connection context manager
        dummy_con = mock.MagicMock()
        conn_cm = mock.MagicMock()
        conn_cm.__enter__.return_value = dummy_con
        mock_engine = mock.MagicMock()
        mock_engine.connect.return_value = conn_cm
        mock_create_engine.return_value = mock_engine
        # Patch df.to_sql to track calls
        df.to_sql = mock.MagicMock()

        # Capture stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            load_to_postgre(df, 'db_url')
        output = buf.getvalue()

        # Assertions
        mock_create_engine.assert_called_once_with('db_url')
        df.to_sql.assert_called_once_with(
            'fashiontoscrape', con=dummy_con, if_exists='append', index=False
        )
        self.assertIn('Data berhasil ditambahkan!', output)

    @mock.patch('utils.load_postgre.create_engine')
    def test_load_to_postgre_error_on_connect(self, mock_create_engine):
        # Prepare DataFrame
        df = pd.DataFrame({'a': [1]})
        # Engine.connect raises Exception
        mock_engine = mock.MagicMock()
        mock_engine.connect.side_effect = Exception('DB down')
        mock_create_engine.return_value = mock_engine
        df.to_sql = mock.MagicMock()

        buf = io.StringIO()
        with redirect_stdout(buf):
            load_to_postgre(df, 'db_url')
        output = buf.getvalue()

        # Should print error message and not call to_sql
        mock_create_engine.assert_called_once_with('db_url')
        df.to_sql.assert_not_called()
        self.assertIn('Terjadi kesalahan saat menyimpan data: DB down', output)

    @mock.patch('utils.load_postgre.create_engine')
    def test_load_to_postgre_error_on_to_sql(self, mock_create_engine):
        # Prepare DataFrame
        df = pd.DataFrame({'a': [1]})
        # Setup fake engine/connection
        dummy_con = mock.MagicMock()
        conn_cm = mock.MagicMock()
        conn_cm.__enter__.return_value = dummy_con
        mock_engine = mock.MagicMock()
        mock_engine.connect.return_value = conn_cm
        mock_create_engine.return_value = mock_engine
        # df.to_sql raises Exception
        def fake_to_sql(table, con, if_exists, index):
            raise Exception('Write failed')
        df.to_sql = fake_to_sql

        buf = io.StringIO()
        with redirect_stdout(buf):
            load_to_postgre(df, 'db_url')
        output = buf.getvalue()

        # Should print error message
        mock_create_engine.assert_called_once_with('db_url')
        self.assertIn('Terjadi kesalahan saat menyimpan data: Write failed', output)

if __name__ == '__main__':
    unittest.main()
