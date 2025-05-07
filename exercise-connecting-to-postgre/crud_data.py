from sqlalchemy import text, create_engine, select, Table, MetaData, update, delete

DATABASE_URL = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/companydb'

engine = create_engine(DATABASE_URL)

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    autoload_with=engine
)

# Menghapus data dengan id == 1
with engine.connect() as connection:
    try:
        delete_statement = delete(user_table).where(user_table.c.id == 3)
        result = connection.execute(delete_statement)

        connection.commit()
        print("Data berhasil dihapus!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Memperbarui data dengan id 2 dengan mengganti nama belakangnya menjadi Sutisna
with engine.connect() as connection:
    try:
        update_statement = update(user_table).where(user_table.c.id == 2).values(last_name='Sutisna')
        result = connection.execute(update_statement)

        connection.commit()
        print("Data berhasil diubah!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Membaca data terbaru
with engine.connect() as connection:
    try:
        # select_statement = text("SELECT * FROM users;") # Gunakan ini jika ingin menggunakan text()
        select_statement = select(user_table)
        result = connection.execute(select_statement)

        for row in result:
            print(row)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")