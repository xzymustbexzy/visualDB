import socket
import struct

import message_pb2
import config


class Server(object):

    def __init__(self, ):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((config.HOST, config.PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    recv_len = conn.recv(4)
                    recv_len = struct.unpack('@I', recv_len)[0]
                    data = b''
                    while len(data) < recv_len:
                        packet = conn.recv(recv_len - len(data))
                        if not packet:
                            break
                        data += packet
                    print(data[:100])
                    message = message_pb2.queryMessage()
                    obj = message.ParseFromString(data)
                    print(obj)
                    print(message.json)
                    with open('server_recieved.jpg', 'wb') as f:
                        f.write(message.blobs[0])
            
