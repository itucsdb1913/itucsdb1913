import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    '''CREATE TABLE IF NOT EXISTS users(
        name varchar(25), 
        id SERIAL, 
        username varchar(25), 
        password varchar(100),
        totalplaylist INTEGER DEFAULT 0, 
        totalsong INTEGER DEFAULT 0, 
        PRIMARY KEY (id)
    )''',
    '''CREATE TABLE IF NOT EXISTS playlists(
        id SERIAL,
        userid INTEGER REFERENCES users(id),
        comment text,
        create_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
        songnum integer DEFAULT 0,
        isprivate integer,
        title varchar(50),
        PRIMARY KEY (id)
    )''',
    '''CREATE TABLE IF NOT EXISTS songs(
        id SERIAL,
        title varchar(50),
        artist varchar(50),
        duration varchar(5),
        playlistid INTEGER REFERENCES playlists(id),
        genre varchar(10),
        bpm varchar(5),
        PRIMARY KEY (id)
    )'''
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
