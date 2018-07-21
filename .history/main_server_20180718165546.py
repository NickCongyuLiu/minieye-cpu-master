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



define("port", default=1213, type=int)


class ChatHandler(WebSocketHandler):



    #建立websocket连接
    def open(self):
        self.write_message("connected")

    def data_cleaning(self,origin_data):
        info = origin_data.split("\n")
        CPU_temp = []
        CPU_one_freq = []
        CPU_two_freq = []
        CPU_timeStamp = []
        CPU_power =[]
        # lane_alg_fps =[]
        # lane_fps=[]
        # vehicle_alg_fps=[]
        # v1_process_fps=[]
        
        data_set = []
        # read_info = []
        takeOrNot=False
        for line in info:
            if ('Output info' in line):
                takeOrNot = True
            elif ('Input info' in line):
                takeOrNot = False    
            elif ('timeStamp' in line):
                if(takeOrNot):
                    CPU_timeStamp.append(int(line.split(':')[1].strip()))
            elif ('mtktscpu :' in line):
                if(takeOrNot):
                    # CPU_temp+=(line.split(':')[1].strip())+' '
                    CPU_temp.append(int(line.split(':')[1].strip()))
            elif ('CPU#0:' in line):
                if(takeOrNot):
                    CPU_one_freq.append(int(line.split(':')[1].strip()))
            elif ('CPU#4:' in line):
                if(takeOrNot):
                    CPU_two_freq.append(int(line.split(':')[1][1:6]))
            elif ('current power =' in line):
                if(takeOrNot):
                    CPU_power.append((line.split('current power =')[1].strip()[0:4]))
            elif ('lane.alg_fps' in line):
                if(takeOrNot):
                    meta_data = line.split('lane.alg_fps')[1].strip()
                    data_set.append(meta_data.split(' '))
                    # data_set.append((line.split('lane.alg_fps')[1].strip().split(' '),))
            elif ('lane.fps' in line):
                if(takeOrNot):
                    continue
                    # data_set.append((line.split('lane.fps')[1].strip().split(' ')))
            elif ('vehicle.alg_fps' in line):
                if(takeOrNot):
                    continue
                    # data_set.append((line.split('vehicle.alg_fps')[1].strip().split(' ')))
            elif ('v1.process_fps' in line):
                if(takeOrNot):
                    continue
                    # data_set.append((line.split('v1.process_fps')[1].strip().split(' ')))        
            
        print(data_set)        
        # mess = ','.join(CPU_timeStamp)+'\n'+','.join(CPU_temp)+'\n'+','.join(CPU_one_freq)+'\n'+','.join(CPU_two_freq)+'\n'+','.join(CPU_power)+'\n'+','.join(lane_alg_fps)
        # self.write_message(mess)

        return 'hello'

    #websocket接受信息
    def on_message(self, message):
        if(message[0:4]=="file"):
            mess = message[4:]
            mess = self.data_cleaning(mess)
            
        else:
            mess = "verybad"
        # self.write_message(mess)
        
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
