from abstract_driver import AbstractDriver
import asyncpg

class AsyncpgDriver(AbstractDriver):
    def __init__(self, config, workload):
        super().__init__(config, workload)
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
        async with self.conn.transaction():
            for query in self.workload:
                await self.conn.execute(query)

    async def close_connection(self):
        if self.conn:
            await self.conn.close()