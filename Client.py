import sys
import socket
import threading
import json

# Có tham khảo trên https://docs.python.org/2/library/socket.html

# Trả về IPV4 của máy hiện tại cho HOST
HOST = socket.gethostbyname(socket.gethostname())
# Đồng nhất port với bên server
PORT = 7654
# Tạo socket CLIENT
try:
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to create Client!")
    sys.exit();
CLIENT.connect((HOST, PORT))       # Kết nối tới SERVER
data = CLIENT.recv(1024)
CLIENT.close()
print('Server Respond: ', repr(data))