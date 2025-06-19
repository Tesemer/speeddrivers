import psycopg2

conn = None
cursor = None
try:
    conn = psycopg2.connect(
        host = "localhost",
        database = "bpmn",
        user = "postgres",
        password = "Pelmeni",
        port = 5432
    )
    cursor = conn.cursor()

    create_script = '''SELECT * FROM "Diagram"'''
    cursor.execute(create_script)
    diagrams = cursor.fetchall()
    for diagram in diagrams:
        print(diagram)

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
    if cursor is not None:
        cursor.close()

