# credits to http://www.sqlitetutorial.net


import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO News(V2.1DATE, V2SOURCECOLLECTIONIDENTIFIER, V2SOURCECOMMONNAME, V2DOCUMENTIDENTIFIER, V1LOCATIONS, V1ORGANIZATIONS, V1.5TONE, V2GCAM, V2.1ALLNAMES, TITLE)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def close_db(conn):
    conn.close()
