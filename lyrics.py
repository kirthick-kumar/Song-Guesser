import requests
from bs4 import BeautifulSoup
import random


class Lyrics:
    def __init__(self, songs, artists):
        self.songs_list = songs
        self.artist_list = artists
        self.lyric_list = []


    def get_lyrics(self):
        songs_to_remove = []
        print("Loading Songs")
        for i in range(len(self.songs_list)):
            lyrics = ''
            song = ''
            for char in self.songs_list[i]:
                if char in '!@#$%^&*()-=_+{}[];",.<>?/\|':
                    break
                song += char
            song = ''.join(filter(lambda x: x.isalpha() or x.isdigit() or x.isspace(), song))
            artist = ''.join(filter(lambda x: x.isalpha() or x.isdigit() or x.isspace(), self.artist_list[i]))
            if song[-1] == ' ':
                song = song.rstrip(song[-1])
            print(f"{i+1}: {song} {artist}")
            page = requests.get(url=f"https://genius.com/{artist.replace(' ', '-')}-{song.replace(' ', '-')}-lyrics")
            print(f"https://genius.com/{artist.replace(' ', '-')}-{song.replace(' ', '-')}-lyrics")
            soup = BeautifulSoup(page.text, 'html.parser')
            result = soup.find(name="div", class_="Lyrics__Container-sc-1ynbvzw-5 Dzxov")
            try:
                for i in result:
                    if '<br/>' in str(i):
                        lyrics += "\n"
                    else:
                        lyrics += i.text
            except TypeError:
                print(f"The lyrics are not available for {self.songs_list[i]}")
                songs_to_remove.append(self.songs_list[i])
            else:
                lyric = ''
                for i in range(len(lyrics) - 1):
                    if lyrics[i] == '\n' and lyrics[i + 1] == '\n':
                        char = ''
                    else:
                        char = lyrics[i]
                    lyric += char
                self.lyric_list.append(lyric)
        # Removing songs without lyrics
        for song in songs_to_remove:
            self.songs_list.remove(song)
        return len(self.songs_list)

    def get_lyric_section(self):
        # Getting 1-3 lines from the lyrics
        i = random.randint(0, len(self.lyric_list) - 1)
        ans = ''
        song = self.songs_list[i]
        lyrics = self.lyric_list[i]
        lyric_list_section = lyrics.split("\n")
        lyric_section = [lyric for lyric in lyric_list_section if "[" not in lyric and "]" not in lyric and song not in lyric]
        try:
            random_line = random.randint(0, len(lyric_section) - 1)
        except ValueError:
            random_line = 0
            ans = song
        str_lyric_section = '\n'.join([str(lyric) for lyric in lyric_section[random_line:random_line + 3]]) + ans
        options = random.sample(self.songs_list, 3)
        if self.songs_list[i] not in options:
            options.append(self.songs_list[i])
        else:
            for s in self.songs_list:
                if s not in options:
                    options.append(s)
                    break
        return str_lyric_section, song, random.sample(options, len(options))
