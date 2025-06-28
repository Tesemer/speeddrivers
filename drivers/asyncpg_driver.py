from abstract_driver import AbstractDriver
import asyncpg

class AsyncpgDriver(AbstractDriver):
    def __init__(self, config):
        super().__init__(config)
        self.conn = None

    async def connect(self):
        db_url = (
                f'postgresql://{self.config.get('database', 'USER')}:' +
                f'{self.config.get('database', 'PASSWORD')}@' +
                f'{self.config.get('database', 'HOST')}:' +
                f'{self.config.get('database', 'PORT')}/' +
                f'{self.config.get('database', 'DATABASE_NAME')}'
        )
        self.conn = await asyncpg.connect(db_url)

    async def handle_workload(self):
        rows = await self.conn.fetchrow('SELECT * FROM datatable')
        print("hello from asyncpg!\n", rows)

    async def close_connection(self):
        if self.conn:
            await self.conn.close()