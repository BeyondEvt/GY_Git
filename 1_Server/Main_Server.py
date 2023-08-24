import pickle
from socketserver import BaseRequestHandler, TCPServer
import socket
from socket import *
import time
import sys


class test(BaseRequestHandler):

    def handle(self):
        # self.client_address连接的客户端
        print('Got connection from', self.client_address)

        #
        # while True:
        print("开始读取")
        # 获取客户端请求的一部分数据
        msg_inp_dim = (self.request.recv(16)).decode('gbk')
        print("接收成功")

        print("接收到的inp_dim:\n\n", msg_inp_dim)

if __name__ == '__main__':
    from threading import Thread
    # 绑定socket服务端所在ip和端口号
    serv = TCPServer(('172.30.203.76', 8081), test)
    serv.serve_forever()
# import socket
#
# HOST = '172.30.203.76'  # 监听所有网络接口
# PORT =  8081
#
# # 创建socket连接，监听指定端口
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST, PORT))
# server_socket.listen()
#
# # 接收客户端连接
# client_socket, client_address = server_socket.accept()
#
# # 接收数据
# data = client_socket.recv(1024)
#
# # 将接收到的数据转换回整数
# received_number = int(data.decode())
#
# print(f"Received number: {received_number}")
#
# # 关闭连接
# client_socket.close()
# server_socket.close()