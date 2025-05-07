from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = './client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SPREADSHEET_ID = '1mjQCCuFmGPvlkx0NRThM_fSkQ7HlxrmhKPhW1Bj76v0'
RANGE_NAME = 'Sheet1!A2:F11'


def main():
    try:
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        values = [
            ['Faiz', 'Jl.FxF, Kota Pahlawan', 'faiz1@example.com', 'Monitor Samsung 4K', '2', '9000000'],
            ['Alya', 'Jl.Anggrek No.5', 'alya@example.com', 'Keyboard Logitech', '1', '350000'],
            ['Raka', 'Jl.Mawar No.3', 'raka@example.com', 'Mouse Razer', '1', '500000'],
            ['Dina', 'Jl.Melati No.7', 'dina@example.com', 'Headset Sony', '2', '1500000'],
            ['Budi', 'Jl.Cempaka No.2', 'budi@example.com', 'Webcam Logitech', '1', '700000'],
            ['Siti', 'Jl.Kemuning No.8', 'siti@example.com', 'Laptop Asus', '1', '12000000'],
            ['Tono', 'Jl.Kenanga No.10', 'tono@example.com', 'SSD Samsung 1TB', '1', '2000000'],
            ['Rani', 'Jl.Angsana No.4', 'rani@example.com', 'Printer Canon', '1', '2500000'],
            ['Agus', 'Jl.Bougenville No.6', 'agus@example.com', 'Router TP-Link', '1', '400000'],
            ['Lina', 'Jl.Akasia No.1', 'lina@example.com', 'Monitor LG', '1', '8500000']
        ]

        body = {
            'values': values
        }

        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("Berhasil menambahkan 10 baris data!")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
