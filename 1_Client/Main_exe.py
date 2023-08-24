from socket import socket,AF_INET,SOCK_STREAM

#服务端的ip地址
server_ip = '172.30.203.76'
#服务端socket绑定的端口号
server_port = 8081

if __name__ == '__main__':
    while True:
        str_msg = input("请输入要发送信息：")
        if str_msg != "":
            bytes_msg = bytes(str_msg, encoding = "gbk")
            client = socket(AF_INET,SOCK_STREAM)
            print(client)
            client.connect((server_ip,server_port))
            client.send(bytes_msg)
            print(str(client.recv(8192),encoding="gbk"))
            client.close()