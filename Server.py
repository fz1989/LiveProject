import tornado.ioloop
import tornado.web
import json
from playvideo import *
from downloadvideo import *


class PlayVideoHandler(tornado.web.RequestHandler):
    def post(self):
        '''
            get the video url 
        '''
        start_time = self.get_argument("start_time")
        end_time = self.get_argument("end_time")
        port_id = self.get_argument("port_id")
        self.write(json.dumps(find_video_url(start_time, end_time, port_id)))


class DownLoadVideoHandle(tornado.web.RequestHandler):
    def get(self):
        start_time = self.get_argument("start_time")
        end_time = self.get_argument("end_time")
        port_id = self.get_argument("port_id")
        task_id = get_task_id(start_time, end_time, port_id)
        self.write(task_id)

    def post(self):
        task_id = self.get_argument("task_id")
        self.write(get_task_status(task_id))


application = tornado.web.Application([
    (r"/play", PlayVideoHandler),
    (r"/download", DownLoadVideoHandle),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


