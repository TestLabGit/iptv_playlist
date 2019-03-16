import os
from shutil import *


class PlaylistManager:

    def __init__(self):
        pass

    def get_ch_list(self):
        pass

    def backup(self):
        dirname = os.path.dirname(__file__)
        directory = dirname + "/backup"
        if not os.path.isdir(directory):
            os.makedirs(directory) 
            copy2('index.m3u', directory + '/index_prev.m3u') 

    def create_list(self):
        pass
