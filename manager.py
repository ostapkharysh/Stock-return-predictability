from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from db_management.DB import Base, Company, News, db_link


def add_company(company):
    engine = create_engine(db_link) #  pool_size=20, max_overflow=0
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)

    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()

    session = DBSession()

    data = session.query(Company).all()
    print(data)
    if company in [el.name for el in data]:
        return "There is already a Table with such name: {}".format(company)

    # Insert a company in the Comapny table
    DBcompany = Company(name=company)
    session.add(DBcompany)
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    
    return "The new table {} is created.".format(company)


def add_news(info_dict):
    # Insert an news in the address table
    
    engine = create_engine(db_link)
    engine.pool_timeout = 60
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()


    company = info_dict['comp_index']

    cur_company = session.query(Company).filter_by(name=company).first()
    if not cur_company:
        print("Not found. Creating company: {}".format(company))
        cur_company = Company(name=company)

    try:
        key = info_dict.keys()
        # WITH SOURCECOLLECTIONIDENTIFIER  AND TITLE
        #new_news = News(DATE=str(info_dict[key[0]]), SOURCECOLLECTIONIDENTIFIER= int(info_dict[key[1]]), SOURCECOMMONNAME=info_dict[key[2]], DOCUMENTIDENTIFIER=info_dict[key[3]], LOCATIONS=info_dict[key[4]],
        #                ORGANIZATIONS=info_dict[key[5]], TONE=info_dict[key[6]], GCAM=info_dict[key[7]], ALLNAMES=info_dict[key[8]], TITLE=info_dict[key[9]], company_id=info_dict[key[10]])

        #WITHOUT SOURCECOLLECTIONIDENTIFIER  AND TITLE
        new_news = News(DATE=str(info_dict[key[0]]),
                        SOURCECOMMONNAME=info_dict[key[2]], DOCUMENTIDENTIFIER=info_dict[key[3]],
                        #LOCATIONS=info_dict[key[4]],
                        ORGANIZATIONS=info_dict[key[5]], TONE=info_dict[key[6]], GCAM=info_dict[key[7]],
                        ALLNAMES=info_dict[key[8]], company_id=cur_company.id)
        session.add(new_news)
        session.commit()

    except IntegrityError:
        session.rollback()
        return 'The link provided seems to exist in DB: {}'.format(info_dict[key[3]])

    except InvalidRequestError:
        session.rollback()
        return 'You are requesting access to the non-existing source'

    try:
        #print("COMMITING...")
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

    #print("The news has been successfully added")
