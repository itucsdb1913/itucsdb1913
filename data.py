import psycopg2
import psycopg2.extras


class Database:

    def __init__(self, dbname="d7a5dl9hnei5sp", user="aqqfheodautezc",
                 password="579a54a9c7f0b81df63811b9c7829d946b2bbb04d5e6917b4ddccaa536f430dc",
                 host="ec2-54-246-100-246.eu-west-1.compute.amazonaws.com"):
        self.con = psycopg2.connect(database=dbname, user=user, password=password, host=host)
        self.cur = self.con.cursor()

    def add_user(self, user):
        with self.con as conn:
            cursor = conn.cursor()
            query = "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (user.name, user.username, user.password))
            conn.commit()

    def get_user(self, username=None, id=None):
        if id is not None:
            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM users WHERE id = %s"
                cursor.execute(query, [id])
                result = cursor.fetchone()
            return result
        else:
            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, [username])
                result = cursor.fetchone()
            return result

    def delete_user(self, id):
        with self.con as conn:
            cursor = conn.cursor()
            playlists = self.get_playlists(id)
            for playlist in playlists:
                self.delete_playlist(playlist['id'])
            query = "DELETE from users WHERE id=%s"
            cursor.execute(query, [id])
            conn.commit()

    def get_songs(self, playlistid):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM songs WHERE playlistid = %s"
            cursor.execute(query, [playlistid])
            songs = cursor.fetchall()
        return songs

    def get_playlist(self, id):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM playlists WHERE id = %s"
            cursor.execute(query, [id])
            playlist = cursor.fetchone()
        return playlist

    def get_playlists(self, userid):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM playlists WHERE userid = %s"
            cursor.execute(query, [userid])
            playlists = cursor.fetchall()
        return playlists

    def get_public_playlists(self):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM playlists WHERE (isprivate = 0) LIMIT 10"
            cursor.execute(query)
            playlists = cursor.fetchall()
        return playlists

    def create_playlist(self, title, comment, userid, isprivate):
        with self.con as conn:
            cursor = conn.cursor()
            query = "INSERT INTO playlists(title, comment, userid, isprivate) VALUES(%s, %s, %s, %s)"
            cursor.execute(query, (title, comment, userid, isprivate))
            query2 = "UPDATE users SET totalplaylist=totalplaylist+1 WHERE id=%s"
            cursor.execute(query2, [userid])
            conn.commit()

    def update_playlist(self, playlistid, title, comment, isprivate):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = 'UPDATE playlists SET title=%s, comment=%s, isprivate=%s WHERE id = %s'
            cursor.execute(query, (title, comment, isprivate, playlistid))
            self.con.commit()

    def update_user(self, id, name=None, password=None):
        with self.con.cursor() as cursor:
            if name is not None:
                    query = "UPDATE users SET name=%s WHERE id=%s"
                    cursor.execute(query, (name, id))
            if password is not None:
                    query = "UPDATE users SET password=%s WHERE id=%s"
                    cursor.execute(query, (password, id))
            self.con.commit()

    def delete_song(self, songid, playlistid):
        with self.con as conn:
            cursor = conn.cursor()
            query = "DELETE FROM songs WHERE id = %s"
            cursor.execute(query, [songid])
            query2 = "UPDATE playlists set songnum = songnum - 1 WHERE id = %s"
            cursor.execute(query2, [playlistid])
            conn.commit()

    def delete_playlist(self, playlistid):
        with self.con as conn:
            cursor = conn.cursor()
            delete_songs = "DELETE FROM songs where playlistid = %s"
            cursor.execute(delete_songs, [playlistid])
            delete_playlist = "DELETE FROM playlists where id = %s"
            cursor.execute(delete_playlist, [playlistid])
            get_userid = "SELECT userid FROM playlists WHERE id=%s"
            cursor.execute(get_userid, [playlistid])
            userid = cursor.fetchone()
            query2 = "UPDATE users SET totalplaylist=totalplaylist-1 WHERE id = %s"
            cursor.execute(query2, [userid)
            conn.commit()

    def add_song(self, title, artist, genre, duration, playlistid):
        with self.con as conn:
            cursor = conn.cursor()
            query = "INSERT INTO songs(title, artist, genre, duration, playlistid) VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(query, (title, artist, genre, duration, playlistid))
            query2 = "UPDATE playlists set songnum = songnum + 1 WHERE id = %s"
            cursor.execute(query2, [playlistid])
            conn.commit()

    def get_song(self, songid):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = 'SELECT * FROM songs WHERE id = %s'
            cursor.execute(query, [songid])
            song = cursor.fetchone()
        return song

    def update_song(self, title, artist, genre, duration, songid):
        with self.con as conn:
            cursor = conn.cursor()
            query = 'UPDATE songs SET title=%s, artist=%s, genre=%s, duration=%s WHERE id=%s'
            cursor.execute(query, (title, artist, genre, duration, songid))
            conn.commit()

    def total_song(self, userid):
        with self.con as conn:
            cursor = conn.cursor()
            query = 'SELECT sum(songnum) FROM playlists WHERE userid=%s'
            cursor.execute(query, [userid])
            result = cursor.fetchone()
            query2 = "UPDATE users SET totalsong=%s WHERE id=%s"
            cursor.execute(query2, [result, userid])
            conn.commit()
        return result
