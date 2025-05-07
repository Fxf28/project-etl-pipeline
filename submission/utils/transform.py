import pandas as pd
import numpy as np

# ─── TRANSFORM DATA TO DATAFRAME ──────────────────────────────────────────────────────────────
def transform_to_dataframe(data):
    """Mengubah data menjadi DataFrame."""
    try:
        if data is None:
            raise ValueError("Input data cannot be None.")

        df = pd.DataFrame(data)
        # Pastikan kolom yang akan diolah bertipe string
        str_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        for col in str_columns:
            if col in df.columns:
                df[col] = df[col].astype('string')
        return df
    except Exception as e:
        print(f"Error saat membuat DataFrame: {e}")
        raise

# ─── HANDLE TITLE ───────────────────────────────────────────────────────────────────────────────
def handle_title(df, column='Title'):
    """Membersihkan kolom Title pada DataFrame"""
    try:
        df[column] = df[column].str.strip()
        df[column] = df[column].replace(['', 'Unknown Product'], pd.NA)
        return df
    except Exception as e:
        print(f"Error saat membersihkan {column}: {e}")
        raise

# ─── HANDLE PRICE ───────────────────────────────────────────────────────────────────────────────
def handle_price(df, column='Price'):
    """Membersihkan kolom Price pada DataFrame"""
    try:
        df[column] = df[column].str.strip()
        df[column] = df[column].replace('Price Unavailable', pd.NA)
        # Menangani harga yang menggunakan koma sebagai pemisah desimal
        df[column] = pd.to_numeric(df[column].str.replace(r'[\$,]', '', regex=True).str.replace(',', '.'), errors='coerce')
        return df
    except Exception as e:
        print(f"Error saat membersihkan {column}: {e}")
        raise

# ─── CONVERT PRICE ───────────────────────────────────────────────────────────────────────────────
def convert_price_to_rupiah(df, column='Price', rate=16000):
    """Konversi nilai kolom Price ke Rupiah pada DataFrame"""
    try:
        df[column] = df[column] * rate
        return df
    except Exception as e:
        print(f"Error saat konversi Price ke Rupiah: {e}")
        raise

# ─── HANDLE RATING ───────────────────────────────────────────────────────────────────────────────
def handle_rating(df, column='Rating'):
    """Membersihkan kolom Rating pada DataFrame"""
    try:
        df[column] = (
            df[column]
            .str.strip()
            .replace('Rating: ⭐ Invalid Rating / 5', pd.NA)
        )
        df[column] = df[column].str.extract(r'(\d+(\.\d+)?)')[0]
        df[column] = pd.to_numeric(df[column], errors='coerce')
        return df
    except Exception as e:
        print(f"Error saat membersihkan {column}: {e}")
        raise

# ─── HANDLE COLORS ───────────────────────────────────────────────────────────────────────────────
def handle_colors(df, column='Colors'):
    """Membersihkan kolom Colors pada DataFrame"""
    try:
        df[column] = df[column].str.extract(r'(\d+)')
        df[column] = pd.to_numeric(df[column], errors='coerce')
        return df
    except Exception as e:
        print(f"Error saat membersihkan {column}: {e}")
        raise

# ─── HANDLE SIZE ───────────────────────────────────────────────────────────────────────────────
def handle_size(df, column='Size'):
    """Membersihkan kolom Size pada DataFrame"""
    try:
        df[column] = df[column].str.extract(r'Size:\s*(\w+)')[0]
        df[column] = df[column].fillna(pd.NA).astype('string')
        return df
    except Exception as e:
        print(f"Error saat membersihkan {column}: {e}")
        raise

# ─── HANDLE GENDER ───────────────────────────────────────────────────────────────────────────────
def handle_gender(df, column='Gender'):
    """Membersihkan kolom Gender pada DataFrame"""
    try:
        df[column] = df[column].str.extract(r'Gender:\s*(\w+)')[0]
        df[column] = df[column].fillna(pd.NA).astype('string')  # Tipe data string dengan pd.NA
        return df
    except Exception as e:
        print(f"Error saat membersihkan {column}: {e}")
        raise

# ─── HANDLE TIMESTAMP ───────────────────────────────────────────────────────────────────────────────
def handle_timestamp(df, column='Timestamp'):
    """Membersihkan dan memformat kolom Timestamp pada DataFrame"""
    try:
        # Mengonversi ke tipe datetime dengan coerce untuk nilai yang tidak valid
        df[column] = pd.to_datetime(df[column], errors='coerce')
        # Menambahkan pemformatan dengan T sebagai pemisah
        df[column] = df[column].dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return df
    except Exception as e:
        print(f"Error saat membersihkan {column}: {e}")
        raise

# ─── DROP MISSING VALUES ────────────────────────────────────────────────────────────────────────
def drop_missing_values(df):
    """Menghapus nilai hilang pada kolom Title, Price dan Rating"""
    try:
        df = df.dropna(subset=['Title', 'Price', 'Rating'])
        return df
    except Exception as e:
        print(f"Error saat menghapus baris dengan nilai kosong: {e}")
        raise

# ─── FULL CLEAN ───────────────────────────────────────────────────────────────────────────────
def full_clean(data):
    """
    Pipeline lengkap:
    - Transform ke DataFrame
    - Handle Title, Price (convert rupiah juga), Rating, Colors, Size, Gender, Timestamp
    - Drop missing di Title/Price/Rating
    """
    try:
        df = transform_to_dataframe(data)
        return (df
                .pipe(handle_title)
                .pipe(handle_price)
                .pipe(convert_price_to_rupiah)
                .pipe(handle_rating)
                .pipe(handle_colors)
                .pipe(handle_size)
                .pipe(handle_gender)
                .pipe(handle_timestamp)
                .pipe(drop_missing_values))
    except Exception as e:
        print(f"ERROR in full_clean pipeline: {e}")
        raise