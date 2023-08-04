from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, FloatField
import requests
from spoti import Spoti
from lyrics import Lyrics


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
score = 0
qno = -1


class SongForm(FlaskForm):
    playlist = StringField('Playlist URL: ', [validators.DataRequired()])
    amount = FloatField('Amount of songs to import: ', [validators.DataRequired()])
    submit = SubmitField('Play!', render_kw={'class': 'btn btn-success', 'style': 'background-color: #1db954'})


class GuessForm(FlaskForm):
    name = StringField('Guess the song: ', [validators.DataRequired()])
    submit = SubmitField('Next', render_kw={'class': 'btn btn-success', 'style': 'background-color: #1db954'})


@app.route("/", methods=['POST', 'GET'])
def home():
    global score, qno
    score = 0
    qno = -1
    song_form = SongForm()
    if request.method == 'POST':
        global lyrics, song
        playlist_url = song_form.playlist.data
        playlist_amount = int(song_form.amount.data)
        spoti = Spoti(playlist_url, playlist_amount)
        songs_list, artist_list = spoti.get_tracks()
        lyrics = Lyrics(songs_list, artist_list)
        tracks_imported = lyrics.get_lyrics()
        lyric_section, song, options = lyrics.get_lyric_section()
        return redirect(url_for('play'))
    return render_template("index.html", form=song_form)


@app.route('/play', methods=['POST', 'GET'])
def play():
    global lyrics, song, score, qno
    ans = song
    qno += 1
    lyric_section, song, options = lyrics.get_lyric_section()
    guess_form = GuessForm()
    lyric_list = lyric_section.split('\n')
    if request.method == 'POST':
        print(guess_form.name.data, ans)
        if guess_form.name.data.lower() == ans.lower():
            result = 'Correct'
            score += 1
        else:
            result = 'Incorrect'

        if len(lyric_list) == 1:
            lyric_list.append('.')
            lyric_list.append('.')
        elif len(lyric_list) == 2:
            lyric_list.append('.')

        return render_template('play.html', form=guess_form, lyric=lyric_list, result=result, correct_ans=ans, score=score, qno=qno)

    return render_template('play.html', form=guess_form, lyric=lyric_list, qno=qno)


if __name__ == '__main__':
    app.run(debug=True)
