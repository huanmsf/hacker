# codeing=utf-8
import socket

target_host = "127.0.0.1"
target_port = 80

# socket.AF_INET:IPV4
# socket.SOCK_DGRAM:UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("aaaabbbb", (target_host, target_port))
data, addr = client.recvfrom(4096)

print 'data:', data
print 'addr:', addr
