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


def create_task(conn, task, table_name):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO ''' + str(table_name)+''' (date_time, title, article_text, link)
              VALUES(?,?,?,?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        ) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def close_db(conn):
    conn.close()
