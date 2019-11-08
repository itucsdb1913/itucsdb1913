from flask import Flask
from views import *

app = Flask(__name__)

app.add_url_rule("/", view_func=home)
app.add_url_rule("/playlist/<string:id>", view_func=playlist)
app.add_url_rule("/register", view_func=register, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/dashboard", view_func=dashboard)
app.add_url_rule("/create_playlist", view_func=create_playlist, methods=["GET", "POST"])
app.add_url_rule("/edit_playlist/<string:id>", view_func=edit_playlist, methods=["GET", "POST"])
app.add_url_rule("/delete_playlist/<string:id>", view_func=delete_playlist)
app.add_url_rule("/add_song/<string:id>", view_func=add_song, methods=["GET", "POST"])
app.add_url_rule("/edit_song/<string:id>", view_func=edit_song, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/edit_playlist_info/<string:id>", view_func=edit_playlist_info, methods=["GET", "POST"])


if __name__ == '__main__':
    app.secret_key = 'hello'
    app.run(debug=True)
