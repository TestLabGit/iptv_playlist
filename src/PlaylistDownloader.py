import os
import urllib.request
from io import BytesIO
from zipfile import ZipFile
import requests


class PlaylistDownloader():

    def __init__(self, playlist_array, zip_playlist_array=None):
        dirname = os.path.dirname(__file__)
        self.directory = dirname + "/playlists/"
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory) 
        self.playlist_array = playlist_array
        self.zip_playlist_array = []
        if zip_playlist_array != None:
            self.zip_playlist_array = zip_playlist_array

    def save_playlists(self):
        self.__clean()
        for ctr, value in enumerate(self.playlist_array):
            try:
                filedata = urllib.request.urlopen(value)
                datatowrite = filedata.read()
                filename = "playlist_" + str(ctr+1) + ".m3u"
                playlist_path = self.directory + filename  
                with open(playlist_path, 'wb') as f:  
                    f.write(datatowrite)
            except urllib.error.HTTPError as e:
                print('Url: {} | HTTPError reason: {}'.format(value, e.reason))
    
    def save_zip_playlist(self):
        for url in self.zip_playlist_array:
            response = requests.get(url)
            with ZipFile(BytesIO(response.content)) as zip_file:
                for file in zip_file.namelist():
                    with open((self.directory + file), "wb") as output:
                        for line in zip_file.open(file).readlines():
                            output.write(line)

    def save_raw_playlist(self):
        self.save_playlists()
        if len(self.zip_playlist_array) > 0:
            self.save_zip_playlist()
        with open(self.directory + "raw_playlist.m3u", 'w+', encoding='utf-8') as outfile:
            for filename in os.listdir(self.directory):
                with open(self.directory + filename, encoding='utf-8') as infile:
                    outfile.write(infile.read())
        self.__clean("playlist_")
        self.__clean("")

    def __clean(self, pattern=""):
        for filename in os.listdir(self.directory):
            if pattern != "":
                if filename.startswith(pattern):
                    os.unlink(self.directory + filename)    
            elif filename.endswith('.m3u'):
                if filename != "raw_playlist.m3u":
                    os.unlink(self.directory + filename)
                