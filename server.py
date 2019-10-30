from flask import Flask
import views
from database import Database
from movie import Movie


app = Flask(__name__)

app.config.from_object("settings")

app.add_url_rule("/", view_func=views.home_page)
app.add_url_rule("/movies", view_func=views.movies_page, methods=["GET", "POST"])
app.add_url_rule("/movies/<int:movie_key>", view_func=views.movie_page)
app.add_url_rule("/new-movie", view_func=views.movie_add_page, methods=["GET", "POST"])
app.add_url_rule(
    "/movies/<int:movie_key>/edit",
    view_func=views.movie_edit_page,
    methods=["GET", "POST"],
)


db = Database()
app.config["db"] = db




if __name__ == "__main__":
    app.run(debug=True)
