#coding=utf-8  
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime
import time
import json
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler



define("port", default=9999, type=int)


class ChatHandler(WebSocketHandler):



    #建立websocket连接
    def open(self):
        self.write_message("connected")

    def data_cleaning(self,origin_data):
        for line in origin_data.readlines():
            print(line)

        return "hello"

    #websocket接受信息
    def on_message(self, message):
        if(message[0:4]=="file"):
            mess = message[4:]
            mess = self.data_cleaning(mess)
            
        else:
            mess = "verybad"
        self.write_message(mess)
        
    #关闭websocket    
    def on_close(self):
        print('connection closed')
        pass

    #允许跨域请求
    def check_origin(self, origin):
        return True  

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/chat", ChatHandler),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
