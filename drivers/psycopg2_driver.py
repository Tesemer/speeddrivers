import psycopg2
import time

from abstract_driver import AbstractDriver


class Psycopg2Driver(AbstractDriver):
    def __init__(self, config, workload):
        super().__init__(config, workload)
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
        for query in self.workload:
            self.cursor.execute(query)

    async def handle_timed_workload(self):
        times = []
        for query in self.workload:
            start = time.perf_counter()  # Start time
            self.cursor.execute(query)
            times.append(time.perf_counter() - start)  # End time - Start time
        return times

    async def close_connection(self):
        if self.conn:
            self.conn.close()
        if self.cursor:
            self.cursor.close()