#!/usr/bin/env python
import sys
import socket
import threading
import time

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        print 'Receive:%s' % data
        if data == 'exit' or not data:
            break
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr
 
if __name__ == "__main__":
    
    if sys.argv[1].lower() == 'server':
        ip = '127.0.0.1'
        port = 31500
        if sys.argv[2]:
            vec = sys.argv[2].split(':', 1)
            if len(vec) == 2:
                ip = vec[0]
                port = int(vec[1])
        address = (ip, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
        s.bind(address)
        s.listen(5)
        print 'Server %s:%s wait for connection ...' % address
        
        while True:
            sock, addr = s.accept()
            print 'Got connected from',addr
            t = threading.Thread(target=tcplink, args=(sock, addr))
            t.start()
    elif sys.argv[1].lower() == 'client':
        ip = '127.0.0.1'
        port = 31500
        if sys.argv[2]:
            vec = sys.argv[2].split(':', 1)
            if len(vec) == 2:
                ip = vec[0]
                port = int(vec[1])
        address = (ip, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
        print s.recv(1024)
        for data in ['kk', 'lili', 'xixi']:
            s.send(data)
            print 'Send:%s; Receive:%s' % (data, s.recv(1024))
        s.send('exit')
        s.close()
    else:
        print 'Usage: %s [server|client] ip:port' % sys.argv[0]
