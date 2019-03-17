import sys
import re
import json
import validators

sys.path.append('..')
from src.PlaylistManager import *



def run():
    # url = 'http://82.193.71.93/MultimaniaLV/video.m3u8'
    # if validators.url(url):
    #     print("ok")
    
    plManager = PlaylistManager()
    plManager.create_list()


if __name__ == '__main__':
    run()
