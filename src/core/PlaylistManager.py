import sys
import os
import glob
import re
import json
import validators
import contextlib
from shutil import *

from .PlaylistDownloader import PlaylistDownloader
from .StreamChecker import StreamChecker

sys.path.append('..')
from src import pl_logger



class PlaylistManager:

    def __init__(self, playlist_array, ch_name_array, zip_playlist_array=None):
        plDownloader = PlaylistDownloader(playlist_array, zip_playlist_array)
        plDownloader.save_raw_playlist()
        self.stream_checker = StreamChecker()
        self.ch_name_array = []
        for ix in range(0, len(ch_name_array)):
            self.ch_name_array.append(ch_name_array[ix].lower())
        pl_logger.info("Playlist manager started")
        
    def get_ch_list(self, filename):
        ch_list = []
        n_lines = sum(1 for line in open(filename, encoding='utf-8'))

        with open(filename, encoding='utf-8') as fpl:  
            line = fpl.readline().rstrip()
            line_cnt = 1
            
            if line.startswith('#EXTM3U'):
                line = fpl.readline().rstrip()
                line_cnt += 1
            
            f_bad_format = True
            while line:
                #if line_cnt % 1000 == 0:
                #    print('Viewed {} lines out of {}'.format(line_cnt, n_lines))
                
                if line.startswith('#EXTINF'):
                    ch_name_ix = line.rfind(',')
                    ch_name = line[ch_name_ix+1:].strip()
                    
                    if not any(ch in ch_name.lower() for ch in self.ch_name_array):
                        line = fpl.readline().rstrip() 
                        line_cnt += 1
                        f_bad_format = False
                        continue
                    else: 
                        f_bad_format = True
                    
                    params = line[0:ch_name_ix].strip()
                    params_list = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', params) # split(' ') & preserve quotes
                    params_json = dict()
                    params_json['EXTINF'] = params_list[0]
                    params_json['ch_name'] = ch_name
                    for el in params_list[1:]:
                        tv = el.split("=")
                        params_json[tv[0]] = tv[1]
                    
                    line = fpl.readline().rstrip()
                    line_cnt += 1
                    
                    if line.startswith('#EXTINF'):
                        continue
                    
                    if line.startswith('#EXT'):
                        line = fpl.readline().rstrip()
                        line_cnt += 1
                            
                    if line and validators.url(line):
                        if self.stream_checker.is_active(line) and \
                           self.stream_checker.is_active_in_vlc(line):
                            params_json['ch_url'] = line
                            line = fpl.readline().rstrip()
                            line_cnt += 1
    
                            params_json['ch_relative_id'] = 1;
                            ch_list.append(params_json)
                            
                            # if len(ch_list) > 1:
                            for ch in ch_list[:-1].copy():
                                if ch['ch_name'].replace(' ', "").lower() == \
                                   params_json['ch_name'].replace(' ', "").lower() and \
                                   ch['ch_url'] != params_json['ch_url']:
                                    params_json['ch_relative_id'] += 1
                                elif ch['ch_name'] == params_json['ch_name'] and \
                                        ch['ch_url'] == params_json['ch_url']:
                                    ch_list.pop()
                        else:
                            line = fpl.readline().rstrip()
                            line_cnt += 1
                            f_bad_format = True
                else:
                    if f_bad_format:
                        pl_logger.exception('{} {}, in file: {}'
                            .format("Bad format of channel on line:", line_cnt, filename))
                    line = fpl.readline().rstrip()
                    line_cnt += 1
            return ch_list

    def backup(self, filename):
        dirname = os.path.dirname(__file__)
        directory = dirname + "/backup"
        if not os.path.isdir(directory):
            os.makedirs(directory) 
            copy2(filename, directory + '/index_prev.m3u') 

    def __create_ch_data(self, ch_dict_info):
        ch_data = ch_dict_info['EXTINF']
        not_params_key = ['EXTINF', 'ch_name', 'ch_url', 'ch_relative_id']
        for key, value in ch_dict_info.items():
            if key not in not_params_key:
                ch_data += " " + key + "=" + value
        ch_data += ","
        ch_data += ch_dict_info['ch_name'] + \
                   " [IV_" + str(ch_dict_info['ch_relative_id']) + "]\n"
        ch_data += ch_dict_info['ch_url'] + "\n"
        return ch_data

    def create_list(self, playlist_name):
        dirname = os.path.dirname(__file__)
        directory = dirname + "/playlists"  
        filenames_list = glob.glob(directory + "/*.m3u")

        directory_result = dirname + "/result_playlist"
        if not os.path.isdir(directory_result):
            os.makedirs(directory_result) 
        res_pl = open(directory_result + "/" + playlist_name + ".m3u", "w+", encoding='utf-8')
        res_pl.write('#EXTM3U\n')
        
        from multiprocessing.pool import ThreadPool
        n_processes = 4
        pool = ThreadPool(processes=n_processes)
  
        async_list = []
        for file in filenames_list:
            async_list.append(pool.apply_async(self.get_ch_list, (file,)))
        
        tmp_ch_list = []
        for i, file in enumerate(filenames_list):
            tmp_ch_list.extend(async_list[i].get())
        
        for ch in tmp_ch_list:
            ch['ch_relative_id'] = 1
        
        tmp2_ch_list = [i for n, i in enumerate(tmp_ch_list) if i not in tmp_ch_list[n + 1:]]
        for i, ch in enumerate(tmp2_ch_list):
            el_cnt = len(tmp2_ch_list)
            if ch['ch_relative_id'] == 1:
                ch_relative_id = 1
                for j in range(i+1, el_cnt):
                    if tmp2_ch_list[j]['ch_name'].replace(' ', "").lower() == \
                       ch['ch_name'].replace(' ', "").lower() and \
                       tmp2_ch_list[j]['ch_url'] != ch['ch_url']:
                        ch_relative_id += 1
                        tmp2_ch_list[j]['ch_relative_id'] = ch_relative_id
                
        sort_ch_list = sorted(tmp2_ch_list, key=lambda k: k['ch_name']) 
        for ch in sort_ch_list:
            ch_data = self.__create_ch_data(ch)
            res_pl.write(ch_data)
        pl_logger.info('Playlist downloader create playlist: %s' % playlist_name)
