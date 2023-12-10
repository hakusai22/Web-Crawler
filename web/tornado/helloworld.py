# -*- coding: utf-8 -*-
# @Author  : hakusai
# @Time    : 2023/12/10 16:56

# /Users/yinpeng/PythonWorkSpace/Web-Crawler/venv/bin/pip3.11 install tornado
# /Users/yinpeng/PythonWorkSpace/Web-Crawler/venv/bin/python

import tornado.ioloop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.options import options, define

define('port', default=8000, help='监听端口')

class HelloHandler(RequestHandler):
    def get(self):
        self.write('hello world')

if __name__ == '__main__':
    options.parse_command_line()
    handlers_routes = [
        (r'/', HelloHandler)
    ]
    app = Application(handlers=handlers_routes)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
