import psycopg2
import configparser
import os

# Reading the config
configParser = configparser.ConfigParser()
configFilePath = os.getcwd() + "/config.cfg"
configParser.read_file(open(configFilePath))
password = configParser.get('My Section', 'password')

conn = None
cursor = None
try:
    conn = psycopg2.connect(
        host = "localhost",
        database = "python_driver_db",
        user = "postgres",
        password = password,
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

