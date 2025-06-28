from sqlalchemy.orm import declarative_base
import sqlalchemy as sa

Base = declarative_base()
class Datatable(Base):
    __tablename__ = 'datatable'
    id = sa.Column(sa.Integer, primary_key=True)
    field0 = sa.Column(sa.String)
    field1 = sa.Column(sa.String)
    field2 = sa.Column(sa.String)
    field3 = sa.Column(sa.String)
    field4 = sa.Column(sa.String)
    field5 = sa.Column(sa.String)
    field6 = sa.Column(sa.String)
    field7 = sa.Column(sa.String)
    field8 = sa.Column(sa.String)
    field9 = sa.Column(sa.String)