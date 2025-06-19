import psycopg2

conn = None
cursor = None
try:
    conn = psycopg2.connect(
        host = "localhost",
        database = "python_driver_db",
        user = "postgres",
        password = "Pelmeni",
        port = 5432
    )
    cursor = conn.cursor()

    create_script = '''SELECT * FROM "datatable";'''
    cursor.execute(create_script)
    conn.commit()
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
    if cursor is not None:
        cursor.close()

