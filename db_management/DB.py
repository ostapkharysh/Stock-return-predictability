

db_link = 'sqlite://///media/ostapkharysh/SP_PHD_U3/database/NO_title.db'

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()


class Company(Base):
    __tablename__ = 'company'
    # define columns for the table agency
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class News(Base):
    __tablename__ = 'news'
    # define columns for the table news.
    id = Column(Integer, primary_key=True)
    DATE = Column(String(100))
    SOURCECOLLECTIONIDENTIFIER = Column(Integer)
    SOURCECOMMONNAME = Column(String(100))
    DOCUMENTIDENTIFIER = Column(String(500))
    LOCATIONS = Column(String(1000))
    ORGANIZATIONS = Column(String(500))
    TONE = Column(String(1000)) 
    GCAM = Column(String(5000))
    ALLNAMES = Column(String(1000))
    TITLE = Column(String(500))

    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship(Company)


# Create an engine that stores data in the local directory's
engine = create_engine(db_link)

# Create all tables in the engine.
Base.metadata.create_all(engine)
