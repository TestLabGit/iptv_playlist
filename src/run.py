import sys
import os
import re
import json
import validators
import vlc
import time
from datetime import datetime

from core.PlaylistManager import PlaylistManager
from core.PlaylistDownloader import PlaylistDownloader
from core.StreamChecker import StreamChecker



def run():
    playlist_array = [
        'https://webhalpme.ru/iptvforever.m3u',
        'https://webhalpme.ru/ruiptvforever.m3u',
        'https://smarttvnews.ru/apps/iptvchannels.m3u',
        'https://smarttvnews.ru/apps/iptvfreefull.m3u',
        'https://smarttvapp.ru/app/iptvfull.m3u',
        'http://iptv.slynet.tv/FreeBestTV.m3u',
        'http://listiptv.ru/iptv18.m3u',
        'https://webarmen.com/my/iptv/auto.nogrp.m3u'
    ]

    # zip_playlist_array = [
    #     'https://www.iptv4sat.com/download-attachment/dI6Dj8ur2XCCyAjyOFt48PYF_UAmqYRi9aE3YiFJrB0' 
    # ]
    
    ch_name_array = [ 
        "ТНТ", "СТС", "НТВ", "Россия", "Первый", "Мир", "Рен ТВ", "ПЯТНИЦА", 
        "ТВЦ", "Fox", "Nat Geo", "National Geographic", "Nickelodeon", "COMEDY", 
        "Sport", "Матч", "Viasat", "Eurosport",
        "News", 
        "MTV", "Music", "Муз"          
    ]
    
    #plManager = PlaylistManager(playlist_array, ch_name_array, zip_playlist_array)
    start_time = datetime.now()
    plManager = PlaylistManager(playlist_array, ch_name_array)
    plManager.create_list("lplaylist")
    end_time = datetime.now()
    print('Executing time: {}'.format(end_time - start_time))
   

if __name__ == '__main__':
    run()
