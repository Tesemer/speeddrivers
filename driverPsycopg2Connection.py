import psycopg2

conn = None
cursor = None
try:
    conn = psycopg2.connect(
        host = "localhost",
        database = "python_driver_db",
        user = "postgres",
        password = "N*63fza*E5gUrayE",
        port = 5432
    )
    cursor = conn.cursor()

    create_script = '''CREATE TABLE datatable (id SERIAL PRIMARY KEY, 
                                               field0 VARCHAR(100), 
                                               field1 VARCHAR(100), 
                                               field2 VARCHAR(100), 
                                               field3 VARCHAR(100), 
                                               field4 VARCHAR(100), 
                                               field5 VARCHAR(100), 
                                               field6 VARCHAR(100), 
                                               field7 VARCHAR(100), 
                                               field8 VARCHAR(100), 
                                               field9 VARCHAR(100));'''
    cursor.execute(create_script)
    conn.commit()
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
    if cursor is not None:
        cursor.close()

