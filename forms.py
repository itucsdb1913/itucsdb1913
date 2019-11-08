from wtforms import Form, StringField, PasswordField, validators, TextAreaField


# register forms
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# playlist forms
class PlaylistForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=50)])
    comment = TextAreaField('Comment(Optional)', [validators.Length(max=300)])


# song forms
class SongForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=50)])
    artist = StringField('Artist Name', [validators.Length(min=1, max=50)])
    genre = StringField('Genre', [validators.Length(min=1, max=50)])
    duration = StringField('Duration', [validators.Length(min=1, max=50)])


