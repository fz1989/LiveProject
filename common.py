#!/usr/bin/env python
# coding=utf-8

import os
import sqlite3
from timeprocess import *

ROOT_PATH = "D:\\live"
HOST_IP = "219.245.64.30"
HOST_PORT = "80"
HOST_NAME = "http://" + HOST_IP + ":" + HOST_PORT

CON = sqlite3.connect("live.db")
CUR = CON.cursor()
CUR.execute(
    "create table if not exists task ( id varchar(32) primary key, result varchar(128)) ")


def _get_dir_file_list(start_time, end_time, port_id):
    '''
        from time get file path, 
    '''
    start_time = set_start(change_time_format(start_time))
    end_time = set_start(change_time_format(end_time))
    days = (start_time - end_time).days
    ret = []
    for day in xrange(0, days + 1):
        now = start_time + datetime.timedelta(days = day)
        ret.extend(os.listdir(get_time_dir(now, port_id)))
    print ret
    return ret

def find_videos(start_time, end_time, port_id):
    '''
        return the files 
    '''
    dir_file_list = _get_dir_file_list(start_time, end_time, port_id)
    left = lower_bound(dir_file_list, start_time)
    right = min(lower_bound(dir_file_list, end_time) + 1,
                len(dir_file_list))
    return dir_file_list[left: right]

def lower_bound(dir_file_list, time_peek):
    '''
        find time_peek < dir_file_list
    '''
    if dir_file_list[0][0:14] > time_peek:
        return 0
    left = 0
    ret = right = len(dir_file_list) - 1
    if dir_file_list[ret][0:14] < time_peek:
        return ret + 1
    while left <= right:
        mid = (left + right) / 2
        if dir_file_list[mid][0:14] <= time_peek:
            ret = mid
            left = mid + 1
        else:
            right = mid - 1
    return ret

def get_time_dir(date_time, port_id):
    '''
        given time and dir, return file path
    '''
    ret = ("%s\\%s\\%s\\%s\\%s\\%s\\") % (ROOT_PATH,
                                          "videos",
                                          date_time.year,
                                          date_time.month,
                                          date_time.day,
                                          port_id)
    print ret
    return ret

def get_slice_dir():
    '''
        return the slice file dir
    '''
    slice_dir = ("%s\\tmp\\") % (ROOT_PATH)
    if not os.path.exists(slice_dir):
        os.mkdir(slice_dir)
    return slice_dir

def get_download_dir():
    '''
        return the slice file dir
    '''
    download_dir = ("%s\\livedownload\\") % (ROOT_PATH)
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    return download_dir

def get_url_prefix(file_name, port_id):
    '''
        given the short file name and port_id, return the 
        full url
    '''
    file_prefix = file_name.split('.')[0]
    return ("%s/%s/%s/%s/%s/%s/") % (HOST_NAME,
                                    "videos",
                                    file_prefix[0:4],
                                    file_prefix[4:6],
                                    file_prefix[6:8],
                                    port_id)

def get_full_filename(file_name, port_id):
    '''
        given the short file name and port_id, return the 
        full file name
    '''
    file_prefix = file_name.split('.')[0]
    ret = ("%s\\%s\\%s\\%s\\%s\\%s\\%s") % (ROOT_PATH,
                                            "videos",
                                            file_prefix[0:4],
                                            file_prefix[4:6],
                                            file_prefix[6:8],
                                            port_id,
                                            file_name)
    return ret
