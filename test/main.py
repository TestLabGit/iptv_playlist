import sys
import re
import json
import validators

sys.path.append('..')
from src.PlaylistManager import *
from src.PlaylistDownloader import *
from src.StreamChecker import *
import vlc
import time


def run():
    playlist_array = [
        #'https://webhalpme.ru/iptvforever.m3u',
        #'https://webhalpme.ru/ruiptvforever.m3u',
        #'https://smarttvnews.ru/apps/iptvchannels.m3u',
        #'https://smarttvnews.ru/apps/iptvfreefull.m3u',
        #'https://smarttvapp.ru/app/iptvfull.m3u',
        'http://iptv.slynet.tv/FreeBestTV.m3u',
        'https://www.iptv4sat.com/download-attachment/dI6Dj8ur2XCCyAjyOFt48PYF_UAmqYRi9aE3YiFJrB0' 
        #'http://listiptv.ru/iptv18.m3u',
        'https://webarmen.com/my/iptv/auto.nogrp.m3u'
    ]

    zip_playlist_array = [
        'https://www.iptv4sat.com/download-attachment/dI6Dj8ur2XCCyAjyOFt48PYF_UAmqYRi9aE3YiFJrB0' 
    ]
    
    ch_name_array = [ 
        "ТНТ", "СТС", "НТВ", "Россия", "Первый", "Мир", "Рен ТВ", "ПЯТНИЦА", 
        "ТВЦ", "Fox", "Nat Geo", "National Geographic", "Nickelodeon", "COMEDY", 
        "SENTANA SPORT", "Sport", "Матч",  "Viasat", "Eurosport",
        "MTV", "Music", "Муз"          
    ]
    
    plManager = PlaylistManager(playlist_array, ch_name_array, zip_playlist_array)
    plManager.create_list("lplaylist")
   
   
def test():
    playlist_array = [
        #'https://webhalpme.ru/iptvforever.m3u',
        #'https://webhalpme.ru/ruiptvforever.m3u',
        #'https://smarttvnews.ru/apps/iptvchannels.m3u',
        #'https://smarttvnews.ru/apps/iptvfreefull.m3u',
        #'https://smarttvapp.ru/app/iptvfull.m3u',
        #s'http://iptv.slynet.tv/FreeBestTV.m3u',
        #'http://listiptv.ru/iptv18.m3u'
    ]

    zip_playlist_array = [
        'https://www.iptv4sat.com/download-attachment/dI6Dj8ur2XCCyAjyOFt48PYF_UAmqYRi9aE3YiFJrB0' 
    ]
    plDown = PlaylistDownloader(playlist_array, zip_playlist_array)
    #plDown.save_raw_playlist()
    
    #for line in zipfile.open(file).readlines():
    #    print(line.decode('utf-8'))

    #s = StreamChecker()
    
    #print(s.is_active('http://stream.mediawork.cz/retrotv//retrotvHQ1/playlist.m3u8﻿#EXTM3U'))
    #url = 'http://109.70.184.20:8080/udp/239.195.32.11:1234'
    # url = 'http://cdn-01.bonus-tv.ru:8080/tntmusic/tracks-v1a1/index.m3u8'
    # #url = 'http://109.70.184.20:8080/udp/239.195.32.1:1234'
    # instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
    # player=instance.media_player_new()
    # media=instance.media_new(url)
    # player.set_media(media)
    # player.play()
    # time.sleep(5)
    # state = str(media.get_state())
   
    # if state == "vlc.State.Error" or state == "State.Error":
    #     print('Stream is dead. Current state = {}'.format(state))
    #     player.stop()
    # elif state == "State.Ended":
    #     print('Stream ended. Current state = {}'.format(state))
    #     player.stop()
    # else:
    #     print('Stream is working. Current state = {}'.format(state))
    #     player.stop()

    
if __name__ == '__main__':
    run()
    #test()
