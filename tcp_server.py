import socket
import sys
from time import sleep

# Create a TCP/IP socket (socket.SOCK_DREAM = UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind() is used to associate the socket with the server address.
server_address = ('localhost', 8000)
sock.bind(server_address)
print >>sys.stderr, 'starting up on %s port %s' % server_address

# listen() puts the socket into server mode and then accept() waits for an incoming connection
sock.listen(5)
while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # accept() returns an open connection between the server and the client, along with the address of the client.
        # 'connnection' is actually a different socket on another port which is assigned by the kernel.
        # Data is read from the connection with recv() and transmitted with sendall()
        # Receive the data in small chunks and retransmit it
        filename = ""
        file_descriptor = None
        while True:
            data = connection.recv(4096)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                str_arr = data.split(" ")
                if str_arr[0].strip().upper() == "SENDFILE":
                    filename = str_arr[1]
                    with open("1_"+filename, 'wb') as f:
                        print 'File Opened ',"1_"+filename
                        while True:
                            try:
                                data = connection.recv(4096)
                            except socket.timeout, e:
                                err = e.args[0]
                                # this next if/else is a bit redundant, but illustrates how the
                                # timeout exception is setup
                                if err == 'timed out':
                                    sleep(1)
                                    print 'recv timed out, retry later'
                                    continue
                                else:
                                    print e
                                    break
                            except socket.error, e:
                                # Something else happened, handle error, exit, etc.
                                print e
                                break
                            else:
                                if len(data) == 0:
                                    print 'orderly shutdown on server end'
                                    break
                                else:
                                    f.write(data)

                else:
                    print >>sys.stderr, 'sending data back to the client'
                    connection.sendall(str_arr[1])
                    connection.close()
            else:
                print >>sys.stderr, 'no more data from ', client_address
                break
    finally:
        # Clean up the connection
        connection.close()



