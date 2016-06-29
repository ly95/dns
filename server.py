import socket
from resolver import Resolver


def run_server(ip='0.0.0.0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, 53))

    while True:
        data, addr = s.recvfrom(1024)
        ret = Resolver(data).do()
        s.sendto(ret, addr)
