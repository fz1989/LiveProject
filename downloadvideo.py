#!/usr/bin/env python
# coding=utf-8
import os
import datetime
import hashlib
from multiprocessing import Process
from timeprocess import *
from common import *


def get_video_url(task_id):
    '''
        return merge video url
    '''
    url = HOST_NAME + "/livedownload/" + task_id + ".mp4"
    return url

def _get_video(task_id, start_time, end_time, port_id):
    '''
        merge video
    '''

    video_files = find_videos(start_time, end_time, port_id)
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
    first_file = get_full_filename(video_files[0], port_id)
    merge_list.append(_slice_video(first_file,
                                   slice_options,
                                   task_id + "begin.mp4"))

    merge_list.extend([get_full_filename(video, port_id) 
                      for video in video_files[1:-1]])

    if len_video_files >= 2:
        last_file = video_files[len_video_files - 1]
        slice_options = get_slice_options(last_file,
                                          start_time,
                                          end_time,
                                          flag=False)
        last_file = get_full_filename(last_file, port_id)
        merge_list.append(_slice_video(last_file,
                                       slice_options,
                                       task_id + "end.mp4"))

    outfile = ("%s.mp4") % task_id
    _merge_video(task_id, merge_list, outfile)

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
    outfile = get_slice_dir() + outfile
    target = "ffmpeg -y -i " + input_file + slice_options + " " + outfile
    print target
    os.system(target)
    return outfile


def _merge_video(task_id, merge_list, outfile):
    '''
    merge video  
    '''
    outfile_cfg = get_download_dir() + str(task_id) + ".txt"
    outfile = get_download_dir() + outfile

    file_object = open(outfile_cfg, 'w')
    for files in merge_list:
        files = files.replace("\\", "\\\\")
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
