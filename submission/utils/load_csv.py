import pandas as pd

# ─── LOAD TO CSV ───────────────────────────────────────────────────────────────────────
def load_to_csv(df, filepath):
    """Fungsi untuk menyimpan data ke dalam CSV."""
    try:
        df.to_csv(filepath, index=False)
        print(f"Data berhasil disimpan ke {filepath}")
    except Exception as e:
        print(f"ERROR saat menyimpan ke CSV: {e}")
        raise