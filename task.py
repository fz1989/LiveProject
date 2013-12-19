
#!/usr/bin/env python
# coding=utf-8
import os
import datetime
import hashlib
import sqlite3
from multiprocessing import Process

ROOT_PATH = "D:\\"
HOST_IP = "219.245.64.30"
HOST_PORT = "80"
HOST_NAME = "http://" + HOST_IP + ":" + HOST_PORT + "/"

CON = sqlite3.connect("live.db")
CUR = CON.cursor()
CUR.execute(
    "create table if not exists task ( id varchar(32) primary key, result varchar(128)) ")


def get_second(time_interval):
    '''
        format time_interval to hour:minute:seconds
    '''
    total_seconds = time_interval.seconds
    print total_seconds
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


def find_video_url(start_time, end_time, port_id):
    '''
        return video_files urls for httpserver
    '''
    video_files = _find_video(start_time, end_time, port_id)
    url_prefix = ("%s%s/%s/%s/%s/%s/") % (HOST_NAME,
                                           "videos",
                                           start_time[0:4],
                                           start_time[4:6],
                                           start_time[6:8],
                                           port_id)

    video_urls = [url_prefix + video for video in video_files]
    return video_urls


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



def _get_dir(start_time, end_time, port_id):
    start_time = set_start(change_time_format(start_time))

    end_time = set_start(change_time_format(end_time))



def _find_video(start_time, end_time, port_id):
    '''
        return the files 
    '''
    dir_path = ROOT_PATH + start_time[0:4] + "\\" + \
        start_time[4:6] + "\\" + start_time[6:8] + "\\" + port_id + "\\"

    dir_file_list = os.listdir(dir_path)
    dir_file_list.sort()
    left = lower_bound(dir_file_list, start_time)
    right = min(lower_bound(dir_file_list, end_time) + 1,
                len(dir_file_list))
    return dir_file_list[left: right]


def get_video_url(task_id):
    '''
        return merge video url
    '''
    url = HOST_NAME + "livedownload/" + task_id + ".mp4"
    return url


def _get_video(task_id, start_time, end_time, port_id):
    '''
        merge video
    '''
    dir_path = ROOT_PATH + \
               "\\" + start_time[0:4] + \
               "\\" + start_time[4:6] + \
               "\\" + start_time[6:8] + \
               "\\" + port_id + "\\"

    video_files = _find_video(start_time, end_time, port_id)
    merge_list = []

    sql = ("insert into task values('%s', '%s')") % (task_id, "None")
    CUR.execute(sql)
    CON.commit()
    len_video_files = len(video_files)
    if len_video_files == 1:
        single = True
    else:
        single = False

    slice_options = get_slice_options(video_files[0],
                                      start_time,
                                      end_time,
                                      single=single)
    merge_list.append(_slice_video(dir_path + video_files[0],
                                   slice_options,
                                   task_id + "begin.mp4"))

    merge_list.extend([dir_path + video for video in video_files[1:-1]])

    if len_video_files >= 2:
        last_file = dir_path + video_files[len_video_files - 1]
        slice_options = get_slice_options(last_file,
                                          start_time,
                                          end_time,
                                          flag=False)
        merge_list.append(_slice_video(last_file,
                                       slice_options,
                                       task_id + "end.mp4"))
    dir_path = ROOT_PATH + "livedownload\\"
    outfile = task_id + ".mp4"
    _merge_video(task_id, merge_list, dir_path + outfile)

    sql = ("update task set result='%s' where id = '%s'") % (get_video_url(task_id), task_id)
    CUR.execute(sql)
    CON.commit()
    return outfile


def get_slice_options(input_file,
                      start_time,
                      end_time,
                      flag=True,
                      single=False):
    '''
        return slice options
    '''
    if flag:
        min_time = min(start_time, input_file[-18:-4])
        max_time = max(start_time, input_file[-18:-4])
        if min_time == max_time:
            return input_file
        slice_options = " -ss " + \
                        get_second(change_time_format(max_time) -
                                   change_time_format(min_time))
        if single:
            slice_options = slice_options + " -t " + \
                get_second(change_time_format(end_time) -
                           change_time_format(start_time))
    else:
        slice_options = " -t " + \
                        get_second(change_time_format(end_time) -
                                   change_time_format(input_file[-18:-4]))
    return slice_options


def _slice_video(input_file,
                 slice_options,
                 outfile):
    '''
        slice video
    '''
    target = "ffmpeg -y -i " + input_file + slice_options + " " + outfile
    print target
    os.system(target)
    return outfile


def _merge_video(task_id, merge_list, outfile):
    '''
    merge video  
    '''
    outfile_cfg = str(task_id) + ".txt"
    file_object = open(outfile_cfg, 'w')
    for files in merge_list:
        print files
        file_object.write("file " + files + "\n")
    file_object.close()
    target = 'ffmpeg -y -f concat -i ' + outfile_cfg + ' -c copy ' + outfile
    print outfile
    print target
    os.system(target)
    return outfile


def get_task_id(start_time, end_time, port_id):
    '''
        init a tesk id
    '''
    src = str(datetime.datetime.now()) + start_time + end_time + port_id
    task_id = hashlib.md5(src).hexdigest().lower()
    process = Process(target=_get_video,
                      args=(task_id, start_time, end_time, port_id))

    process.start()
    return task_id


def get_task_status(task_id):
    '''
        return task_id status
    '''
    sql = ("select result from task where id = '%s'") % (task_id)
    CUR.execute(sql)
    return CUR.fetchone()[0]
