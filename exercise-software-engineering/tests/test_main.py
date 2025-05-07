from unittest import TestCase, mock
from main import main

class TestIntegrations(TestCase):
    @mock.patch('builtins.input', return_value='q')
    def test_quit_program(self, mock_input):
        # Pilihan 'q' harus keluar dengan SystemExit
        with self.assertRaises(SystemExit):
            main()

    @mock.patch('main.get_numbers', return_value=[2.0, 2.1])
    @mock.patch('builtins.input', return_value='1')
    def test_addition(self, mock_input, mock_get_numbers):
        # Operasi penjumlahan berjalan normal, pastikan cetak hasil di antara banyak print
        with mock.patch('builtins.print') as mock_print:
            main()
        mock_print.assert_any_call('Hasil: 4.1')

    @mock.patch('main.get_numbers', side_effect=ValueError("Masukkan angka dengan spasi sebagai pemisah dan gunakan '.' ketika menggunakan desimal."))
    @mock.patch('builtins.input', return_value='1')
    def test_value_error(self, mock_input, mock_get_numbers):
        # ValueError pada parsing angka
        with mock.patch('builtins.print') as mock_print:
            main()
        mock_print.assert_any_call(
            "Terjadi kesalahan ValueError: Masukkan angka dengan spasi sebagai pemisah dan gunakan '.' ketika menggunakan desimal."
        )

    @mock.patch('main.get_numbers', side_effect=ZeroDivisionError("Anda tidak bisa membagi bilangan dengan angka 0!"))
    @mock.patch('builtins.input', return_value='4')
    def test_zero_division_error(self, mock_input, mock_get_numbers):
        # ZeroDivisionError saat pembagian
        with mock.patch('builtins.print') as mock_print:
            main()
        mock_print.assert_any_call(
            "Terjadi kesalahan ZeroDivisionError: Anda tidak bisa membagi bilangan dengan angka 0!"
        )

    @mock.patch('main.get_numbers', side_effect=TypeError("Invalid Data Type!"))
    @mock.patch('builtins.input', return_value='4')
    def test_general_exception(self, mock_input, mock_get_numbers):
        # Exception selain ValueError/ZeroDivisionError
        with mock.patch('builtins.print') as mock_print:
            main()
        mock_print.assert_any_call("Terjadi kesalahan Invalid Data Type!")
