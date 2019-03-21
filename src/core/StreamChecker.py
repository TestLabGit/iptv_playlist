import urllib.request
from socket import timeout
import vlc
import time

import sys
sys.path.append('..')
from src import pl_logger



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
            pl_logger.exception('Check url: {} | HTTPError: {}'.format(url, e.code))
            return False
        except urllib.error.URLError as e:
            pl_logger.exception('Check url: {} | URLError: {}'.format(url, e.reason))
            return False
        except timeout:
            pl_logger.exception('Check url: {} | Timeout'.format(url))
            return False
        except Exception as e:
            pl_logger.exception('Check url: {} | Undefined error'.format(url))
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
            pl_logger.info('Url check {} | Stream is dead. Current state = {}'.format(url, state))
            player.stop()
            return False
        elif state == "State.Ended":
            pl_logger.info('Url check {} | Stream ended. Current state = {}'.format(url, state))
            player.stop()
            return False
        else:
            #print('Stream is working. Current state = {}'.format(state))
            player.stop()
            return True
