from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
 
Base = declarative_base()

class Manifest(Base):

    __tablename__ = 'manifest'

    primary_key = Column(Integer, autoincrement=True, primary_key=True)
    # section_id,section_name,row_id,row_name
    section_id = Column(Integer)
    section_name = Column(String(40))
    row_id = Column(Integer)
    row_name = Column(String(40))

def get_engine():
    return create_engine('sqlite:///manifest_data.db')

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def create_all():
    Base.metadata.create_all(get_engine())

if __name__ == '__main__':
    create_all()
    print "Created the table"
