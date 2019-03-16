from src.PlaylistManager import *
from src.PlaylistDownloader import *



def main():
    #plManager = PlaylistManager()
    #plManager.backup()
    plDownloader = PlaylistDownloader()
    plDownloader.save()
    

if __name__ == '__main__':
    main()
