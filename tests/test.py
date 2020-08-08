import sys
import re
import json
import validators

sys.path.append('..')
from src.core.PlaylistManager import PlaylistManager
from src.core.PlaylistDownloader import PlaylistDownloader
from src.core.StreamChecker import StreamChecker
import vlc
import time


def test1():
    playlist_array = [
        #'https://webhalpme.ru/iptvforever.m3u',
        #'https://webhalpme.ru/ruiptvforever.m3u',
        #'https://smarttvnews.ru/apps/iptvchannels.m3u',
        #'https://smarttvnews.ru/apps/iptvfreefull.m3u',
        #'https://smarttvapp.ru/app/iptvfull.m3u',
        #'http://iptv.slynet.tv/FreeBestTV.m3u',
        #'http://listiptv.ru/iptv18.m3u',
        'https://webarmen.com/my/iptv/auto.nogrp.m3u'
    ]

    ch_name_array = [ 
        "ТНТ", "СТС", "НТВ", "Россия", "Первый", "Мир", "Рен ТВ", "ПЯТНИЦА", 
        "ТВЦ", "Fox", "Nat Geo", "National Geographic", "Nickelodeon", "COMEDY", 
        "SENTANA SPORT", "Sport", "Матч",  "Viasat", "Eurosport",
        "MTV", "Music", "Муз"          
    ]

    zip_playlist_array = [
        #'https://www.iptv4sat.com/download-attachment/dI6Dj8ur2XCCyAjyOFt48PYF_UAmqYRi9aE3YiFJrB0' 
    ]

    plDown = PlaylistDownloader(playlist_array, zip_playlist_array)
    plDown.save_raw_playlist()


def test2():
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

    ch_name_array = [ 
        "ТНТ", "СТС", "НТВ", "Россия", "Первый", "Мир", "Рен ТВ", "ПЯТНИЦА", 
        "ТВЦ", "Fox", "Nat Geo", "National Geographic", "Nickelodeon", "COMEDY", 
        "SENTANA SPORT", "Sport", "Матч",  "Viasat", "Eurosport",
        "MTV", "Music", "Муз"          
    ]

    plDown = PlaylistDownloader(playlist_array)
    plDown.save_raw_playlist()


def test3():
    sc = StreamChecker()
    assert sc.is_active('http://stream.mediawork.cz/retrotv//retrotvHQ1/playlist.m3u8﻿#EXTM3U') is False
    assert sc.is_active('http://ott-cdn.ucom.am/s51/04.m3u8') is True
    print(sc.is_active_in_vlc('http://ott-cdn.ucom.am/s51/04.m3u8'))
    print(sc.is_active_in_vlc('http://hls.mirtv.cdnvideo.ru/mirtv-parampublish/hd/playlist.m3u8\n'))


if __name__ == '__main__':
    test1()
    test2()
#    test3()
