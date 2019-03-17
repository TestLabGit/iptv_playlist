import os
import urllib.request



class PlaylistDownloader():

    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.directory = dirname + "/playlists/"
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory) 
        self.playlist_array = [  
            'https://webhalpme.ru/iptvforever.m3u',
            'https://webhalpme.ru/ruiptvforever.m3u',
            'https://smarttvnews.ru/apps/iptvchannels.m3u',
            'https://smarttvnews.ru/apps/iptvfreefull.m3u',
            'https://smarttvapp.ru/app/iptvfull.m3u',
            'http://iptv.slynet.tv/FreeBestTV.m3u', 
            'http://iptv.slynet.tv/PeerstvSlyNet.m3u',
            'http://listiptv.ru/iptv18.m3u'
        ]

    def append_url(self, url):
        self.playlist_array.append(url);

    def save(self):
        self.clean()
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
    
    def clean(self):
        for filename in os.listdir(self.directory):
            if filename.endswith('.m3u'):
                os.unlink(self.directory + filename)
                