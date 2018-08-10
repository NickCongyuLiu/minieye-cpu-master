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
        # self.write_message("connected")
        print("new websocket guest connected")
        pass

    def data_cleaning(self,origin_data,data_type):
        
        info = origin_data.split("\n")
        data_set = []
        takeOrNot=False
        for line in info:
            if ('Output info' in line):
                takeOrNot = True
            elif ('Input info' in line):
                takeOrNot = False    
            elif ('timeStamp' in line):
                if(takeOrNot):
                    meta_data = int(line.split(':')[1].strip()[0:13])
                    data_set.append([meta_data])
            elif ('mtktscpu :' in line):
                if(takeOrNot):
                    meta_data = int(line.split(':')[1].strip())
                    data_set[-1].append(meta_data/1000)
            elif ('CPU#0:' in line):
                if(takeOrNot):
                    meta_data = int(line.split(':')[1].strip())
                    data_set[-1].append(meta_data/10000)
            elif ('CPU#4:' in line):
                if(takeOrNot):
                    meta_data = int(line.split(':')[1].strip())
                    data_set[-1].append(meta_data/10000)
            elif ('current power =' in line):
                if(takeOrNot):
                    meta_data = int(line.split('current power =')[1].strip()[0:4])
                    data_set[-1].append(meta_data/10)
            elif ('lane.alg_fps' in line):
                if(takeOrNot):
                    meta_data = line.split('lane.alg_fps')[1].strip()
                    meta_data_arr = meta_data.split(' ')
                    try:
                        if(float(meta_data_arr[1])>100 or int(meta_data_arr[0][0:13])<1000000000000 or int(meta_data_arr[0][0:13])==1531531713894):
                            continue
                        else:
                            data_set.append([int(meta_data_arr[0][0:13]),float(meta_data_arr[1]),'lane_alg_fps'])
                    except:
                        pass
            elif ('lane.fps' in line):
                if(takeOrNot):
                    meta_data = line.split('lane.fps')[1].strip()
                    meta_data_arr = meta_data.split(' ')
                    try:
                        if(float(meta_data_arr[1])>100 or int(meta_data_arr[0][0:13])<1000000000000):
                            continue
                        else:
                            data_set.append([int(meta_data_arr[0][0:13]),float(meta_data_arr[1]),'lane_fps'])
                    except:
                        pass
            elif ('vehicle.alg_fps' in line):
                if(takeOrNot):
                    meta_data = line.split('vehicle.alg_fps')[1].strip()
                    meta_data_arr = meta_data.split(' ')
                    try:
                        if(float(meta_data_arr[1])>100 or int(meta_data_arr[0][0:13])<1000000000000 or int(meta_data_arr[0][0:13])>1800000000000):
                            continue
                        else:
                            data_set.append([int(meta_data_arr[0][0:13]),float(meta_data_arr[1]),'vehicle_alg_fps'])
                    except:
                        pass
            elif ('v1.process_fps' in line):
                if(takeOrNot):
                    meta_data = line.split('v1.process_fps')[1].strip()
                    meta_data_arr = meta_data.split(' ')
                    try:
                        if(float(meta_data_arr[1])>100 or int(meta_data_arr[0][0:13])<1000000000000):
                            continue
                        else:
                            data_set.append([int(meta_data_arr[0][0:13]),float(meta_data_arr[1]),'v1_process_fps'])
                    except:
                        pass
        data_set.sort()
        mess = json.dumps(data_set,ensure_ascii=False)
        if(data_type=="sing"):
            self.write_message("sing"+mess)
        elif(len(data_type)==2):
            self.write_message("mult"+data_type+mess)
        

    #websocket接受信息
    def on_message(self, message):
        if(message[0:4]=="sing"):
            mess = message[4:]
            self.data_cleaning(mess,'sing')
        elif(message[0:4]=="mult"):
            num = message[4:6]
            mess = message[6:]
            self.data_cleaning(mess,num)

    def on_send(self,message):
        self.write_message(message)

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
            (r, ChatHandler)],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
