import sys
import re
import json
import validators
import vlc
import time

from core.PlaylistManager import PlaylistManager
from core.PlaylistDownloader import PlaylistDownloader
from core.StreamChecker import StreamChecker



def run():
    playlist_array = [
        #'https://webhalpme.ru/iptvforever.m3u',
        #'https://webhalpme.ru/ruiptvforever.m3u',
        #'https://smarttvnews.ru/apps/iptvchannels.m3u',
        #'https://smarttvnews.ru/apps/iptvfreefull.m3u',
        #'https://smarttvapp.ru/app/iptvfull.m3u',
        #'http://iptv.slynet.tv/FreeBestTV.m3u',
        'http://listiptv.ru/iptv18.m3u',
        'https://webarmen.com/my/iptv/auto.nogrp.m3u'
    ]

    # zip_playlist_array = [
    #     'https://www.iptv4sat.com/download-attachment/dI6Dj8ur2XCCyAjyOFt48PYF_UAmqYRi9aE3YiFJrB0' 
    # ]
    
    ch_name_array = [ 
        "ТНТ", "СТС", "НТВ", "Россия", "Первый", "Мир", "Рен ТВ", "ПЯТНИЦА", 
        "ТВЦ", "Fox", "Nat Geo", "National Geographic", "Nickelodeon", "COMEDY", 
        "SENTANA SPORT", "Sport", "Матч",  "Viasat", "Eurosport",
        "MTV", "Music", "Муз"          
    ]
    
    #plManager = PlaylistManager(playlist_array, ch_name_array, zip_playlist_array)
    plManager = PlaylistManager(playlist_array, ch_name_array)
    plManager.create_list("lplaylist")
   

if __name__ == '__main__':
    run()
    