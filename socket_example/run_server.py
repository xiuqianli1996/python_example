from socket_example.socket_test import SocketServer

if __name__ == '__main__':
    server = SocketServer(1234)
    server.start()
