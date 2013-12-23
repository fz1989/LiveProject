
#!/usr/bin/env python
# coding=utf-8

from common import get_url_prefix
from common import find_videos


def find_video_url(start_time, end_time, port_id):
    '''
        return video_files urls for httpserver
    '''
    video_files = find_videos(start_time, end_time, port_id)
    video_urls = [get_url_prefix(video, port_id) + video 
                  for video in video_files]
    return video_urls
