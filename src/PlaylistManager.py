import os
from shutil import *
import glob
import re
import json
import validators

from src.PlaylistDownloader import *
from src.StreamChecker import *



class PlaylistManager:

    def __init__(self, playlist_array, ch_name_array, zip_playlist_array=None):
        plDownloader = PlaylistDownloader(playlist_array, zip_playlist_array)
        plDownloader.save_raw_playlist()
        self.stream_checker = StreamChecker()
        self.ch_name_array = []
        for ix in range(0, len(ch_name_array)):
            self.ch_name_array.append(ch_name_array[ix].lower())
        
    def get_ch_list(self, filename):
        ch_list = []
        
        with open(filename, encoding='utf-8') as fpl:  
            line = fpl.readline()
            line_cnt = 1
            
            if line.startswith('#EXTM3U'):
                line = fpl.readline()
                line_cnt += 1
            
            while line:
                print(line_cnt)
                if line.startswith('#EXTINF'):
                    ch_name_ix = line.rfind(',')
                    ch_name = line[ch_name_ix+1:].strip()

                    if not any(ch in ch_name.lower() for ch in self.ch_name_array):
                        line = fpl.readline() 
                        line_cnt += 1
                        continue

                    params = line[0:ch_name_ix].strip()
                    params_list = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', params) # split(' ') & preserve quotes
                    params_json = dict()
                    params_json['EXTINF'] = params_list[0]
                    params_json['ch_name'] = ch_name
                    for el in params_list[1:]:
                        tv = el.split("=")
                        params_json[tv[0]] = tv[1]
                    
                    line = fpl.readline() 
                    line_cnt += 1
                    
                    if line.startswith('#EXT'):
                        line = fpl.readline()
                        line_cnt += 1
                    
                    if line and validators.url(line):
                        if self.stream_checker.is_active(line):
                            params_json['ch_url'] = line.rstrip()
                            line = fpl.readline()
                            line_cnt += 1
    
                            params_json['ch_relative_id'] = 1;
                            ch_list.append(params_json)
                            
                            # if len(ch_list) > 1:
                            for ch in ch_list[:-1].copy():
                                if ch['ch_name'].replace(' ', "").lower() == params_json['ch_name'].replace(' ', "").lower() and \
                                   ch['ch_url'] != params_json['ch_url']:
                                    params_json['ch_relative_id'] += 1
                                elif ch['ch_name'] == params_json['ch_name'] and \
                                        ch['ch_url'] == params_json['ch_url']:
                                    ch_list.pop()   
                else:
                    #print('{} {}, in file: {}'.format("Bad format of channel on line:", line_cnt, filename))
                    #print(line)
                    line = fpl.readline()
                    line_cnt += 1
            # for el in ch_list:
            #     print(el)
            return ch_list

    def backup(self):
        dirname = os.path.dirname(__file__)
        directory = dirname + "/backup"
        if not os.path.isdir(directory):
            os.makedirs(directory) 
            copy2('/../index.m3u', directory + '/index_prev.m3u') 

    def __create_ch_data(self, ch_dict_info):
        ch_data = ch_dict_info['EXTINF']
        not_params_key = ['EXTINF', 'ch_name', 'ch_url', 'ch_relative_id']
        for key, value in ch_dict_info.items():
            if key not in not_params_key:
                ch_data += " " + key + "=" + value
        ch_data += ","
        ch_data += ch_dict_info['ch_name'].rstrip() + \
                   " [IV_" + str(ch_dict_info['ch_relative_id']) + "]\n"
        ch_data += ch_dict_info['ch_url'] + "\n"
        return ch_data

    def create_list(self, playlist_name):
        self.backup()
        dirname = os.path.dirname(__file__)
        directory = dirname + "/playlists"  
        filenames_list = glob.glob(directory + "/*.m3u")

        directory_result = dirname + "/result_playlist"
        if not os.path.isdir(directory_result):
            os.makedirs(directory_result) 
        res_pl = open(directory_result + "/" + playlist_name + ".m3u","w+", encoding='utf-8')
        res_pl.write('#EXTM3U\n')
        
        for file in filenames_list:
            tmp_ch_list = self.get_ch_list(file)
            sort_ch_list = sorted(tmp_ch_list, key=lambda k: k['ch_name']) 
            for ch in sort_ch_list:
                ch_data = self.__create_ch_data(ch)
                res_pl.write(ch_data)
