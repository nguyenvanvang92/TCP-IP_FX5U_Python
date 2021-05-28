import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(5)
h = "192.168.1.40"
p = 2040
client.connect(h,p)