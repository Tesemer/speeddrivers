import psycopg2

from abstract_driver import AbstractDriver


class Psycopg2Driver(AbstractDriver):
    def __init__(self, config):
        super().__init__(config)
        self.conn = None
        self.cursor = None

    async def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.config.get('database', 'HOST'),
                database=self.config.get('database', 'DATABASE_NAME'),
                user=self.config.get('database', 'USER'),
                password=self.config.get('database', 'PASSWORD'),
                port=self.config.get('database', 'PORT')
            )
            self.cursor = self.conn.cursor()

        except Exception as error:
            print(error)

    async def handle_workload(self):
        self.cursor.execute("SELECT * FROM datatable")
        rows = self.cursor.fetchall()
        print("hello from psycopg2!\n", rows)

    async def close_connection(self):
        if self.conn:
            self.conn.close()
        if self.cursor:
            self.cursor.close()