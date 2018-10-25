

db_link = 'sqlite:////home/ostapkharysh/Documents/bt_data/DB/news_info.db'

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Agency(Base):
    __tablename__ = 'agency'
    # define columns for the table agency
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class News(Base):
    __tablename__ = 'news'
    # define columns for the table news.
    id = Column(Integer, primary_key=True)
    date_time = Column(String(250))
    title = Column(String(250))
    article_text = Column(String(1000))
    link = Column(String(250), unique=True)  # nullable=False
    agency_id = Column(Integer, ForeignKey('agency.id'))
    agency = relationship(Agency)


# Create an engine that stores data in the local directory's
engine = create_engine(db_link)

# Create all tables in the engine.
Base.metadata.create_all(engine)