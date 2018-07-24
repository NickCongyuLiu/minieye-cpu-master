# Minieye-CPU-Master
Minieye-CPU-Master 是一个数据可视化cpu状态txt文件的工具。
v0.1
:toc:

:numbered:

### TodoList

. 尝试使用python自带websocket库 *todo*
    
  https://github.com/aaugustin/websockets


### 依赖

* tornaodo_websocket
* echartJS4.1.0.rc2
* Jquery1.4
* python 3

安装 

```shell
下载安装tornado
pip install tornado
```

### 使用
#### 运行

```shell
usage: python3 tornado server.py

```
双击打开visualization.html 上传想可视化的文件, 会自动传递文件到后端进行清洗,并将清洗好的文件发送前端进行展示
超大文件会截断传送并展示
有上下翻页展示功能.
data-visualization-web.html 是纯前端展示,清洗处理数据都完成在前端,不支持超大文件展示.