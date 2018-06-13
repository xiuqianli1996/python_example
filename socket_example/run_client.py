from socket.socket_test import SocketClient

if __name__ == '__main__':
    client = SocketClient('127.0.0.1', 1234)
    print('连接成功， 输入任意字符发送消息，exit退出')
    client.read()
    while True:
        msg = input('请输入消息：').strip()
        if not msg:
            continue
        client.send(msg)
        if msg == 'exit':
            break

    client.close()


