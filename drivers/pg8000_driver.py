import pg8000.native

from abstract_driver import AbstractDriver


class Pg8000(AbstractDriver):
    def __init__(self, config, workload):
        super().__init__(config, workload)
        self.conn = None

    async def connect(self):
        self.conn = pg8000.native.Connection(
            database = self.config.get('database', 'DATABASE_NAME'),
            user = self.config.get('database', 'USER'),
            password = self.config.get('database', 'PASSWORD'),
            host = self.config.get('database', 'HOST'),
            port = self.config.get('database', 'PORT')
        )

    async def handle_workload(self):
        for query in self.workload:
            self.conn.run(query)

    async def close_connection(self):
        if self.conn:
            self.conn.close()