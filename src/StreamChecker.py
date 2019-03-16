import urllib


class StreamChecker:
    
    def __init__(self):
        pass

    def is_active(self):
        url = 'http://cdnmg.secure.live.rtr-vesti.ru/live/smil:r1.smil/chunklist_b1600000.m3u8'
        code = urllib.urlopen(url).getcode()
        if str(code).startswith('2') or str(code).startswith('3'):
            return True
        else:
            return False

