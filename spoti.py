import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "5982421f095e4696a71f79b6da05f94d"
CLIENT_SECRET = "15a2dc76148d4a01be282c1919667dd2"
REDIRECT_URI = "https://open.spotify.com/"
SPOTIPY_ENDPOINT = "https://spotipy.readthedocs.io/en/2.22.1/#spotipy.client.Spotify.user_playlist_create"


class Spoti:
    def __init__(self, PLAYLIST, NUM):
        self.playlist = PLAYLIST
        self.num_of_tracks = NUM

    def get_tracks(self):
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope="playlist-modify-private",
                redirect_uri="https://open.spotify.com/",
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                show_dialog=True,
                cache_path="token.txt",
                username="Top 100",
            )
        )
        user_id = sp.current_user()["id"]

        tracks = sp.playlist_tracks(playlist_id=self.playlist, limit=self.num_of_tracks, fields="items(track(name,artists(name)))")
        songs = []
        artists = []
        for i in range(len(tracks['items'])):
            songs.append(tracks['items'][i]['track']['name'])
            artists.append(tracks['items'][i]['track']['artists'][0]['name'])
        return songs, artists
