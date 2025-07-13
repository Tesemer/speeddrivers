import sqlalchemy as sa
import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from abstract_driver import AbstractDriver
from schema import Base, Datatable


class SqlalchemyDriver(AbstractDriver):
    def __init__(self, config, workload):
        super().__init__(config, workload)
        self.engine = None
        self.session = None

    async def connect(self):
        db_url = (
                f'postgresql://{self.config.get("database", "USER")}:' +
                f'{self.config.get("database", "PASSWORD")}@' +
                f'{self.config.get("database", "HOST")}:' +
                f'{self.config.get("database", "PORT")}/' +
                f'{self.config.get("database", "DATABASE_NAME")}'
        )
        self.engine = sa.create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    async def handle_workload(self):
        for query in self.workload:
            self.session.execute(text(query))

    async def handle_timed_workload(self):
        times = []
        for query in self.workload:
            start = time.perf_counter()  # Start time
            self.session.execute(text(query))
            times.append(time.perf_counter() - start)  # End time - Start time
        return times

    async def close_connection(self):
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
