import urllib.request
from socket import timeout
import vlc
import time



class StreamChecker:
    
    def __init__(self):
        pass

    def is_active(self, url):
        try:
            code = urllib.request.urlopen(url, timeout=8).getcode()
            if str(code).startswith('2'):
                return True
            else:
                return False
        except urllib.error.HTTPError as e:
            print('HTTPError: {}'.format(e.code))
            return False
        except urllib.error.URLError as e:
            print('URLError: {}'.format(e.reason))
            return False
        except timeout:
            return False
        except Exception as e:
            return False
        else:
            return True

    def is_active_in_vlc(self, url):
        instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        player=instance.media_player_new()
        media=instance.media_new(url)
        player.set_media(media)
        player.play()
        time.sleep(5)
        state = str(media.get_state())

        if state == "vlc.State.Error" or state == "State.Error":
            print('Stream is dead. Current state = {}'.format(state))
            player.stop()
            return False
        elif state == "State.Ended":
            print('Stream ended. Current state = {}'.format(state))
            player.stop()
            return False
        else:
            print('Stream is working. Current state = {}'.format(state))
            player.stop()
            return True
