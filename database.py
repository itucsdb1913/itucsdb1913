import psycopg2

from movie import Movie



class Database:

    def __init__(self, dbname="d7a5dl9hnei5sp", user="aqqfheodautezc", password="579a54a9c7f0b81df63811b9c7829d946b2bbb04d5e6917b4ddccaa536f430dc", host="ec2-54-246-100-246.eu-west-1.compute.amazonaws.com"):
        self.con = psycopg2.connect(database=dbname, user=user, password=password, host=host)
        self.cur = self.con.cursor()

    def add_movie(self, movie):

        cursor = self.cur
        query = "INSERT INTO MOVIE (TITLE, YR) VALUES (%s, %s)"
        cursor.execute(query, (movie.title, movie.year))
        self.con.commit()
        movie_key = cursor.lastrowid
        return movie_key

    def update_movie(self, movie_key, movie):

        cursor = self.cur
        query = "UPDATE MOVIE SET TITLE = %s, YR = %s WHERE (ID = %s)"
        cursor.execute(query, (movie.title, movie.year, movie_key))
        self.con.commit()

    def delete_movie(self, movie_key):

        cursor = self.cur
        query = "DELETE FROM MOVIE WHERE (ID = %s)"
        cursor.execute(query, (movie_key,))
        self.con.commit()

    def get_movie(self, movie_key):

        cursor = self.cur
        query = "SELECT TITLE, YR FROM MOVIE WHERE (ID = %s)"
        cursor.execute(query, (movie_key,))
        title, year = cursor.fetchone()
        movie_ = Movie(title, year=year)
        return movie_

    def get_movies(self):
        movies = []

        cursor = self.cur
        query = "SELECT ID, TITLE, YR FROM MOVIE ORDER BY ID"
        cursor.execute(query)
        for movie_key, title, year in cursor:
            movies.append((movie_key, Movie(title, year)))
        return movies

