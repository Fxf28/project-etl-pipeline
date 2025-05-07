from utils import *

# ─── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    base_url = 'https://fashion-studio.dicoding.dev/'
    db_url = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashion_products'

    try:
        products = scrape_product(base_url)
        print("✅ Scraping selesai.")
    except Exception as e:
        print(f"❌ Gagal scraping: {e}")
        return

    try:
        df = full_clean(products)
        print("✅ Cleaning selesai.")
        print("✅ Berikut preview data:")
        print(df)
    except Exception as e:
        print(f"❌ Gagal cleaning data: {e}")
        return

    try:
        load_to_csv(df=df, filepath='products.csv')
        print("✅ Data berhasil disimpan ke CSV.")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke CSV: {e}")

    try:
        load_to_spreadsheets(df=df)
        print("✅ Data berhasil disimpan ke Google Sheets.")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke Google Sheets: {e}")

    try:
        load_to_postgre(df, db_url)
        print("✅ Data berhasil dimasukkan ke PostgreSQL.")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke PostgreSQL: {e}")

if __name__ == '__main__':
    main()