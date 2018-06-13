import socket
import threading
import json

# 简单的聊天室程序

# 消息列表最大长度
MAX_MSG_LIST_LEN = 15


class SocketServer:

    def __init__(self, port):
        self.port = port
        self.running = False
        self.msg_list = []

    def start(self):
        if self.port <= 0:
            raise RuntimeError('port error')
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.bind(('0.0.0.0', self.port))
        sc.listen(5)
        self.running = True

        while self.running:
            s, addr = sc.accept()
            t = threading.Thread(target=self.__process_request, args=(s, addr))
            t.start()

    def __process_request(self, sock, addr):
        print('Accept new connection from %s:%s...' % addr)
        # 先发送现有消息
        sock.send(json.dumps(self.msg_list).encode('utf-8'))
        print('send %s' % json.dumps(self.msg_list).encode('utf-8'))
        while True:
            data = sock.recv(4096)
            data = str(data, 'utf-8')
            print('recv: %s' % data)
            if data == 'exit':
                break
            self.msg_list.insert(0, ('From %s:%s' % addr) + ': ' + data)
            if len(self.msg_list) > MAX_MSG_LIST_LEN:
                self.msg_list = self.msg_list[:MAX_MSG_LIST_LEN]
            sock.send(json.dumps(self.msg_list).encode('utf-8'))
        sock.close()


class SocketClient:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, msg):
        self.sock.send(msg.encode('utf-8'))
        if msg != 'exit':
            self.read()

    def read(self):
        # while True:
        #     data = self.sock.recv(4096)
        #     print(data)
        #     if not data:
        #         break
        #     buffer.append(data)

        # data = ''.join(buffer)
        data = str(self.sock.recv(2 * 8192), 'utf-8')
        data = json.loads(data)
        if data:
            data.reverse()
            for item in data:
                print(item)

    def close(self):
        self.sock.close()
