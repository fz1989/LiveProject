import os
import inspect
ROOT_PATH = "D:\\live"
HOST_IP = "219.245.64.129"
HOST_PORT = "80"
HOST_NAME = "http://" + HOST_IP + ":" + HOST_PORT
CONF = '''
#user  nobody;
worker_processes  1;

error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    upstream frontends {
        server 127.0.0.1:8888;
    }

    include       mime.types;
    default_type  application/octet-stream;

    access_log  logs/access.log;

    keepalive_timeout 65;
    proxy_read_timeout 200;
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    gzip on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_types text/plain text/html text/css text/xml
               application/x-javascript application/xml
               application/atom+xml text/javascript;

    server {
        listen       80;
        server_name  %s;
        autoindex       on;
        autoindex_exact_size    off;
        autoindex_localtime     on;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;
        
        location ^~ /Player/ {
            root %s;
            if ($query_string) {
                expires max;
            }
        }

        location ^~ /livedownload/ {
            root %s;
            limit_rate 800k;
            autoindex on;
            sendfile on;
            tcp_nopush on;
            add_header Content-Type "application/octet-stream";
            default_type application/octet-stream;
        }

        location ^~ /videodownload/ {
            root %s;
            limit_rate 800k;
            autoindex on;
            sendfile on;
            tcp_nopush on;
            add_header Content-Type "application/octet-stream";
            default_type application/octet-stream;
        }

        location ^~ /videos/{
            root %s;  
            expires      30d;
        }
        

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://frontends;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}''' % (HOST_NAME, ROOT_PATH, ROOT_PATH, ROOT_PATH, ROOT_PATH)
this_file = inspect.getfile(inspect.currentframe())
current_dir = os.path.abspath(os.path.dirname(this_file))
FILE_OBJECT = open(current_dir + '/nginx/conf/nginx.conf', 'w')
FILE_OBJECT.write(CONF)
FILE_OBJECT.close()

LIVE_DOWNLOAD_DIR = ROOT_PATH + "livedownload"
VIDEOS_DIR  = ROOT_PATH + "videos"
VIDEO_DWONLOAD_DIR = ROOT_PATH + "videodownload"
TMP_DIR = ROOT_PATH + "tmp"

if __name__ == "__main__":
    if not os.path.exists(LIVE_DOWNLOAD_DIR):
        os.mkdir(LIVE_DOWNLOAD_DIR)
    if not os.path.exists(VIDEOS_DIR):
        os.mkdir(VIDEOS_DIR)
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
    if not os.path.exists(VIDEO_DWONLOAD_DIR):
        target = "mklink /D %s %s" % (VIDEO_DWONLOAD_DIR, VIDEOS_DIR)
        os.system(target)
