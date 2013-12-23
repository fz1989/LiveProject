#!/usr/bin/env python
# coding=utf-8

import os
import sqlite3
from timeprocess import *

ROOT_PATH = "D:"
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
    for day in xrange(0, days):
        now = start_time + datetime.timedelta(days = day)
        ret.extend(os.listdir(get_time_dir(now, port_id)))
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
