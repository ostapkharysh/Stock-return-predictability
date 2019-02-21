

#db_link = 'sqlite://///media/ostapkharysh/SP_PHD_U3/database/NO_title_GOOG.db'
#db_link = 'postgresql://ostap:12345@localhost:5432/goog'   #google with no titles
db_link = 'postgresql://ostap:12345@localhost:5432/googtitle'
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
    DATE = Column(String(20))
    #SOURCECOLLECTIONIDENTIFIER = Column(Integer)
    SOURCECOMMONNAME = Column(String(50))
    DOCUMENTIDENTIFIER = Column(String(300))
    #LOCATIONS = Column(String(10003))
    ORGANIZATIONS = Column(String(6000)) # REDUCE
    TONE = Column(String(150)) 
    GCAM = Column(String(30000))
    ALLNAMES = Column(String(6000))  # REDUCE
    TITLE = Column(String(2000))

    company = relationship(Company)
    company_id = Column(Integer, ForeignKey('company.id'))



# Create an engine that stores data in the local directory's
engine = create_engine(db_link)

# Create all tables in the engine.
Base.metadata.create_all(engine)
