from unittest import TestCase, mock
import io
from contextlib import redirect_stdout

import pandas as pd

from utils.load_spreadsheet import *


class TestLoadToSpreadsheets(TestCase):
    @mock.patch('utils.load_spreadsheet.build')
    def test_load_to_spreadsheets_success(self, mock_build):
        # Prepare DataFrame
        df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})

        # Setup mocks
        mock_service = mock.MagicMock()
        mock_spreadsheets = mock.MagicMock()
        mock_values = mock.MagicMock()
        mock_append = mock.MagicMock()
        mock_execute = mock.MagicMock(return_value={'updates': {}})

        # Chain method calls
        mock_values.append.return_value.execute = mock_execute
        mock_spreadsheets.values.return_value = mock_values
        mock_service.spreadsheets.return_value = mock_spreadsheets
        mock_build.return_value = mock_service

        # Capture stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            load_to_spreadsheets(df)
        output = buf.getvalue()

        # Assertions
        mock_build.assert_called_once()
        self.assertIn('Upload result:', output)
        self.assertIn('Berhasil mengupload 2 baris data!', output)

    @mock.patch('utils.load_spreadsheet.build')
    def test_load_to_spreadsheets_error(self, mock_build):
        # Prepare DataFrame
        df = pd.DataFrame({'a': [1]})

        # Simulate build() raising an exception
        mock_build.side_effect = Exception('Google API down')

        buf = io.StringIO()
        with redirect_stdout(buf):
            load_to_spreadsheets(df)
        output = buf.getvalue()

        # Should print error message
        self.assertIn('An error occurred: Google API down', output)


if __name__ == '__main__':
    unittest.main()