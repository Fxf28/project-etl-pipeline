import os
import tempfile
import io
from unittest import TestCase
from contextlib import redirect_stdout

import pandas as pd

from utils.load_csv import *

class TestLoadToCSV(TestCase):
    def test_load_to_csv_success(self):
        # Prepare sample DataFrame
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        # Use temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'output.csv')
            buf = io.StringIO()
            with redirect_stdout(buf):
                load_to_csv(df, filepath)
            output = buf.getvalue()
            # Check print message
            self.assertIn(f"Data berhasil disimpan ke {filepath}", output)
            # Check file existence and content
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertIn('col1,col2', content)
            self.assertIn('1,a', content)
            self.assertIn('2,b', content)

    def test_load_to_csv_error(self):
        # Prepare DataFrame
        df = pd.DataFrame({'col': [1]})
        # Monkey-patch to_csv to raise IOError
        def fake_to_csv(fp, index=False):
            raise IOError("Disk is full")
        df.to_csv = fake_to_csv

        buf = io.StringIO()
        # Expect IOError and error message printed
        with self.assertRaises(IOError):
            with redirect_stdout(buf):
                load_to_csv(df, 'dummy.csv')
        output = buf.getvalue()
        self.assertIn('ERROR saat menyimpan ke CSV: Disk is full', output)

if __name__ == '__main__':
    unittest.main()
