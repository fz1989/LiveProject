#!/usr/bin/env python
# coding=utf-8
import datetime
import os


def set_start(time):
    return datetime.datetime(time.year, 
                             time.month,
                             time.day,
                             0, 0, 0)

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





