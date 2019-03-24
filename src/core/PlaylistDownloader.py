import sys
import os
import urllib.request
import validators
import requests
from io import BytesIO
from zipfile import ZipFile

sys.path.append('..')
from src import pl_logger



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
        pl_logger.info("Playlist downloader started")

    def save_playlists(self):
        self.__clean("*.")
        for ctr, value in enumerate(self.playlist_array):
            try:
                filedata = urllib.request.urlopen(value)
                datatowrite = filedata.read()
                filename = "playlist_" + str(ctr+1) + ".m3u"
                playlist_path = self.directory + filename  
                with open(playlist_path, 'wb') as f:  
                    f.write(datatowrite)
            except urllib.error.HTTPError as e:
                pl_logger.exception('Check url: {} | HTTPError reason: {}'
                    .format(value, e.code))
                
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
        common_file_name = self.directory + "raw_playlist.m3u"
        with open(common_file_name, 'w+', encoding='utf-8') as outfile:
            for filename in os.listdir(self.directory):
                with open(self.directory + filename, encoding='utf-8') as infile:
                    outfile.write(infile.read())
        self.__clean("playlist_")
        n_raw_pl_lines = sum(1 for line in open(common_file_name, encoding='utf-8'))
        self.__split_raw_playlist(common_file_name, n_raw_pl_lines)
        self.__clean()

    def __split_raw_playlist(self, filename, lines_per_file):
        smallfile = None
        n_plf = 0
        n_files = 4;
        n_lines_per_file = int(lines_per_file / n_files)
        with open(filename, encoding='utf-8') as bigfile:
            line = "#"
            line_cnt = 0
            while line:
                if line_cnt % (n_lines_per_file + 2) == 0:
                    if line_cnt != 1:
                        while line and not validators.url(line) and smallfile:
                            smallfile.write(line)
                            line = bigfile.readline()
                            line_cnt += 1
                        if line and smallfile and validators.url(line):
                            smallfile.write(line)
                            line = bigfile.readline()
                            line_cnt += 1
                    if smallfile:
                        smallfile.close()
                    n_plf += 1
                    small_filename = self.directory + 'pl_chunk_{}.m3u'.format(n_plf)
                    smallfile = open(small_filename, "w+", encoding='utf-8')
                    if line_cnt == 0:
                        line_cnt = 1
                    if line == "#":
                        line = bigfile.readline()
                        line_cnt += 1
                    if not line.startswith("#EXTM3U"):
                        smallfile.write("#EXTM3U\n")
                smallfile.write(line)
                line = bigfile.readline()
                line_cnt += 1
            if smallfile:
                smallfile.close()

    def __clean(self, pattern=""):
        for filename in os.listdir(self.directory):
            if pattern == "*.":
                os.unlink(self.directory + filename)
            elif pattern != "":
                if filename.startswith(pattern):
                    os.unlink(self.directory + filename)    
            elif filename.endswith('.m3u'):
                if not filename.startswith("pl_chunk"):
                    os.unlink(self.directory + filename)
                