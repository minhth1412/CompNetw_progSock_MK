import sys
import socket
import threading
import json

# Có tham khảo trên https://docs.python.org/2/library/socket.html

# Thiết lập địa chỉ, về sau sẽ mở rộng bằng cách cho client tự nhập địa chỉ IP của server để kết nối
HOST = socket.gethostbyname(socket.gethostname())
# Thiết lập port lắng nghe, không để nhỏ hơn 1024, tránh bị trùng với port trên máy tính
PORT = 7654
# tạo socket SERVER, với địa chỉ IPV4, giao thức TCP
try:
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to create Server!")
    sys.exit();
print("Server created!");
SERVER.bind((HOST, PORT))    # Gán địa chỉ (HOST, PORT) cho s
Backlog = 1
SERVER.listen(Backlog)     # Thiết lập tối đa một lượng nhất định kết nối đồng thời, bắt đầu TCP listen
print("Server is waiting for client to connect...")
conn, addr = SERVER.accept()     # thiết lập kết nối với Client
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()