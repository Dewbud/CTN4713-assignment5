import psycopg2
from os import getenv

def connection():
    return psycopg2.connect(getenv('DATABASE_URL'))

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = connection()

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return True
        return False

def migrate():
    """ Migrate database """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id          SERIAL      NOT NULL PRIMARY KEY,
            firstname   VARCHAR(50) NOT NULL,
            lastname    VARCHAR(50) NOT NULL,
            email       VARCHAR(64) NOT NULL,
            age         INT         NOT NULL,
            location    VARCHAR(64) NOT NULL,
            date        VARCHAR(64) NOT NULL
        )
        """,
    )
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = connection()
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            print(command)
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
