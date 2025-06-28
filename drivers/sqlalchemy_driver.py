from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from abstract_driver import AbstractDriver
from schema import Base, Datatable


class SqlalchemyDriver(AbstractDriver):
    def __init__(self, config):
        super().__init__(config)
        self.engine = None
        self.session = None

    async def connect(self):
        db_url = (
                f'postgresql://{self.config.get('database', 'USER')}:' +
                f'{self.config.get('database', 'PASSWORD')}@' +
                f'{self.config.get('database', 'HOST')}:' +
                f'{self.config.get('database', 'PORT')}/' +
                f'{self.config.get('database', 'DATABASE_NAME')}'
        )
        self.engine = sa.create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    async def handle_workload(self):
        stmt = sa.select(Datatable)
        row = self.session.execute(stmt).first()
        print("hello from sqlalchemy!\n return row id:", row.Datatable.id)

    async def close_connection(self):
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
