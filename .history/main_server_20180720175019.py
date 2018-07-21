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

class UpFileHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        #查看上传文件的完整格式，files以字典形式返回
        #print(self.request.files)
        #{'file1':
        #[{'filename': '新建文本文档.txt', 'body': b'61 60 -83\r\n-445 64 -259', 'content_type': 'text/plain'}],
        #'file2':
        filesDict=self.request.files
        for inputname in filesDict:
            #第一层循环取出最外层信息，即input标签传回的name值
            #用过filename键值对对应，取出对应的上传文件的真实属性
            http_file=filesDict[inputname]
            for fileObj in http_file:
                #第二层循环取出完整的对象
                #取得当前路径下的upfiles文件夹+上fileObj.filename属性(即真实文件名)
                filePath=os.path.join(os.path.dirname(__file__),fileObj.filename)
                with open(filePath,'wb') as f:
                     f.write(fileObj.body)
        ChatHandler.on_send('上传成功')

class ChatHandler(WebSocketHandler):

    #建立websocket连接
    def open(self):
        self.write_message("connected")
        print("new websocket guest connected")
        pass

    def data_cleaning(self,origin_data):
        
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
                    # 脏数据
                    if(meta_data_arr[0] =='fps'):
                        data_set.append([int(meta_data_arr[1][0:13]),float(meta_data_arr[2]),'lane_alg_fps'])
                    else:
                        data_set.append([int(meta_data_arr[0][0:13]),float(meta_data_arr[1]),'lane_alg_fps'])
            elif ('lane.fps' in line):
                if(takeOrNot):
                    meta_data = line.split('lane.fps')[1].strip()
                    meta_data_arr = meta_data.split(' ')
                    data_set.append([int(meta_data_arr[0][0:13]),float(meta_data_arr[1]),'lane_fps'])
                    # data_set.append((line.split('lane.fps')[1].strip().split(' ')))
            elif ('vehicle.alg_fps' in line):
                if(takeOrNot):
                    meta_data = line.split('vehicle.alg_fps')[1].strip()
                    meta_data_arr = meta_data.split(' ')
                    data_set.append([int(meta_data_arr[0][0:13]),float(meta_data_arr[1]),'vehicle_alg_fps'])
            elif ('v1.process_fps' in line):
                if(takeOrNot):
                    meta_data = line.split('v1.process_fps')[1].strip()
                    meta_data_arr = meta_data.split(' ')
                    data_set.append([int(meta_data_arr[0][0:13]),float(meta_data_arr[1]),'v1.process_fps'])     
            
        data_set.sort()
        if(len(data_set)<=20000):
            mess = json.dumps(data_set,ensure_ascii=False)
            self.write_message(mess)
        else:
            self.write_message("too big file")

    #websocket接受信息
    def on_message(self, message):
        if(message[0:4]=="file"):
            mess = message[4:]
            self.data_cleaning(mess)
    
        elif(message[0:4]=="more"):
            mess = "verybad"
            print("received mess"+mess)

    def on_send(message):
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
            (r"/chat", ChatHandler),
            (r"/fileUploading",UpFileHandler)
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
