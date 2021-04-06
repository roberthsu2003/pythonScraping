from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,Float,String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class TSMC(Base):
    __tablename__ = 'table1'
    id = Column(Integer,primary_key=True)
    year = Column(String,index=True)
    field1 = Column(Integer)
    field2 = Column(Integer)
    field3 = Column(Float)
    field4 = Column(Float)
    field5 = Column(Float)
    field6 = Column(Float)

conn = create_engine('sqlite:///tsmc.sqlite',echo=True)
Base.metadata.create_all(conn)