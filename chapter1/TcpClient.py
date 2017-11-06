# codeing=utf-8
import socket

target_host = "www.cnblogs.com"
target_port = 80

# socket.AF_INET:IPV4
# socket.SOCK_STREAM:TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send("GET / HTTP/1.1\r\nHost:cnblogs.com \r\n\r\n")
response = client.recv(4096)
print response
