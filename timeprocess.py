#!/usr/bin/env python
# coding=utf-8
import datetime

ROOT_PATH = "D:"
HOST_IP = "219.245.64.30"
HOST_PORT = "80"
HOST_NAME = "http://" + HOST_IP + ":" + HOST_PORT + "/"

def set_start(time):
    time.hour = 0
    time.minute = 0
    time.seconds = 0
    return time

def get_second(time_interval):
    '''
        format time_interval to hour:minute:seconds
    '''
    total_seconds = time_interval.seconds
    hour = total_seconds / 3600
    minute = (total_seconds - hour * 3600) / 60
    seconds = total_seconds % 60
    return "%02d:%02d:%02d" % (hour, minute, seconds)


def change_time_format(str_time):
    '''
        format the time from 20121216214750 to python datetime
    '''
    return datetime.datetime(int(str_time[0:4]),
                             int(str_time[4:6]),
                             int(str_time[6:8]),
                             int(str_time[8:10]),
                             int(str_time[10:12]),
                             int(str_time[12:14]))

def get_time_dir(str_time, port_id):
    '''
        given time and dir, return file path
    '''
    return ("%s\\%s\\%s\\%s\\%s\\") % (ROOT_PATH,
                                       str_time[0:4],
                                       str_time[4:6],
                                       str_time[6:8],
                                       port_id)

def get_slice_dir(str_time):
    '''
        return the slice file dir
    '''
    return ("%s\\tmp\\") % (ROOT_PATH)

def get_download_dir():
    '''
        return the slice file dir
    '''
    return ("%s\\download\\") % (ROOT_PATH)

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
        full directory
    '''
    file_prefix = file_name.split('.')[0]
    return ("%s/%s/%s/%s/%s/%s/") % (HOST_NAME,
                                    "videos",
                                    file_prefix[0:4],
                                    file_prefix[4:6],
                                    file_prefix[6:8],
                                    port_id)




