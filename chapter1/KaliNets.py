# coding=utf-8
"""
netcat
"""
import sys
import socket
import getopt
import threading
import subprocess

# 定义全局变量
listen = False
command = False
upload = False
execute = ""
target = ""
upload_dest = ""
port = 0


# 提示
def usage():
    print "KALI NET TOOL"
    print
    print "Usage: kalinet.py -t target_host -p port"
    print "-l --listen                          listen on [host]:[port]"
    print "-e --execute=file_to_run             execute the given file"
    print "-c --command                         init a command shell"
    print "-u --upload=deat                     upload a file"
    print "Examples:"
    print "kalinet.py -t 192.168.1.100 -p 8080 -l -c"
    print "kalinet.py -t 192.168.1.100 -p 8080 -l -u 'c:\\target.exe'"
    print "kalinet.py -t 192.168.1.100 -p 8080 -l -e 'cat /etc/passwd' "
    print "echo 'ABCD'| ./kalinet.py -t 192.168.1.100 -p 8080 "
    sys.exit(0)


def server_loop():
    print ">>>server_loop"
    global target
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # 新建一个线程处理客户端
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

    pass


def run_command(command):
    print ">>>run_command"
    # 换行
    command = command.rstrip()
    # 运行命令行并返回结果
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = "Failed to execute command. \r\n"

    return output


def client_handler(client_socket):
    print ">>>client_handler"
    global upload
    global execute
    global command

    # 检测文件上传
    if len(upload_dest):
        pass

    # 检测命令执行
    if len(execute):
        # 运行命令
        output = run_command(execute)
        client_socket.send(output)

    # 检测是否要返回shell
    if command:
        while True:
            # 新的命令行
            client_socket.send("<KaliNet:#> ")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            response = run_command(cmd_buffer)
            client_socket.send(response)


def client_sender(buffer):
    print ">>>client_sender"
    # print "I am client :", buffer
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))

        # 发送数据
        if len(buffer):
            client.send(buffer)

        # 接收数据
        while True:
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break

            # 输出接收的数据
            print response

            # 再次发送数据
            buffer = raw_input("")
            buffer += "\n"
            client.send(buffer)

    except Exception as e:
        # 关闭连接
        client.close()
        print '[*] Exception Exit'
        print e


def main():
    global listen
    global command
    global upload
    global execute
    global target
    global upload_dest
    global port

    if not len(sys.argv[1:]):
        print sys.argv
        usage()

    # 获取参数
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ['help', 'listen', 'execute=', 'target=', 'port=', 'command', 'upload='])

    except Exception as e:

        print e
        usage()

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        elif o in ('-c', '--command'):
            command = True
        elif o in ('-u', '--upload'):
            upload_dest = a
        else:
            assert False, "Unhandled Option"
        print ">>> ", o, a

    # 判断是作为客户端还是服务端
    if not listen and len(target) and port > 0:
        # 客户端
        buffer = sys.stdin.read()
        client_sender(buffer)

    if listen:
        # 服务端
        server_loop()


main()
