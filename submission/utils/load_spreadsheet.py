from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ──── SPREADSHEET CONFIG ─────────────────────────────────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = './google_sheets_api.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SPREADSHEET_ID = '1uO3Pkg42q63O8D4Xs97z4AX9_v8ZdYB1afTPFdu3HOY'
SHEET_NAME = 'Sheet1'

# ─── LOAD TO GOOGLE SPREADSHEET ──────────────────────────────────────────────────────────────────
def load_to_spreadsheets(df):
    """Fungsi untuk menyimpan data ke dalam google spreadsheets."""
    try:
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        # Siapkan data untuk diunggah
        values = [df.columns.tolist()] + df.values.tolist()

        body = {
            'values': values
        }
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_NAME,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()

        print(f"Upload result: {result}")
        print(f"Berhasil mengupload {len(df)} baris data!")
    except Exception as e:
        print(f"An error occurred: {e}")